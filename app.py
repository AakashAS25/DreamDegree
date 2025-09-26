from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dreamdegree.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Note: Gemini API will be configured per request for better error handling

# Cache for last successful Gemini model to avoid re-listing every request
LAST_WORKING_GEMINI_MODEL = None

# User model for database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    career = db.Column(db.String(100))
    stream = db.Column(db.String(100))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# College data (static for now)
college_data = [
  {
    "name": "Indian Institute of Science (IISc)",
    "city": "Bengaluru",
    "state": "Karnataka",
    "pincode": "560012",
    "nirf_engineering_rank": 1,
    "departments": [
      "Electrical Communication Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Computer Science and Engineering",
      "Aerospace Engineering"
    ]
  },
  {
    "name": "Indian Institute of Technology Madras (IIT Madras)",
    "city": "Chennai",
    "state": "Tamil Nadu",
    "pincode": "600036",
    "nirf_engineering_rank": 2,
    "departments": [
      "Computer Science and Engineering",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Aerospace Engineering"
    ]
  },
  {
    "name": "Indian Institute of Technology Delhi (IIT Delhi)",
    "city": "New Delhi",
    "state": "Delhi",
    "pincode": "110016",
    "nirf_engineering_rank": 3,
    "departments": [
      "Computer Science and Engineering",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Chemical Engineering"
    ]
  },
  {
    "name": "Indian Institute of Technology Bombay (IIT Bombay)",
    "city": "Mumbai",
    "state": "Maharashtra",
    "pincode": "400076",
    "nirf_engineering_rank": 4,
    "departments": [
      "Computer Science and Engineering",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Aerospace Engineering"
    ]
  },
  {
    "name": "National Institute of Technology Tiruchirappalli (NIT Trichy)",
    "city": "Tiruchirappalli",
    "state": "Tamil Nadu",
    "pincode": "620015",
    "nirf_engineering_rank": 5,
    "departments": [
      "Computer Science and Engineering",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Electronics and Communication Engineering"
    ]
  },
  {
    "name": "Birla Institute of Technology and Science (BITS Pilani)",
    "city": "Pilani",
    "state": "Rajasthan",
    "pincode": "333031",
    "nirf_engineering_rank": 6,
    "departments": [
      "Computer Science and Engineering",
      "Electrical and Electronics Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Chemical Engineering"
    ]
  },
  {
    "name": "Vellore Institute of Technology (VIT)",
    "city": "Vellore",
    "state": "Tamil Nadu",
    "pincode": "632014",
    "nirf_engineering_rank": 7,
    "departments": [
      "Computer Science and Engineering",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Electronics and Communication Engineering"
    ]
  },
  {
    "name": "Delhi Technological University (DTU)",
    "city": "New Delhi",
    "state": "Delhi",
    "pincode": "110042",
    "nirf_engineering_rank": 8,
    "departments": [
      "Computer Science and Engineering",
      "Electrical Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Chemical Engineering"
    ]
  },
  {
    "name": "St. Xavier's Catholic College of Engineering",
    "city": "Nagercoil",
    "state": "Tamil Nadu",
    "pincode": "629003",
    "nirf_engineering_rank": 172,
    "departments": [
      "Computer Science and Engineering",
      "Electrical and Electronics Engineering",
      "Electronics and Communication Engineering",
      "Civil Engineering",
      "Information Technology",
      "Mechanical Engineering",
      "Artificial Intelligence and Data Science"
    ]
  },
  {
    "name": "PES University",
    "city": "Bengaluru",
    "state": "Karnataka",
    "pincode": "560085",
    "nirf_engineering_rank": 60,
    "departments": [
      "Computer Science and Engineering",
      "Electrical and Electronics Engineering",
      "Mechanical Engineering",
      "Civil Engineering",
      "Electronics and Communication Engineering"
    ]
  }
]

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Broad questions to decide stream
broad_questions = [
    {
        "id": 1,
        "question": "Which subjects do you prefer?",
        "options": [
            {"text": "Science and Maths", "stream": "Science"},
            {"text": "Arts and Social studies", "stream": "Arts"},
            {"text": "Both equally", "stream": "Both"},
            {"text": "Not sure", "stream": "Undecided"}
        ]
    },
    {
        "id": 2,
        "question": "Do you enjoy lab experiments?",
        "options": [
            {"text": "Yes, very much", "stream": "Science"},
            {"text": "Sometimes", "stream": "Both"},
            {"text": "Rarely", "stream": "Arts"},
            {"text": "Not at all", "stream": "Arts"}
        ]
    },
    {
        "id": 3,
        "question": "Do you like reading literature or history?",
        "options": [
            {"text": "Yes, it fascinates me", "stream": "Arts"},
            {"text": "Sometimes", "stream": "Both"},
            {"text": "Not really", "stream": "Science"},
            {"text": "No interest", "stream": "Science"}
        ]
    },
    {
        "id": 4,
        "question": "Are you interested in technology and gadgets?",
        "options": [
            {"text": "Yes, very much", "stream": "Science"},
            {"text": "Sometimes", "stream": "Both"},
            {"text": "Not really", "stream": "Arts"},
            {"text": "No interest", "stream": "Arts"}
        ]
    },
    {
        "id": 5,
        "question": "How do you prefer to work?",
        "options": [
            {"text": "With formulas and problem solving", "stream": "Science"},
            {"text": "Creative writing and arts", "stream": "Arts"},
            {"text": "A mix of both", "stream": "Both"},
            {"text": "Still unsure", "stream": "Undecided"}
        ]
    },
]

