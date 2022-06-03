# import httplib2
# import apiclient.discovery
# from oauth2client.service_account import ServiceAccountCredentials as SAC
#
# CREDENTIALS_FILE = 'pyhoroscope-9bfba590b29e.json'
#
# credentials = SAC.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
#                                                             'https://www.googleapis.com/auth/drive'])
#
# httpAuth = credentials.authorize(httplib2.Http())
# service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
#
# spreadsheet = service.spreadsheets().create(body={
#     'properties': {'title': 'Users_sheet', 'locale': 'ru_RU'},
#     'sheets': [{'properties': {'sheetType': 'GRID',
#                                'sheetId': 0,
#                                'title': 'Users',
#                                'gridProperties': {'rowCount': 15, 'columnCount': 15}}}]
# }).execute()
# spreadsheetId = spreadsheet['spreadsheetId']
# print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
#
# driveService = apiclient.discovery.build('drive', 'v3', http=httpAuth)
# access = driveService.permissions().create(
#     fileId=spreadsheetId,
#     body={'type': 'user', 'role': 'writer', 'emailAddress': 'dima.kuvirok1and6@gmail.com'},
#     fields='id'
# ).execute()
#
#
# def hor_sheet(message, bot, chat_id):
#     user_id = message.from_user.id
#     user_name = message.from_user.first_name
#
#     results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
#         "valueInputOption": "USER_ENTERED",
#         "data": [
#             {"range": "Users!A1:D5",
#              "majorDimension": "ROWS",
#              "values": [
#                  [user_name],
#                  [user_id]
#              ]}
#         ]
#     }).execute()