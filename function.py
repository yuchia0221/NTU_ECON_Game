import gspread
from collections import namedtuple
from oauth2client.service_account import ServiceAccountCredentials
from Country import (Atlantis, Asgard, Olympus, Wakanda, ShangriLa,
                     Varanasi, Maya, Tartarus, Teotihuacan, EasterIsland)


def read_file():
    country_info = namedtuple("country_info",
                              "id name wonders gold population weapon air food_speed wood_speed steel_speed stone_speed food wood steel stone")

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("google.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("國家資訊表").sheet1
    data = sheet.get_all_records()
    raw_data = [country_info(*i.values()) for i in data]

    return raw_data


def createCountry():
    name = {"亞特蘭提斯": Atlantis, "阿斯嘉": Asgard, "奧林帕斯": Olympus, "瓦干達": Wakanda,
            "香格里拉": ShangriLa, "瓦拉納西": Varanasi, "瑪雅": Maya, "塔爾塔洛斯": Tartarus,
            "特奧蒂瓦坎": Teotihuacan, "復活節島": EasterIsland}

    data = read_file()
    return_list = [name[i.name](*i) for i in data]

    return return_list
