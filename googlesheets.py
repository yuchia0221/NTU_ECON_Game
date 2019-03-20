import gspread
# import time
# import random
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("google.json", scope)
client = gspread.authorize(creds)
sheet = client.open("股價").sheet1
data = sheet.get_all_records()

# print(data)
# sheet.clear()
# sheet.append_row(list)
# sheet.insert_row([items...], index=1)
# help(sheet)
