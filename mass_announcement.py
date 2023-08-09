from credentials_flow import getcreds
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import build_http

# Add course list generating function here

def classroom_list_all_courses() -> list:
    try:
        creds = getcreds()
        service = build('classroom', 'v1', credentials=creds)
        api_response_json_course_list = (service
            .courses()
            .list(courseStates='ACTIVE')
            .execute()['courses'])
        courses = []
        for course in api_response_json_course_list:
            courses.append(course['id'])
        return courses
    except HttpError as error:
        print(f'An error occurred: {error}')
        return error # type: ignore

def compose_message() -> dict:
    print('Post an announcement to all active courses.')
    announcement_text = input('Text:\n')
    message = {
            'text': announcement_text,
            'state': 'PUBLISHED',
            'creatorUserId': 'gam@example.com'
            }
    return message

# course_list = [543522084535]
# uncomment this line to announce to all courses
course_list = classroom_list_all_courses()

def class_announcement(message):
    http = build_http()
    creds = getcreds()
    service = build('classroom', 'v1', credentials=creds)
    batch = service.new_batch_http_request(callback=callback)
    for course in course_list:
        request = service.courses().announcements().create(body=message,courseId=str(course))
        batch.add(request, request_id=str(course))
    batch.execute(http=http)
        
def callback(request_id, exception):
    if exception is None:
        print(f'Announcement added to course with id {request_id}.')
    elif exception.resp.status == 409:
        course_code = request_id
        print(f'Course {course_code} already exists.')
    elif exception.resp.status == 403:
        print('Request forbidden.')
    else:
        print(f'Error code {exception.resp.status}. {exception._get_reason()}.')

message = compose_message()
class_announcement(message)

# print(compose_message())
