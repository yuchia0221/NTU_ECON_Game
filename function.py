import csv
import gspread
from collections import namedtuple
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
                              "id name wonders gold population weapon defense food_speed wood_speed steel_speed stone_speed food wood steel stone education")
    action = namedtuple("action", "time name Pfood Pwood Psteel Pstone useCard soldCard education war solider resource Rspeed Pwonders")

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
    elif file_name == "伊康攻略回應表 (回應)":
        return [action(*i.values()) for i in data]
    else:
        return [list(i.values()) for i in data]


def write_country_file(countryDict):
    # 抓取google雲端上的試算表
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("國家資訊表").sheet1
    sheet.clear()

    # 更新成現在的國家資訊
    sheet.append_row(['編號', '國家', '世界奇觀', '黃金', '人民', '武器倍率', '防禦力', '糧食倍率',
                      '木頭倍率', '鐵礦倍率', '石頭倍率', '糧食', '木頭', '鐵', '石頭', '教育'])
    for i in countryDict.values():
        sheet.append_row(i.to_list())


def write_individual(countryDict, name, roundnow, boolean=False):
    def clear_sheet(sheet):
        sheet.clear()
        sheet.append_row(['回合', '國家', '世界奇觀', '黃金', '人民', '武器倍率', '防禦力', '糧食倍率',
                          '木頭倍率', '鐵礦倍率', '石頭倍率', '糧食', '木頭', '鐵礦', '石頭', '教育'])

    # 抓取google雲端上的試算表
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(name).sheet1

    # 更新成現在的國家資訊
    if boolean:
        clear_sheet(sheet)
    tempt = list(roundnow) + countryDict[name].to_list()[1:]
    sheet.insert_row(tempt, 2)


def write_wonders(countryDict):
    # 抓取google雲端上的試算表
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("世界奇觀").sheet1

    # 更新世界奇觀位置
    row = 2
    appendList = [i.wonders for i in countryDict.values()]
    for i, j in zip(appendList[::2], appendList[1::2]):
        sheet.update_cell(row, 3, i + j)
        sheet.update_cell(row, 5, i)
        sheet.update_cell(row, 6, j)
        if i + j < 25:                                  # 0~24 第零階段 25~49 第一階段 50~74 第二階段 75~99 第三階段 100 第四階段
            sheet.update_cell(row, 4, 0)
        elif i + j < 50:
            sheet.update_cell(row, 4, 1)
        elif i + j < 75:
            sheet.update_cell(row, 4, 2)
        elif i + j < 100:
            sheet.update_cell(row, 4, 3)
        elif i + j == 100:
            sheet.update_cell(row, 4, 4)
        row += 1


