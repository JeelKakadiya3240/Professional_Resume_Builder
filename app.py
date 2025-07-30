from flask import Flask, render_template, request, jsonify, send_file
import openai
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import io
import asyncio

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract-keywords', methods=['POST'])
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
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=128,
            temperature=0.2,
        )
        
        keywords_text = response.choices[0].message.content.strip()
        keywords = [kw.strip() for kw in keywords_text.replace("\n", ",").split(",") if kw.strip()]
        
        return jsonify({'keywords': keywords})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/resume-maker')
def resume_maker():
    return render_template('resume_maker.html')

@app.route('/generate-resume', methods=['POST'])
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
                                    template_style=data.get('template', 'modern'))
        
        return jsonify({'resume_html': resume_html})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-pdf', methods=['POST'])
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
                                    template_style=data.get('template', 'modern'))
        
        # Use Playwright to generate PDF from HTML
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
def ai_rewrite_job_description():
    try:
        data = request.get_json()
        bullet_points = data.get('bullet_points', [])
        
        if not bullet_points:
            return jsonify({'error': 'No bullet points provided'}), 400
        
        # Create a comprehensive prompt for rewriting job descriptions
        prompt = f"""You are a professional resume writer. Rewrite the following job description bullet points to make them more impactful, professional, and human-like. 

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
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
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
def ai_rewrite_project_description():
    try:
        data = request.get_json()
        bullet_points = data.get('bullet_points', [])
        
        if not bullet_points:
            return jsonify({'error': 'No bullet points provided'}), 400
        
        # Create a comprehensive prompt for rewriting project descriptions
        prompt = f"""You are a professional resume writer. Rewrite the following project description bullet points to make them more impactful, professional, and human-like. 

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
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
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
    app.run(debug=True, port=5001, host='0.0.0.0') 