# Detailed questions for science stream
science_questions = [
    {
        "id": 1,
        "question": "Which area excites you most?",
        "options": [
            {"text": "Engineering and machinery", "career": "Engineering"},
            {"text": "Medical and healthcare", "career": "Medical"},
            {"text": "Research and development", "career": "Research"},
            {"text": "Environmental science", "career": "Environmental Science"}
        ]
    },
    {
        "id": 2,
        "question": "What kind of work environment do you prefer?",
        "options": [
            {"text": "Labs and industries", "career": "Engineering"},
            {"text": "Hospitals and clinics", "career": "Medical"},
            {"text": "Research labs and universities", "career": "Research"},
            {"text": "Fieldwork outdoors", "career": "Environmental Science"}
        ]
    },
    {
        "id": 3,
        "question": "What is your strongest skill?",
        "options": [
            {"text": "Building and fixing things", "career": "Engineering"},
            {"text": "Empathy and care", "career": "Medical"},
            {"text": "Analytical thinking", "career": "Research"},
            {"text": "Observation and practical skills", "career": "Environmental Science"}
        ]
    },
    {
        "id": 4,
        "question": "What motivates you most?",
        "options": [
            {"text": "Creating new technology", "career": "Engineering"},
            {"text": "Saving and improving lives", "career": "Medical"},
            {"text": "Discovering new knowledge", "career": "Research"},
            {"text": "Protecting nature", "career": "Environmental Science"}
        ]
    },
    {
        "id": 5,
        "question": "What type of study do you prefer?",
        "options": [
            {"text": "Applied sciences", "career": "Engineering"},
            {"text": "Biological sciences", "career": "Medical"},
            {"text": "Theoretical sciences", "career": "Research"},
            {"text": "Earth and life sciences", "career": "Environmental Science"}
        ]
    },
    {
        "id": 6,
        "question": "Which subject do you perform best in?",
        "options": [
            {"text": "Physics and Mathematics", "career": "Engineering"},
            {"text": "Biology and Chemistry", "career": "Medical"},
            {"text": "Math and Logic", "career": "Research"},
            {"text": "Geography and Biology", "career": "Environmental Science"}
        ]
    },
    {
        "id": 7,
        "question": "Work style you prefer?",
        "options": [
            {"text": "Team projects and building", "career": "Engineering"},
            {"text": "Patient interaction", "career": "Medical"},
            {"text": "Independent analysis and writing", "career": "Research"},
            {"text": "Outdoor data collection and reporting", "career": "Environmental Science"}
        ]
    },
    {
        "id": 8,
        "question": "Future career goal?",
        "options": [
            {"text": "Engineer in tech company", "career": "Engineering"},
            {"text": "Doctor or healthcare professional", "career": "Medical"},
            {"text": "Scientist or professor", "career": "Research"},
            {"text": "Conservationist or environmentalist", "career": "Environmental Science"}
        ]
    },
    {
        "id": 9,
        "question": "Preferred work setting?",
        "options": [
            {"text": "Industry or manufacturing unit", "career": "Engineering"},
            {"text": "Healthcare centers", "career": "Medical"},
            {"text": "Research institutes", "career": "Research"},
            {"text": "Field research centers", "career": "Environmental Science"}
        ]
    },
    {
        "id": 10,
        "question": "What kind of challenges do you enjoy?",
        "options": [
            {"text": "Designing and building systems", "career": "Engineering"},
            {"text": "Diagnosing and treating patients", "career": "Medical"},
            {"text": "Solving scientific puzzles", "career": "Research"},
            {"text": "Conserving ecosystems", "career": "Environmental Science"}
        ]
    },
]

