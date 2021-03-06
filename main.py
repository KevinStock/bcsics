from flask import Flask, render_template, redirect, url_for, session, request, send_file
import apiFunctions
from datetime import datetime, timedelta
from ics import Calendar, Event
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from dotenv import load_dotenv
import os

load_dotenv()

sentry_sdk.init(
dsn=os.getenv("SENTRY_DSN"),
integrations=[FlaskIntegration()],
traces_sample_rate=1.0
)

app = Flask(__name__)
app.config.from_pyfile('config.py')


# home page
@app.route('/')
def welcome():
    return render_template('index.html')

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # GET request
    if request.method == 'GET':
        # check if we already have a token
        if is_logged_in():
            return redirect(url_for('calendar'))
        return render_template('login.html')

    # POST request
    else:
        user_detail = apiFunctions.get_token(request.form['Email'],
                                             request.form['Password'])
        if user_detail['errorCode'] is None:
            session['token'] = user_detail['authenticationInfo']['authToken']
            session['user_id'] = user_detail['authenticationInfo']['userId']
            return redirect(url_for('calendar'))
        else:
            return render_template('login.html',
                                   error='Authentication Issue. Please check your credentials and try again.',
                                   email=request.form['Email'])


# calendar page
@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    # GET request
    if request.method == 'GET':
        # check if user is logged in
        if is_logged_in():
            enrollments = apiFunctions.get_enrollments(session['token'])
            if not enrollments:
                return render_template('calendar.html',
                                        enrollments=enrollments,
                                        error="You do not belong to any courses.")
            else:
                return render_template('calendar.html',
                                        enrollments=enrollments)
        else:
            return redirect(url_for('login'))

    # POST request
    else:
        enrollment_id = request.form['Course']
        options = {}
        options['academicCal'] = True if (request.form.get('academicCheck')) else False
        options['officeHours'] = True if (request.form.get('officeHoursCheck')) else False
        options['academicIsTrans'] = True if (int(request.form.get('academicIsTrans'))) else False
        options['careerCal'] = True if (request.form.get('careerCheck')) else False
        options['careerIsTrans'] = True if (int(request.form.get('careerIsTrans'))) else False
        options['assignmentCal'] = True if (request.form.get('assignmentsCheck')) else False
        options['assignmentsIsTrans'] = True if (int(request.form.get('assignmentsIsTrans'))) else False
    
    calendar_files = apiFunctions.create_calendar(session['token'], enrollment_id, options)
    return render_template('calendar.html', fileList=calendar_files)


@app.route('/files/<filename>')
def files(filename):
    file = os.path.join(app.root_path, 'files', filename)
    return send_file(file, as_attachment=True)


@app.route('/logout')
def logout():
    session.pop('token', None)
    session.pop('user_id', None)
    return redirect(url_for('welcome'))


def is_logged_in():
    if 'token' in session:
        return True
    return False

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0


if __name__ == '__name__':
    app.run(port=3000)
