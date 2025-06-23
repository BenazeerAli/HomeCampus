from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import get_user_by_username, get_user_by_id
from flask import abort
import Grade7PageConfig 
from LearnMappings import Grade3Mapper as mapper
import traceback
from flask import send_file
from flask import send_from_directory, abort
import os
from auth2 import get_user_by_id  # import user loader from auth.py
from routes import auth_bp 
app = Flask(__name__)
app.secret_key = 'your-secret-key'
#changes pip 
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # redirect to login page if unauthorized
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# Register blueprint for auth routes
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    print("User authenticated:", current_user.is_authenticated)
    print("Username:", current_user.username if current_user.is_authenticated else "Anonymous")
    return render_template('HomePage.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Clears the session and logs out the user
    flash('You have been logged out.')
    return redirect(url_for('index'))  # Redirect to homepage or login page

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@app.route('/LoginPage', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('LoginPage.html')



@app.route('/Primary_Grade_3_Mathematics')
#@login_required
def primary3():
    grade_concept_rank = {}

    if current_user.is_authenticated:
        username = current_user.username
        #grade_concept_rank = GetConceptRank(3, username)

    return render_template('Primary_Grade_3.html')#, grade_concept_rank="ninja-rank")

@app.route('/Primary_Grade_4_Mathematics')
#@login_required
def primary4():
    grade_concept_rank = {}

    if current_user.is_authenticated:
        username = current_user.username
        #grade_concept_rank = GetConceptRank(4, username)

    return render_template('Primary_Grade_4.html')#, grade_concept_rank="ninja-rank")

@app.route('/Primary_Grade_5_Mathematics')
#@login_required
def primary5():
    grade_concept_rank = {}

    if current_user.is_authenticated:
        username = current_user.username
        #grade_concept_rank = GetConceptRank(5, username)

    return render_template('Primary_Grade_5.html')#, grade_concept_rank="ninja-rank")@app.route('/Primary_Grade_4_Mathematics')
@app.route('/Primary_Grade_6_Mathematics')
#@login_required ncomment this
def primary6():
    grade_concept_rank = {}

    if current_user.is_authenticated:
        username = current_user.username
        #grade_concept_rank = GetConceptRank(6, username) #figire this out w db

    return render_template('Primary_Grade_6.html')#, grade_concept_rank="ninja-rank") #uncomment this


@app.route('/Secondary-1-Grade-7-Mathematics')
def secondary1():
    page_name = request.args.get('pageName')
    ajax_bot_param = request.args.get('_escaped_fragment_')

    if ajax_bot_param:
        # Handle Googlebot requests
        try:
            html_page_name = Grade7PageConfig.PageMapping7A[ajax_bot_param]
            page_number = Grade7PageConfig.Grade7APages.index(html_page_name)
        except KeyError:
            try:
                html_page_name = Grade7PageConfig.PageMapping7B[ajax_bot_param]
                page_number = Grade7PageConfig.Grade7BPages.index(html_page_name)
            except KeyError:
                return f"Unknown AJAX fragment: {ajax_bot_param}", 404

        # Confirm the file exists (debugging tip)
        try:
            return render_template(html_page_name, page_number=page_number)
        except:
            return f"Template not found: {html_page_name}", 500

    else:
        # Normal user request
        params = {}
        if page_name:
            params['pageRedirectName'] = page_name

        try:
            return render_template('Grade-7/Grade-7.html', pageRedirectName='QuadraticEquations')
        except:
            return "Template not found: Grade-7/Grade-7.html", 500


@app.route('/Learn/Primary-Grade-3/<topic>/<subtopic>')
def primary3_handler1(topic, subtopic):
    try:
        fn, data = mapper.getMapping(subtopic, topic=topic,grade = 'Primary3')

        fn_clean = fn.strip("/")
        if fn_clean.startswith("Learn/"):
            fn_clean = fn_clean[len("Learn/"):]
        if ('Primary3' not in fn_clean):
            fn_clean = 'Primary3/'+fn_clean
        fn_clean=fn_clean.replace("Primary-Grade-3","Primary3")
        
        filename = "Notes/{}".format(fn_clean)

        print("Rendering:", filename)  # Debug print

        return render_template(filename, **data)
    except KeyError:
        print(fn)
        abort(404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        abort(500)


@app.route('/Learn/Primary-Grade-3/<subtopic>')
def primary3_handler2(subtopic):
    try:
        fn, data = mapper.getMapping(subtopic,grade='Primary3')
        filename = "Notes/Primary3" + fn
        if (".html" not in filename):
            filename = filename+".html"
        filename = filename.replace('/Primary-Grade-3',"")
        print("\n\nRENDERING: ",filename)
        return render_template(filename, **data)
    except KeyError:
        abort(404)

@app.route('/Learn/Primary-Grade-4/<topic>/<subtopic>')
def primary4_handler1(topic, subtopic):
    try:
        fn, data = mapper.getMapping(subtopic, topic=topic,grade='Primary4')

        # Clean the filename
        fn_clean = fn.strip("/")
        if "Learn/" in fn_clean:
            fn_clean = fn_clean[len("Learn/"):]
        fn_clean=fn_clean.replace("Primary-Grade-4","Primary4")
        filename = "Notes/{}".format(fn_clean)

        print("RENDERING:", filename)  # Debug print

        return render_template(filename, **data)
    except KeyError:
        abort(404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        abort(500)

@app.route('/Learn/Primary-Grade-6/Speed/Advanced-Word-Problems')
def primary6_handler3():
    try:
        return render_template("Notes/Primary6/Speed/Speed-Advanced-Word-Problems.html")
    except KeyError:
        abort(404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        abort(500)

@app.route('/Learn/Primary4/<topic>/<subtopic>')
def primary4_handler3(topic, subtopic):
    try:
        fn, data = mapper.getMapping(subtopic, topic=topic,grade='Primary4')

        # Clean the filename
        fn_clean = fn.strip("/")
        if fn_clean.startswith("Learn/"):
            fn_clean = fn_clean[len("Learn/"):]
        fn_clean=fn_clean.replace("Primary-Grade-4","Primary4")
        filename = "Notes/{}".format(fn_clean)

        print("RENDERING:", filename)  # Debug print

        return render_template(filename, **data)
    except KeyError:
        abort(404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        abort(500)

@app.route('/Learn/Primary-Grade-4/<subtopic>')
def primary4_handler2(subtopic):
    try:
        fn, data = mapper.getMapping(subtopic,grade='Primary4')
        filename = "Notes/Primary4" + fn
        return render_template(filename, **data)
    except KeyError:
        abort(404)

@app.route('/Learn/Primary-Grade-5/<topic>/<subtopic>')
def primary5_handler1(topic, subtopic):
    try:
        fn, data = mapper.getMapping(subtopic, topic=topic,grade='Primary5')

        # Clean the filename
        fn_clean = fn.strip("/")
        if fn_clean.startswith("Learn/"):
            fn_clean = fn_clean[len("Learn/"):]
        fn_clean=fn_clean.replace("Primary-Grade-5","Primary5")
        
        filename = "Notes/{}".format(fn_clean)
        if ('.html' not in filename):
            filename = filename + '.html'
        print("Rendering:", filename)  # Debug print

        return render_template(filename, **data)
    except KeyError:
        abort(404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        abort(500)



@app.route('/Learn/Primary-Grade-5/<subtopic>')
def primary5_handler2(subtopic):
    try:
        fn, data = mapper.getMapping(subtopic,grade='Primary5')
        filename = "Notes/Primary5" + fn
        return render_template(filename, **data)
    except KeyError:
        abort(404)

@app.route('/Learn/Primary-Grade-6/<topic>/<subtopic>')
def primary6_handler1(topic, subtopic):
    try:
        fn, data = mapper.getMapping(subtopic, topic=topic,grade = 'Primary6')

        # Clean the filename
        fn_clean = fn.strip("/")
        if fn_clean.startswith("Learn/"):
            fn_clean = fn_clean[len("Learn/"):]
        fn_clean=fn_clean.replace("Primary-Grade-6","Primary6")
        filename = "Notes/{}.html".format(fn_clean)

        print("Rendering:", filename)  # Debug print

        return render_template(filename, **data)
    except KeyError:
        abort(404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        abort(500)

@app.route('/Learn/Primary-Grade-6/<subtopic>')
def primary6_handler2(subtopic):
    try:
        fn, data = mapper.getMapping(subtopic,grade='Primary6')
        filename = "Notes/Primary6" + fn
        return render_template(filename, **data)
    except KeyError:
        abort(404)

@app.route('/AboutHomeCampus')
def about_home_campus():
    try:
        return render_template('AboutHomeCampus.html')
    except Exception as e:
        traceback.print_exc()
        abort(500)


@app.route('/What_is_Singapore_Math')
def singapore_math():
    try:
        return render_template('Singapore_Math.html')
    except Exception as e:
        traceback.print_exc()
        abort(500)

@app.route('/Math-Calculators') 
def math_calculators():
    try:
        return render_template('Notes/Math-Calculators.html')
    except Exception as e:
        traceback.print_exc()
        abort(500)
@app.route('/Learn/<calculator_name>')
def calculator(calculator_name):
    try:
        return render_template(f'{calculator_name}.html')
    
    except Exception as e:
        traceback.print_exc()
        abort(404)

from flask import render_template, abort
import traceback

# =======================
# TIME UNITS CONVERTER
# =======================

@app.route('/Learn/Time-Units-Converter')
def time_units_converter():
    try:
        return render_template('Time-Units-Converter/Time-Units-Converter.html')
    except Exception as e:
        traceback.print_exc()
        abort(404)

@app.route('/Learn/Hours-Unit-Converter')
def hours_unit_converter():
    try:
        return render_template('Time-Units-Converter/Hours-Unit-Converter.html')
    except Exception as e:
        traceback.print_exc()
        abort(404)

@app.route('/Learn/Hours-to-<unit>-Converter')
def hours_to_unit_converter(unit):
    try:
        filename = f'Time-Units-Converter/Hours-to-{unit}-Converter.html'
        return render_template(filename)
    except Exception as e:
        traceback.print_exc()
        abort(404)

# =======================
# LENGTH UNITS CONVERTER
# =======================

@app.route('/Learn/Length-Units-Converter')
def length_units_converter():
    try:
        return render_template('Length-Units-Converter/Length-Units-Converter.html')
    except Exception as e:
        traceback.print_exc()
        abort(404)

@app.route('/Learn/Meter-Unit-Converter')
def meter_converter():
    try:
        return render_template('Length-Units-Converter/Meter-Unit-Converter.html')
    except Exception as e:
        traceback.print_exc()
        abort(404)

@app.route('/Learn/Meter-to-<unit>-Converter')
def meter_to_unit_converter(unit):
    try:
        filename = f'Length-Units-Converter/Meter-to-{unit}-Converter.html'
        return render_template(filename)
    except Exception as e:
        traceback.print_exc()
        abort(404)
@app.route('/Learn/Meter-to-<unit>-Conversion')
def meter_to_unit_conversion(unit):
    try:
        filename = f'Length-Units-Converter/Meter-to-{unit}-Converter.html'
        return render_template(filename)
    except Exception as e:
        traceback.print_exc()
        abort(404)

@app.route('/Learn/Meter-to-<unit1>-and-<unit2>-Conversion')
def meter_to_two_units_conversion(unit1, unit2):
    try:
        filename = f'Length-Units-Converter/Meter-to-{unit1}-and-{unit2}-Conversion.html'
        return render_template(filename)
    except Exception as e:
        traceback.print_exc()
        abort(404)
#-----------------------------------------------------

@app.route('/Contact') 
def Contact():
    try:
        return render_template('Contact.html')
    except Exception as e:
        traceback.print_exc()
        abort(500)
#MATH WORKSHEETS---------------------------------------------
@app.route('/Math-Worksheets') 
def math_worksheets():
    try:
        return render_template('Notes/Math-Worksheets.html')
    except Exception as e:
        traceback.print_exc()
        abort(500)

@app.route('/Free-Math-Worksheets/<worksheet_name>')
def free_math_worksheet(worksheet_name):
    try:
        filename = f'Notes/Worksheets/{worksheet_name}.html'
        return render_template(filename)
    except Exception as e:
        traceback.print_exc()
        abort(404)

@app.route('/<worksheet_name>')
def free_math_worksheet_direct(worksheet_name):
    try:
        filename = f'Notes/Worksheets/{worksheet_name}.html'
        return render_template(filename)
    except Exception as e:
        traceback.print_exc()
        abort(404)


@app.route('/Download-Worksheets/<path:filename>')
def download_worksheet(filename):
    try:
        return send_from_directory('pdfworksheets', filename)
    except Exception as e:
        print(f"Error serving PDF: {e}")
        abort(404)

@app.route('/download-worksheets/<path:filename>')
def download_worksheet1(filename):
    try:
        return send_from_directory('pdfworksheets', filename)
    except Exception as e:
        print(f"Error serving PDF: {e}")
        abort(404)
#MATH WORKSHEETS END----------------------------
@app.route('/FAQs') 
def FAQs():
    try:
        return render_template('FAQs.html')
    except Exception as e:
        traceback.print_exc()
        abort(500)

@app.route('/Disclaimer') 
def Disclaimer():
    try:
        return render_template('Disclaimer.html')
    except Exception as e:
        traceback.print_exc()
        abort(500)

@app.route('/PrivacyPolicy') 
def PrivacyPolicy():
    try:
        return render_template('PrivacyPolicy.html')
    except Exception as e:
        traceback.print_exc()
        abort(500)



@app.route('/Home_Campus_User_Guide.pdf')
def serve_pdf():
    try:
        return send_file('Home_Campus_User_Guide.pdf', as_attachment=False)
    except Exception as e:
        traceback.print_exc()
        abort(404)

@app.route('/Grade_3_Math_Practice') 
def Grade_3_Math_Practice():
    try:
        return render_template('Practice_Primary_Grade_3.html')
    except Exception as e:
        traceback.print_exc()
        abort(500)


@app.route('/learn')
def learn_page():
    return render_template('LearnPage.html', section='content')

#----------------------------------LOG IN----------------------------------------------------------------
"""from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from google.cloud import datastore
import hashlib

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this!

# Initialize Google Cloud Datastore client
client = datastore.Client(project='homecampus-flask')

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# User class
class User(UserMixin):
    def __init__(self, user_id, username, password_hash):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash

# Password hashing (simple sha256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    key = client.key('User', int(user_id))
    user_entity = client.get(key)
    if not user_entity:
        return None
    return User(user_id=str(user_entity.key.id), username=user_entity['username'], password_hash=user_entity['password_hash'])

# Get user by username
def get_user_by_username(username):
    query = client.query(kind='User')
    query.add_filter('username', '=', username)
    results = list(query.fetch(limit=1))
    if not results:
        return None
    user_entity = results[0]
    return User(user_id=str(user_entity.key.id), username=user_entity['username'], password_hash=user_entity['password_hash'])

# Create new user
def create_user(username, password):
    if get_user_by_username(username):
        return None  # User exists
    key = client.key('User')
    user_entity = datastore.Entity(key=key)
    user_entity.update({
        'username': username,
        'password_hash': hash_password(password)
    })
    client.put(user_entity)
    return User(user_id=str(user_entity.key.id), username=username, password_hash=user_entity['password_hash'])

# Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password are required')
            return redirect(url_for('register'))

        if get_user_by_username(username):
            flash('User already exists')
            return redirect(url_for('register'))

        user = create_user(username, password)
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Error creating user')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user_by_username(username)
        if user and user.password_hash == hash_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! You are logged in.'
"""

if __name__ == '__main__':
    app.run(debug=True)
