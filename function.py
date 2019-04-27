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
                              "id name wonders gold population weapon defense food_speed wood_speed steel_speed stone_speed food wood steel stone")
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
        if i + j < 25:
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


def createCountry():
    """透過read_file函數建立Class，回傳儲存各國Class的dictionary"""

    class_list = {"亞特蘭提斯": Atlantis, "阿斯嘉": Asgard, "奧林帕斯": Olympus, "瓦干達": Wakanda,
                  "香格里拉": ShangriLa, "瓦拉納西": Varanasi, "瑪雅": Maya, "塔爾塔洛斯": Tartarus,
                  "特奧蒂瓦坎": Teotihuacan, "復活節島": EasterIsland}

    return {i.name: class_list[i.name](*i) for i in read_file("國家資訊表")}


def handle_action():
    """將各國的行動單做處理，讓接下來資料處理起來比較方便"""
    info = namedtuple("info", "name produceList useCard soldCard Pwonders war solider occupyMan resource Rspeed")

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
    def production_f(times, speed):
        total = 0
        temp = 500
        for i in range(times):
            total += temp
            temp -= 25 * times
        return round(total * speed, -1)

    if countryDict[name].population - warrior < sum(produce_num) * 100:     # 人民不足生產
        times = (countryDict[name].population - warrior) // 100             # 計算本回合共能生產幾次
        for i in range(4):
            if times >= produce_num[i]:
                times -= produce_num[i]
            else:
                produce_num[i] = times
                times = 0

        print(f"{name}的人民不夠來生產")

    countryDict[name].food += production_f(produce_num[0], countryDict[name].food_speed)
    countryDict[name].wood += production_f(produce_num[1], countryDict[name].wood_speed)
    countryDict[name].steel += production_f(produce_num[2], countryDict[name].steel_speed)
    countryDict[name].stone += production_f(produce_num[3], countryDict[name].stone_speed)

    return


