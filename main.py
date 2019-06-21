import pandas as pd
from time import time
from function import (read_file, write_country_file, createCountry, write_individual, consume, education,
                      handle_action, production, read_card, card, war, wonder, write_wonders)


if __name__ == "__main__":

    before = time()

    countryDict = createCountry()
    actionList = handle_action()
    cardDict = read_card()
    wonderlist = read_file("世界奇觀")
    produceNum = pd.read_csv("生產函數表.csv", index_col=0, encoding="ANSI")
    defeated = {'亞特蘭提斯': False, '阿斯嘉': False, '奧林帕斯': False, '瓦干達': False, '香格里拉': False,
                '瓦拉納西': False, '瑪雅': False, '塔爾塔洛斯': False, '特奧蒂瓦坎': False, '復活節島': False}

    after = time()
    print(f"讀取檔案完成，共花費{after - before:.1f}s")

    before = time()

    for i in actionList:
        production(countryDict, produceNum, i.name, i.produceList, i.occupyMan)
        if i.useCard or i.soldCard:
            card(countryDict, i.name, cardDict, i.useCard, i.soldCard, defeated)
        education(countryDict, i.name, i.education)

    del cardDict

    for i in actionList:
        if i.war[0] != "不戰爭":
            for j in range(len(i.war)):
                war(countryDict, i.name, i.war[j], i.solider[j], i.resource[j], i.Rspeed[j], defeated)
        else:
            continue

    wonder(countryDict, wonderlist, actionList)

    consume(countryDict)

    after = time()
    print(f"基本函數完成，共花費{after - before:.1f}s")

    print("開始寫檔")
    before = time()

    loop = "一"
    write_country_file(countryDict)
    write_wonders(countryDict)
    countryName = ['亞特蘭提斯', '阿斯嘉', '奧林帕斯', '瓦干達', '香格里拉',
                   '瓦拉納西', '瑪雅', '塔爾塔洛斯', '特奧蒂瓦坎', '復活節島']
    for i in countryName:
        try:
            write_individual(countryDict, i, loop, True)
        except:
            write_individual(countryDict, i, loop, True)

    after = time()
    print(f"寫檔完成，共花費{after - before:.1f}s")
