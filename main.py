import pandas as pd
from time import sleep
from function import (read_file, write_country_file, createCountry, write_individual, consume, education,
                      handle_action, production, read_card, card, war, wonder, write_wonders)


if __name__ == "__main__":
    print("開始執行程式")

    countryDict = createCountry()
    actionList, cardDict = handle_action(countryDict), read_card()
    wonderlist = read_file("世界奇觀")
    produceNum = pd.read_csv("生產函數表.csv", index_col=0, encoding="ANSI")
    countryName = ["亞特蘭提斯", "阿斯嘉", "奧林帕斯", "瓦干達", "香格里拉",
                   "瓦拉納西", "瑪雅", "塔爾塔洛斯", "特奧蒂瓦坎", "復活節島"]
    defeated, messageDict = {i: False for i in countryName}, {i: [] for i in countryName}

    print("讀取檔案完成")

    for i in actionList:
        production(countryDict, produceNum, i.name, i.produceList, i.occupyMan, messageDict)
        if i.useCard or i.soldCard:
            card(countryDict, i.name, cardDict, i.useCard, i.soldCard, defeated, messageDict)
        education(countryDict, i.name, i.education, messageDict)

    for i in actionList:
        if i.war[0] != "不戰爭":
            for j in range(len(i.war)):
                war(countryDict, i.name, i.war[j], i.soldier[j], i.resource[j], i.Rspeed[j], defeated, messageDict)

    wonder(countryDict, wonderlist, actionList, messageDict)
    consume(countryDict, messageDict)

    print("基本函數完成\n開始寫檔")

    for i, j in messageDict.items():
        print(j)

    loop = "二"
    try:
        write_country_file(countryDict)
        write_wonders(countryDict)
    except:
        print(f"Google API存取過度，暫停存取100s再繼續")
        sleep(100)
        write_country_file(countryDict)
        write_wonders(countryDict)

    for i in countryName:
        try:
            write_individual(countryDict, i, loop)
        except:
            print(f"Google API存取過度，暫停存取100s再繼續")
            sleep(100)
            write_individual(countryDict, i, loop)

    print("寫檔完成")
