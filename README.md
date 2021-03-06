# BootcampSpot ICS Generator

## Introduction
**3rd Place Winning Submission** for Trilogy BCS API Hack-a-thon using the new Bootcamp Spot API.

This application is designed to allow a user to login with their BCS credentials, select a course cohort which they are active in, and generate an ICS file for all Academic, Career, and Assignment calendars. Optionally, a user can enable office hours on the Academic Calendar.

## Getting Started
### Run local
1. Install dependencies with `pip install -r requirements.txt`
2. Set SECRET_KEY
`echo "SECRET_KEY='SuperSecretKey'" >> .env`
3. Set Sentry DSN
`echo "SENTRY_DSN='YourSentryDSN" >> .env`
3. Execute `FLASK_APP=main.py flask run`
4. Open browser to http://127.0.0.1:5000/
5. Login with BootcampSpot credentials (user must have an active enrollment to create a calendar file)

## Dependencies
Python3, Flask, requests, ics, python-dotenv, sentry-sdk[flask]

## Built With

[ics](https://github.com/C4ptainCrunch/ics.py) - Python module to create ics files.

## Notes
This application still needs quite a bit of error handling. While authentication errors are being handled on login, no checks are made to ensure that the API returns appropriate data at this time.

Assignment due dates are being manually adjusted due to the time returned by the API is GMT and there is no decent way to identify a cohort's time zone for appropriate conversion.

## Future Enhancements
* Add ability to set alarms
* Add Location (relies on BCS data to be clean)
