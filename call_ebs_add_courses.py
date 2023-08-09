import urllib.request
import json
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import build_http
from credentials_flow import getcreds


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses']

## Call API and return api_response_json object
url = 'example.com'
hds = {'accept': 'application/json'}

req = urllib.request.Request(url, headers=hds)
with urllib.request.urlopen(req) as response:
   api_response = response.read().decode('UTF-8')
api_response_json = json.loads(api_response)

# ## Bypass API call with local file, also returns api_response_json object
# with open('test_response.json', 'r') as opened_json_file:
#      api_response_json = json.load(opened_json_file)

## Move down one level through the json, this returns a list of course objects
api_response_json_course_list = api_response_json['Courses']

def classroom_add_courses():
    http = build_http()
    creds = getcreds()
    # try:
    service = build('classroom', 'v1', credentials=creds)
    batch = service.new_batch_http_request(callback=callback)
    # list index here determines how many courses from the list to add
    for course in api_response_json_course_list[0:1]:
        course_code = 'd:' + course['course_code'],
        course_codestr = ''.join(course_code)
        courseinfo = {
            'id': course_codestr,
            'name': course['course_title'],
            'description': course['description'],
            'section': course['offorg'],
            'ownerId': 'me'
        }
        request = service.courses().create(body=courseinfo)
        batch.add(request, request_id=course_codestr)
    batch.execute(http=http)

def callback(request_id, response, exception):
    if exception is None:
        course_id = response.get('id')
        print(f'Course {request_id[2:]} created with id {course_id}.')
        # this is the point in the code where we have a course and an id
        # and can probably go on to call some other function? add rooms, add learners?
        # created_course = {
        #     'alias': course_code,
        #     'id': course_id
        # }
        # print(created_course)
    elif exception.resp.status == 409:
        course_code = request_id[2:]
        print(f'Course {course_code} already exists.')
    elif exception.resp.status == 403:
        print('Request forbidden.')
    else:
        print(f'Error code {exception.resp.status}. {exception._get_reason()}.')

if __name__ == '__main__':
    classroom_add_courses()
