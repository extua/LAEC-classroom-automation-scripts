# LAEC classroom automation scripts

This is a collection of python scripts used for automating common Google Classroom admin tasks, using the [Google Workspace API](https://developers.google.com/classroom/reference/rest).

## Scope

These scripts were written to handle courses at [Leicester Adult Education](https://leicesteradulted.ac.uk/), they're not designed to be usable for other use cases. Email addresses and API calls to the Leicester Adult Education database have been replaced with `example.com`.

Consider this a starting point and inspiration for your own code. For a more comprehensive solution, see [GAM](https://github.com/GAM-team/GAM) and [GAMADV-XTD3](https://github.com/taers232c/GAMADV-XTD3/)

## Usage

Follow the steps [here](https://developers.google.com/admin-sdk/directory/v1/quickstart/python)	and make sure you have the client libraries in your python environment.

All API calls need to be authenticated with your credentials, and so in each script the first API call needs to be prefixed with credential validation. For the sake of simplicity, the credential handling has been put in its own file `credentials_flow.py` which provides the `getcreds()` function.

The first time you run the credentials flow you'll have to go through an authentication process with google, which will leave you with the `credentials.json` and `token'json` files in the project directory defined in the credentials flow.

### Bulk add courses

Take a csv containing course information for many courses, and create these on Google Classroom. You can also do this using GAM, but the script gives some more flexibility with what you add to the course object.

### Call ebs, add courses

Same as above but this time getting course information by making a call to an API provided by [ebs](https://www.tribalgroup.com/solutions/student-information-systems/ebs).[^tribal] With this, courses on ebs could be automatically added to Google Classroom.

[^tribal]: A student information system used for administration of student records and course information.

### Bulk delete users

Take a csv containing lots of old user ids of people who haven't taken a course in several years. Check whether their account is unused,[^last_login] and if not, delete the account. With a huge number of accounts you quickly encounter rate limiting and have to slow down the script, which makes this one a pain to run.

[^last_login]: An account is unused if the last login date equals the Unix epoch (1970-01-01 00:00:00), and you can change that to get accounts not logged into since a set date.

### Get course ids


