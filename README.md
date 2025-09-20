# 🎓 DreamDegree - AI-Powered Career Guidance Platform

## 📋 Overview

DreamDegree is an intelligent career guidance platform that helps students make informed decisions about their educational and career paths. Powered by Google's Gemini AI, the platform provides personalized career counseling, college recommendations, and educational resources.

## ✨ Features

### 🤖 AI Career Guidance
- **Personalized AI Counselor**: Powered by Google Gemini AI with expert-level career guidance prompts
- **Real-time Chat Interface**: Interactive chatbot with typing indicators and quick question prompts
- **Context-Aware Responses**: AI considers user's academic stream, career interests, and personal profile
- **Professional Guidance**: Responses formatted as an experienced career counselor with 20+ years of experience

### 🏛️ College Information System
- **Comprehensive College Database**: Detailed information about top engineering colleges in India
- **NIRF Rankings**: Colleges ranked according to National Institutional Ranking Framework
- **Department-wise Information**: Detailed department listings and specializations
- **Location-based Search**: Find colleges by state, city, and pincode

### 🎯 User Management
- **Secure Authentication**: User registration and login with password hashing
- **Profile Management**: Store career interests and academic stream preferences
- **Session Management**: Persistent user sessions with Flask-Login
- **Personalized Experience**: Tailored content based on user profile

### 📚 Educational Resources
- **Career Roadmaps**: Step-by-step guidance for different career paths
- **Scholarship Information**: Details about available scholarships and financial aid
- **Application Portal**: Streamlined college application process
- **Dashboard**: Centralized hub for all user activities

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Login
- **AI Integration**: Google Generative AI (Gemini)
- **Security**: Werkzeug password hashing

### Frontend
- **Template Engine**: Jinja2
- **Styling**: Modern CSS with gradients and animations
- **Interactive Elements**: Real-time chat interface
- **Responsive Design**: Mobile-friendly layouts

### Configuration
- **Environment Management**: python-dotenv
- **API Security**: Environment variables for API keys
- **Database**: SQLite for development (easily scalable to PostgreSQL/MySQL)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Quick Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AakashAS25/DreamDegree.git
   cd DreamDegree
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Copy environment template
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```

5. **Configure API Keys**
   Edit `.env` file and add your credentials:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   FLASK_SECRET_KEY=your_flask_secret_key_here
   DATABASE_URL=sqlite:///dreamdegree.db
   ```

6. **Get Google Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

7. **Initialize Database**
   ```bash
   python app.py
   # Database will be created automatically on first run
   ```

8. **Run the Application**
   ```bash
   python app.py
   ```

9. **Access the Platform**
   Open your browser and navigate to: `http://localhost:5000`

## 🚀 Usage

### Getting Started
1. **Register**: Create a new account with username and password
2. **Login**: Access your personalized dashboard
3. **Set Profile**: Add your career interests and academic stream
4. **Explore**: Browse colleges, scholarships, and career information
5. **Get Guidance**: Chat with the AI career counselor for personalized advice

### AI Career Guidance
1. Navigate to the **Career Guidance** section
2. Type your career-related questions
3. Receive personalized advice from the AI counselor
4. Ask follow-up questions for deeper insights

### College Search
1. Browse the comprehensive college database
2. Filter by rankings, location, or departments
3. View detailed college profiles
4. Access application information

## 📁 Project Structure

```
DreamDegree/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
├── templates/                 # HTML templates
│   ├── index.html            # Landing page
│   ├── dashboard.html        # User dashboard
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── career_guidance.html  # AI chat interface
│   ├── college.html          # College listings
│   ├── roadmap.html          # Career roadmaps
│   ├── scholarships.html     # Scholarship information
│   └── application_portal.html # Application portal
├── instance/                  # Instance-specific files
│   └── dreamdegree.db        # SQLite database (auto-generated)
└── venv/                     # Virtual environment (created during setup)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini AI API key | Yes |
| `FLASK_SECRET_KEY` | Flask session security key | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |

### Database Schema

#### Users Table
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password
- `career`: Career interest
- `stream`: Academic stream

## 🤖 AI Integration

### Google Gemini AI Features
- **Model**: gemini-1.5-flash
- **Expert Prompting**: Configured as experienced career counselor
- **Context Awareness**: Considers user profile and preferences
- **Personalization**: Addresses users by name
- **Professional Tone**: Maintains counselor persona

### AI Prompt Engineering
The AI is configured with:
- 20+ years of career counseling experience
- Industry insights and job market trends
- Skills development recommendations
- Educational pathway guidance
- Interview and resume guidance

## 🔒 Security Features

- **Password Security**: Werkzeug password hashing
- **Environment Protection**: `.gitignore` configured for sensitive files
- **Session Management**: Secure Flask sessions
- **API Key Protection**: Environment variable storage
- **Input Validation**: Request data validation

## 🚀 Deployment

### Local Development
```bash
python app.py
# Application runs on http://localhost:5000
```

### Production Deployment
1. **Environment Setup**: Configure production environment variables
2. **Database**: Migrate to PostgreSQL or MySQL for production
3. **WSGI Server**: Use Gunicorn or uWSGI
4. **Reverse Proxy**: Configure Nginx or Apache
5. **SSL**: Enable HTTPS for security

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

**API Key Issues**
- Ensure your Gemini API key is valid and active
- Check API quotas and usage limits
- Verify environment variable configuration

**Database Issues**
- Database is created automatically on first run
- Check write permissions in the project directory
- Ensure SQLite is properly installed

**Installation Issues**
- Use Python 3.8 or higher
- Ensure all dependencies are installed via requirements.txt
- Check virtual environment activation

### Getting Help
- **Issues**: Report bugs via GitHub Issues
- **Documentation**: Check this README for setup instructions
- **Community**: Join discussions in the repository

## 🙏 Acknowledgments

- **Google AI**: For providing the Gemini AI API
- **Flask Community**: For the excellent web framework
- **Open Source Contributors**: For the amazing Python ecosystem

## 📧 Contact

**Project Maintainer**: Aakash AS  
**GitHub**: [@AakashAS25](https://github.com/AakashAS25)  
**Repository**: [DreamDegree](https://github.com/AakashAS25/DreamDegree)

---

*Building the future of career guidance with AI 🚀*