# Detailed questions for arts stream
arts_questions = [
    {
        "id": 1,
        "question": "Which career path interests you most?",
        "options": [
            {"text": "Management and business", "career": "Management Studies"},
            {"text": "Law and justice", "career": "Law"},
            {"text": "Media and communication", "career": "Media Studies"},
            {"text": "Design and arts", "career": "Fine Arts"}
        ]
    },
    {
        "id": 2,
        "question": "Preferred work environment?",
        "options": [
            {"text": "Corporate offices", "career": "Management Studies"},
            {"text": "Courts and legal firms", "career": "Law"},
            {"text": "TV, radio or newspaper", "career": "Media Studies"},
            {"text": "Art studios and galleries", "career": "Fine Arts"}
        ]
    },
    {
        "id": 3,
        "question": "What skill do you excel at?",
        "options": [
            {"text": "Leadership and organizing", "career": "Management Studies"},
            {"text": "Argumentation and analysis", "career": "Law"},
            {"text": "Writing and speaking", "career": "Media Studies"},
            {"text": "Creativity and painting", "career": "Fine Arts"}
        ]
    },
    {
        "id": 4,
        "question": "What motivates you to work?",
        "options": [
            {"text": "Running businesses", "career": "Management Studies"},
            {"text": "Upholding justice", "career": "Law"},
            {"text": "Informing and entertaining", "career": "Media Studies"},
            {"text": "Creating artistic works", "career": "Fine Arts"}
        ]
    },
    {
        "id": 5,
        "question": "What subjects do you enjoy?",
        "options": [
            {"text": "Economics and accounting", "career": "Management Studies"},
            {"text": "Political science and law", "career": "Law"},
            {"text": "Journalism and communication", "career": "Media Studies"},
            {"text": "Drawing and design", "career": "Fine Arts"}
        ]
    },
    {
        "id": 6,
        "question": "Preferred type of projects?",
        "options": [
            {"text": "Business plans and marketing", "career": "Management Studies"},
            {"text": "Legal research and case studies", "career": "Law"},
            {"text": "Media campaigns and storytelling", "career": "Media Studies"},
            {"text": "Art exhibitions and portfolios", "career": "Fine Arts"}
        ]
    },
    {
        "id": 7,
        "question": "Work style you prefer?",
        "options": [
            {"text": "Team leader or manager", "career": "Management Studies"},
            {"text": "Litigation or advisory", "career": "Law"},
            {"text": "Interviewing and reporting", "career": "Media Studies"},
            {"text": "Creating art independently", "career": "Fine Arts"}
        ]
    },
    {
        "id": 8,
        "question": "Long term goal?",
        "options": [
            {"text": "CEO or Business Owner", "career": "Management Studies"},
            {"text": "Judge or Lawyer", "career": "Law"},
            {"text": "Editor or Producer", "career": "Media Studies"},
            {"text": "Renowned artist", "career": "Fine Arts"}
        ]
    },
    {
        "id": 9,
        "question": "Where do you see yourself working?",
        "options": [
            {"text": "Corporate sectors", "career": "Management Studies"},
            {"text": "Courts or legal firms", "career": "Law"},
            {"text": "TV, radio studios", "career": "Media Studies"},
            {"text": "Art galleries or museums", "career": "Fine Arts"}
        ]
    },
    {
        "id": 10,
        "question": "Challenges you enjoy?",
        "options": [
            {"text": "Business strategy and growth", "career": "Management Studies"},
            {"text": "Debates and legal problem solving", "career": "Law"},
            {"text": "Creating impactful stories", "career": "Media Studies"},
            {"text": "Innovative art and concepts", "career": "Fine Arts"}
        ]
    },
]

