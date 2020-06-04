import requests
import json
from datetime import datetime, timedelta
from ics import Calendar, Event


# Login
# POST https://bootcampspot.com/api/instructor/v1/login
def get_token(email, password):
    try:
        response = requests.post(
            url="https://bootcampspot.com/api/instructor/v1/login",
            headers={
                "Content-Type": "text/plain; charset=utf-8",
            },
            data=json.dumps({
                "email": email,
                "password": password
            })
        )
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Me
# POST https://bootcampspot.com/api/instructor/v1/me
def get_user_detail(token):
    try:
        response = requests.post(
            url="https://bootcampspot.com/api/instructor/v1/me",
            headers={
                "Content-Type": "application/json",
                "authToken": token,
            },
        )
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Sessions
# POST https://bootcampspot.com/api/instructor/v1/sessions
def get_sessions(token, enrollment_id):
    try:
        response = requests.post(
            url="https://bootcampspot.com/api/instructor/v1/sessions",
            headers={
                "Content-Type": "application/json",
                "authToken": token,
            },
            data=json.dumps({
                "enrollmentId": int(enrollment_id)
            })
        )
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Assignments
# POST https://bootcampspot.com/api/instructor/v1/assignments
def get_assignments(token, enrollment_id):
    try:
        response = requests.post(
            url="https://bootcampspot.com/api/instructor/v1/assignments",
            headers={
                "Content-Type": "application/json",
                "authToken": token,
            },
            data=json.dumps({
                "enrollmentId": int(enrollment_id)
            })
        )
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def get_enrollments(token):
    # get session enrollments
    user_enrollments = []
    for enrollment in get_user_detail(token)['Enrollments']:
        if enrollment['active']:
            user_enrollments.append({'id': enrollment['id'],
                                'name': enrollment['course']['name'],
                                'startDate': datetime.strptime(enrollment['course']['startDate'],
                                                               '%Y-%m-%dT%H:%M:%SZ').strftime("%B %d, %Y")})
    return user_enrollments


def create_calendar(token, enrollment_id, options):
    file_list = []
    if options['academicCal'] or options['careerCal']:
        academic_calendar = Calendar()
        career_calendar = Calendar()
        for sess in get_sessions(token, enrollment_id)['calendarSessions']:
            e = Event()
            if (sess['context']['id'] == 1) and options['academicCal']:
                start_time = datetime.strptime(sess['session']['startTime'], '%Y-%m-%dT%H:%M:%SZ')
                end_time = datetime.strptime(sess['session']['endTime'], '%Y-%m-%dT%H:%M:%SZ')
                e.name = str(sess['session']['chapter']) + ': ' + sess['session']['name']
                e.transparent = True if options['academicIsTrans'] else False
                if options['officeHours']:
                    e.begin = start_time - timedelta(minutes=45)
                    e.end = end_time + timedelta(minutes=30)
                else:
                    e.begin = start_time
                    e.end = end_time
                academic_calendar.events.add(e)

            elif (sess['context']['id'] == 2) and options['careerCal']:
                e.name = sess['session']['name']
                e.begin = sess['session']['startTime']
                e.end = sess['session']['endTime']
                e.transparent = True if options['careerIsTrans'] else False
                career_calendar.events.add(e)

        if len(academic_calendar.events) > 0:
            academic_file_name = str(enrollment_id) + '-academic-calendar'
            academic_file_name = academic_file_name + '-oh.ics' if options['officeHours'] else academic_file_name + '.ics'
            file_list.append(academic_file_name)
            with open('files/' + academic_file_name, 'w') as f:
                f.writelines(academic_calendar)

        if len(career_calendar.events) > 0:
            career_file_name = str(enrollment_id) + '-career-calendar.ics'
            file_list.append(career_file_name)
            with open('files/' + career_file_name, 'w') as f:
                f.writelines(career_calendar)

    if options['assignmentCal']:
        assignment_calendar = Calendar()
        for assignment in get_assignments(token, enrollment_id)['calendarAssignments']:
            e = Event()
            if assignment['context']['id'] == 1:
                e.name = assignment['title']
                e.begin = datetime.strptime(assignment['effectiveDueDate'], '%Y-%m-%dT%H:%M:%SZ') - timedelta(days=1)
                e.end = datetime.strptime(assignment['effectiveDueDate'], '%Y-%m-%dT%H:%M:%SZ') - timedelta(days=1)
                e.make_all_day()
                e.transparent = True if options['assignmentsIsTrans'] else False
                assignment_calendar.events.add(e)
        assignment_file_name = str(enrollment_id) + '-assignment-calendar.ics'
        file_list.append(assignment_file_name)
        with open('files/' + assignment_file_name, 'w') as f:
            f.writelines(assignment_calendar)

    return file_list
