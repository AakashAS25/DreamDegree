from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory user store (replace with DB in production)
users = {}

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


# Route to serve college data as JSON
@app.route('/colleges')
def get_colleges():
    return jsonify(college_data)


from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

# College page route
@app.route('/college')
@login_required
def college():
    return render_template('college.html')
from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

# College page route
@app.route('/college')
@login_required
def college():
    return render_template('college.html')

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory user store (replace with DB in production)
users = {}

class User(UserMixin):
    def __init__(self, id, username, password_hash, stream=None, career=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.stream = stream
        self.career = career
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.get_id() == user_id:
            return user
    return None

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


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists!')
            return redirect(url_for('register'))
        user = User(id=len(users)+1, username=username, password_hash=generate_password_hash(password))
        users[username] = user
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user.password_hash, password):
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
    users[current_user.username].stream = recommended_stream
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
    users[current_user.username].career = recommended_career
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


if __name__ == '__main__':
    app.run(debug=True)
