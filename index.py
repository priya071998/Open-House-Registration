from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, render_template, session, redirect, url_for
import pandas as pd
from celery import Celery
from celery.schedules import crontab
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
from flask import g

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'

schools = [
    "Admiralty Secondary School",
    "Ahmad Ibrahim Secondary School",
    "Anderson Secondary School",
    "Anglican High School",
    "Anglo-Chinese School (Barker Road)",
    "Anglo-Chinese School (Independent)",
    "Ang Mo Kio Secondary School",
    "Assumption English School",
    "Bartley Secondary School",
    "Beatty Secondary School",
    "Bedok Green Secondary School",
    "Bedok South Secondary School",
    "Bedok View Secondary School",
    "Bendemeer Secondary School",
    "Boon Lay Secondary School",
    "Bowen Secondary School",
    "Broadrick Secondary School",
    "Bukit Batok Secondary School",
    "Bukit Merah Secondary School",
    "Bukit Panjang Government High School",
    "Bukit View Secondary School",
    "Catholic High School",
    "Canberra Secondary School",
    "Cedar Girls' Secondary School",
    "Changkat Changi Secondary School",
    "CHIJ Katong Convent (Secondary)",
    "CHIJ Secondary (Toa Payoh)",
    "CHIJ St. Joseph's Convent",
    "CHIJ St. Nicholas Girls' School",
    "CHIJ St. Theresa's Convent",
    "Chua Chu Kang Secondary School",
    "Christ Church Secondary School",
    "Chung Cheng High School (Main)",
    "Chung Cheng High School (Yishun)",
    "Clementi Town Secondary School",
    "Commonwealth Secondary School",
    "Compassvale Secondary School",
    "Crescent Girls' School",
    "Damai Secondary School",
    "Deyi Secondary School",
    "Dunearn Secondary School",
    "Dunman High School",
    "Dunman Secondary School",
    "East Spring Secondary School",
    "Edgefield Secondary School",
    "Evergreen Secondary School",
    "Fairfield Methodist Secondary School",
    "Fuchun Secondary School",
    "Fuhua Secondary School",
    "Gan Eng Seng School",
    "Geylang Methodist School (Secondary)",
    "Greendale Secondary School",
    "Greenridge Secondary School",
    "Guangyang Secondary School",
    "Hai Sing Catholic School",
    "Hillgrove Secondary School",
    "Holy Innocents' High School",
    "Hougang Secondary School",
    "Hua Yi Secondary School",
    "Hwa Chong Institution",
    "Junyuan Secondary School",
    "Jurong Secondary School",
    "Jurong West Secondary School",
    "Jurongville Secondary School",
    "Juying Secondary School",
    "Kent Ridge Secondary School",
    "Kranji Secondary School",
    "Kuo Chuan Presbyterian Secondary School",
    "Loyang View Secondary School",
    "Manjusri Secondary School",
    "Maris Stella High School",
    "Marsiling Secondary School",
    "Mayflower Secondary School",
    "Meridian Secondary School",
    "Methodist Girls' School (Secondary)",
    "Montfort Secondary School",
    "Nan Chiau High School",
    "Nan Hua High School",
    "Nanyang Girls' High School",
    "National Junior College",
    "Naval Base Secondary School",
    "New Town Secondary School",
    "Ngee Ann Secondary School",
    "North Vista Secondary School",
    "Northbrooks Secondary School",
    "Northland Secondary School",
    "NUS High School of Mathematics and Science",
    "Orchid Park Secondary School",
    "Outram Secondary School",
    "Pasir Ris Crest Secondary School",
    "Pasir Ris Secondary School",
    "Paya Lebar Methodist Girls' School (Secondary)",
    "Pei Hwa Secondary School",
    "Peicai Secondary School",
    "Peirce Secondary School",
    "Presbyterian High School",
    "Punggol Secondary School",
    "Queenstown Secondary School",
    "Queensway Secondary School",
    "Raffles Girls' School (Secondary)"
    "Raffles Institution",
    "Regent Secondary School",
    "Riverside Secondary School",
    "River Valley High School",
    "St. Andrew's Secondary School",
    "St. Patrick's School",
    "School of Science and Technology, Singapore",
    "School of the Arts",
    "Sembawang Secondary School",
    "Sengkang Secondary School",
    "Serangoon Garden Secondary School",
    "Serangoon Secondary School",
    "Singapore Chinese Girls' School",
    "Singapore Sports School",
    "Springfield Secondary School",
    "St. Anthony's Canossian Secondary School",
    "St. Gabriel's Secondary School",
    "St. Hilda's Secondary School",
    "St. Margaret's Secondary School",
    "St. Joseph's Institution",
    "Swiss Cottage Secondary School",
    "Tanglin Secondary School",
    "Tampines Secondary School",
    "Tanjong Katong Girls' School",
    "Tanjong Katong Secondary School",
    "Temasek Junior College",
    "Temasek Secondary School",
    "Unity Secondary School",
    "Victoria School",
    "West Spring Secondary School",
    "Westwood Secondary School",
    "Whitley Secondary School",
    "Woodgrove Secondary School",
    "Woodlands Ring Secondary School",
    "Woodlands Secondary School",
    "Xinmin Secondary School",
    "Yio Chu Kang Secondary School",
    "Yishun Secondary School",
    "Yishun Town Secondary School",
    "Yuan Ching Secondary School",
    "Yuhua Secondary School",
    "Yusof Ishak Secondary School",
    "Yuying Secondary School",
    "Zhenghua Secondary School",
    "Zhonghua Secondary School"
];

