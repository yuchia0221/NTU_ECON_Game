import gspread
from collections import namedtuple
from oauth2client.service_account import ServiceAccountCredentials

country_info = namedtuple("country_info",
                          "id name wonders gold population weapon air food_speed wood_speed steel_speed stone_speed food wood steel stone")

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("google.json", scope)
client = gspread.authorize(creds)
sheet = client.open("國家資訊表").sheet1
data = sheet.get_all_records()
country_list = [country_info(*i.values()) for i in data]
