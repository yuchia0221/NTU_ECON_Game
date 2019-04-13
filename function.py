import csv
import gspread
from collections import namedtuple
from oauth2client.service_account import ServiceAccountCredentials
from Country import (Atlantis, Asgard, Olympus, Wakanda, ShangriLa,
                     Varanasi, Maya, Tartarus, Teotihuacan, EasterIsland)


def read_file(file_name):
    """讀取位於Google雲端的試算表，用list回傳資料"""

    country_info = namedtuple("country_info",
                              "id name wonders gold population weapon air food_speed wood_speed steel_speed stone_speed food wood steel stone")
    action = namedtuple("action", "time name Pfood Pwood Psteel Ptone useCard soldCard Pwonders war solider resource speed")

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(file_name).sheet1
    data = sheet.get_all_records()

    if file_name == "國家資訊表":
        return [country_info(*i.values()) for i in data]
    else:
        return [action(*i.values()) for i in data]


def createCountry(file_name):
    """透過read_file函數建立Class，回傳儲存各國Class的dictionary"""

    class_list = {"亞特蘭提斯": Atlantis, "阿斯嘉": Asgard, "奧林帕斯": Olympus, "瓦干達": Wakanda,
                  "香格里拉": ShangriLa, "瓦拉納西": Varanasi, "瑪雅": Maya, "塔爾塔洛斯": Tartarus,
                  "特奧蒂瓦坎": Teotihuacan, "復活節島": EasterIsland}

    return {i.name: class_list[i.name](*i) for i in read_file(file_name)}


def card(countryDict, password, name):
    """發動卡片效果"""

    """.................卡片函數區............................."""
    def f():
        print("test")
    """.................卡片函數區............................."""

    password = password.upper()

    with open("卡片.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        useCard, soldCard = dict(), dict()
        for i in csv_reader:
            useCard[i[1]] = (i[4], i[3])
            soldCard[i[2]] = (i[4], i[5])

        if password in useCard:
            if useCard[password][0] == "N":
                locals()[useCard[password][1]]()
                useCard[password][0] == "Y"
            else:
                print(f"這張卡片已經用過了，驗證碼:{password}")
            return

        elif password in soldCard:
            if soldCard[password][0] == "N":
                countryDict[name].gold += int(soldCard[password][1])
                soldCard[password][0] == "Y"
            else:
                print(f"這張卡片已經用過了，驗證碼:{password}")
            return

        else:
            raise NameError(f"驗證碼無效:{password.upper()}")


if __name__ == "__main__":
    print(read_file("伊康攻略(回覆)"))
