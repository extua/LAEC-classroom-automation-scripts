import time
from credentials_flow import getcreds
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import build_http

# Initialise some variables for use below
creds = getcreds()
service = build('classroom', 'v1', credentials=creds)
courses = service.courses()

def classroom_list_course_ids() -> list[int]:
    try:
        course_id_list = []
        request = (courses
                    .list(
                        fields = 'courses(id),nextPageToken',
                        courseStates = ['PROVISIONED'])
                )
        courses_in_total: int = 0
        while request is not None:
            run_request = request.execute()
            if 'courses' in run_request:
                id_list: list = run_request['courses']
                courses_in_batch: int = len(id_list)
                courses_in_total: int = courses_in_total + courses_in_batch
                print(f'Requested {courses_in_batch} course ids, '
                    f'{courses_in_total} so far')
                for course in id_list:
                    course_id_list.append(course.get('id'))
                request = courses.list_next(request, run_request)
            else:
                break
            time.sleep(0.4)
        assert course_id_list is not None
        return course_id_list
    except HttpError as error:
        print(f'An error occurred: {error}')
        return error # type: ignore
    
id_list = classroom_list_course_ids()
listlen: int = len(id_list)
print(listlen)
