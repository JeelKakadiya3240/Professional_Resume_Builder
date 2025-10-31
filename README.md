# Professional Resume Builder

A modern, feature-rich web application for creating professional resumes with drag-and-drop section reordering, real-time preview, and cloud storage capabilities.

![Resume Builder](https://img.shields.io/badge/Resume-Builder-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Flask](https://img.shields.io/badge/Flask-2.0+-orange)
![AWS](https://img.shields.io/badge/AWS-Integrated-yellow)
🌐 **[Live Demo](https://professional-resume-builder-7pkt21vsj-jeel-kakadiyas-projects.vercel.app/)** )
<img width="1440" height="900" alt="Screenshot 2025-10-16 at 3 51 46 PM" src="https://github.com/user-attachments/assets/6d1e3646-1214-4204-a4ea-93b0fb23a1e3" />
<img width="1440" height="900" alt="Screenshot 2025-10-16 at 3 51 59 PM" src="https://github.com/user-attachments/assets/e4c8c1ae-3fc7-40ba-aa83-b49def9df1fd" />
<img width="1440" height="900" alt="Screenshot 2025-10-16 at 3 52 13 PM" src="https://github.com/user-attachments/assets/0730cbcd-6eb4-4ebf-836c-fc715c0d2e68" />
<img width="1440" height="900" alt="Screenshot 2025-10-16 at 3 52 36 PM" src="https://github.com/user-attachments/assets/3a523b9c-9a4d-465b-9ea6-5d3d17f5d252" />
<img width="1440" height="900" alt="Screenshot 2025-10-16 at 3 52 48 PM" src="https://github.com/user-attachments/assets/a806cb01-66f3-4ba2-a529-4b432367a701" />



## ✨ Features

### 🤖 **AI-Powered Resume Enhancement**
- **Smart keyword extraction** from job descriptions using advanced AI
- **Intelligent bullet point rewriting** for professional impact
- **ATS optimization** with relevant keywords and phrases
- **Real-time AI assistance** for better job descriptions
- **Professional content suggestions** to improve resume quality

### 🎨 **Modern Resume Templates**
- **Professional LaTeX-style formatting** for academic and professional use
- **Multiple template options** (Modern, Classic, Minimal)
- **Real-time preview** with instant updates
- **Print-optimized** design for PDF generation

### 🔧 **Drag-and-Drop Section Reordering**
- **Customizable section order** - arrange sections as you prefer
- **Visual drag handles** for intuitive reordering
- **Persistent order** - saves your preferred layout
- **Real-time preview updates** as you reorder

### 📝 **Comprehensive Resume Sections**
- **Personal Information** - Contact details and professional links
- **Professional Summary** - Compelling career overview
- **Education** - Academic background with GPA and coursework
- **Technical Skills** - Categorized skill sets
- **Prgofessional Experience** - Work history with achievements
- **Academic Projects** - Project experience and contributions
- **Other Work Experience** - Additional employment history
- **Activities** - Extracurricular involvement and leadership

### 🚀 **Advanced Features**
- **Cloud Storage** - Save and access resumes from anywhere
- **Auto-save functionality** - Never lose your work
- **Resume versioning** - Multiple saved versions
- **PDF Export** - Download professional PDF resumes
- **Responsive Design** - Works on desktop, tablet, and mobile

### 🔐 **User Authentication & Security**
- **Secure user accounts** with AWS Cognito integration
- **Personalized dashboard** with resume management
- **Data privacy** - Your information stays secure
- **Session management** for seamless experience



## 🛠️ Technology Stack

### Backend
- **Python 3.11+** - Core application logic
- **Flask** - Web framework
- **AWS Services** - Cloud infrastructure
  - **Cognito** - User authentication
  - **S3** - Resume storage
  - **DynamoDB** - User data management
- **Playwright** - PDF generation
- **OpenAI API** - AI-powered content enhancement

### Frontend
- **HTML5/CSS3** - Modern web standards
- **JavaScript (ES6+)** - Interactive functionality
- **Tailwind CSS** - Responsive styling
- **Drag-and-Drop API** - Section reordering

### Development Tools
- **Git** - Version control
- **Virtual Environment** - Dependency management
- **Requirements.txt** - Package management

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- AWS Account (for cloud features)
- Modern web browser

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-builder.git
   cd resume-builder
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

5. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   FLASK_SECRET_KEY=your_secret_key_here
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=us-east-2
   COGNITO_USER_POOL_ID=your_user_pool_id
   COGNITO_APP_CLIENT_ID=your_app_client_id
   COGNITO_APP_CLIENT_SECRET=your_app_client_secret
   COGNITO_DOMAIN=your_cognito_domain
   S3_BUCKET_NAME=your_s3_bucket_name
   DYNAMODB_TABLE_NAME=your_dynamodb_table_name
   OPENAI_API_KEY=your_openai_api_key
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🚀 Usage Guide

### Creating Your First Resume

1. **Sign Up/Login**
   - Create a new account or sign in with existing credentials
   - Your dashboard will show all saved resumes

2. **Fill Personal Information**
   - Enter your full name, contact details, and professional links
   - Add your location and LinkedIn profile

3. **Write Professional Summary**
   - Craft a compelling 2-3 sentence summary
   - Highlight your key strengths and career goals

4. **Add Education**
   - Include your degree, institution, and graduation date
   - Add GPA and relevant coursework

5. **List Technical Skills**
   - Organize skills by categories (e.g., "Programming: Python, JavaScript")
   - Use semicolons to separate different skill categories
   - **AI Keyword Integration**: Use extracted keywords from job descriptions to enhance your skills section

6. **Add Work Experience**
   - Include job title, company, location, and dates
   - Add detailed bullet points for achievements
   - Use action verbs and quantify results
   - **AI Enhancement**: Click "AI Rewrite" to improve bullet points with professional language

7. **Include Projects**
   - Add academic or personal projects
   - Describe your role and key contributions
   - Highlight technologies and outcomes
   - **AI Enhancement**: Use "AI Rewrite" to enhance project descriptions

8. **Reorder Sections**
   - Drag and drop sections to your preferred order
   - Preview updates in real-time
   - Save your custom layout

### Advanced Features

#### **Section Reordering**
- Click and drag the handle icon on any section
- Drop sections in your preferred order
- Changes are automatically saved

#### **Cloud Storage**
- Click "Save Resume" to store in the cloud
- Access your resumes from any device
- Multiple versions supported

#### **PDF Export**
- Click "Download PDF" for professional output
- Print-ready format for job applications
- Maintains all formatting and styling

#### **AI-Powered Content Enhancement**
- **Job Description Analysis**: Upload job descriptions to extract relevant keywords
- **Smart Keyword Extraction**: AI automatically identifies important skills and requirements
- **Bullet Point Rewriting**: Transform basic descriptions into professional, impactful statements
- **ATS Optimization**: Ensure your resume contains the right keywords for applicant tracking systems
- **Real-time AI Assistance**: Get instant suggestions while writing your resume

## 🏗️ Project Structure

```
resume-builder/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── build.sh              # Deployment script
├── templates/
│   ├── index.html        # Landing page
│   ├── resume_maker.html # Resume builder interface
│   ├── resume_template.html # Resume output template
│   ├── login.html        # Authentication page
│   └── dashboard.html    # User dashboard
├── static/               # CSS, JS, and assets
├── venv/                 # Virtual environment
└── README.md            # This file
```

## 🔧 Configuration

### AWS Services Setup

1. **Cognito User Pool**
   - Create user pool for authentication
   - Configure app client with callback URLs
   - Set up hosted UI domain

2. **S3 Bucket**
   - Create bucket for resume storage
   - Configure CORS and permissions
   - Enable versioning for backup

3. **DynamoDB Table**
   - Create table for user metadata
   - Set up proper indexes
   - Configure access permissions

4. **IAM Permissions**
   - Create IAM user with necessary permissions
   - Attach policies for S3, DynamoDB, and Cognito
   - Generate access keys


## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment (Render)
1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Configure build command: `./build.sh`
4. Deploy automatically on git push

### Other Platforms
- **Heroku**: Add `Procfile` and configure buildpacks
- **AWS Elastic Beanstalk**: Package application and deploy
- **DigitalOcean App Platform**: Connect repository and configure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## 🔄 Version History

- **v2.0.0** - Added drag-and-drop reordering, cloud storage, user authentication
- **v1.5.0** - Enhanced templates, improved PDF generation
- **v1.0.0** - Initial release with basic resume building features

---

**Built with ❤️ for professionals who want to create outstanding resumes**