def initialize():
    """ 根據初始國家資訊表，初始化google雲端上的所有檔案 """
    # 建立namedtuple object
    country_info = namedtuple("country_info",
                              "id name wonders gold population weapon defense food_speed wood_speed steel_speed stone_speed food wood steel stone education")
    class_list = {"亞特蘭提斯": Atlantis, "阿斯嘉": Asgard, "奧林帕斯": Olympus, "瓦干達": Wakanda,
                  "香格里拉": ShangriLa, "瓦拉納西": Varanasi, "瑪雅": Maya, "塔爾塔洛斯": Tartarus,
                  "特奧蒂瓦坎": Teotihuacan, "復活節島": EasterIsland}

    with open("初始國家資訊.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        countryList = [country_info(*i) for i in csv_reader]
        countryDict = {i.name: class_list[i.name](*i) for i in countryList}

    write_country_file(countryDict)
    for i in class_list.keys():
        write_individual(countryDict, i, "一", True)


def createCountry():
    """透過read_file函數建立Class，回傳儲存各國Class的dictionary"""

    class_list = {"亞特蘭提斯": Atlantis, "阿斯嘉": Asgard, "奧林帕斯": Olympus, "瓦干達": Wakanda,
                  "香格里拉": ShangriLa, "瓦拉納西": Varanasi, "瑪雅": Maya, "塔爾塔洛斯": Tartarus,
                  "特奧蒂瓦坎": Teotihuacan, "復活節島": EasterIsland}

    return {i.name: class_list[i.name](*i) for i in read_file("國家資訊表")}


def handle_action():
    """ 將各國的行動單做處理，讓接下來資料處理起來比較方便 """
    info = namedtuple("info", "name produceList useCard soldCard education war solider occupyMan resource Rspeed Pwonders")

    returnList = []
    for i in read_file("伊康攻略回應表 (回應)"):
        if "不戰爭" in i.war.replace(",", "").split():
            war, occupyMan, solider, resource, Rspeed = ["不戰爭"], 0, [], [], []
        else:
            war = i.war.replace(",", "").split()
            occupyMan = sum([int(j) for j in str(i.solider).split()])
            solider = [int(j) for j in str(i.solider).split()]
            resource = i.resource.split()
            Rspeed = i.Rspeed.split()

        tempt = info(i.name, [i.Pfood, i.Pwood, i.Psteel, i.Pstone], i.useCard.split(),
                     i.soldCard.split(), i.education, war, solider, occupyMan, resource, Rspeed, i.Pwonders)
        returnList.append(tempt)

    return returnList


def production(countryDict, produceData, name, produce_num, warrior):
    """ 生產順序:糧食、木頭、鐵礦、石頭 """

    if countryDict[name].population < warrior:              # 如果打仗人數超過人口上限，因為全民皆兵，本次生產作廢
        for i in range(4):
            produce_num[i] = 0

    if countryDict[name].population - warrior < sum(produce_num) * 100:     # 人民不足生產
        times = (countryDict[name].population - warrior) // 100             # 計算本回合共能生產幾次
        for i in range(4):                                                  # 對每一項物資
            if times >= produce_num[i]:                                     # 讓預期生產次數和實際上剩餘生產次數比較
                times -= produce_num[i]
            else:
                produce_num[i] = times                                      # 如果已經無法生產，則讓實際生產次數歸0
                times = 0

        print(f"{name}的人民不夠來生產, 生產:{produce_num}")

    # 依序執行食物、木頭、鐵礦、石頭的生產

    food = dict(produceData[str(produce_num[0])])[float(countryDict[name].food_speed)]
    wood = dict(produceData[str(produce_num[1])])[float(countryDict[name].wood_speed)]
    steel = dict(produceData[str(produce_num[2])])[float(countryDict[name].steel_speed)]
    stone = dict(produceData[str(produce_num[3])])[float(countryDict[name].stone_speed)]

    countryDict[name].food += int(food)                                          # 讓該國物資量加上本回合生產量
    countryDict[name].wood += int(wood)
    countryDict[name].steel += int(steel)
    countryDict[name].stone += int(stone)

    print(f"{name} has produced {food} food {wood} wood {steel} steel {stone} stone ")  # 顯示該國生產量

    return


def read_card():
    with open("卡片.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        return {i[1]: (i[2], i[3], i[4]) for i in csv_reader}


def card(countryDict, name, cardDict, useCard, soldCard, defeated):
    def food1():
        if (countryDict[name].food >= 600 and countryDict[name].wood >= 200 and countryDict[name].steel >= 200 and
                countryDict[name].stone >= 200 and countryDict[name].gold >= 400):
            countryDict[name].food -= 600
            countryDict[name].wood -= 200
            countryDict[name].steel -= 200
            countryDict[name].stone -= 200
            countryDict[name].gold -= 400
        else:
            print(f"{name} dosen't have enough resource to invest food1")
            return

        countryDict[name].food_speed += 0.4
        print(f"{name} has successfully invest food1")

    def food2():
        if (countryDict[name].food >= 1000 and countryDict[name].wood >= 400 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 600):
            countryDict[name].food -= 1000
            countryDict[name].wood -= 400
            countryDict[name].steel -= 400
            countryDict[name].stone -= 400
            countryDict[name].gold -= 600
        else:
            print(f"{name} dosen't have enough resource to invest food2")
            return

        countryDict[name].food_speed += 0.8
        print(f"{name} has successfully invest food2")

    def food3():
        countryDict[name].food *= 1.5
        print(f"{name} has successfully invest food3")

    def wood1():
        if (countryDict[name].food >= 200 and countryDict[name].wood >= 600 and countryDict[name].steel >= 200 and
                countryDict[name].stone >= 200 and countryDict[name].gold >= 400):
            countryDict[name].food -= 200
            countryDict[name].wood -= 600
            countryDict[name].steel -= 200
            countryDict[name].stone -= 200
            countryDict[name].gold -= 400
        else:
            print(f"{name} dosen't have enough resource to invest wood1")
            return

        countryDict[name].wood_speed += 0.4
        print(f"{name} has successfully invest wood1")

    def wood2():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 1000 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 600):
            countryDict[name].food -= 400
            countryDict[name].wood -= 1000
            countryDict[name].steel -= 400
            countryDict[name].stone -= 400
            countryDict[name].gold -= 600
        else:
            print(f"{name} dosen't have enough resource to invest wood2")
            return

        countryDict[name].wood_speed += 0.8
        print(f"{name} has successfully invest wood2")

    def wood3():
        countryDict[name].wood *= 1.5
        print(f"{name} has successfully invest wood3")

    def steel1():
        if (countryDict[name].food >= 200 and countryDict[name].wood >= 200 and countryDict[name].steel >= 600 and
                countryDict[name].stone >= 200 and countryDict[name].gold >= 400):
            countryDict[name].food -= 200
            countryDict[name].wood -= 200
            countryDict[name].steel -= 600
            countryDict[name].stone -= 200
            countryDict[name].gold -= 400
        else:
            print(f"{name} dosen't have enough resource to invest steel1")
            return

        countryDict[name].steel_speed += 0.4
        print(f"{name} has successfully invest steel1")

    def steel2():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 400 and countryDict[name].steel >= 1000 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 600):
            countryDict[name].food -= 400
            countryDict[name].wood -= 400
            countryDict[name].steel -= 1000
            countryDict[name].stone -= 400
            countryDict[name].gold -= 600
        else:
            print(f"{name} dosen't have enough resource to invest steel2")
            return

        countryDict[name].steel_speed += 0.8
        print(f"{name} has successfully invest steel2")

    def steel3():
        countryDict[name].steel *= 1.5
        print(f"{name} has successfully invest steel3")

    def stone1():
        if (countryDict[name].food >= 200 and countryDict[name].wood >= 200 and countryDict[name].steel >= 200 and
                countryDict[name].stone >= 600 and countryDict[name].gold >= 400):
            countryDict[name].food -= 200
            countryDict[name].wood -= 200
            countryDict[name].steel -= 200
            countryDict[name].stone -= 600
            countryDict[name].gold -= 400
        else:
            print(f"{name} dosen't have enough resource to invest stone1")
            return

        countryDict[name].stone_speed += 0.4
        print(f"{name} has successfully invest stone1")

    def stone2():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 400 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 1000 and countryDict[name].gold >= 600):
            countryDict[name].food -= 400
            countryDict[name].wood -= 400
            countryDict[name].steel -= 400
            countryDict[name].stone -= 1000
            countryDict[name].gold -= 600
        else:
            print(f"{name} dosen't have enough resource to invest stone2")
            return

        countryDict[name].stone_speed += 0.8
        print(f"{name} has successfully invest stone2")

    def stone3():
        countryDict[name].stone *= 1.5
        print(f"{name} has successfully invest stone3")

    def food_wood():
        if (countryDict[name].food >= 800 and countryDict[name].wood >= 800 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 800
            countryDict[name].wood -= 800
            countryDict[name].steel -= 400
            countryDict[name].stone -= 400
            countryDict[name].gold -= 1200
        else:
            print(f"{name} dosen't have enough resource to invest food_wood")
            return

        countryDict[name].food_speed += 0.5
        countryDict[name].wood_speed += 0.5
        print(f"{name} has successfully invest food_wood")

    def food_steel():
        if (countryDict[name].food >= 800 and countryDict[name].wood >= 400 and countryDict[name].steel >= 800 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 800
            countryDict[name].wood -= 400
            countryDict[name].steel -= 800
            countryDict[name].stone -= 400
            countryDict[name].gold -= 1200
        else:
            print(f"{name} dosen't have enough resource to invest food_steel")
            return

        countryDict[name].food_speed += 0.5
        countryDict[name].steel_speed += 0.5
        print(f"{name} has successfully invest food_steel")

    def food_stone():
        if (countryDict[name].food >= 800 and countryDict[name].wood >= 400 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 800 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 800
            countryDict[name].wood -= 400
            countryDict[name].steel -= 400
            countryDict[name].stone -= 800
            countryDict[name].gold -= 1200
        else:
            print(f"{name} dosen't have enough resource to invest food_stone")
            return

        countryDict[name].food_speed += 0.5
        countryDict[name].stone_speed += 0.5
        print(f"{name} has successfully invest food_stone")

    def wood_steel():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 800 and countryDict[name].steel >= 800 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 400
            countryDict[name].wood -= 800
            countryDict[name].steel -= 800
            countryDict[name].stone -= 400
            countryDict[name].gold -= 1200
        else:
            print(f"{name} dosen't have enough resource to invest wood_steel")
            return

        countryDict[name].wood_speed += 0.5
        countryDict[name].steel_speed += 0.5
        print(f"{name} has successfully invest wood_steel")

    def wood_stone():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 800 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 800 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 400
            countryDict[name].wood -= 800
            countryDict[name].steel -= 400
            countryDict[name].stone -= 800
            countryDict[name].gold -= 1200
        else:
            print(f"{name} dosen't have enough resource to invest wood_stone")
            return

        countryDict[name].wood_speed += 0.5
        countryDict[name].stone_speed += 0.5
        print(f"{name} has successfully invest wood_stone")

    def steel_stone():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 400 and countryDict[name].steel >= 800 and
                countryDict[name].stone >= 800 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 400
            countryDict[name].wood -= 400
            countryDict[name].steel -= 800
            countryDict[name].stone -= 800
            countryDict[name].gold -= 1200
        else:
            print(f"{name} dosen't have enough resource to invest steel_stone")
            return

        countryDict[name].steel_speed += 0.5
        countryDict[name].stone_speed += 0.5
        print(f"{name} has successfully invest steel_stone")

    def defense1():
        if countryDict[name].wood >= 500 and countryDict[name].steel >= 500 and countryDict[name].gold >= 500:
            countryDict[name].wood -= 500
            countryDict[name].steel -= 500
            countryDict[name].gold -= 500
        else:
            print(f"{name} dosen't have enough resource to invest defense1")
            return

        countryDict[name].defense += 100
        print(f"{name} has successfully invest defense1")

    def defense2():
        if countryDict[name].wood >= 1000 and countryDict[name].steel >= 1000 and countryDict[name].gold >= 1000:
            countryDict[name].wood -= 1000
            countryDict[name].steel -= 1000
            countryDict[name].gold -= 1000
        else:
            print(f"{name} dosen't have enough resource to invest defense2")
            return

        countryDict[name].defense += 300
        print(f"{name} has successfully invest defense2")

    def defense3():
        if countryDict[name].wood >= 1500 and countryDict[name].steel >= 1500 and countryDict[name].gold >= 1500:
            countryDict[name].wood -= 1500
            countryDict[name].steel -= 1500
            countryDict[name].gold -= 1500
        else:
            print(f"{name} dosen't have enough resource to invest defense3")
            return

        countryDict[name].defense += 500
        print(f"{name} has successfully invest defense3   ")

    def weapon1():
        if (countryDict[name].wood >= 300 and countryDict[name].steel >= 500 and
                countryDict[name].stone >= 300 and countryDict[name].gold >= 300):
            countryDict[name].wood -= 300
            countryDict[name].steel -= 500
            countryDict[name].stone -= 300
            countryDict[name].gold -= 300
        else:
            print(f"{name} dosen't have enough resource to invest weapon1")
            return

        countryDict[name].weapon += 0.2
        print(f"{name} has successfully invest weapon1")

    def weapon2():
        if (countryDict[name].wood >= 550 and countryDict[name].steel >= 1000 and
                countryDict[name].stone >= 550 and countryDict[name].gold >= 900):
            countryDict[name].wood -= 550
            countryDict[name].steel -= 1000
            countryDict[name].stone -= 550
            countryDict[name].gold -= 900
        else:
            print(f"{name} dosen't have enough resource to invest weapon2")
            return

        countryDict[name].weapon += 0.4
        print(f"{name} has successfully invest weapon2")

    def weapon3():
        if (countryDict[name].wood >= 800 and countryDict[name].steel >= 1500 and
                countryDict[name].stone >= 800 and countryDict[name].gold >= 1500):
            countryDict[name].wood -= 800
            countryDict[name].steel -= 1500
            countryDict[name].stone -= 800
            countryDict[name].gold -= 1500
        else:
            print(f"{name} dosen't have enough resource to invest weapon3")
            return

        countryDict[name].weapon += 0.6
        print(f"{name} has successfully invest weapon3")

    def war1():
        if (countryDict[name].wood >= 600 and countryDict[name].steel >= 1000 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 1000):
            countryDict[name].wood -= 600
            countryDict[name].steel -= 1000
            countryDict[name].stone -= 400
            countryDict[name].gold -= 1000
        else:
            print(f"{name} dosen't have enough resource to invest war1")
            return

        countryDict[name].weapon += 0.3
        countryDict[name].defense += 150
        print(f"{name} has successfully invest war1")

    def war2():                                                            # 石中劍
        if (countryDict[name].wood >= 2000 and countryDict[name].steel >= 2500 and
                countryDict[name].stone >= 600 and countryDict[name].gold >= 2500):
            countryDict[name].wood -= 2000
            countryDict[name].steel -= 2500
            countryDict[name].stone -= 600
            countryDict[name].gold -= 2500
        else:
            print(f"{name} dosen't have enough resource to invest war2")
            return

        countryDict[name].weapon += 0.5
        countryDict[name].defense += 450
        print(f"{name} has successfully invest war2")

    def all1():                                                            # 蟹堡秘方
        if (countryDict[name].food >= 1200 and countryDict[name].wood >= 600 and countryDict[name].steel >= 600 and
                countryDict[name].stone >= 600 and countryDict[name].gold >= 2500):
            countryDict[name].food -= 1200
            countryDict[name].wood -= 600
            countryDict[name].steel -= 600
            countryDict[name].stone -= 600
            countryDict[name].gold -= 2500
        else:
            print(f"{name} dosen't have enough resource to invest all1")
            return

        countryDict[name].food_speed += 0.5
        countryDict[name].wood_speed += 0.3
        countryDict[name].steel_speed += 0.3
        countryDict[name].stone_speed += 0.3
        print(f"{name} has successfully invest all1")

    def all2():                                                            # 國富論
        if (countryDict[name].food >= 600 and countryDict[name].wood >= 700 and countryDict[name].steel >= 600 and
                countryDict[name].stone >= 800 and countryDict[name].gold >= 2000):
            countryDict[name].food -= 600
            countryDict[name].wood -= 700
            countryDict[name].steel -= 600
            countryDict[name].stone -= 800
            countryDict[name].gold -= 2000
        else:
            print(f"{name} dosen't have enough resource to invest all2")
            return

        countryDict[name].food_speed += 0.3
        countryDict[name].wood_speed += 0.3
        countryDict[name].steel_speed += 0.3
        countryDict[name].stone_speed += 0.3
        print(f"{name} has successfully invest all2")

    def gold1():
        countryDict[name].gold *= 1.5
        print(f"{name} has successfully invest gold1")

    def gold2():
        countryDict[name].gold *= 2
        print(f"{name} has successfully invest gold2")

    def human1():
        countryDict[name].population += 100
        print(f"{name} has successfully invest human1")

    def human2():
        countryDict[name].population += 200
        print(f"{name} has successfully invest human2")

    def human3():
        countryDict[name].population += 300
        print(f"{name} has successfully invest human3")

    for card in useCard:
        try:
            if cardDict[card][1] == "Y":
                print(f"這張卡片已經使用過了")
            else:
                locals()[cardDict[card][0]]()

        except KeyError:
            raise KeyError(f"卡片驗證碼:{card}不存在")

    for card in soldCard:
        try:
            if cardDict[card][1] == "Y":
                print(f"這張卡片已經使用過了")
            else:
                countryDict[name].gold += int(cardDict[card][2])

        except KeyError:
            raise KeyError(f"卡片驗證碼:{card}不存在")


def eduction(countryDict, name, invest):
    if invest == "是":
        if countryDict[name].education == 0:
            try:
                countryDict[name].food -= 3000
                countryDict[name].education = 1
            except ValueError as e:
                print(f"{name}沒有足夠的物資投資教育")

        if countryDict[name].eduction == 1:
            try:
                countryDict[name].food -= 5000
                countryDict[name].education = 2
            except ValueError as e:
                print(f"{name}沒有足夠的物資投資教育")

        if countryDict[name].eduction == 2:
            try:
                countryDict[name].food -= 7000
                countryDict[name].education = 3
            except ValueError as e:
                print(f"{name}沒有足夠的物資投資教育")

        if countryDict[name].eduction == 3:
            try:
                countryDict[name].food -= 9000
                countryDict[name].education = 4
            except ValueError as e:
                print(f"{name}沒有足夠的物資投資教育")

    else:
        return


def war(countryDict, attackingCountry, attackedCountry, soilder, resource, speed, defeated):
    if attackingCountry == attackedCountry:                             # 如果攻打國和被攻打國屬於同一個國家，則攻擊無效
        print(f"{attackingCountry} can't attack itself")
        return
    elif defeated[attackedCountry] == "Cannot attack":
        return
    elif countryDict[attackingCountry].population < soilder:            # 如果派出的士兵比人口還多，則攻擊無效
        print(f"{attackingCountry}的士兵比人口還多")
        return

    rubrate = 0.001                                                     # 搶奪比率為0.001
    diff = countryDict[attackingCountry].weapon * soilder - countryDict[attackedCountry].defense    # 勝負的判定為，A國武器倍率 * 士兵 vs B國防禦力
    if diff >= 0 and not defeated[attackedCountry]:                                                 # 如果A國戰勝而且B國之前沒有戰敗過
        countryDict[attackingCountry].population -= soilder * 0.5                                   # A國損失五成士兵
        countryDict[attackedCountry].population *= 0.9                                              # B國損失一成人口
        countryDict[attackingCountry].gold += countryDict[attackedCountry].gold * 0.5               # A國盜取B國一半黃金
        countryDict[attackedCountry].gold *= 0.5
        defeated[attackedCountry] = True                                                            # B國戰敗的布林值改為true

        print(f"{attackingCountry}戰勝了{attackedCountry}，掠奪了{resource}和{speed}倍率")            # A國搶奪B國一半加上0.001 * 戰力差的資源

        if resource == "糧食":
            try:
                countryDict[attackingCountry].food += countryDict[attackedCountry].food * (0.5 + rubrate * diff)
                countryDict[attackedCountry].food -= countryDict[attackedCountry].food * (0.5 + rubrate * diff)
            except ValueError:
                countryDict[attackingCountry].food += countryDict[attackedCountry].food
                countryDict[attackedCountry].food = 0
        elif resource == "木頭":
            try:
                countryDict[attackingCountry].wood += countryDict[attackedCountry].wood * (0.5 + rubrate * diff)
                countryDict[attackedCountry].wood -= countryDict[attackedCountry].wood * (0.5 + rubrate * diff)
            except ValueError:
                countryDict[attackingCountry].wood += countryDict[attackedCountry].wood
                countryDict[attackedCountry].wood = 0
        elif resource == "鐵礦":
            try:
                countryDict[attackingCountry].steel += countryDict[attackedCountry].steel * (0.5 + rubrate * diff)
                countryDict[attackedCountry].steel -= countryDict[attackedCountry].steel * (0.5 + rubrate * diff)
            except ValueError:
                countryDict[attackingCountry].steel += countryDict[attackedCountry].steel
                countryDict[attackedCountry].steel = 0
        elif resource == "石頭":
            try:
                countryDict[attackingCountry].stone += countryDict[attackedCountry].stone * (0.5 + rubrate * diff)
                countryDict[attackedCountry].stone -= countryDict[attackedCountry].stone * (0.5 + rubrate * diff)
            except ValueError:
                countryDict[attackingCountry].stone += countryDict[attackedCountry].stone
                countryDict[attackedCountry].stone = 0

        if speed == "糧食":                                                                           # A國搶奪B國某種倍率
            countryDict[attackingCountry].food_speed += 0.2
            countryDict[attackedCountry].food_speed -= 0.2
        elif speed == "木頭":
            countryDict[attackingCountry].wood_speed += 0.2
            countryDict[attackedCountry].wood_speed -= 0.2
        elif speed == "鐵礦":
            countryDict[attackingCountry].steel_speed += 0.2
            countryDict[attackedCountry].steel_speed -= 0.2
        elif speed == "石頭":
            countryDict[attackingCountry].stone_speed += 0.2
            countryDict[attackedCountry].stone_speed -= 0.2

    elif diff >= 0 and defeated[attackedCountry]:                                                       # 如果A國打贏B國，且B國曾經被打敗過
        countryDict[attackingCountry].population -= soilder * 0.1                                       # A國損失一成士兵
        countryDict[attackingCountry].gold += countryDict[attackedCountry].gold * 0.5                   # A國搶奪B國一半黃金
        countryDict[attackedCountry].gold *= 0.5

        if resource == "糧食":                                                                            # A國搶奪B國一半的物資和戰力差 * 0.001
            try:
                countryDict[attackingCountry].food += 0.5 * countryDict[attackedCountry].food * (0.5 + rubrate * diff)
                countryDict[attackedCountry].food -= 0.5 * countryDict[attackedCountry].food * (0.5 + rubrate * diff)
            except ValueError:
                countryDict[attackingCountry].food += countryDict[attackedCountry].food
                countryDict[attackedCountry].food = 0
        elif resource == "木頭":
            try:
                countryDict[attackingCountry].wood += 0.5 * countryDict[attackedCountry].wood * (0.5 + rubrate * diff)
                countryDict[attackedCountry].wood -= 0.5 * countryDict[attackedCountry].wood * (0.5 + rubrate * diff)
            except ValueError:
                countryDict[attackingCountry].wood += countryDict[attackedCountry].wood
                countryDict[attackedCountry].wood = 0
        elif resource == "鐵礦":
            try:
                countryDict[attackingCountry].steel += 0.5 * countryDict[attackedCountry].steel * (0.5 + rubrate * diff)
                countryDict[attackedCountry].steel -= 0.5 * countryDict[attackedCountry].steel * (0.5 + rubrate * diff)
            except ValueError:
                countryDict[attackingCountry].steel += countryDict[attackedCountry].steel
                countryDict[attackedCountry].steel = 0
        elif resource == "石頭":
            try:
                countryDict[attackingCountry].stone += 0.5 * countryDict[attackedCountry].stone * (0.5 + rubrate * diff)
                countryDict[attackedCountry].stone -= 0.5 * countryDict[attackedCountry].stone * (0.5 + rubrate * diff)
            except ValueError:
                countryDict[attackingCountry].stone += countryDict[attackedCountry].stone
                countryDict[attackedCountry].stone = 0

    elif diff < 0:                                                  # 如果B國防守成功， A國損失七成士兵
        countryDict[attackingCountry].population -= soilder * 0.4
        print(f"{attackingCountry}進攻了{attackedCountry}但失敗了，損失四成士兵")

    return


def buildwonder(countryDict, name, Wname, percentWonders, state, Update):              # 建造奇蹟的函數
    bundle = {}     # bundle是一個字典，key 是奇觀名字, value是一個二維陣列， 第一個index值對應到階段， 第二個index值對應到物資數量
    bundle["經思闕"] = [[300, 200, 200, 500], [800, 300, 400, 1500], [1500, 1000, 800, 2500], [2500, 1500, 1800, 3500]]    # 物資依序為[木頭, 鐵礦, 石頭, 黃金]
    bundle["亡星陵"] = [[300, 200, 200, 500], [500, 700, 300, 1500], [1200, 900, 1200, 2500], [1400, 2000, 2400, 3500]]
    bundle["釗晁榭"] = [[300, 200, 200, 500], [700, 400, 400, 1500], [900, 1000, 1400, 2500], [2200, 2000, 1600, 3500]]
    bundle["橡彶軒"] = [[300, 200, 200, 500], [350, 800, 350, 1500], [800, 1000, 1500, 2500], [1800, 2500, 1500, 3500]]
    bundle["噱町閣"] = [[300, 200, 200, 500], [400, 350, 750, 1500], [1000, 1300, 1000, 2500], [1800, 2200, 1800, 3500]]
    package = bundle[Wname][state]                              # 選擇本次建造組合

    countryDict[name].wood -= package[0] * percentWonders
    countryDict[name].steel -= package[1] * percentWonders
    countryDict[name].stone -= package[2] * percentWonders
    countryDict[name].gold -= package[3] * percentWonders

    if Update:
        if state == 0:                                              # 第一階段完成的獎勵
            countryDict[name].weapon += 2
            countryDict[name].defense += 200

        elif state == 1:                                            # 第二階段完成的獎勵
            countryDict[name].food_speed += 1
            countryDict[name].wood_speed += 1
            countryDict[name].steel_speed += 1
            countryDict[name].stone_speed += 1
            countryDict[name].population += 400

        elif state == 2:                                            # 第三階段完成的獎勵
            countryDict[name].weapon += 4
            countryDict[name].defense += 1000
            countryDict[name].food_speed += 2
            countryDict[name].wood_speed += 2
            countryDict[name].steel_speed += 2
            countryDict[name].stone_speed += 2

        elif state == 3:                                            # 第四階段完成的獎勵
            createCountry[name].population += 3000

    if state == 4:
        return

    countryDict[name].wonders += int(percentWonders)
    print(f"{name} 貢獻了 {percentWonders}% 給{Wname}")


def wonder(countryDict, wonderlist, actionlist):
    # 這邊把actionlist傳進去的寫法很糟，但目前我沒想到好辦法
    currstate = {}      # [奇觀名字] : 現在階段
    totalwonder = {}    # [奇觀名字] : 準備要建造多少比例
    currwonder = {}     # [奇觀名字] : 現在有多少比例
    wonderdict = {i.name: i.Pwonders for i in actionlist}     # [國家名字] : 每國準備貢獻多少比例
    Update = {}

    for i in wonderlist:                                        # 對於每個奇觀
        temp = list(i)
        Wname = temp[0]                                         # Wname 為奇觀名字
        currstate[Wname] = int(temp[3])                         # 目前階段
        currwonder[Wname] = temp[2]                             # 目前進度
        Update[Wname] = False
        for name in temp[1].split():                            # 對每一個國家
            revisePwonder(countryDict, name, Wname, currstate[Wname], wonderdict)  # 確認物資是否足夠投資
            if Wname in totalwonder:
                totalwonder[Wname] += wonderdict[name]
            else:
                totalwonder[Wname] = wonderdict[name]

        print(totalwonder, wonderdict)

        if currwonder[Wname] + totalwonder[Wname] - currstate[Wname] * 25 > 25:     # 確認是否晉級
            Update[Wname] = True
            print(f"{Wname} 達到了第{currstate[Wname] + 1}階段，所有在這奇觀下的國家都獲得加成")
            weight = (25 + currstate[Wname] * 25 - currwonder[Wname]) / totalwonder[Wname]  # 計算線性權重
            for name in temp[1].split():                                                    # 重寫每個國家的投資數量
                wonderdict[name] = int(round(wonderdict[name] * weight, 0))

        for name in temp[1].split():                                                    # 蓋奇觀
            buildwonder(countryDict, name, Wname, wonderdict[name], temp[3], Update[Wname])


def revisePwonder(countryDict, name, Wname, state, wonderdict):
    bundle = {}                                                 # 物資依序為[木頭, 鐵礦, 石頭, 黃金]
    bundle["經思闕"] = [[300, 200, 200, 500], [800, 300, 400, 1500], [1500, 1000, 800, 2500], [2500, 1500, 1800, 3500]]
    bundle["亡星陵"] = [[300, 200, 200, 500], [500, 700, 300, 1500], [1200, 900, 1200, 2500], [1400, 2000, 2400, 3500]]
    bundle["釗晁榭"] = [[300, 200, 200, 500], [700, 400, 400, 1500], [900, 1000, 1400, 2500], [2200, 2000, 1600, 3500]]
    bundle["橡彶軒"] = [[300, 200, 200, 500], [350, 800, 350, 1500], [800, 1000, 1500, 2500], [1800, 2500, 1500, 3500]]
    bundle["噱町閣"] = [[300, 200, 200, 500], [400, 350, 750, 1500], [1000, 1300, 1000, 2500], [1800, 2200, 1800, 3500]]
    package = bundle[Wname][state]                              # 選擇本次建造組合
    material = []

    material.append(countryDict[name].wood / package[0])        # 確認最大可能生產次數
    material.append(countryDict[name].steel / package[1])
    material.append(countryDict[name].stone / package[2])
    material.append(countryDict[name].gold / package[3])

    if min(material) < wonderdict[name]:                        # 如果欲建造次數超過能力上限，則讓欲建造次數等同能力上限
        wonderdict[name] = int(min(material))


def consume(countryDict):
    for i in countryDict.values():
        i.population += 100
        try:
            i.food -= i.population * 2
        except ValueError as e:
            try:
                i.gold -= i.population * 2
            except ValueError as e:
                i.gold = 0


if __name__ == "__main__":
    # initialize()
    pass
