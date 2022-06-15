from __future__ import print_function
import os.path
#from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
#from google.auth.transport.requests import Request
#from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '1YuDd-o8xuix8iqJImKwR_bc2rFeZiBOn19hFCjcUk68'
SAMPLE_RANGE_NAME = 'Sheet1'

# Path to the Service Account's Private Key file
SERVICE_ACCOUNT_KEY_FILE_LOCATION_JSON = '/opt/zhangtao-test-4639d72a1de5.json'

USER_EMAIL = 'zhangtao@yunion-hk.com'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_KEY_FILE_LOCATION_JSON,
        scopes=SCOPES)

    credentials = credentials.create_delegated(USER_EMAIL)

    service = discovery.build('sheets', 'v4', credentials=credentials)

    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME
    ).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        ret = ''
        for row in values:
            new_row = []
            for _ in row:
                if ',' in _:
                    try:
                        _ = str(_).replace(',', '')
                    except Exception:
                        pass
                else:
                    pass
                new_row.append(_)
            ret += ','.join(new_row) + os.linesep
        print(ret)
        with open('sheet1.csv', mode='w') as f_csv:
            f_csv.write(ret)


if __name__ == '__main__':
    main()
