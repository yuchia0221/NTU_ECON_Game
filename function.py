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
                              "id name wonders gold population weapon defense food_speed wood_speed steel_speed stone_speed food wood steel stone")
    action = namedtuple("action", "name Pfood Pwood Psteel Pstone useCard soldCard Pwonders war solider resource Rspeed")

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
    elif file_name == "伊康攻略(回覆)":
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
                      '木頭倍率', '鐵礦倍率', '石頭倍率', '糧食', '木頭', '鐵', '石頭'])
    for i in countryDict.values():
        sheet.append_row(i.to_list())


def write_individual(countryDict, name, roundnow):
    def clear_sheet(sheet):
        sheet.clear()
        sheet.append_row(['回合', '國家', '世界奇觀', '黃金', '人民', '武器倍率', '防禦力', '糧食倍率',
                          '木頭倍率', '鐵礦倍率', '石頭倍率', '糧食', '木頭', '鐵', '石頭'])

    # 抓取google雲端上的試算表
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(name).sheet1

    # 更新成現在的國家資訊
    # clear_sheet(sheet)
    sheet.insert_row(list(roundnow) + countryDict[name].to_list()[1:], 2)


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
        if "不戰爭" in i.war.replace(",", "").split():
            war, occupyMan, solider, resource, Rspeed = ["不戰爭"], 0, [], [], []
        else:
            war = i.war.replace(",", "").split()
            occupyMan = sum([int(j) for j in str(i.solider).split()])
            solider = [int(j) for j in str(i.solider).split()]
            resource = i.resource.split()
            Rspeed = i.Rspeed.split()

        tempt = info(i.name, [i.Pfood, i.Pwood, i.Psteel, i.Pstone], i.useCard.split(),
                     i.soldCard.split(), i.Pwonders, war, solider, occupyMan, resource, Rspeed)
        returnList.append(tempt)

    return returnList


def production(countryDict, name, produce_num, warrior):
    """ 生產順序:糧食、木頭、鐵礦、石頭 """

    if countryDict[name].population - warrior < sum(produce_num) * 100:
        raise ValueError("人民不夠來生產")

    countryDict[name].food += round(sqrt(produce_num[0]) * pow(countryDict[name].food_speed, (2 / 3)), 1) * 1000
    countryDict[name].wood += round(sqrt(produce_num[1]) * pow(countryDict[name].wood_speed, (2 / 3)), 1) * 1000
    countryDict[name].steel += round(sqrt(produce_num[2]) * pow(countryDict[name].steel_speed, (2 / 3)), 1) * 1000
    countryDict[name].stone += round(sqrt(produce_num[3]) * pow(countryDict[name].stone_speed, (2 / 3)), 1) * 1000

    return


