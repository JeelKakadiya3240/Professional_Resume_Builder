from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

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

if __name__ == '__main__':
    app.run(debug=True, port=5000) 