# Celery configuration
celery = Celery(__name__, broker='http://127.0.0.1:5000')

# Connect to the database
engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)
Session = sessionmaker(bind=engine)
# Define the base for SQLAlchemy models
base = declarative_base()


class Feedback(base):
    __tablename__ = 'Feedback'
    feedback_id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    age = Column(Integer)
    school = Column(String)
    distance = Column(String)
    privacy = Column(String)
    ai_travel_rating = Column(Integer, nullable=True)
    break_the_code_rating = Column(Integer, nullable=True)
    classroom_rating = Column(Integer, nullable=True)
    drones_rating = Column(Integer, nullable=True)
    global_warming_rating = Column(Integer, nullable=True)
    our_courses_rating = Column(Integer, nullable=True)
    industry_partners_rating = Column(Integer, nullable=True)
    protect_our_sky_rating = Column(Integer, nullable=True)
    pursue_your_dreams_rating = Column(Integer, nullable=True)
    sit_tour_rating = Column(Integer, nullable=True)

    def __init__(self, age, email, school, distance, privacy, password,ai_travel_rating=0, break_the_code_rating=0,
                classroom_rating=0,
                 drones_rating=0, global_warming_rating=0, our_courses_rating=0,
                 industry_partners_rating=0, protect_our_sky_rating=0,
                 pursue_your_dreams_rating=0, sit_tour_rating=0):
        self.email = email
        self.age = age
        self.school = school
        self.distance = distance
        self.privacy = privacy
        self.password = password
        self.ai_travel_rating = ai_travel_rating
        self.break_the_code_rating = break_the_code_rating
        self.classroom_rating = classroom_rating
        self.drones_rating = drones_rating
        self.global_warming_rating = global_warming_rating
        self.our_courses_rating = our_courses_rating
        self.industry_partners_rating = industry_partners_rating
        self.protect_our_sky_rating = protect_our_sky_rating
        self.pursue_your_dreams_rating = pursue_your_dreams_rating
        self.sit_tour_rating = sit_tour_rating


class User(base):
    __tablename__ = 'User'
    registration_id = Column(Integer, primary_key=True)
    email = Column(String(200))
    password = Column(String(200))

    def __init__(self, email, password):
        self.email = email
        self.password = password


# Create the database tables
base.metadata.create_all(engine)


# Function to update Excel file from database
def update_excel():
    try:
        engine = create_engine('sqlite:///sqlalchemy.sqlite')
        # Query the database to fetch new data
        query = "SELECT * FROM Feedback"
        df_feedback = pd.read_sql_query(query, engine)
        df_feedback = df_feedback.drop(columns=['feedback_id'])
        df_feedback = df_feedback.rename(columns={
            'feedback_id': '',
            'email': 'Email',
            'password': 'Password',
            'name': 'Name',
            'age': 'Age',
            'gender': 'Gender',
            'school': 'School',
            'distance': 'Distance to NYP',
            'privacy': 'Consent to Data Collection',
        })
        # Export the DataFrame to an Excel file
        excel_file = "submitted_feedback_data.xlsx"
        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
            df_feedback.to_excel(writer, sheet_name="Feedback", index=False)
    except Exception as e:
        print(f"Error generating Excel file: {str(e)}")