# Scholarship data
scholarship_data = [
    {
        "scholarship_name": "National Scholarship Portal (NSP)",
        "description": "Platform for applying to multiple government scholarships including Pre/Post Matric and Top Class schemes.",
        "portal_link": "http://scholarships.gov.in"
    },
    {
        "scholarship_name": "Vidyadhan Tamil Nadu Plus 1 Scholarship 2025",
        "description": "Scholarship for meritorious students from economically weaker sections in Tamil Nadu for Plus 1 and Plus 2 studies.",
        "portal_link": "https://vidyadhan.org"
    },
    {
        "scholarship_name": "Post Matric Scholarships, Karnataka (SSP) 2025",
        "description": "Covers tuition, accommodation, and other education expenses for reserved category students in Karnataka.",
        "portal_link": "http://scholarships.gov.in"
    },
    {
        "scholarship_name": "NSP Central Sector Scheme for College and University Students 2025",
        "description": "Supports meritorious students from economically weaker sections pursuing higher education across India.",
        "portal_link": "http://scholarships.gov.in"
    },
    {
        "scholarship_name": "ICCR Scholarships 2025-26",
        "description": "Scholarships offered by Indian Council for Cultural Relations for foreign students and Indian students for higher education.",
        "portal_link": "https://www.indiaingreece.gov.in/page/iccr-scholarships-2025-26/"
    },
    {
        "scholarship_name": "Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP)",
        "description": "Central Sector Scheme for financial assistance to college and university students in India.",
        "portal_link": "https://www.myscheme.gov.in/schemes/csss-cus"
    },
    {
        "scholarship_name": "SC/ST/OBC Scholarship Schemes 2025",
        "description": "Financial aid schemes for SC, ST, and OBC students with coverage for tuition, books, hostel charges, and maintenance.",
        "portal_link": "https://educationforallinindia.com/sc-st-obc-scholarship-schemes-2025-%E2%82%B960000-and-%E2%82%B948000-programs-explained/"
    },
    {
        "scholarship_name": "Reliance Foundation Undergraduate Scholarships 2025-26",
        "description": "Merit-cum-means scholarship offering up to ₹2 lakh to undergraduates with mentorship and alumni support.",
        "portal_link": "https://www.scholarships.reliancefoundation.org/UG_Scholarship.aspx"
    },
    {
        "scholarship_name": "Oasis Scholarship Portal (West Bengal)",
        "description": "Online scholarship platform for SC, ST, and OBC students domiciled in West Bengal.",
        "portal_link": "https://oasis.gov.in"
    },
    {
        "scholarship_name": "Vidyasaarathi Scholarship Portal",
        "description": "Leading independent scholarship platform in India offering a wide range of scholarships.",
        "portal_link": "https://www.vidyasaarathi.co.in"
    }
]

