import csv
from credentials_flow import getcreds
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import build_http

def classroom_add_courses():
    creds = getcreds()
    service = build('classroom', 'v1', credentials=creds)
    with open('sourcedata/new_classrooms.csv', 'r') as classrooms_csv:
            class_row = csv.reader(classrooms_csv)
            for course in class_row:
                try:
                    alias1 = 'd:' + course[0]
                    course_codestr = ''.join(alias1)
                    owner = course[3]
                    ownermail = ''
                    courseinfo = {
                        'id': course_codestr,
                        'name': course[1],
                        'room': course[2],
                        'ownerId': ownermail,
                        'descriptionHeading': course[4],
                        'section': course[5]
                    }
                    request = service.courses().create(body=courseinfo).execute()
                    print(f'adding course {alias1}, sleeping 2s')
                    time.sleep(0.6)
                    print(request)
                except HttpError as error:
                    print(f"An error occurred: {error}")

classroom_add_courses()