# Celery task to update Excel file
@celery.task
def scheduled_update():
    update_excel()


# Schedule the Celery task to run daily at midnight
celery.conf.beat_schedule = {
    'update-excel': {
        'task': 'scheduled_update',
        'schedule': crontab(minute=0, hour=0),  # Run daily at midnight
    },
}


@app.route('/update_excel_manually')
def update_excel_manually():
    update_excel()
    return "Excel updated manually"


@app.route('/success')
def success():
    return render_template('success.html')


def is_duplicate_email(email):
    Session = sessionmaker(bind=engine)
    session = Session()
    existing_feedback = session.query(Feedback).filter(Feedback.email == email).first()
    session.close()
    return existing_feedback is not None


@app.route('/')
def home():
    return render_template('home.html')


@app.before_request
def before_request():
    g.user_email = session.get('user_email', None)


@app.route('/dashboard')
def dashboard():
    error_message = ''

    if request.method == 'POST':
        age = request.form.get('age')
        school = request.form.get('school')
        distance = request.form.get('distance')
        privacy = request.form.get('privacy')
        password = request.form.get('password')
        ai_travel_rating = request.form.get('ai_travel_rating', 0)
        break_the_code_rating = request.form.get('break_the_code_rating', 0)
        classroom_rating = request.form.get('classroom_rating', 0)
        drones_rating = request.form.get('drones_rating', 0)
        global_warming_rating = request.form.get('global_warming_rating', 0)
        our_courses_rating = request.form.get('our_courses_rating', 0)
        industry_partners_rating = request.form.get('industry_partners_rating', 0)
        protect_our_sky_rating = request.form.get('protect_our_sky_rating', 0)
        pursue_your_dreams_rating = request.form.get('pursue_your_dreams_rating', 0)
        sit_tour_rating = request.form.get('sit_tour_rating', 0)
        # Get the current user's email from the context
        email = g.user_email

        # Fetch the existing feedback for the user
        Session = sessionmaker(bind=engine)
        session = Session()
        user_feedback = session.query(Feedback).filter_by(email=email).first()

        if user_feedback:
            # Update the existing feedback with the new ratings
            user_feedback.ai_travel_rating = request.form.get('ai_travel_rating', 0)
            user_feedback.break_the_code_rating = request.form.get('break_the_code_rating', 0)
            user_feedback.classroom_rating = request.form.get('classroom_rating', 0)
            user_feedback.drones_rating = request.form.get('drones_rating', 0)
            user_feedback.global_warming_rating = request.form.get('global_warming_rating', 0)
            user_feedback.our_courses_rating = request.form.get('our_courses_rating', 0)
            user_feedback.industry_partners_rating = request.form.get('industry_partners_rating', 0)
            user_feedback.protect_our_sky_rating = request.form.get('protect_our_sky_rating', 0)
            user_feedback.pursue_your_dreams_rating = request.form.get('pursue_your_dreams_rating', 0)
            user_feedback.sit_tour_rating = request.form.get('sit_tour_rating', 0)
        else:
            # Create a new feedback entry if it doesn't exist
            user_feedback = Feedback(email=email,
                                     ai_travel_rating=request.form.get('ai_travel_rating', 0),
                                     break_the_code_rating=request.form.get('break_the_code_rating', 0),
                                     classroom_rating=request.form.get('classroom_rating', 0),
                                     drones_rating=request.form.get('drones_rating', 0),
                                     global_warming_rating=request.form.get('global_warming_rating', 0),
                                     our_courses_rating=request.form.get('our_courses_rating', 0),
                                     industry_partners_rating=request.form.get('industry_partners_rating', 0),
                                     protect_our_sky_rating=request.form.get('protect_our_sky_rating', 0),
                                     pursue_your_dreams_rating=request.form.get('pursue_your_dreams_rating', 0),
                                     sit_tour_rating=request.form.get('sit_tour_rating', 0))
            error_message = 'Feedback record not found for the user.'
        session.add(user_feedback)
        session.commit()
        session.close()

    elif request.method == 'GET':

        email = g.user_email

        Session = sessionmaker(bind=engine)

        session = Session()

        user_feedback = session.query(Feedback).filter_by(email=email).first()

        session.close()

        if user_feedback:
            # Render the dashboard template with the existing ratings

            return render_template('dashboard.html', error_message=error_message, user_feedback=user_feedback)

    return render_template('dashboard.html', error_message=error_message)