# Entrance Exam data
exam_data = [
    {
        "exam_name": "Joint Entrance Examination (JEE) Main",
        "description": "National level entrance exam for admission to NITs, IIITs, and other centrally funded technical institutions.",
        "portal_url": "https://jeemain.nta.nic.in"
    },
    {
        "exam_name": "Joint Entrance Examination (JEE) Advanced",
        "description": "Entrance exam for admission to the Indian Institutes of Technology (IITs) for candidates who clear JEE Main.",
        "portal_url": "https://jeeadv.ac.in"
    },
    {
        "exam_name": "BITSAT (Birla Institute of Technology and Science Admission Test)",
        "description": "Entrance test for admission to undergraduate engineering programs at BITS Pilani campuses.",
        "portal_url": "https://bitsadmission.com"
    },
    {
        "exam_name": "VITEEE (Vellore Institute of Technology Engineering Entrance Examination)",
        "description": "Entrance exam conducted by VIT University for admissions to undergraduate engineering courses.",
        "portal_url": "https://vit.ac.in"
    },
    {
        "exam_name": "SRMJEEE (SRM Joint Engineering Entrance Examination)",
        "description": "SRM University entrance exam for admission to undergraduate engineering programs.",
        "portal_url": "https://www.srmist.edu.in"
    },
    {
        "exam_name": "COMEDK UGET (Consortium of Medical, Engineering and Dental Colleges of Karnataka Undergraduate Entrance Test)",
        "description": "State-level entrance test for admission to engineering, medical, and dental courses in Karnataka private colleges.",
        "portal_url": "https://comedk.org"
    },
    {
        "exam_name": "MHT CET (Maharashtra Health and Technical Common Entrance Test)",
        "description": "State-level entrance exam for admission to engineering and pharmacy colleges in Maharashtra.",
        "portal_url": "https://cetcell.mahacet.org"
    },
    {
        "exam_name": "WBJEE (West Bengal Joint Entrance Examination)",
        "description": "State-level entrance exam for engineering admissions in colleges of West Bengal.",
        "portal_url": "https://wbjeeb.nic.in"
    },
    {
        "exam_name": "TNEA (Tamil Nadu Engineering Admissions)",
        "description": "Counseling and entrance process for admission to engineering courses in Tamil Nadu government and private colleges; based on 12th board marks.",
        "portal_url": "https://www.tneaonline.in"
    },
    {
        "exam_name": "KEAM (Kerala Engineering Architecture Medical)",
        "description": "State-level entrance exam for engineering, architecture, and medical courses in Kerala.",
        "portal_url": "https://cee.kerala.gov.in"
    }
]

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Find user in database
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!')
            # If user has not chosen stream/career, go to quiz
            if not user.stream or not user.career:
                return redirect(url_for('quiz'))
            # Otherwise, go to dashboard
            session['stream'] = user.stream
            session['career'] = user.career
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!')
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

# Home route (redirect to login if not authenticated)
@app.route('/')
def home():
    if current_user.is_authenticated:
        # If user has not chosen stream/career, go to quiz
        if not getattr(current_user, 'stream', None) or not getattr(current_user, 'career', None):
            return redirect(url_for('quiz'))
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Quiz route (choose stream/career)
@app.route('/quiz')
@login_required
def quiz():
    return render_template('index.html')

@app.route('/questions/broad', methods=['GET'])
def get_broad_questions():
    clean_questions = []
    for q in broad_questions:
        clean_q = {
            "id": q["id"],
            "question": q["question"],
            "options": [opt["text"] for opt in q["options"]]
        }
        clean_questions.append(clean_q)
    return jsonify(clean_questions)

@app.route('/questions/detailed/<stream>', methods=['GET'])
def get_detailed_questions(stream):
    if stream == "Science":
        qlist = science_questions
    elif stream == "Arts":
        qlist = arts_questions
    else:
        return jsonify({"error": "Invalid stream"}), 400
    clean_questions = []
    for q in qlist:
        clean_q = {
            "id": q["id"],
            "question": q["question"],
            "options": [opt["text"] for opt in q["options"]]
        }
        clean_questions.append(clean_q)
    return jsonify(clean_questions)

@app.route('/submit_answers/broad', methods=['POST'])
@login_required
def submit_broad_answers():
    answers = request.json
    stream_scores = {"Science": 0, "Arts": 0, "Both": 0, "Undecided": 0}
    for i, selected_index in enumerate(answers):
        stream = broad_questions[i]["options"][selected_index]["stream"]
        stream_scores[stream] += 1
    recommended_stream = max(stream_scores, key=stream_scores.get)
    # Save to user and session
    current_user.stream = recommended_stream
    db.session.commit()
    session['stream'] = recommended_stream
    return jsonify({"stream": recommended_stream})

