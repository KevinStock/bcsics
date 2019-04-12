import requests
import json

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