def is_valid_login(email, password):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(Feedback).filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session.close()
        return True

    session.close()
    return False


# Handle form submissions
@app.route('/index', methods=['GET', 'POST'])
def index():
    error_message = ''  # Initialize an empty error message

    if request.method == 'POST':
        age = request.form['age']
        email = request.form['email']
        password = request.form['password']
        school = request.form['school']
        distance = request.form['distance']
        privacy = request.form['privacy']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error_message = 'Passwords do not match'
            return render_template('index.html', error_message='Password and Confirm Password do not match', schools=schools)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Check if the email already exists in the database
        if is_duplicate_email(email):
            error_message = 'This email already exists.'
        if school == "Others":
            school = request.form['otherSchool']

        if not error_message:
            # Create a new Feedback object and add it to the database
            feedback = Feedback(age=age, email=email, school=school,
                                distance=distance, privacy=privacy, password=hashed_password)

            # Create a session to interact with the database
            Session = sessionmaker(bind=engine)
            session = Session()

            # Add the feedback object to the session
            session.add(feedback)

            # Commit the changes to the database
            session.commit()
            session.close()
            # Close the session

            update_excel()

            return redirect(url_for('login'))

    if request.method == 'GET' or error_message:
        return render_template('index.html', error_message=error_message, schools=schools)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the login credentials are valid
        if is_valid_login(email, password):
            # If valid, set a session variable to indicate the user is logged in
            session['logged_in'] = True
            session['user_email'] = email  # Set the user's email in the session
            return redirect('/dashboard')  # Redirect to the dashboard page

        # If login credentials are invalid, show an error message
        error_message = 'Invalid email or password.'
        flash(error_message, 'error')  # Flash the error message

    return render_template('login.html', error_message=error_message)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Remove the 'logged_in' session variable
    session.pop('user_email', None)  # Remove the 'user_email' session variable
    return redirect('/')


@app.route('/submit_ratings', methods=['POST'])
def submit_ratings():
    if 'logged_in' not in session:
        return redirect('/login') # Redirect to if not logged in

    # Get the logged-in user's email from the session
    email = session['user_email']

    # Fetch the existing feedback for the user
    Session = sessionmaker(bind=engine)
    db_session = Session() # Rename the 'session' variable to 'db_session'
    user_feedback = db_session.query(Feedback).filter_by(email=email).first()

    if user_feedback:
        # Update the existing feedback with the new ratings
        user_feedback.ai_travel_rating = int(request.form.get('ai_travel_rating', 0))
        user_feedback.break_the_code_rating = int(request.form.get('break_the_code_rating', 0))
        user_feedback.classroom_rating = int(request.form.get('classroom_rating', 0))
        user_feedback.drones_rating = int(request.form.get('drones_rating', 0))
        user_feedback.global_warming_rating = int(request.form.get('global_warming_rating', 0))
        user_feedback.our_courses_rating = int(request.form.get('our_courses_rating', 0))
        user_feedback.industry_partners_rating = int(request.form.get('industry_partners_rating', 0))
        user_feedback.protect_our_sky_rating = int(request.form.get('protect_our_sky_rating', 0))
        user_feedback.pursue_your_dreams_rating = int(request.form.get('pursue_your_dreams_rating', 0))
        user_feedback.sit_tour_rating = int(request.form.get('sit_tour_rating', 0))

        # Commit the changes to the database
        db_session.commit()
        db_session.close()

        return redirect('/success') # Redirect to a success page or any other desired page

    return render_template('error.html', error_message='User not found in the database')


if __name__ == '__main__':
    base.metadata.create_all(engine)
    app.run(debug=True, host='172.26.184.243', port=3000)
