import requests
import json
from datetime import datetime, timedelta


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
def get_sessions(token, enrollmentId):
  try:
      response = requests.post(
          url="https://bootcampspot.com/api/instructor/v1/sessions",
          headers={
              "Content-Type": "application/json",
              "authToken": token,
          },
          data=json.dumps({
              "enrollmentId": int(enrollmentId)
          })
      )
      return response.json()
  except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Assignments
# POST https://bootcampspot.com/api/instructor/v1/assignments
def get_assignments(token, enrollmentId):
  try:
      response = requests.post(
          url="https://bootcampspot.com/api/instructor/v1/assignments",
          headers={
              "Content-Type": "application/json",
              "authToken": token,
          },
          data=json.dumps({
              "enrollmentId": int(enrollmentId)
          })
      )
      return response.json()
  except requests.exceptions.RequestException:
      print('HTTP Request failed')


def get_enrollments(token):
    # get session enrollments
    user_detail = get_user_detail(token)
    enrollments = []
    for enrollment in get_user_detail(token)['enrollments']:
        if enrollment['active']:
            enrollments.append({ 'id': enrollment['id'],
                                 'name': enrollment['course']['name'],
                                 'startDate': datetime.strptime(enrollment['course']['startDate'],
                                                                '%Y-%m-%dT%H:%M:%SZ').strftime("%B %d, %Y") })
    return enrollments

def create_calenar(token, enrollmentID, calType):

    return