@app.route('/submit_answers/detailed/<stream>', methods=['POST'])
@login_required
def submit_detailed_answers(stream):
    answers = request.json
    if stream == "Science":
        qlist = science_questions
    elif stream == "Arts":
        qlist = arts_questions
    else:
        return jsonify({"error": "Invalid stream"}), 400

    career_scores = {opt["career"]: 0 for q in qlist for opt in q["options"]}

    for i, selected_index in enumerate(answers):
        career = qlist[i]["options"][selected_index]["career"]
        career_scores[career] += 1

    recommended_career = max(career_scores, key=career_scores.get)
    # Save to user and session
    current_user.career = recommended_career
    db.session.commit()
    session['career'] = recommended_career
    return jsonify({"career": recommended_career})

@app.route('/roadmap/<career>')
def roadmap(career):
    valid_careers = {
        'Engineering', 'Medical', 'Research', 'Environmental Science',
        'Management Studies', 'Law', 'Media Studies', 'Fine Arts'
    }
    if career not in valid_careers:
        return "Roadmap not found", 404
    return render_template('roadmap.html', career=career)

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's name and career/stream from session or default
    username = current_user.username
    career = session.get('career', 'Not selected')
    stream = session.get('stream', 'Not selected')
    return render_template('dashboard.html', username=username, career=career, stream=stream)

# Route to serve college data as JSON
@app.route('/colleges')
def get_colleges():
    return jsonify(college_data)

# College page route
@app.route('/college')
@login_required
def college():
    return render_template('college.html')

# Scholarship page route
@app.route('/scholarships')
@login_required
def scholarships():
    return render_template('scholarships.html', scholarships=scholarship_data)

# Route to serve scholarship data as JSON
@app.route('/scholarships-data')
def get_scholarships():
    return jsonify(scholarship_data)

# Application Portal page route
@app.route('/application-portal')
@login_required
def application_portal():
    return render_template('application_portal.html', exams=exam_data)

# Route to serve exam data as JSON
@app.route('/exams-data')
def get_exams():
    return jsonify(exam_data)

# Career Guidance Bot routes
@app.route('/career-guidance-bot')
@login_required
def career_guidance_bot():
    return render_template('career_guidance.html')

