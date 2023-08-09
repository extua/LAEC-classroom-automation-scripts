import random
import time
from os import path
from credentials_flow import getcreds
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import build_http

# Initialise some variables for use below
creds = getcreds()
service = build('classroom', 'v1', credentials=creds)
courses = service.courses()
rate_limited_list = []

### overwrite csv with headers, ready for appending info
with open('google_class_ids_api.csv', 'w') as id_file:
            id_file.write('course_id,ebs_code\n')
            print('Opened csv file afresh')

def classroom_list_course_ids():
    try:
        course_id_list: list = []
        request = courses.list(
                    fields = 'courses(id),nextPageToken',
                    courseStates = 'ACTIVE')
        courses_in_total: int = 0
        while request is not None:
            run_request = request.execute()
            courses_in_batch = len(run_request['courses'])
            courses_in_total = courses_in_batch + courses_in_total
            print(f'Requested {courses_in_batch} course ids, '
                  f'{courses_in_total} so far')
            for course in run_request['courses']:
                course_id_list.append(course.get('id'))
            request = courses.list_next(request, run_request)
            wait_time = random.randint(0, 3)
            time.sleep(wait_time)
        return course_id_list
    
    except HttpError as error:
        print(f'An error occurred: {error}')

def get_aliases(big_course_list):

    ### Uncomment either of the three lines if you want to get
    ### ids from google or from existing file

    course_id_list_length: int = len(big_course_list)
    print(f'{course_id_list_length} course ids received.')

    # with open('course_ids_list.csv', 'r') as course_list_file:
    #     course_list_string = course_list_file.read()
    #     big_course_list: list = course_list_string.split(',')
    
    course_id_list_length = len(big_course_list)

    increase_step: int = ((course_id_list_length // 2)
                          - (course_id_list_length // 7))
    print(f'Fetching batches of aliases in increments of {increase_step}')
    batch_start: int = 0
    batch_end = increase_step
    course_id_list_length = course_id_list_length + 1
    while batch_end <= course_id_list_length and batch_start != batch_end:
        http = build_http()
        batch = service.new_batch_http_request(callback=callback_fun)
        print(f'compose batch from {batch_start} to {batch_end}')
        request_counter: int = 0
        for course_id in big_course_list[batch_start:batch_end]:
            request = (courses
                    .aliases()
                    .list(courseId = course_id))
            batch.add(request, request_id=course_id)
            request_counter = request_counter + 1
        if (batch_end + increase_step) > course_id_list_length:
            batch_start = batch_end
            batch_end = course_id_list_length
        else:
            batch_start = batch_end + 1
            batch_end = batch_end + increase_step
        batch.execute(http=http)
        print(f'batch sent with {request_counter} requests')
        wait_time = ((request_counter // random.randint(16, 32))
                    + random.randint(1, 5))
        time.sleep(wait_time)

def callback_fun(request_id, response, exception):
    ### remember to change this filepath when deploying
    with open('google_class_ids_api.csv', 'a') as id_file:
        if exception is None:
                if 'aliases' not in response:
                    id_file.write(f'{request_id},\n')
                else:
                    for aliases in response.get('aliases', {}):
                        alias = aliases.get('alias', {})
                        id_file.write(f'{request_id},{alias[2:]}\n')
        elif exception.resp.status == 429:
            # rate_limited_list.append(request_id)
            print('Error 429. Hit API rate limit.')
        else:
            print('Error {0}. {1}.'.format(
                 exception.resp.status,exception._get_reason()))

big_course_list = classroom_list_course_ids()
get_aliases(big_course_list)
print('data written to file')


## rate limiting stuff
# while len(rate_limited_list) > 0:
#     ids_rate_limited = len(rate_limited_list)
#     print(f'{ids_rate_limited} requests rate limited')
#     print('run through batches again')
#     get_aliases(ids_rate_limited)
