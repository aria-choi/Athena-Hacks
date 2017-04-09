
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
from datetime import timedelta
from tzlocal import get_localzone

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar Bullet Journal'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the events in the next
    X days on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    """x = int(input('How many days would you like to view?'))

    if x == 1:
       print('You selected', x, 'day')
    else:
       print('You selected', x, 'days')"""
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    DAY = timedelta(1)
    endDay = now + str(DAY)

    """now = datetime.datetime.utcnow().isoformat()
    now = str(now)
    s = datetime.datetime.strptime(now, '%Y-%m-%dT%H:%M:%S.%f')
    s = s.strftime('%m/%d')
    DAY = timedelta(1)
    DAY = str(DAY)
    e = datetime.datetime.strptime(DAY, '1 day, %H:%M:%S')
    e = e.strftime('%m/%d')
    endDay = s + e

    if x == 1:
       print('Getting your events for the next', x, 'day')
    else:
       print('Getting your events for the next', x, 'days')"""

    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, timeMax='2017-4-20T00:00:00Z', singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()