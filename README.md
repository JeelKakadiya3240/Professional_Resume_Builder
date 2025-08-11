# Professional Resume Builder

A modern, feature-rich web application for creating professional resumes with drag-and-drop section reordering, real-time preview, and cloud storage capabilities.

![Resume Builder](https://img.shields.io/badge/Resume-Builder-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Flask](https://img.shields.io/badge/Flask-2.0+-orange)
![AWS](https://img.shields.io/badge/AWS-Integrated-yellow)

## ✨ Features

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
- **Professional Experience** - Work history with achievements
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

### 🎯 **Smart Content Enhancement**
- **Keyword extraction** from job descriptions
- **Content optimization** for better ATS compatibility
- **Professional writing suggestions**
- **Bullet point enhancement**

## 🛠️ Technology Stack

### Backend
- **Python 3.11+** - Core application logic
- **Flask** - Web framework
- **AWS Services** - Cloud infrastructure
  - **Cognito** - User authentication
  - **S3** - Resume storage
  - **DynamoDB** - User data management
- **Playwright** - PDF generation

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

6. **Add Work Experience**
   - Include job title, company, location, and dates
   - Add detailed bullet points for achievements
   - Use action verbs and quantify results

7. **Include Projects**
   - Add academic or personal projects
   - Describe your role and key contributions
   - Highlight technologies and outcomes

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

#### **Content Enhancement**
- Use the "Add Job Description" modal
- Extract relevant keywords automatically
- Enhance bullet points with professional suggestions

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

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FLASK_SECRET_KEY` | Flask session encryption | Yes |
| `AWS_ACCESS_KEY_ID` | AWS access key | Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Yes |
| `AWS_REGION` | AWS region | Yes |
| `COGNITO_USER_POOL_ID` | Cognito user pool ID | Yes |
| `COGNITO_APP_CLIENT_ID` | Cognito app client ID | Yes |
| `COGNITO_APP_CLIENT_SECRET` | Cognito app client secret | Yes |
| `COGNITO_DOMAIN` | Cognito hosted UI domain | Yes |
| `S3_BUCKET_NAME` | S3 bucket for resumes | Yes |
| `DYNAMODB_TABLE_NAME` | DynamoDB table name | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Yes |

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

## 🆘 Support

- **Documentation**: Check this README for detailed instructions
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Email**: Contact support at support@resumebuilder.com

## 🔄 Version History

- **v2.0.0** - Added drag-and-drop reordering, cloud storage, user authentication
- **v1.5.0** - Enhanced templates, improved PDF generation
- **v1.0.0** - Initial release with basic resume building features

---

**Built with ❤️ for professionals who want to create outstanding resumes**
