from flask import Flask, render_template, request, jsonify, send_file
import openai
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import io

import requests
import secrets
import jwt
from functools import wraps
from flask import session, redirect, url_for
import boto3
import json
from datetime import datetime
from urllib.parse import urlencode
import hmac
import hashlib
import base64

# Add WeasyPrint import for alternative PDF generation
# try:
#     from weasyprint import HTML
#     WEASYPRINT_AVAILABLE = True
# except ImportError:
#     WEASYPRINT_AVAILABLE = False
WEASYPRINT_AVAILABLE = False  
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Cognito configuration
COGNITO_REGION = os.getenv("COGNITO_REGION", "us-east-2")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
COGNITO_APP_CLIENT_SECRET = os.getenv("COGNITO_APP_CLIENT_SECRET")
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_REDIRECT_URI = os.getenv("COGNITO_REDIRECT_URI", "http://localhost:5001/callback")
COGNITO_POST_LOGOUT_REDIRECT_URI = os.getenv("COGNITO_POST_LOGOUT_REDIRECT_URI", "http://localhost:5001/")

# AWS configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize AWS clients
s3_client = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Initialize Cognito client
cognito_client = boto3.client(
    'cognito-idp',
    region_name=COGNITO_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def secret_hash(username: str) -> str:
    """Compute secret hash for Cognito authentication"""
    msg = (username + COGNITO_APP_CLIENT_ID).encode("utf-8")
    key = COGNITO_APP_CLIENT_SECRET.encode("utf-8")
    dig = hmac.new(key, msg, hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

# S3 bucket name (you'll need to create this)
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "app-resume-data")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "ResumeData")

# Flask app configuration
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))

# Configure session cookies for better compatibility
app.config.update(
    SESSION_COOKIE_NAME="resumeai",
    SESSION_COOKIE_SAMESITE="Lax",   # fine for top-level redirects
    SESSION_COOKIE_SECURE=True,      # True for production HTTPSgit
)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def make_state():
    """Generate and store state parameter for CSRF protection"""
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    return state

# AWS helper functions
def save_resume_to_s3(user_id, resume_data):
    """Save resume data to S3"""
    try:
        filename = f"{user_id}/resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=filename,
            Body=json.dumps(resume_data),
            ContentType='application/json'
        )
        return filename
    except Exception as e:
        print(f"Error saving to S3: {e}")
        return None

def get_user_resumes_from_s3(user_id):
    """Get all resumes for a user from S3"""
    try:
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET_NAME,
            Prefix=f"{user_id}/"
        )
        resumes = []
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Key'].endswith('.json'):
                    file_response = s3_client.get_object(
                        Bucket=S3_BUCKET_NAME,
                        Key=obj['Key']
                    )
                    resume_data = json.loads(file_response['Body'].read())
                    resumes.append({
                        'filename': obj['Key'],
                        'data': resume_data,
                        'created': obj['LastModified'].isoformat()
                    })
        return resumes
    except Exception as e:
        print(f"Error getting resumes from S3: {e}")
        return []

def save_user_to_dynamodb(user_id, email, resume_count=0):
    """Save user info to DynamoDB"""
    try:
        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        table.put_item(
            Item={
                'userId': user_id,  # Changed to match DynamoDB schema
                'email': email,
                'resume_count': resume_count,
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat()
            }
        )
        return True
    except Exception as e:
        print(f"Error saving to DynamoDB: {e}")
        return False

