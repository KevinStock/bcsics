from flask import Flask, render_template, redirect, url_for, session, request, send_file
import json
import requests
from apiFunctions import get_token, get_user_detail, get_sessions, get_assignments
from datetime import datetime, timedelta
from ics import Calendar, Event
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'fMvMODwbtoDHxQGKUTDU'

# home page
@app.route('/')
def welcome():
  return render_template('index.html')

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
  # if form is posted
  if request.method == 'POST':
    user_detail = get_token(request.form['Email'],
                            request.form['Password'])
    session['token'] = user_detail['authenticationInfo']['authToken']
    session['user_id'] = user_detail['authenticationInfo']['userId']
    return redirect(url_for('calendar'))

  # get request
  else:
    # check if we already have a token
    if 'token' in session:
      return redirect(url_for('calendar'))
    return render_template('login.html')

# calendar page
@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
  # get request
  if request.method == 'GET':
    # check if user is logged in
    if session.get('token') is not None:
      # get session enrollments
      user_detail = get_user_detail(session['token'])
      enrollments = []
      for enrollment in user_detail['enrollments']:
        if enrollment['active'] == True:
          enrollments.append({'id': enrollment['id'],
                              'name': enrollment['course']['name'],
                              'startDate': datetime.strptime(enrollment['course']['startDate'], '%Y-%m-%dT%H:%M:%SZ').strftime("%B %d, %Y")})
      return render_template('calendar.html', enrollments=enrollments)
    else:
      return redirect(url_for('login'))
  else:
    academicCheck = False
    careerCheck = False
    officeHoursCheck = False
    assignmentsCheck = False
    
    enrollmentID = request.form['Course']
    if request.form.get('academicCheck'):
      academicCheck = True
    if request.form.get('careerCheck'):
      careerCheck = True
    if request.form.get('officeHoursCheck'):
      officeHoursCheck = True
    if request.form.get('assignmentsCheck'):
      assignmentsCheck = True
    
    sessions = get_sessions(session['token'], enrollmentID)
    academicCalendar = Calendar()
    academicSessions = []
    careerCalendar = Calendar()
    careerSessions = []
    assignmentCalendar = Calendar()
    assignmentList = []

    if academicCheck or careerCheck:
      for sess in get_sessions(session['token'], enrollmentID)['calendarSessions']:
          e = Event()
          if ((sess['context']['id'] == 1) and academicCheck):
            start_time = datetime.strptime(sess['session']['startTime'], '%Y-%m-%dT%H:%M:%SZ')
            end_time = datetime.strptime(sess['session']['endTime'], '%Y-%m-%dT%H:%M:%SZ')
            e.name = str(sess['session']['chapter']) + ': ' + sess['session']['name']
            if officeHoursCheck:
              e.begin = start_time - timedelta(minutes = 45)
              e.end = end_time + timedelta(minutes = 30)
            else:
              e.begin = start_time
              e.end = end_time
            academicCalendar.events.add(e)
            academicSessions.append({'chapter': sess['session']['chapter'],
                                     'session_name': sess['session']['name'],
                                     'start_time': sess['session']['startTime'],
                                     'end_time': sess['session']['endTime']})
          elif ((sess['context']['id'] == 2) and careerCheck):
            e.name = sess['session']['name']
            e.begin = sess['session']['startTime']
            e.end = sess['session']['endTime']
            careerCalendar.events.add(e)
            careerSessions.append({'session_name': sess['session']['name'],
                                   'start_time': sess['session']['startTime'],
                                   'end_time': sess['session']['endTime']})

    if assignmentsCheck:
      for assignment in get_assignments(session['token'], enrollmentID)['calendarAssignments']:
        e = Event()
        if assignment['context']['id'] == 1:
          e.name = assignment['title']
          e.begin = datetime.strptime(assignment['effectiveDueDate'], '%Y-%m-%dT%H:%M:%SZ')
          e.end = datetime.strptime(assignment['effectiveDueDate'], '%Y-%m-%dT%H:%M:%SZ')
          e.make_all_day()
          assignmentCalendar.events.add(e)
          assignmentList.append({'title': assignment['title'],
                                 'due_date': assignment['effectiveDueDate']})
    
    fileList = []
    if len(academicCalendar.events) > 0:
      academicFileName = str(session['user_id']) + '-' + str(enrollmentID) + '-academic-calendar.ics'
      fileList.append(academicFileName)
      with open('files/' + academicFileName, 'w') as f:
        f.writelines(academicCalendar)
    if len(careerCalendar.events) > 0:
      careerFileName = str(session['user_id']) + '-' + str(enrollmentID) + '-career-calendar.ics'
      fileList.append(careerFileName)
      with open('files/' + careerFileName, 'w') as f:
        f.writelines(careerCalendar)
    if len(assignmentCalendar.events) > 0:
      assignmentFileName = str(session['user_id']) + '-' + str(enrollmentID) + '-assignment-calendar.ics'
      fileList.append(assignmentFileName)
      with open('files/' + assignmentFileName, 'w') as f:
        f.writelines(assignmentCalendar)

    
    return render_template('calendar.html', fileList=fileList)

@app.route('/files/<filename>')
def files(filename):
  file = os.path.join(app.root_path, 'files', filename)
  return send_file(file, as_attachment=True)

@app.route('/logout')
def logout():
  session.pop('token', None)
  session.pop('user_id', None)
  return redirect(url_for('welcome'))

if __name__ == '__name__':
  app.run(debug=True, port=3000)
