from credentials_flow import getcreds
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
import random

creds = getcreds()
service = build('admin', 'directory_v1', credentials=creds)

def load_accounts() -> list:
    with open ('sourcedata/accounts_for_deletion_3.csv', 'r') as accounts_file:
        accounts_list: list = (accounts_file
                            .read()
                            .strip()
                            .split("\n"))
    return accounts_list
        
def delete_user(googid) -> bool:
    try:
        (service
            .users()
            .delete(userKey=f'{googid}@example.com')
            .execute())
        return True
    except HttpError as error:
        if error.resp.status == 404:
            print(f'User {googid} not found')
        else:
            print(f'HTTP error: {error}')
        return False

def last_login_lookup(googid) -> str:
    time.sleep(0.1)
    try:
        response = (service
            .users()
            .get(userKey=f'{googid}@example.com'
                 ,projection='basic')
            .execute()).get('lastLoginTime')
        return response
    except HttpError as error:
        if error.resp.status == 404:
            response = (f'User not found')
        else:
            response = (f'HTTP error: {error}')
        return response

def remove_account(accounts_list):
    accounts_list.pop(0)
    print(f'There are {len(accounts_list)} accounts in the list')
    with open ('sourcedata/accounts_for_deletion_3.csv', 'w') as accounts_file_new:
        for account in accounts_list:
            accounts_file_new.write(f'{account}\n')

account_counter:int = 0
missing_account_counter:int = 0
deletion_counter:int = 0
successful_deletion_counter:int = 0
failed_deletion_counter:int = 0
error_counter:int = 0
old_enrolments_count:int = len(load_accounts())
print(f'start with {old_enrolments_count} accounts')

accounts_list:list = load_accounts()

for person_code in accounts_list:
    wait_time:int = random.randint(1, 4)
    account_counter = account_counter + 1
    last_login = last_login_lookup(person_code)
    time.sleep(wait_time)
    if last_login == '1970-01-01T00:00:00.000Z':
        print(f'User {person_code} has never logged in')
        deletion_outcome = delete_user(person_code)
        deletion_counter = deletion_counter + 1
        if deletion_outcome == True:
            print(f'User {person_code} deleted')
            successful_deletion_counter = successful_deletion_counter + 1
        else:
            print(f'User {person_code} not deleted')
            failed_deletion_counter = failed_deletion_counter + 1
    elif last_login == 'User not found':
        print(f'User {person_code} not found')
        missing_account_counter = missing_account_counter + 1
    else:
        error_counter = error_counter + 1
    remove_account(accounts_list)


with open ('sourcedata/deleted_account_results.txt', 'w') as final_count:
    results:str = (f'{old_enrolments_count} learners have not enrolled on any courses in last two years\n'
                   + f'of these, {missing_account_counter} have no google account\n'
                   + f'{deletion_counter} have never logged in and flagged for deletion\n'
                   + f'{successful_deletion_counter} accounts were successfully deleted\n'
                   + f'for {failed_deletion_counter} accounts the deletion failed for some reason\n'
                   + f'and there were {error_counter} errors\n')
    final_count.write(results)