@app.route('/career-guidance', methods=['POST'])
@login_required
def career_guidance():
    try:
        # Check if API key is configured
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return jsonify({
                'success': False, 
                'error': 'API key not configured. Please contact administrator.'
            })
        
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({'success': False, 'error': 'No message provided'})
        
        # Get user's career and stream context
        user_career = current_user.career or "Not yet determined"
        user_stream = current_user.stream or "Not yet determined"
        user_name = current_user.username or "Student"
        
        # Create a comprehensive career guidance prompt
        career_expert_prompt = f"""
        You are a highly experienced Career Guidance Counselor and Education Expert with over 20 years of experience helping students and professionals navigate their career paths. Your expertise includes:

        - Career assessment and matching
        - Educational pathway guidance
        - Industry insights and job market trends
        - Skills development recommendations
        - Interview and resume guidance
        - Salary and growth prospects analysis

        Student Context:
        - Student Name: {user_name}
        - Current Career Interest: {user_career}
        - Academic Stream: {user_stream}
        - Platform: DreamDegree Career Guidance System

        Guidelines for your responses:
        1. Address the student by their name ({user_name}) in your response
        2. Be supportive, encouraging, and professional
        3. Provide specific, actionable advice
        4. Include relevant examples and real-world insights
        5. Mention specific skills, courses, or certifications when applicable
        6. Consider current market trends and future prospects
        7. Be honest about challenges while remaining positive
        8. Keep responses concise but comprehensive (200-400 words)
        9. Use a warm, mentoring tone

        Student's Question: {user_message}

        Please provide a detailed, personalized response as their career guidance counselor, making sure to address {user_name} by name:
        """
        
        # Configure Gemini API with fresh instance
        genai.configure(api_key=api_key)
        
        global LAST_WORKING_GEMINI_MODEL
        model = None
        quota_exceeded = False
        last_error = None

        preferred_models = []
        # If we already have a working model cached, try it first
        if LAST_WORKING_GEMINI_MODEL:
            preferred_models.append(LAST_WORKING_GEMINI_MODEL)
        # Known lightweight / broadly accessible model we saw working
        preferred_models.append('models/gemini-1.5-flash-8b')
        # Add generic names as fallbacks (may or may not exist for account)
        preferred_models.extend([
            'gemini-1.5-flash',
            'gemini-1.5-flash-latest',
            'gemini-pro',
            'gemini-1.5-pro'
        ])

        tried = set()

        def try_model(name):
            nonlocal model, quota_exceeded, last_error
            if name in tried:
                return False
            tried.add(name)
            try:
                candidate = genai.GenerativeModel(name)
                test = candidate.generate_content("Hi")
                if test and getattr(test, 'text', None):
                    model = candidate
                    print(f"[Gemini] Using model: {name}")
                    return True
            except Exception as ex:
                err = str(ex)
                last_error = err
                print(f"[Gemini] Model {name} failed: {err}")
                if '429' in err or 'quota' in err.lower():
                    quota_exceeded = True
            return False

        # 1. Try preferred list
        for mname in preferred_models:
            if try_model(mname):
                LAST_WORKING_GEMINI_MODEL = mname
                break

        # 2. If still none and no quota issue, attempt discovery once
        if model is None and not quota_exceeded:
            try:
                print("[Gemini] Discovering available models...")
                for m in genai.list_models():
                    if 'generateContent' in getattr(m, 'supported_generation_methods', []):
                        if try_model(m.name):
                            LAST_WORKING_GEMINI_MODEL = m.name
                            break
            except Exception as disc_err:
                print(f"[Gemini] Discovery failed: {disc_err}")
                if not last_error:
                    last_error = str(disc_err)

        if quota_exceeded and model is None:
            return jsonify({
                'success': False,
                'error': 'Daily usage limit reached for AI service. Please try again tomorrow or upgrade your plan.'
            })

        if model is None:
            print(f"[Gemini] No working model. Last error: {last_error}")
            fallback_response = f"""
            Hi {user_name}! 👋\n\nI'm currently experiencing technical difficulties, but I'm here to help with your career guidance needs.\n\nBased on your interest in {user_career} and {user_stream} stream, here are some general recommendations:\n\n🎯 Career Development Tips:\n• Research industry trends and required skills\n• Build a strong portfolio showcasing your work\n• Network with professionals in your field\n• Consider internships and hands-on experience\n• Stay updated with latest technologies and methodologies\n\n📚 Educational Path:\n• Focus on core subjects related to your stream\n• Develop both technical and soft skills\n• Look into certifications relevant to your career\n• Join professional communities and forums\n\n🔍 Next Steps:\n• Explore college programs that align with your goals\n• Research scholarship opportunities\n• Connect with mentors in your field of interest\n\nPlease try again later for more personalized AI-powered guidance, or feel free to ask specific questions!"""
            return jsonify({'success': True, 'response': fallback_response})
        
        # Generate response using Gemini
        response = model.generate_content(career_expert_prompt)
        
        if response.text:
            return jsonify({
                'success': True, 
                'response': response.text
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'Unable to generate response from AI service'
            })
            
    except Exception as e:
        print(f"Career guidance error: {str(e)}")
        # Check for common API errors
        if "API_KEY_INVALID" in str(e):
            return jsonify({
                'success': False, 
                'error': 'Invalid API key. Please check your configuration.'
            })
        elif "QUOTA_EXCEEDED" in str(e):
            return jsonify({
                'success': False, 
                'error': 'API quota exceeded. Please try again later.'
            })
        elif "PERMISSION_DENIED" in str(e):
            return jsonify({
                'success': False, 
                'error': 'API access denied. Please check your API key permissions.'
            })
        else:
            return jsonify({
                'success': False, 
                'error': f'Service temporarily unavailable. Error: {str(e)}'
            })

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)