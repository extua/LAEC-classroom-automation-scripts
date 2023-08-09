# LAEC classroom automation scripts

This is a collection of python scripts used for automating common Google Classroom admin tasks, using the [Google Workspace API](https://developers.google.com/classroom/reference/rest).

## Scope

These scripts were written to handle courses at Leicester Adult Education, they're not designed to be usable for other use cases. Email addresses and API calls to the Leicester Adult Education database have been replaced with `example.com`.

Consider this a starting point and inspiration for your own code. For a more comprehensive solution, see [GAM](https://github.com/GAM-team/GAM) and [GAMADV-XTD3](https://github.com/taers232c/GAMADV-XTD3/)

## Usage

Follow the steps [here](https://developers.google.com/admin-sdk/directory/v1/quickstart/python)	and make sure you have the client libraries in your python environment.

All API calls need to be authenticated with your credentials, and so in each script the first API call needs to be prefixed with credential validation. For the sake of simplicity, the credential handling has been put in its own file `credentials_flow.py` which provides the `getcreds()` function.

The first time you run the credentials flow you'll have to go through an authentication process with google, which will leave you with the `credentials.json` and `token'json` files in the project directory defined in the credentials flow.
