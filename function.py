import csv
import gspread
from random import randint
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
    action = namedtuple("action", "time name Pfood Pwood Psteel Pstone useCard soldCard education war soldier resource Rspeed Pwonders")

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
        roundnow = "零"
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


def createCountry():
    """透過read_file函數建立Class，回傳儲存各國Class的dictionary"""

    class_list = {"亞特蘭提斯": Atlantis, "阿斯嘉": Asgard, "奧林帕斯": Olympus, "瓦干達": Wakanda,
                  "香格里拉": ShangriLa, "瓦拉納西": Varanasi, "瑪雅": Maya, "塔爾塔洛斯": Tartarus,
                  "特奧蒂瓦坎": Teotihuacan, "復活節島": EasterIsland}

    return {i.name: class_list[i.name](*i) for i in read_file("國家資訊表")}


def handle_action(countryDict):
    """ 將各國的行動單做處理，讓接下來資料處理起來比較方便 """
    info = namedtuple("info", "name produceList useCard soldCard education war soldier occupyMan resource Rspeed Pwonders")

    returnList = []
    for i in read_file("伊康攻略回應表 (回應)"):
        if "不戰爭" in i.war.replace(",", "").split():                             # 如果選擇了"不戰爭"，那麼無論有沒有想攻打其他國家，這回合都無法戰爭
            war, occupyMan, soldier, resource, Rspeed = ["不戰爭"], 0, [], [], []
        else:                                                                     # 先處理看看資訊再檢查看看有沒有問題
            war = i.war.replace(",", "").split()                                  # 先把資訊存放好然後開始檢查
            soldier = [int(j) for j in str(i.soldier).split()]
            resource, Rspeed = i.resource.split(), i.Rspeed.split()
            occupyMan = sum(soldier)

            if (len(war) != len(soldier)) or (len(war) != len(resource)) or (len(war) != len(Rspeed)):  # 如果表單填錯的話，就會出現error
                raise IndexError(f"{i.name}戰爭國家和資料對不齊")

            elif countryDict[i.name].population < occupyMan:                      # 如果派出去戰爭的人數比人口總數的話，此回合就無法戰爭
                war, occupyMan, soldier, resource, Rspeed = ["不戰爭"], 0, [], [], []
                print(f"{i.name}所派出去戰爭的人大於所有人民，因此此回合無法戰爭")

        tempt = info(i.name, [i.Pfood, i.Pwood, i.Psteel, i.Pstone], str(i.useCard).split(),
                     str(i.soldCard).split(), i.education, war, soldier, occupyMan, resource, Rspeed, i.Pwonders)
        returnList.append(tempt)

    return returnList


def production(countryDict, produceData, name, produce_num, warrior, messageDict):
    """ 生產順序:糧食、木頭、鐵礦、石頭 """

    if countryDict[name].population <= warrior:              # 如果打仗人數超過人口上限，因為全民皆兵，本次生產作廢
        messageDict[name].append(f"{name}的人民都去當兵了，無法從事生產")
        return

    if countryDict[name].population - warrior < sum(produce_num) * 100:     # 人民不足生產
        times = (countryDict[name].population - warrior) // 100             # 計算本回合共能生產幾次
        for i in range(4):                                                  # 對每一項物資
            if times >= produce_num[i]:                                     # 讓預期生產次數和實際上剩餘生產次數比較
                times -= produce_num[i]
            else:
                produce_num[i] = times                                      # 如果已經無法生產，則讓實際生產次數歸0
                times = 0

        messageDict[name].append(f"{name}的人民不夠來生產, 改為生產:{produce_num[0]}次糧食, {produce_num[1]}次木頭, {produce_num[2]}次鐵礦, {produce_num[3]}次石頭")

    else:
        messageDict[name].append(f"{name}生產:{produce_num[0]}次糧食, {produce_num[1]}次木頭, {produce_num[2]}次鐵礦, {produce_num[3]}次石頭")

    # 先選取生產次數再對生產倍率
    # dict(produceData[生產次數]): 回傳後的東西轉成dictionary:{1: 550, 1.1: 610...}
    # 接著利用[float(countryDict[name].food_speed)]去對生產總額為何
    food = dict(produceData[str(produce_num[0])])[float(countryDict[name].food_speed)]
    wood = dict(produceData[str(produce_num[1])])[float(countryDict[name].wood_speed)]
    steel = dict(produceData[str(produce_num[2])])[float(countryDict[name].steel_speed)]
    stone = dict(produceData[str(produce_num[3])])[float(countryDict[name].stone_speed)]

    # 依序執行食物、木頭、鐵礦、石頭的生產
    countryDict[name].food += int(food)
    countryDict[name].wood += int(wood)
    countryDict[name].steel += int(steel)
    countryDict[name].stone += int(stone)

    messageDict[name].append(f"{name}總計生產了{food}糧食,{wood}木頭,{steel}鐵礦,{stone}石頭")  # 顯示該國生產量

    return


