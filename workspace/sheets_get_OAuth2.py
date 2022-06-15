from googleapiclient.discovery import build
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

# Email of the Service Account

# Path to the Service Account's Private Key file
SERVICE_ACCOUNT_KEY_FILE_LOCATION_JSON = '/opt/zhangtao-test-4639d72a1de5.json'


credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_KEY_FILE_LOCATION_JSON,
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])

credentials = credentials.create_delegated("zhangtao@yunion-hk.com")

service = discovery.build('sheets', 'v4', credentials=credentials)

spreadsheet_id = '1YuDd-o8xuix8iqJImKwR_bc2rFeZiBOn19hFCjcUk68'  # TODO: Update placeholder value.

# The A1 notation of the values to retrieve.
range_ = 'Sheet1'  # TODO: Update placeholder value.

request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)

response = request.execute()

    
print(response)