def read_card():
    with open("卡片.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        return {i[1]: (i[2], i[3], i[4]) for i in csv_reader}


def card(countryDict, name, cardDict, useCard, soldCard):
    """ 發動卡片效果 """

    def food1():
        countryDict[name].food -= 200
        countryDict[name].wood -= 100
        countryDict[name].steel -= 100
        countryDict[name].stone -= 100
        countryDict[name].gold -= 100

        countryDict[name].food_speed += 0.2

    def food2():
        countryDict[name].food -= 500
        countryDict[name].wood -= 200
        countryDict[name].steel -= 200
        countryDict[name].stone -= 200
        countryDict[name].gold -= 500

        countryDict[name].food_speed += 0.4

    def wood1():
        countryDict[name].food -= 100
        countryDict[name].wood -= 200
        countryDict[name].steel -= 100
        countryDict[name].stone -= 100
        countryDict[name].gold -= 100

        countryDict[name].wood_speed += 0.2

    def wood2():
        countryDict[name].food -= 200
        countryDict[name].wood -= 500
        countryDict[name].steel -= 200
        countryDict[name].stone -= 200
        countryDict[name].gold -= 500

        countryDict[name].wood_speed += 0.4

    def steel1():
        countryDict[name].food -= 100
        countryDict[name].wood -= 100
        countryDict[name].steel -= 200
        countryDict[name].stone -= 100
        countryDict[name].gold -= 100

        countryDict[name].steel_speed += 0.2

    def steel2():
        countryDict[name].food -= 200
        countryDict[name].wood -= 200
        countryDict[name].steel -= 500
        countryDict[name].stone -= 200
        countryDict[name].gold -= 500

        countryDict[name].steel_speed += 0.4

    def stone1():
        countryDict[name].food -= 100
        countryDict[name].wood -= 100
        countryDict[name].steel -= 100
        countryDict[name].stone -= 200
        countryDict[name].gold -= 100

        countryDict[name].stone_speed += 0.2

    def stone2():
        countryDict[name].food -= 200
        countryDict[name].wood -= 200
        countryDict[name].steel -= 200
        countryDict[name].stone -= 500
        countryDict[name].gold -= 500

        countryDict[name].stone_speed += 0.4

    def weapon1():
        countryDict[name].wood -= 300
        countryDict[name].steel -= 500
        countryDict[name].stone -= 300
        countryDict[name].gold -= 300

        countryDict[name].weapon += 0.2

    def weapon2():
        countryDict[name].wood -= 800
        countryDict[name].steel -= 1500
        countryDict[name].stone -= 800
        countryDict[name].gold -= 1500

        countryDict[name].weapon += 0.4

    def food_wood():
        countryDict[name].food -= 900
        countryDict[name].wood -= 900
        countryDict[name].steel -= 400
        countryDict[name].stone -= 400
        countryDict[name].gold -= 1000

        countryDict[name].food_speed += 0.3
        countryDict[name].wood_speed += 0.3

    def food_steel():
        countryDict[name].food -= 900
        countryDict[name].wood -= 400
        countryDict[name].steel -= 900
        countryDict[name].stone -= 400
        countryDict[name].gold -= 1000

        countryDict[name].food_speed += 0.3
        countryDict[name].steel_speed += 0.3

    def food_stone():
        countryDict[name].food -= 900
        countryDict[name].wood -= 400
        countryDict[name].steel -= 400
        countryDict[name].stone -= 900
        countryDict[name].gold -= 1000

        countryDict[name].food_speed += 0.3
        countryDict[name].stone_speed += 0.3

    def wood_steel():
        countryDict[name].food -= 400
        countryDict[name].wood -= 900
        countryDict[name].steel -= 900
        countryDict[name].stone -= 400
        countryDict[name].gold -= 1000

        countryDict[name].wood_speed += 0.3
        countryDict[name].steel_speed += 0.3

    def wood_stone():
        countryDict[name].food -= 400
        countryDict[name].wood -= 900
        countryDict[name].steel -= 400
        countryDict[name].stone -= 900
        countryDict[name].gold -= 1000

        countryDict[name].wood_speed += 0.3
        countryDict[name].stone_speed += 0.3

    def steel_stone():
        countryDict[name].food -= 400
        countryDict[name].wood -= 400
        countryDict[name].steel -= 900
        countryDict[name].stone -= 900
        countryDict[name].gold -= 1000

        countryDict[name].steel_speed += 0.3
        countryDict[name].stone_speed += 0.3

    def defense1():
        countryDict[name].wood -= 500
        countryDict[name].steel -= 500
        countryDict[name].gold -= 500

        countryDict[name].defense += 200

    def defense2():
        countryDict[name].wood -= 1500
        countryDict[name].steel -= 1500
        countryDict[name].gold -= 1500

        countryDict[name].defense += 500

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


def war(countryDict, attackingCountry, attackedCountry, soilder, resource, speed, defeated):
    rubrate = 0.001
    diff = countryDict[attackingCountry].weapon * soilder - countryDict[attackedCountry].defense
    if diff >= 0 and not defeated[attackedCountry]:
        countryDict[attackingCountry].population -= soilder * 0.3
        countryDict[attackedCountry].population *= 0.9
        countryDict[attackingCountry].gold += countryDict[attackedCountry].gold * 0.5
        countryDict[attackedCountry].gold *= 0.5
        defeated[attackedCountry] = True

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

        if speed == "糧食":
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

    elif diff >= 0 and defeated:
        countryDict[attackingCountry].population -= soilder * 0.1
        countryDict[attackingCountry].gold += countryDict[attackedCountry].gold * 0.5
        countryDict[attackedCountry].gold *= 0.5

        if resource == "糧食":
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

    elif diff < 0:
        countryDict[attackingCountry].population -= soilder * 0.4


def buildwonder(countryDict, name, percentWonders, state, Update):

    if state == 0:
        countryDict[name].wood -= 300 * percentWonders
        countryDict[name].stone -= 200 * percentWonders
        countryDict[name].gold -= 500 * percentWonders
        if Update:
            countryDict[name].weapon += 2
            countryDict[name].defense += 200

    elif state == 1:
        countryDict[name].wood -= 800 * percentWonders
        countryDict[name].stone -= 400 * percentWonders
        countryDict[name].gold -= 1500 * percentWonders
        if Update:
            countryDict[name].food_speed += 2
            countryDict[name].wood_speed += 2
            countryDict[name].steel_speed += 2
            countryDict[name].stone_speed += 2
            countryDict[name].population += 400

    elif state == 2:
        countryDict[name].wood -= 1500 * percentWonders
        countryDict[name].stone -= 800 * percentWonders
        countryDict[name].gold -= 3000 * percentWonders
        if Update:
            countryDict[name].weapon += 4
            countryDict[name].defense += 1000
            countryDict[name].food_speed += 1
            countryDict[name].wood_speed += 1
            countryDict[name].steel_speed += 1
            countryDict[name].stone_speed += 1
            countryDict[name].population += 200

    elif state == 3:
        countryDict[name].wood -= 3000 * percentWonders
        countryDict[name].stone -= 1500 * percentWonders
        countryDict[name].gold -= 6000 * percentWonders
        if Update:
            createCountry[name].population += 3000


def wonder(countryDict, wonderlist, actionlist):  # 這邊把actionlist傳進去的寫法很糟，但目前我沒想到好辦法
    currstate = {}      # [奇觀名字] : 現在階段
    totalwonder = {}    # [奇觀名字] : 準備要建造多少比例
    currwonder = {}     # [奇觀名字] : 現在有多少比例
    wonderdict = {}     # [國家名字] : 每國準備貢獻多少比例
    Update = {}
    for i in actionlist:
        wonderdict[i.name] = i.Pwonders

    for i in wonderlist:
        temp = list(i)
        currstate[temp[0]] = temp[3]
        currwonder[temp[0]] = temp[2]
        Update[temp[0]] = False
        for j in temp[1].split():
            revisePwonder(countryDict, j, currstate[0], wonderdict)
            if temp[0] in totalwonder:
                totalwonder[temp[0]] += wonderdict[j]
            else:
                totalwonder[temp[0]] = wonderdict[j]

        if currwonder[temp[0]] + totalwonder[temp[0]] - currstate[temp[0]] * 25 > 25:
            Update[temp[0]] = True
            weight = (25 - (currwonder % 25)) / (totalwonder[temp[0]] - currwonder[temp[0]])
            for j in temp[1].split():
                wonderdict[j] = round(wonderdict[j] * weight, 0)

        for j in temp[1].split():
            buildwonder(countryDict, j, wonderdict[j], temp[3], Update[temp[0]])


def revisePwonder(countryDict, name, state, wonderdict):
    material = []
    if state == 0:
        material.append(countryDict[name].wood / 300)
        material.append(countryDict[name].stone / 200)
        material.append(countryDict[name].gold / 500)

        if min(material) < wonderdict[name]:
            wonderdict[name] = min(material)
    elif state == 1:
        material.append(countryDict[name].wood / 800)
        material.append(countryDict[name].stone / 400)
        material.append(countryDict[name].gold / 1500)

        if min(material) < wonderdict[name]:
            wonderdict[name] = min(material)

    elif state == 2:
        material.append(countryDict[name].wood / 1500)
        material.append(countryDict[name].stone / 800)
        material.append(countryDict[name].gold / 3000)

        if min(material) < wonderdict[name]:
            wonderdict[name] = min(material)

    elif state == 3:
        material.append(countryDict[name].wood / 3000)
        material.append(countryDict[name].stone / 1500)
        material.append(countryDict[name].gold / 6000)

        if min(material) < wonderdict[name]:
            wonderdict[name] = min(material)


if __name__ == "__main__":
    pass
