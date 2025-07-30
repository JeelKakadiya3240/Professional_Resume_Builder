# ATS Keyword Extractor & Resume Maker

A Flask web application that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) by extracting keywords from job descriptions and creating professional resumes.

## Features

- **ATS Keyword Extraction**: Extract relevant keywords from job descriptions using AI
- **Resume Builder**: Create professional resumes with modern templates
- **PDF Generation**: Download resumes as PDF files
- **AI-Powered**: Uses OpenAI API for intelligent keyword extraction and content rewriting

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/JeelKakadiya3240/Job.git
   cd Job
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Set up environment variables**
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open http://localhost:5001 in your browser

## Deployment

The application is configured for deployment on Render:

- **Build Command**: `pip install -r requirements.txt && playwright install chromium`
- **Start Command**: `python app.py`
- **Environment Variables**: Add `OPENAI_API_KEY` in Render dashboard

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **AI**: OpenAI GPT-3.5-turbo
- **PDF Generation**: Playwright
- **Testing**: pytest

## Project Structure

```
Job/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── test_app.py           # Test suite
├── pytest.ini           # pytest configuration
├── templates/            # HTML templates
│   ├── index.html       # Home page
│   ├── resume_maker.html # Resume builder
│   └── resume_template.html # Resume template
└── .github/workflows/   # GitHub Actions CI/CD
    └── python-app.yml   # Workflow configuration
```

## License

MIT License