def get_user_from_dynamodb(user_id):
    """Get user info from DynamoDB"""
    try:
        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        response = table.get_item(Key={'userId': user_id})  # Changed to match DynamoDB schema
        return response.get('Item')
    except Exception as e:
        print(f"Error getting user from DynamoDB: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login-page')
def login_page():
    """Custom login page"""
    return render_template('login.html')



@app.route('/custom-login', methods=['POST'])
def custom_login():
    """Handle custom login with email/password using USER_PASSWORD_AUTH"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
        # Authenticate user with Cognito using USER_PASSWORD_AUTH
        try:
            params = {
                "AuthFlow": "USER_PASSWORD_AUTH",
                "ClientId": COGNITO_APP_CLIENT_ID,
                "AuthParameters": {
                    "USERNAME": email,
                    "PASSWORD": password,
                    "SECRET_HASH": secret_hash(email),  # required for clients with secret
                }
            }
            
            response = cognito_client.initiate_auth(**params)
            
            # Handle challenges (MFA, new password, etc.)
            if "ChallengeName" in response:
                session["Session"] = response["Session"]  # keep for next step
                return jsonify({
                    "success": False,
                    "challenge": response["ChallengeName"],
                    "error": f"Challenge required: {response['ChallengeName']}"
                }), 400
            
            # Success → Tokens
            if 'AuthenticationResult' in response:
                auth_result = response['AuthenticationResult']
                
                # Extract user info from ID token instead of calling AdminGetUser
                # This avoids the permission issue
                id_token = auth_result.get('IdToken')
                
                # Store user info in session
                session['user_id'] = email  # Use email as user ID
                session['email'] = email
                session['id_token'] = id_token
                session['access_token'] = auth_result.get('AccessToken')
                session['refresh_token'] = auth_result.get('RefreshToken')
                
                # Save user to DynamoDB
                save_user_to_dynamodb(email, email)
                
                return jsonify({
                    'success': True, 
                    'redirect_url': '/dashboard',
                    'message': 'Login successful'
                })
            else:
                return jsonify({'success': False, 'error': 'Authentication failed'}), 401
                
        except cognito_client.exceptions.NotAuthorizedException:
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        except cognito_client.exceptions.UserNotFoundException:
            return jsonify({'success': False, 'error': 'User not found. Please sign up first.'}), 404
        except cognito_client.exceptions.UserNotConfirmedException:
            return jsonify({'success': False, 'error': 'Please confirm your email address'}), 400
        except Exception as e:
            print(f"Cognito error: {e}")
            return jsonify({'success': False, 'error': f'Authentication failed: {str(e)}'}), 500
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'error': 'Login failed. Please try again.'}), 500

@app.route('/login')
def login():
    # 1) create & save state
    state = make_state()
    
    # 2) build redirect_uri from the actual host used (localhost OR 127.0.0.1)
    redirect_uri = url_for("callback", _external=True, _scheme="http")
    session["redirect_uri"] = redirect_uri   # remember exactly what we sent

    # Build authorization URL
    auth_url = f"https://{COGNITO_DOMAIN}/oauth2/authorize"
    params = {
        'response_type': 'code',
        'client_id': COGNITO_APP_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'scope': 'openid email profile',
        'state': state
    }
    
    # Add query parameters to URL
    query_string = urlencode(params)
    full_auth_url = f"{auth_url}?{query_string}"
    
    return redirect(full_auth_url, code=302)

@app.route('/callback')
def callback():
    # Check for auth errors first
    err = request.args.get("error")
    if err:
        return f"Auth error: {err}, desc={request.args.get('error_description')}", 400

    # Verify state parameter
    returned = request.args.get('state')
    saved = session.get('oauth_state')

    if not saved or returned != saved:
        return "Invalid state", 400
    
    # Get authorization code
    code = request.args.get('code')
    if not code:
        return "Missing code", 400
    
    try:
        # Use the EXACT redirect_uri we used in /login
        redirect_uri = session.get("redirect_uri")
        
        # Exchange code for tokens
        token_url = f"https://{COGNITO_DOMAIN}/oauth2/token"
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': COGNITO_APP_CLIENT_ID,
            'code': code,
            'redirect_uri': redirect_uri
        }
        
        # Add client secret if available
        if COGNITO_APP_CLIENT_SECRET:
            token_data['client_secret'] = COGNITO_APP_CLIENT_SECRET
        
        response = requests.post(token_url, data=token_data, timeout=15)
        if response.status_code != 200:
            return f"Token exchange failed: {response.status_code} {response.text}", 400
        
        tokens = response.json()
        id_token = tokens.get('id_token')
        
        if not id_token:
            return "No ID token received", 400
        
        # Decode and verify ID token (basic verification)
        # In production, you should verify the JWT signature
        try:
            decoded_token = jwt.decode(id_token, options={"verify_signature": False})
            
            # Store user info in session
            user_id = decoded_token.get('sub')
            email = decoded_token.get('email')
            
            session['user_id'] = user_id
            session['email'] = email
            session['id_token'] = id_token
            session['access_token'] = tokens.get('access_token')
            session['refresh_token'] = tokens.get('refresh_token')
            
            # Save user to DynamoDB
            save_user_to_dynamodb(user_id, email)
            
            # Optional: prevent replay by clearing single-use values
            session.pop("oauth_state", None)
            session.pop("redirect_uri", None)
            
            return redirect(url_for('index'), code=302)
            
        except jwt.InvalidTokenError:
            return "Invalid ID token", 400
            
    except requests.RequestException as e:
        return f"Token exchange failed: {str(e)}", 400

@app.route('/logout')
def logout():
    # Clear session
    session.clear()
    
    # Simple redirect to home page
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing saved resumes"""
    try:
        user_id = session.get('user_id')
        user_email = session.get('email')
        
        # Get user info from DynamoDB
        user_info = get_user_from_dynamodb(user_id)
        
        # Get user's resumes from S3
        resumes = get_user_resumes_from_s3(user_id)
        
        return render_template('dashboard.html', 
                             user_email=user_email,
                             user_info=user_info,
                             resumes=resumes)
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

@app.route('/resume-maker')
@login_required
def resume_maker():
    return render_template('resume_maker.html')

@app.route('/save-resume', methods=['POST'])
@login_required
def save_resume():
    """Save resume data to S3 and update DynamoDB"""
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Save resume data to S3
        filename = save_resume_to_s3(user_id, data)
        
        if filename:
            # Update user's resume count in DynamoDB
            user_info = get_user_from_dynamodb(user_id)
            resume_count = user_info.get('resume_count', 0) + 1 if user_info else 1
            
            save_user_to_dynamodb(user_id, session.get('email'), resume_count)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'message': 'Resume saved successfully'
            })
        else:
            return jsonify({'error': 'Failed to save resume'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-resumes')
@login_required
def get_resumes():
    """Get all resumes for the current user"""
    try:
        user_id = session.get('user_id')
        resumes = get_user_resumes_from_s3(user_id)
        return jsonify({'resumes': resumes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load-resume/<path:filename>')
@login_required
def load_resume(filename):
    """Load a specific resume from S3"""
    try:
        user_id = session.get('user_id')
        
        # Verify the file belongs to the user
        if not filename.startswith(f"{user_id}/"):
            return jsonify({'error': 'Unauthorized'}), 403
        
        response = s3_client.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=filename
        )
        
        resume_data = json.loads(response['Body'].read())
        
        return jsonify({'resume': resume_data})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete-resume/<filename>', methods=['DELETE'])
@login_required
def delete_resume(filename):
    """Delete a resume from S3"""
    try:
        user_id = session.get('user_id')
        
        # Verify the file belongs to the user
        if not filename.startswith(f"{user_id}/"):
            return jsonify({'error': 'Unauthorized'}), 403
        
        s3_client.delete_object(
            Bucket=S3_BUCKET_NAME,
            Key=filename
        )
        
        return jsonify({'success': True, 'message': 'Resume deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract-keywords', methods=['POST'])
@login_required
def extract_keywords():
    try:
        data = request.get_json()
        job_description = data.get('job_description', '').strip()
        
        # Minimum length check (e.g., 30 characters)
        if not job_description or len(job_description) < 30:
            return jsonify({'error': 'Please enter a more detailed job description (at least 30 characters).'}), 400
        
        prompt = (
            "Extract all the most important keywords, technical skills, qualifications, tools, "
            "and relevant industry terms from the job description below. These keywords should reflect "
            "what an ATS (Applicant Tracking System) would look for to match a resume with the job.\n\n"
            f"Job Description:\n{job_description}\n\nKeywords:"
        )
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256,
            temperature=0.2,
        )
        
        keywords_text = response.choices[0].message.content.strip()
        keywords = [kw.strip() for kw in keywords_text.replace("\n", ",").split(",") if kw.strip()]
        
        return jsonify({'keywords': keywords})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-resume', methods=['POST'])
@login_required
def generate_resume():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'summary']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field.title()} is required'}), 400
        
        # Generate resume HTML
        resume_html = render_template('resume_template.html', 
                                    data=data,
                                    template_style=data.get('template', 'modern'),
                                    section_order=data.get('section_order', []))
        
        return jsonify({'resume_html': resume_html})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-pdf', methods=['POST'])
@login_required
def generate_pdf():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'summary']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field.title()} is required'}), 400
        
        # Generate resume HTML (exact same as preview)
        resume_html = render_template('resume_template.html', 
                                    data=data,
                                    template_style=data.get('template', 'modern'),
                                    section_order=data.get('section_order', []))
        
        pdf_bytes = None
        
        # Try Playwright first (faster and better rendering)
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                
                # Set content to the HTML
                page.set_content(resume_html)
                
                # Generate PDF with A4 size and proper styling
                pdf_bytes = page.pdf(
                    format='A4',
                    print_background=True,
                    margin={
                        'top': '0.5in',
                        'right': '0.5in',
                        'bottom': '0.5in',
                        'left': '0.5in'
                    }
                )
                
                browser.close()
        except Exception as playwright_error:
            print(f"Playwright PDF generation failed: {playwright_error}")
            
            # Fallback to WeasyPrint if available
            if WEASYPRINT_AVAILABLE:
                try:
                    # Create HTML object and generate PDF
                    html_doc = HTML(string=resume_html)
                    pdf_bytes = html_doc.write_pdf()
                    print("Successfully generated PDF using WeasyPrint")
                except Exception as weasyprint_error:
                    print(f"WeasyPrint PDF generation failed: {weasyprint_error}")
                    return jsonify({'error': 'PDF generation failed. Please try again later.'}), 500
            else:
                return jsonify({'error': 'PDF generation failed. Please try again later.'}), 500
        
        if pdf_bytes is None:
            return jsonify({'error': 'PDF generation failed. Please try again later.'}), 500
        
        # Create a file-like object from the PDF bytes
        pdf_io = io.BytesIO(pdf_bytes)
        pdf_io.seek(0)
        
        # Generate filename
        filename = f"{data['name'].replace(' ', '_')}_Resume.pdf"
        
        return send_file(
            pdf_io,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ai-rewrite-job-description', methods=['POST'])
@login_required
def ai_rewrite_job_description():
    try:
        data = request.get_json()
        bullet_points = data.get('bullet_points', [])
        selected_keywords = data.get('selected_keywords', [])
        

        
        if not bullet_points:
            return jsonify({'error': 'No bullet points provided'}), 400
        
        # Create a comprehensive prompt for rewriting job descriptions
        keyword_instruction = ""
        if selected_keywords:
            keyword_instruction = f"""
                                        CRITICAL REQUIREMENT: You MUST include these keywords in your rewritten bullet points: {', '.join(selected_keywords)}

                                        MANDATORY INSTRUCTIONS:
                                        - Each bullet point MUST contain at least one of these keywords
                                        - Use the keywords naturally within the sentence structure
                                        - If a keyword doesn't fit naturally, rephrase the bullet point to include it
                                        - Make sure all keywords are used across the bullet points
                                        - Prioritize keyword inclusion over perfect flow if necessary

                                        EXAMPLE: If keywords are ["Git", "SQL"], rewrite like:
                                        "Implemented Git version control and SQL database optimization, resulting in..."

                                        Original Bullet Points:
                                        {chr(10).join([f"{i+1}. {point}" for i, point in enumerate(bullet_points)])}

                                        Now rewrite all {len(bullet_points)} bullet points using the given instructions.
                                        """
        
        prompt = f"""You are a professional resume writer. Rewrite the following job description bullet points to make them more impactful, professional, and human-like. 

{keyword_instruction}

Guidelines:
- Use strong action verbs at the beginning of each bullet point
- Include specific metrics, numbers, and achievements when possible
- Make them sound natural and professional
- Keep each point concise but impactful
- Focus on results and accomplishments
- Use industry-standard terminology
- Make them sound like they were written by a human professional

Original bullet points:
{chr(10).join([f"- {point}" for point in bullet_points])}

Please rewrite each bullet point to be more professional and impactful. Return only the rewritten bullet points, one per line, without numbering or bullet symbols:"""

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3,
        )
        
        rewritten_text = response.choices[0].message.content.strip()
        
        # Split the response into individual bullet points
        rewritten_points = []
        for line in rewritten_text.split('\n'):
            line = line.strip()
            if line:
                # Remove any bullet symbols or numbering that might be in the response
                line = line.lstrip('•-1234567890. ')
                if line:
                    rewritten_points.append(line)
        
        # Ensure we have the same number of points or fewer
        if len(rewritten_points) > len(bullet_points):
            rewritten_points = rewritten_points[:len(bullet_points)]
        
        return jsonify({'rewritten_points': rewritten_points})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ai-rewrite-project-description', methods=['POST'])