def read_card():
    # 讀取卡片.csv
    with open("卡片.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        return {i[1]: (i[2], i[3], i[4]) for i in csv_reader}


def card(countryDict, name, cardDict, useCard, soldCard, defeated, messageDict):
    def food1():
        if (countryDict[name].food >= 600 and countryDict[name].wood >= 200 and countryDict[name].steel >= 200 and
                countryDict[name].stone >= 200 and countryDict[name].gold >= 400):
            countryDict[name].food -= 600
            countryDict[name].wood -= 200
            countryDict[name].steel -= 200
            countryDict[name].stone -= 200
            countryDict[name].gold -= 400
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資綠色革命")
            return

        countryDict[name].food_speed += 0.4
        messageDict[name].append(f"{name}已經成功投資綠色革命")

    def food2():
        if (countryDict[name].food >= 1000 and countryDict[name].wood >= 400 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 600):
            countryDict[name].food -= 1000
            countryDict[name].wood -= 400
            countryDict[name].steel -= 400
            countryDict[name].stone -= 400
            countryDict[name].gold -= 600
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資神農氏萬歲")
            return

        countryDict[name].food_speed += 0.8
        messageDict[name].append(f"{name}已經成功投資神農氏萬歲")

    def food3():
        countryDict[name].food *= 1.5
        messageDict[name].append(f"{name}已經成功投資糧食酒")

    def wood1():
        if (countryDict[name].food >= 200 and countryDict[name].wood >= 600 and countryDict[name].steel >= 200 and
                countryDict[name].stone >= 200 and countryDict[name].gold >= 400):
            countryDict[name].food -= 200
            countryDict[name].wood -= 600
            countryDict[name].steel -= 200
            countryDict[name].stone -= 200
            countryDict[name].gold -= 400
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資天降黑森林")
            return

        countryDict[name].wood_speed += 0.4
        messageDict[name].append(f"{name}已經成功投資天降黑森林")

    def wood2():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 1000 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 600):
            countryDict[name].food -= 400
            countryDict[name].wood -= 1000
            countryDict[name].steel -= 400
            countryDict[name].stone -= 400
            countryDict[name].gold -= 600
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資人造林")
            return

        countryDict[name].wood_speed += 0.8
        messageDict[name].append(f"{name}已經成功投資人造林")

    def wood3():
        countryDict[name].wood *= 1.5
        messageDict[name].append(f"{name}已經成功投資榆木椅")

    def steel1():
        if (countryDict[name].food >= 200 and countryDict[name].wood >= 200 and countryDict[name].steel >= 600 and
                countryDict[name].stone >= 200 and countryDict[name].gold >= 400):
            countryDict[name].food -= 200
            countryDict[name].wood -= 200
            countryDict[name].steel -= 600
            countryDict[name].stone -= 200
            countryDict[name].gold -= 400
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資挖礦機器人")
            return

        countryDict[name].steel_speed += 0.4
        messageDict[name].append(f"{name}已經成功投資挖礦機器人")

    def steel2():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 400 and countryDict[name].steel >= 1000 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 600):
            countryDict[name].food -= 400
            countryDict[name].wood -= 400
            countryDict[name].steel -= 1000
            countryDict[name].stone -= 400
            countryDict[name].gold -= 600
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資華鐵爐")
            return

        countryDict[name].steel_speed += 0.8
        messageDict[name].append(f"{name}已經成功投資華鐵爐")

    def steel3():
        countryDict[name].steel *= 1.5
        messageDict[name].append(f"{name}已經成功投資熔爐")

    def stone1():
        if (countryDict[name].food >= 200 and countryDict[name].wood >= 200 and countryDict[name].steel >= 200 and
                countryDict[name].stone >= 600 and countryDict[name].gold >= 400):
            countryDict[name].food -= 200
            countryDict[name].wood -= 200
            countryDict[name].steel -= 200
            countryDict[name].stone -= 600
            countryDict[name].gold -= 400
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資找到烏魯魯")
            return

        countryDict[name].stone_speed += 0.4
        messageDict[name].append(f"{name}已經成功投資找到烏魯魯")

    def stone2():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 400 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 1000 and countryDict[name].gold >= 600):
            countryDict[name].food -= 400
            countryDict[name].wood -= 400
            countryDict[name].steel -= 400
            countryDict[name].stone -= 1000
            countryDict[name].gold -= 600
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資愚公移山")
            return

        countryDict[name].stone_speed += 0.8
        messageDict[name].append(f"{name}已經成功投資愚公移山")

    def stone3():
        countryDict[name].stone *= 1.5
        messageDict[name].append(f"{name}已經成功投資留遷石")

    def food_wood():
        if (countryDict[name].food >= 800 and countryDict[name].wood >= 800 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 800
            countryDict[name].wood -= 800
            countryDict[name].steel -= 400
            countryDict[name].stone -= 400
            countryDict[name].gold -= 1200
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資免洗餐具")
            return

        countryDict[name].food_speed += 0.5
        countryDict[name].wood_speed += 0.5
        messageDict[name].append(f"{name}已經成功投資免洗餐具")

    def food_steel():
        if (countryDict[name].food >= 800 and countryDict[name].wood >= 400 and countryDict[name].steel >= 800 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 800
            countryDict[name].wood -= 400
            countryDict[name].steel -= 800
            countryDict[name].stone -= 400
            countryDict[name].gold -= 1200
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資菠菜罐頭")
            return

        countryDict[name].food_speed += 0.5
        countryDict[name].steel_speed += 0.5
        messageDict[name].append(f"{name}已經成功投資菠菜罐頭")

    def food_stone():
        if (countryDict[name].food >= 800 and countryDict[name].wood >= 400 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 800 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 800
            countryDict[name].wood -= 400
            countryDict[name].steel -= 400
            countryDict[name].stone -= 800
            countryDict[name].gold -= 1200
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資石板烤肉")
            return

        countryDict[name].food_speed += 0.5
        countryDict[name].stone_speed += 0.5
        messageDict[name].append(f"{name}已經成功投資石板烤肉")

    def wood_steel():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 800 and countryDict[name].steel >= 800 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 400
            countryDict[name].wood -= 800
            countryDict[name].steel -= 800
            countryDict[name].stone -= 400
            countryDict[name].gold -= 1200
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資金斧頭銀斧頭")
            return

        countryDict[name].wood_speed += 0.5
        countryDict[name].steel_speed += 0.5
        messageDict[name].append(f"{name}已經成功投資金斧頭銀斧頭")

    def wood_stone():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 800 and countryDict[name].steel >= 400 and
                countryDict[name].stone >= 800 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 400
            countryDict[name].wood -= 800
            countryDict[name].steel -= 400
            countryDict[name].stone -= 800
            countryDict[name].gold -= 1200
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資原始人")
            return

        countryDict[name].wood_speed += 0.5
        countryDict[name].stone_speed += 0.5
        messageDict[name].append(f"{name}已經成功投資原始人")

    def steel_stone():
        if (countryDict[name].food >= 400 and countryDict[name].wood >= 400 and countryDict[name].steel >= 800 and
                countryDict[name].stone >= 800 and countryDict[name].gold >= 1200):
            countryDict[name].food -= 400
            countryDict[name].wood -= 400
            countryDict[name].steel -= 800
            countryDict[name].stone -= 800
            countryDict[name].gold -= 1200
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資鏗鏘鏗鏘")
            return

        countryDict[name].steel_speed += 0.5
        countryDict[name].stone_speed += 0.5
        messageDict[name].append(f"{name}已經成功投資鏗鏘鏗鏘")

    def defense1():
        if countryDict[name].wood >= 500 and countryDict[name].steel >= 500 and countryDict[name].gold >= 500:
            countryDict[name].wood -= 500
            countryDict[name].steel -= 500
            countryDict[name].gold -= 500
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資自強運動")
            return

        countryDict[name].defense += 100
        messageDict[name].append(f"{name}已經成功投資自強運動")

    def defense2():
        if countryDict[name].wood >= 1000 and countryDict[name].steel >= 1000 and countryDict[name].gold >= 1000:
            countryDict[name].wood -= 1000
            countryDict[name].steel -= 1000
            countryDict[name].gold -= 1000
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資埃癸斯")
            return

        countryDict[name].defense += 300
        messageDict[name].append(f"{name}已經成功投資埃癸斯")

    def defense3():
        if countryDict[name].wood >= 1500 and countryDict[name].steel >= 1500 and countryDict[name].gold >= 1500:
            countryDict[name].wood -= 1500
            countryDict[name].steel -= 1500
            countryDict[name].gold -= 1500
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資葵花寶典")
            return

        countryDict[name].defense += 500
        messageDict[name].append(f"{name}已經成功投資葵花寶典")

    def weapon1():
        if (countryDict[name].wood >= 300 and countryDict[name].steel >= 500 and
                countryDict[name].stone >= 300 and countryDict[name].gold >= 300):
            countryDict[name].wood -= 300
            countryDict[name].steel -= 500
            countryDict[name].stone -= 300
            countryDict[name].gold -= 300
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資曼哈頓計畫")
            return

        countryDict[name].weapon += 0.2
        messageDict[name].append(f"{name}已經成功投資曼哈頓計畫")

    def weapon2():
        if (countryDict[name].wood >= 550 and countryDict[name].steel >= 1000 and
                countryDict[name].stone >= 550 and countryDict[name].gold >= 900):
            countryDict[name].wood -= 550
            countryDict[name].steel -= 1000
            countryDict[name].stone -= 550
            countryDict[name].gold -= 900
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資甲不離人")
            return

        countryDict[name].weapon += 0.4
        messageDict[name].append(f"{name}已經成功投資甲不離人")

    def weapon3():
        if (countryDict[name].wood >= 800 and countryDict[name].steel >= 1500 and
                countryDict[name].stone >= 800 and countryDict[name].gold >= 1500):
            countryDict[name].wood -= 800
            countryDict[name].steel -= 1500
            countryDict[name].stone -= 800
            countryDict[name].gold -= 1500
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資石中劍")
            return

        countryDict[name].weapon += 0.6
        messageDict[name].append(f"{name}已經成功投資石中劍")

    def war1():
        if (countryDict[name].wood >= 600 and countryDict[name].steel >= 1000 and
                countryDict[name].stone >= 400 and countryDict[name].gold >= 1000):
            countryDict[name].wood -= 600
            countryDict[name].steel -= 1000
            countryDict[name].stone -= 400
            countryDict[name].gold -= 1000
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資劍盾在身")
            return

        countryDict[name].weapon += 0.3
        countryDict[name].defense += 150
        messageDict[name].append(f"{name}已經成功投資劍盾在身")

    def war2():                                                            # 石中劍
        if (countryDict[name].wood >= 2000 and countryDict[name].steel >= 2500 and
                countryDict[name].stone >= 600 and countryDict[name].gold >= 2500):
            countryDict[name].wood -= 2000
            countryDict[name].steel -= 2500
            countryDict[name].stone -= 600
            countryDict[name].gold -= 2500
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資上下其手")
            return

        countryDict[name].weapon += 0.5
        countryDict[name].defense += 450
        messageDict[name].append(f"{name}已經成功投資上下其手")

    def all1():                                                            # 蟹堡秘方
        if (countryDict[name].food >= 1200 and countryDict[name].wood >= 600 and countryDict[name].steel >= 600 and
                countryDict[name].stone >= 600 and countryDict[name].gold >= 2500):
            countryDict[name].food -= 1200
            countryDict[name].wood -= 600
            countryDict[name].steel -= 600
            countryDict[name].stone -= 600
            countryDict[name].gold -= 2500
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資蟹堡秘方")
            return

        countryDict[name].food_speed += 0.5
        countryDict[name].wood_speed += 0.3
        countryDict[name].steel_speed += 0.3
        countryDict[name].stone_speed += 0.3
        messageDict[name].append(f"{name}已經成功投資蟹堡秘方")

    def all2():                                                            # 國富論
        if (countryDict[name].food >= 600 and countryDict[name].wood >= 700 and countryDict[name].steel >= 600 and
                countryDict[name].stone >= 800 and countryDict[name].gold >= 2000):
            countryDict[name].food -= 600
            countryDict[name].wood -= 700
            countryDict[name].steel -= 600
            countryDict[name].stone -= 800
            countryDict[name].gold -= 2000
        else:
            messageDict[name].append(f"{name}沒有足夠的資源投資國富論")
            return

        countryDict[name].food_speed += 0.3
        countryDict[name].wood_speed += 0.3
        countryDict[name].steel_speed += 0.3
        countryDict[name].stone_speed += 0.3
        messageDict[name].append(f"{name}已經成功投資國富論")

    def gold1():
        countryDict[name].gold *= 1.5
        messageDict[name].append(f"{name}已經成功投資發小財")

    def gold2():
        countryDict[name].gold *= 2
        messageDict[name].append(f"{name}已經成功投資發大財")

    def human1():
        countryDict[name].population += 100
        messageDict[name].append(f"{name}已經成功投資轉小人")

    def human2():
        countryDict[name].population += 200
        messageDict[name].append(f"{name}已經成功投資做中人")

    def human3():
        countryDict[name].population += 300
        messageDict[name].append(f"{name}已經成功投資登大人")

    def special1():
        countryDict[name].gold += 100000
        messageDict[name].append(f"{name}已經成功使用海神王的王冠，效果為黃金+100000")

    def special2():
        defeated[name] = "Cannot attack"
        messageDict[name].append(f"{name}已經成功使用隱形斗篷，效果為這回合進攻你的國家行動無效")

    def special3():
        countryDict[name].weapon *= 2
        messageDict[name].append(f"{name}已經成功使用誓約勝利之劍，效果武器倍率+2")
        print(f"回合結束記得改{name}的武器倍率")

    def special4():
        randnum = randint(0, 3)
        if randnum:
            messageDict[name].append(f"{name}執行雷神之鎚失敗")
        else:
            countryDict[name].defense += 2000
            messageDict[name].append(f"{name}已經成功使用雷神之鎚，效果為防禦力+2000")

    def special5():
        countryDict[name].food *= 0.5
        messageDict[name].append(f"{name}已經成功使用南北菜蟲一起串連，效果為糧食減少一半")

    def special6():
        try:
            countryDict[name].population -= 500
            countryDict[name].food_speed += 0.5
            countryDict[name].wood_speed += 0.5
            countryDict[name].steel_speed += 0.5
            countryDict[name].stone_speed += 0.5
            messageDict[name].append(f"{name}已經成功使用富士康，效果為犧牲500人民，換取全部生產效率+0.5")

        except ValueError:
            messageDict[name].append(f"{name}無法使用富士康")

    def special7():
        try:
            countryDict[name].gold -= 1000
            countryDict[name].defense += 1500
            messageDict[name].append(f"{name}已經成功使用墨西哥圍牆，效果為付出1000黃金換取1500防禦力")

        except ValueError:
            messageDict[name].append(f"{name}無法使用墨西哥圍牆")

    def special8():
        messageDict[name].append(f"{name}已經成功使用慈姑觀音")

    def special9():
        countryDict[name].population += 800
        messageDict[name].append(f"{name}已經成功使用愛情摩天輪，效果為人口+800")

    def special10():
        countryDict[name].gold = 0
        countryDict[name].population *= 3
        messageDict[name].append(f"{name}已經成功使用人多好辦事，效果為黃金歸0，人口增加為3倍")

    def nothing():
        return

    for card in soldCard:
        try:
            if cardDict[card][1] == "Y":
                messageDict[name].append(f"這張卡片已經使用過了")
            else:
                messageDict[name].append(f"{name}對{cardDict[card][0]}販賣成功")
                countryDict[name].gold += int(cardDict[card][2])

        except KeyError:
            raise KeyError(f"卡片驗證碼:{card}不存在")

    for card in useCard:
        try:
            if cardDict[card][1] == "Y":
                messageDict[name].append(f"這張卡片已經使用過了")
            else:
                locals()[cardDict[card][0]]()

        except KeyError:
            raise KeyError(f"卡片驗證碼:{card}不存在")


def education(countryDict, name, invest, messageDict):
    if invest == "是":                                                               # 如果本回合選擇投資教育
        if countryDict[name].education == 0:                                         # 如果等級是0而且有3000糧食，則升級成功
            if countryDict[name].food >= 3000:
                countryDict[name].food -= 3000
                countryDict[name].education = 1
                messageDict[name].append(f"{name}已經成功投資教育LV.1")
                return

            else:
                messageDict[name].append(f"{name}沒有足夠的糧食投資教育LV.1，因為你的食物只有{countryDict[name].food} < 3000")
                return

        elif countryDict[name].education == 1:                                         # 如果等級是1而且有5000糧食，則升級成功
            if countryDict[name].food >= 6000:
                countryDict[name].food -= 6000
                countryDict[name].education = 2
                messageDict[name].append(f"{name}已經成功投資教育LV.2")
                return

            else:
                messageDict[name].append(f"{name}沒有足夠的糧食投資教育LV.2，因為你的食物只有{countryDict[name].food} < 6000")
                return

        elif countryDict[name].education == 2:                                         # 如果等級是2而且有9000糧食，則升級成功
            if countryDict[name].food >= 12000:
                countryDict[name].food -= 12000
                countryDict[name].education = 3
                messageDict[name].append(f"{name}已經成功投資教育LV.3")
                return

            else:
                messageDict[name].append(f"{name}沒有足夠的糧食投資教育LV.3，因為你的食物只有{countryDict[name].food} < 12000")
                return

        else:                                                                           # 如果等級是3，則無法繼續投資
            messageDict[name].append(f"{name}的教育已經滿級，不能再投資了")
            return

    else:
        return


def war(countryDict, attackingCountry, attackedCountry, soldier, resource, speed, defeated, messageDict):
    if attackingCountry == attackedCountry:                             # 如果攻打國和被攻打國屬於同一個國家，則攻擊無效
        messageDict[attackingCountry].append(f"{attackingCountry}無法攻擊自己")
        return

    elif defeated[attackedCountry] == "Cannot attack":                  # 如果該國家無法被攻擊，則攻擊無效
        messageDict[attackingCountry].append(f"{attackedCountry}發動特殊效果，無法被攻擊")
        return

    rubrate = 0.001                                                     # 搶奪比率為0.001
    diff = countryDict[attackingCountry].weapon * soldier - countryDict[attackedCountry].defense    # 勝負的判定為，A國武器倍率 * 士兵 vs B國防禦力
    if diff >= 0 and not defeated[attackedCountry]:                                                 # 如果A國戰勝而且B國之前沒有戰敗過
        rubgold = countryDict[attackedCountry].gold * 0.5
        countryDict[attackingCountry].population -= soldier * 0.7                                   # A國損失七成士兵
        countryDict[attackedCountry].population *= 0.9                                              # B國損失一成人口
        countryDict[attackingCountry].gold += countryDict[attackedCountry].gold * 0.5               # A國盜取B國一半黃金
        countryDict[attackedCountry].gold *= 0.5                                                    # B國損失一半黃金
        defeated[attackedCountry] = True                                                            # B國戰敗的布林值改為True

        if resource == "糧食":
            try:
                rubresource = countryDict[attackedCountry].food * (0.5 + rubrate * diff)
                countryDict[attackingCountry].food += countryDict[attackedCountry].food * (0.5 + rubrate * diff)
                countryDict[attackedCountry].food -= countryDict[attackedCountry].food * (0.5 + rubrate * diff)
            except ValueError:
                rubresource = countryDict[attackedCountry].food
                countryDict[attackingCountry].food += countryDict[attackedCountry].food
                countryDict[attackedCountry].food = 0
        elif resource == "木頭":
            try:
                rubresource = countryDict[attackedCountry].wood * (0.5 + rubrate * diff)
                countryDict[attackingCountry].wood += countryDict[attackedCountry].wood * (0.5 + rubrate * diff)
                countryDict[attackedCountry].wood -= countryDict[attackedCountry].wood * (0.5 + rubrate * diff)
            except ValueError:
                rubresource = countryDict[attackedCountry].wood
                countryDict[attackingCountry].wood += countryDict[attackedCountry].wood
                countryDict[attackedCountry].wood = 0
        elif resource == "鐵礦":
            try:
                rubresource = countryDict[attackedCountry].steel * (0.5 + rubrate * diff)
                countryDict[attackingCountry].steel += countryDict[attackedCountry].steel * (0.5 + rubrate * diff)
                countryDict[attackedCountry].steel -= countryDict[attackedCountry].steel * (0.5 + rubrate * diff)
            except ValueError:
                rubresource = countryDict[attackedCountry].steel
                countryDict[attackingCountry].steel += countryDict[attackedCountry].steel
                countryDict[attackedCountry].steel = 0
        elif resource == "石頭":
            try:
                rubresource = countryDict[attackedCountry].stone * (0.5 + rubrate * diff)
                countryDict[attackingCountry].stone += countryDict[attackedCountry].stone * (0.5 + rubrate * diff)
                countryDict[attackedCountry].stone -= countryDict[attackedCountry].stone * (0.5 + rubrate * diff)
            except ValueError:
                rubresource = countryDict[attackedCountry].stone
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

        messageDict[attackingCountry].append(f"{attackingCountry}戰勝了{attackedCountry}，掠奪了{rubgold}黃金{rubresource}{resource}和{speed}倍率, 戰力差為{diff}")            # A國搶奪B國一半加上0.001 * 戰力差的資源
        messageDict[attackedCountry].append(f"{attackedCountry}被{attackingCountry}攻擊並戰敗了，被掠奪了{rubgold}黃金{rubresource}{resource}和{speed}倍率, 戰力差為{diff}")

    elif diff >= 0 and defeated[attackedCountry]:                                                       # 如果A國打贏B國，且B國曾經被打敗過
        rubgold = countryDict[attackedCountry].gold * 0.5
        countryDict[attackingCountry].population -= soldier * 0.1                                       # A國損失一成士兵
        countryDict[attackingCountry].gold += countryDict[attackedCountry].gold * 0.5                   # A國搶奪B國一半黃金
        countryDict[attackedCountry].gold *= 0.5

        if resource == "糧食":                                                                            # A國搶奪B國一半的物資和戰力差 * 0.001
            try:
                rubresource = countryDict[attackedCountry].food * (0.5 + rubrate * diff)
                countryDict[attackingCountry].food += 0.5 * countryDict[attackedCountry].food * (0.5 + rubrate * diff)
                countryDict[attackedCountry].food -= 0.5 * countryDict[attackedCountry].food * (0.5 + rubrate * diff)
            except ValueError:
                rubresource = countryDict[attackedCountry].food
                countryDict[attackingCountry].food += countryDict[attackedCountry].food
                countryDict[attackedCountry].food = 0
        elif resource == "木頭":
            try:
                rubresource = countryDict[attackedCountry].wood * (0.5 + rubrate * diff)
                countryDict[attackingCountry].wood += 0.5 * countryDict[attackedCountry].wood * (0.5 + rubrate * diff)
                countryDict[attackedCountry].wood -= 0.5 * countryDict[attackedCountry].wood * (0.5 + rubrate * diff)
            except ValueError:
                rubresource = countryDict[attackedCountry].wood
                countryDict[attackingCountry].wood += countryDict[attackedCountry].wood
                countryDict[attackedCountry].wood = 0
        elif resource == "鐵礦":
            try:
                rubresource = countryDict[attackedCountry].steel * (0.5 + rubrate * diff)
                countryDict[attackingCountry].steel += 0.5 * countryDict[attackedCountry].steel * (0.5 + rubrate * diff)
                countryDict[attackedCountry].steel -= 0.5 * countryDict[attackedCountry].steel * (0.5 + rubrate * diff)
            except ValueError:
                rubresource = countryDict[attackedCountry].steel
                countryDict[attackingCountry].steel += countryDict[attackedCountry].steel
                countryDict[attackedCountry].steel = 0
        elif resource == "石頭":
            try:
                rubresource = countryDict[attackedCountry].stone * (0.5 + rubrate * diff)
                countryDict[attackingCountry].stone += 0.5 * countryDict[attackedCountry].stone * (0.5 + rubrate * diff)
                countryDict[attackedCountry].stone -= 0.5 * countryDict[attackedCountry].stone * (0.5 + rubrate * diff)
            except ValueError:
                rubresource = countryDict[attackedCountry].stone
                countryDict[attackingCountry].stone += countryDict[attackedCountry].stone
                countryDict[attackedCountry].stone = 0

        messageDict[attackingCountry].append(f"{attackingCountry}戰勝了{attackedCountry}，掠奪了{rubgold}黃金和{rubresource}{resource}，因{attackedCountry}已經被打過了，因此無法掠奪倍率, 戰力差為{diff}")
        messageDict[attackedCountry].append(f"{attackedCountry}被{attackingCountry}攻擊並戰敗了，因為之前已經戰敗過，因此只被掠奪{rubgold}黃金和{rubresource}{resource}, 戰力差為{diff}")

    elif diff < 0:                                                  # 如果B國防守成功， A國損失四成士兵
        countryDict[attackingCountry].population -= soldier * 0.4
        messageDict[attackingCountry].append(f"{attackingCountry}進攻了{attackedCountry}但失敗了，損失四成士兵")
        messageDict[attackedCountry].append(f"{attackedCountry}被{attackingCountry}攻擊但失敗了")

    return


def buildwonder(countryDict, name, Wname, percentWonders, state, Update, bundle, messageDict):
    # 建造奇蹟的函數
    package = bundle[Wname][state]                                  # 選擇本次建造組合
    # package = [糧食, 木頭, 鐵礦, 石頭]

    countryDict[name].wood -= package[0] * percentWonders           # 建造奇觀成本 = 該階段成本 * 次數
    countryDict[name].steel -= package[1] * percentWonders
    countryDict[name].stone -= package[2] * percentWonders
    countryDict[name].gold -= package[3] * percentWonders

    if Update:
        messageDict[name].append(f"{name}成功得到第{state}階段升級效果")
        if state == 0:                                              # 第一階段完成的獎勵
            countryDict[name].weapon += 1
            countryDict[name].defense += 500

        elif state == 1:                                            # 第二階段完成的獎勵
            countryDict[name].food_speed += 1
            countryDict[name].wood_speed += 1
            countryDict[name].steel_speed += 1
            countryDict[name].stone_speed += 1
            countryDict[name].population += 1000

        elif state == 2:                                            # 第三階段完成的獎勵
            countryDict[name].weapon += 2
            countryDict[name].defense += 1000
            countryDict[name].food_speed += 1
            countryDict[name].wood_speed += 1
            countryDict[name].steel_speed += 1
            countryDict[name].stone_speed += 1

        elif state == 3:                                            # 第四階段完成的獎勵
            createCountry[name].population += 5000

    if state == 4:                                                  # 如果達到第四階段，則不再升級
        messageDict[name].append(f"{Wname}已經達到最高級了")
        return

    rwood, rsteel, rstone, rgold = [i * percentWonders for i in package]
    countryDict[name].wonders += int(percentWonders)
    messageDict[name].append(f"{name} 貢獻了 {percentWonders}% 給{Wname}, 耗費了{rwood}木頭, {rsteel}鐵礦, {rstone}石頭, {rgold}黃金")


def wonder(countryDict, wonderlist, actionlist, messageDict):
    bundle = {}                                                 # 物資依序為[木頭, 鐵礦, 石頭, 黃金]
    bundle["經思闕"] = [[300, 200, 200, 500], [800, 300, 400, 1500], [1500, 1000, 800, 2500], [2500, 1500, 1800, 3500]]
    bundle["亡星陵"] = [[300, 200, 200, 500], [500, 700, 300, 1500], [1200, 900, 1200, 2500], [1400, 2000, 2400, 3500]]
    bundle["釗晁榭"] = [[300, 200, 200, 500], [700, 400, 400, 1500], [900, 1000, 1400, 2500], [2200, 2000, 1600, 3500]]
    bundle["橡彶軒"] = [[300, 200, 200, 500], [350, 800, 350, 1500], [800, 1000, 1500, 2500], [1800, 2500, 1500, 3500]]
    bundle["噱町閣"] = [[300, 200, 200, 500], [400, 350, 750, 1500], [1000, 1300, 1000, 2500], [1800, 2200, 1800, 3500]]
    currstate = {}                                              # [奇觀名字] : 現在階段
    totalwonder = {}                                            # [奇觀名字] : 準備要建造多少比例
    currwonder = {}                                             # [奇觀名字] : 現在有多少比例
    wonderdict = {i.name: i.Pwonders for i in actionlist}       # [國家名字] : 每國準備貢獻多少比例

    countryName = ['亞特蘭提斯', '阿斯嘉', '奧林帕斯', '瓦干達', '香格里拉',
                   '瓦拉納西', '瑪雅', '塔爾塔洛斯', '特奧蒂瓦坎', '復活節島']
    for i in countryName:
        if i in wonderdict:
            pass
        else:
            wonderdict[i] = 0

    Update = {}

    for i in wonderlist:                                        # 對於每個奇觀
        temp = list(i)
        Wname = temp[0]                                         # Wname 為奇觀名字
        currstate[Wname] = int(temp[3])                         # 目前階段
        currwonder[Wname] = temp[2]                             # 目前進度
        Update[Wname] = False
        for name in temp[1].split():                            # 對每一個國家
            revisePwonder(countryDict, name, Wname, currstate[Wname], wonderdict, bundle, messageDict)  # 確認物資是否足夠投資
            if Wname in totalwonder:
                totalwonder[Wname] += wonderdict[name]
            else:
                totalwonder[Wname] = wonderdict[name]

        if currwonder[Wname] + totalwonder[Wname] - currstate[Wname] * 25 >= 25:            # 確認是否晉級
            rest = (currstate[Wname] + 1) * 25 - currwonder[Wname]
            country = temp[1].split()
            Update[Wname] = True
            messageDict[name].append(f"{Wname} 達到了第{currstate[Wname] + 1}階段，所有在這奇觀下的國家都獲得加成")
            weight = (25 + currstate[Wname] * 25 - currwonder[Wname]) / totalwonder[Wname]  # 計算線性權重
            for name in country:                                                            # 重寫每個國家的投資數量
                wonderdict[name] = int(wonderdict[name] * weight)
                rest -= wonderdict[name]
            if rest != 0:
                if randint(0, 1) == 0:
                    wonderdict[country[0]] += 1
                    messageDict[country[0]].append(f"進入世界奇觀隨機分配過程，由{country[0]}獲得最後一單位")
                    messageDict[country[1]].append(f"進入世界奇觀隨機分配過程，由{country[0]}獲得最後一單位")
                else:
                    wonderdict[country[1]] += 1
                    messageDict[country[0]].append(f"進入世界奇觀隨機分配過程，由{country[1]}獲得最後一單位")
                    messageDict[country[1]].append(f"進入世界奇觀隨機分配過程，由{country[1]}獲得最後一單位")

        for name in temp[1].split():                                                        # 蓋奇觀
            buildwonder(countryDict, name, Wname, wonderdict[name], temp[3], Update[Wname], bundle, messageDict)


def revisePwonder(countryDict, name, Wname, state, wonderdict, bundle, messageDict):
    package = bundle[Wname][state]                              # 選擇本次建造組合
    material = []

    material.append(countryDict[name].wood // package[0])        # 確認最大可能生產次數
    material.append(countryDict[name].steel // package[1])
    material.append(countryDict[name].stone // package[2])
    material.append(countryDict[name].gold // package[3])

    if min(material) < wonderdict[name]:                        # 如果欲建造次數超過能力上限，則讓欲建造次數等同能力上限
        messageDict[name].append(f"{name}沒有足夠多的資源投資{Wname}{wonderdict[name]}%，只能投資{int(min(material))}%")
        wonderdict[name] = min(material)


def consume(countryDict, messageDict):
    for i in countryDict.values():                              # 對於每一個國家
        try:
            i.food -= i.population + 500                        # 消耗 人民 + 500 糧食
            i.population += 100                                 # 再增加100人口
            messageDict[i.name].append(f"{i.name}耗費了{i.population + 500}糧食，增加100人口")
        except ValueError:                                      # 如果糧食耗盡
            i.food = 0                                          # 讓該國糧食耗盡
            i.population -= 100                                 # 人口減100
            messageDict[i.name].append(f"{i.name}有{i.population}人民，但糧食不夠，餓死了100人")


if __name__ == "__main__":
    initialize()