def read_card():
    with open("卡片.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        return {i[1]: (i[2], i[3], i[4]) for i in csv_reader}


def card(countryDict, name, cardDict, useCard, soldCard):
    """ 發動卡片效果 """

    def food1():
        try:
            countryDict[name].food -= 200
            countryDict[name].wood -= 100
            countryDict[name].steel -= 100
            countryDict[name].stone -= 100
            countryDict[name].gold -= 100
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest food1")
            return

        countryDict[name].food_speed += 0.2
        print(f"{name} has successfully invest food1")

    def food2():
        try:
            countryDict[name].food -= 500
            countryDict[name].wood -= 200
            countryDict[name].steel -= 200
            countryDict[name].stone -= 200
            countryDict[name].gold -= 500
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest food2")
            return

        print(f"{name} has successfully invest food2")
        countryDict[name].food_speed += 0.4

    def wood1():
        try:
            countryDict[name].food -= 100
            countryDict[name].wood -= 200
            countryDict[name].steel -= 100
            countryDict[name].stone -= 100
            countryDict[name].gold -= 100
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest wood1")
            return

        countryDict[name].wood_speed += 0.2
        print(f"{name} has successfully invest wood1")

    def wood2():
        try:
            countryDict[name].food -= 200
            countryDict[name].wood -= 500
            countryDict[name].steel -= 200
            countryDict[name].stone -= 200
            countryDict[name].gold -= 500
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest wood2")
            return

        countryDict[name].wood_speed += 0.4
        print(f"{name} has successfully invest wood2")

    def steel1():
        try:
            countryDict[name].food -= 100
            countryDict[name].wood -= 100
            countryDict[name].steel -= 200
            countryDict[name].stone -= 100
            countryDict[name].gold -= 100
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest steel1")
            return

        countryDict[name].steel_speed += 0.2
        print(f"{name} has successfully invest steel1")

    def steel2():
        try:
            countryDict[name].food -= 200
            countryDict[name].wood -= 200
            countryDict[name].steel -= 500
            countryDict[name].stone -= 200
            countryDict[name].gold -= 500
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest steel2")
            return

        countryDict[name].steel_speed += 0.4
        print(f"{name} has successfully invest steel2")

    def stone1():
        try:
            countryDict[name].food -= 100
            countryDict[name].wood -= 100
            countryDict[name].steel -= 100
            countryDict[name].stone -= 200
            countryDict[name].gold -= 100
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest stone1")
            return

        countryDict[name].stone_speed += 0.2
        print(f"{name} has successfully invest stone1")

    def stone2():
        try:
            countryDict[name].food -= 200
            countryDict[name].wood -= 200
            countryDict[name].steel -= 200
            countryDict[name].stone -= 500
            countryDict[name].gold -= 500
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest stone2")
            return

        countryDict[name].stone_speed += 0.4
        print(f"{name} has successfully invest stone2")

    def food_wood():
        try:
            countryDict[name].food -= 900
            countryDict[name].wood -= 900
            countryDict[name].steel -= 400
            countryDict[name].stone -= 400
            countryDict[name].gold -= 1000
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest food_wood")
            return

        countryDict[name].food_speed += 0.3
        countryDict[name].wood_speed += 0.3
        print(f"{name} has successfully invest food_wood")

    def food_steel():
        try:
            countryDict[name].food -= 900
            countryDict[name].wood -= 400
            countryDict[name].steel -= 900
            countryDict[name].stone -= 400
            countryDict[name].gold -= 1000
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest food_steel")
            return

        countryDict[name].food_speed += 0.3
        countryDict[name].steel_speed += 0.3
        print(f"{name} has successfully invest food_steel")

    def food_stone():
        try:
            countryDict[name].food -= 900
            countryDict[name].wood -= 400
            countryDict[name].steel -= 400
            countryDict[name].stone -= 900
            countryDict[name].gold -= 1000
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest food_stone")
            return

        countryDict[name].food_speed += 0.3
        countryDict[name].stone_speed += 0.3
        print(f"{name} has successfully invest food_stone")

    def wood_steel():
        try:
            countryDict[name].food -= 400
            countryDict[name].wood -= 900
            countryDict[name].steel -= 900
            countryDict[name].stone -= 400
            countryDict[name].gold -= 1000
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest wood_steel")
            return

        countryDict[name].wood_speed += 0.3
        countryDict[name].steel_speed += 0.3
        print(f"{name} has successfully invest wood_steel")

    def wood_stone():
        try:
            countryDict[name].food -= 400
            countryDict[name].wood -= 900
            countryDict[name].steel -= 400
            countryDict[name].stone -= 900
            countryDict[name].gold -= 1000
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest wood_stone")
            return

        countryDict[name].wood_speed += 0.3
        countryDict[name].stone_speed += 0.3
        print(f"{name} has successfully invest wood_stone")

    def steel_stone():
        try:
            countryDict[name].food -= 400
            countryDict[name].wood -= 400
            countryDict[name].steel -= 900
            countryDict[name].stone -= 900
            countryDict[name].gold -= 1000
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest steel_stone")
            return

        countryDict[name].steel_speed += 0.3
        countryDict[name].stone_speed += 0.3
        print(f"{name} has successfully invest steel_stone")

    def defense1():
        try:
            countryDict[name].wood -= 500
            countryDict[name].steel -= 500
            countryDict[name].gold -= 500
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest defense1")
            return

        countryDict[name].defense += 200
        print(f"{name} has successfully invest defense1")

    def defense2():
        try:
            countryDict[name].wood -= 1500
            countryDict[name].steel -= 1500
            countryDict[name].gold -= 1500
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest defense2")
            return

        countryDict[name].defense += 500
        print(f"{name} has successfully invest defense2")

    def weapon1():
        try:
            countryDict[name].wood -= 300
            countryDict[name].steel -= 500
            countryDict[name].stone -= 300
            countryDict[name].gold -= 300
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest weapon1")
            return

        countryDict[name].weapon += 0.3
        print(f"{name} has successfully invest weapon1")

    def weapon2():
        try:
            countryDict[name].wood -= 800
            countryDict[name].steel -= 1500
            countryDict[name].stone -= 800
            countryDict[name].gold -= 1500
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest weapon2")
            return

        countryDict[name].weapon += 0.5
        print(f"{name} has successfully invest weapon2")

    def all1():
        try:
            countryDict[name].food -= 3000
            countryDict[name].wood -= 1000
            countryDict[name].steel -= 1000
            countryDict[name].stone -= 1000
            countryDict[name].gold -= 2500
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest all1")
            return

        countryDict[name].food += 0.3
        countryDict[name].wood += 0.3
        countryDict[name].steel += 0.3
        countryDict[name].stone += 0.3
        print(f"{name} has successfully invest all1")

    def all2():
        try:
            countryDict[name].food -= 3000
            countryDict[name].wood -= 1000
            countryDict[name].steel -= 1000
            countryDict[name].stone -= 1000
            countryDict[name].gold -= 2500
        except ValueError as e:
            print(f"{name} dosen't have enough resource to invest all2")
            return

        countryDict[name].food += 0.2
        countryDict[name].wood += 0.2
        countryDict[name].steel += 0.2
        countryDict[name].stone += 0.2
        print(f"{name} has successfully invest all2")

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
    if attackedCountry == attackedCountry:
        print(f"{attackedCountry} can't attack herself")
        return
    rubrate = 0.001
    diff = countryDict[attackingCountry].weapon * soilder - countryDict[attackedCountry].defense
    if diff >= 0 and not defeated[attackedCountry]:
        countryDict[attackingCountry].population -= round(soilder * 0.3, -1)
        countryDict[attackedCountry].population = round(countryDict[attackedCountry].population * 0.9, -1)
        countryDict[attackingCountry].gold += round(countryDict[attackedCountry].gold * 0.5, -1)
        countryDict[attackedCountry].gold = round(0.5 * countryDict[attackedCountry].gold, -1)
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

    elif diff >= 0 and defeated[attackedCountry]:
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

    return


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

    elif state == 4:
        return

    countryDict[name].wonders += int(percentWonders)


def wonder(countryDict, wonderlist, actionlist):  # 這邊把actionlist傳進去的寫法很糟，但目前我沒想到好辦法
    currstate = {}      # [奇觀名字] : 現在階段
    totalwonder = {}    # [奇觀名字] : 準備要建造多少比例
    currwonder = {}     # [奇觀名字] : 現在有多少比例
    wonderdict = {i.name: i.Pwonders for i in actionlist}     # [國家名字] : 每國準備貢獻多少比例
    Update = {}

    for i in wonderlist:
        temp = list(i)
        Wname = temp[0]
        currstate[Wname] = int(temp[3])
        currwonder[Wname] = temp[2]
        Update[Wname] = False
        for name in temp[1].split():
            revisePwonder(countryDict, name, currstate[Wname], wonderdict)
            if Wname in totalwonder:
                totalwonder[Wname] += wonderdict[name]
            else:
                totalwonder[Wname] = wonderdict[name]

        if currwonder[Wname] + totalwonder[Wname] - currstate[Wname] * 25 > 25:
            Update[Wname] = True
            weight = (25 + currstate[Wname] * 25 - currwonder[Wname]) / totalwonder[Wname]
            for name in temp[1].split():
                wonderdict[name] = round(wonderdict[name] * weight, 0)

        for name in temp[1].split():
            buildwonder(countryDict, name, wonderdict[name], temp[3], Update[Wname])


def revisePwonder(countryDict, name, state, wonderdict):
    material = []
    if state == 0:
        material.append(countryDict[name].wood / 300)
        material.append(countryDict[name].stone / 200)
        material.append(countryDict[name].gold / 500)

        if min(material) < wonderdict[name]:
            wonderdict[name] = int(min(material))
    elif state == 1:
        material.append(countryDict[name].wood / 800)
        material.append(countryDict[name].stone / 400)
        material.append(countryDict[name].gold / 1500)

        if min(material) < wonderdict[name]:
            wonderdict[name] = int(min(material))

    elif state == 2:
        material.append(countryDict[name].wood / 1500)
        material.append(countryDict[name].stone / 800)
        material.append(countryDict[name].gold / 3000)

        if min(material) < wonderdict[name]:
            wonderdict[name] = int(min(material))

    elif state == 3:
        material.append(countryDict[name].wood / 3000)
        material.append(countryDict[name].stone / 1500)
        material.append(countryDict[name].gold / 6000)

        if min(material) < wonderdict[name]:
            wonderdict[name] = int(min(material))


if __name__ == "__main__":
    pass