@login_required
def ai_rewrite_project_description():
    try:
        data = request.get_json()
        bullet_points = data.get('bullet_points', [])
        selected_keywords = data.get('selected_keywords', [])
        

        
        if not bullet_points:
            return jsonify({'error': 'No bullet points provided'}), 400
        
        # Create a comprehensive prompt for rewriting project descriptions
        keyword_instruction = ""
        if selected_keywords:
            keyword_instruction = f"""
CRITICAL REQUIREMENT: You MUST include these keywords in your rewritten bullet points: {', '.join(selected_keywords)}

MANDATORY INSTRUCTIONS:
- Each bullet point MUST contain at least one of these keywords
- Use the keywords naturally within the sentence structure
- If a keyword doesn't fit naturally, rephrase the bullet point to include it
- Make sure all keywords are used across the bullet points
- Prioritize keyword inclusion over perfect flow if necessary

EXAMPLE: If keywords are ["Git", "SQL"], rewrite like:
"Implemented Git version control and SQL database optimization, resulting in..."

Original Bullet Points:
{chr(10).join([f"{i+1}. {point}" for i, point in enumerate(bullet_points)])}

Now rewrite all {len(bullet_points)} bullet points using the given instructions.
"""
        
        prompt = f"""You are a professional resume writer. Rewrite the following project description bullet points to make them more impactful, professional, and human-like. 

{keyword_instruction}

Guidelines:
- Use strong action verbs at the beginning of each bullet point
- Include specific technologies, tools, and methodologies used
- Highlight technical achievements and problem-solving skills
- Make them sound natural and professional
- Keep each point concise but impactful
- Focus on technical results and accomplishments
- Use industry-standard terminology
- Make them sound like they were written by a human professional
- Emphasize the technical complexity and impact of the project

Original bullet points:
{chr(10).join([f"- {point}" for point in bullet_points])}

Please rewrite each bullet point to be more professional and impactful. Return only the rewritten bullet points, one per line, without numbering or bullet symbols:"""

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3,
        )
        
        rewritten_text = response.choices[0].message.content.strip()
        
        # Split the response into individual bullet points
        rewritten_points = []
        for line in rewritten_text.split('\n'):
            line = line.strip()
            if line:
                # Remove any bullet symbols or numbering that might be in the response
                line = line.lstrip('•-1234567890. ')
                if line:
                    rewritten_points.append(line)
        
        # Ensure we have the same number of points or fewer
        if len(rewritten_points) > len(bullet_points):
            rewritten_points = rewritten_points[:len(bullet_points)]
        
        return jsonify({'rewritten_points': rewritten_points})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=False, port=int(os.environ.get('PORT', 5001)), host='0.0.0.0') 