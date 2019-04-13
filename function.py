import csv
import gspread
from math import sqrt
from collections import namedtuple
from recordclass import recordclass
from oauth2client.service_account import ServiceAccountCredentials
from Country import (Atlantis, Asgard, Olympus, Wakanda, ShangriLa,
                     Varanasi, Maya, Tartarus, Teotihuacan, EasterIsland)


def read_file(file_name):
    """
        函式作用:讀取位於Google雲端的試算表
        如果讀取的檔案為國家資訊表，則回回傳內層為各個國家的class外層為list的物件，
        如果讀取的檔案為伊康攻略回覆表單，則會回傳內層為各國行動資料的namedtuple，外層為list的物件。
    """

    # 建立namedtuple object
    country_info = namedtuple("country_info",
                              "id name wonders gold population weapon air food_speed wood_speed steel_speed stone_speed food wood steel stone")
    action = namedtuple("action", "time name Pfood Pwood Psteel Pstone useCard soldCard Pwonders war solider resource Rspeed")

    # 抓取google雲端上的試算表
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(file_name).sheet1
    data = sheet.get_all_records()

    # 根據抓取檔案的不同，回傳不同的物件
    if file_name == "國家資訊表":
        return [country_info(*i.values()) for i in data]
    else:
        return [action(*i.values()) for i in data]


def createCountry():
    """透過read_file函數建立Class，回傳儲存各國Class的dictionary"""

    class_list = {"亞特蘭提斯": Atlantis, "阿斯嘉": Asgard, "奧林帕斯": Olympus, "瓦干達": Wakanda,
                  "香格里拉": ShangriLa, "瓦拉納西": Varanasi, "瑪雅": Maya, "塔爾塔洛斯": Tartarus,
                  "特奧蒂瓦坎": Teotihuacan, "復活節島": EasterIsland}

    return {i.name: class_list[i.name](*i) for i in read_file("國家資訊表")}


def handle_action():
    """將各國的行動單做處理，讓接下來資料處理起來比較方便"""
    info = recordclass("info", "name produceList useCard soldCard Pwonders war solider occupyMan resource Rspeed")

    returnList = []
    for i in read_file("伊康攻略(回覆)"):
        if "不戰爭" in i.war.split():
            occupyMan, solider, resource, Rspeed = 0, [], [], []
        else:
            occupyMan = sum([int(j) for j in i.solider.split()])
            solider = [int(j) for j in i.solider.split()]
            resource = i.resource.split()
            Rspeed = i.Rspeed.split()

        tempt = info(i.name, [i.Pfood, i.Pwood, i.Psteel, i.Pstone], i.useCard.split(),
                     i.soldCard.split(), i.Pwonders, i.war.split(), solider, occupyMan, resource, Rspeed)
        returnList.append(tempt)

    return returnList


def production(countryDict, name, produce_num, warrior):
    """ 生產順序:糧食、木頭、鐵礦、石頭 """

    if countryDict[name].population - warrior < sum(produce_num) * 100:
        raise ValueError("人民不夠來生產")

    countryDict[name].food += round(sqrt(produce_num[0]) * pow(countryDict[name].food_speed, (2 / 3)), 0)
    countryDict[name].wood += round(sqrt(produce_num[1]) * pow(countryDict[name].wood_speed, (2 / 3)), 0)
    countryDict[name].steel += round(sqrt(produce_num[2]) * pow(countryDict[name].steel_speed, (2 / 3)), 0)
    countryDict[name].stone += round(sqrt(produce_num[3]) * pow(countryDict[name].stone_speed, (2 / 3)), 0)

    return


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
    a = handle_action()
    print(a)
    try:
        card()
    except Exception as e:
        pass
