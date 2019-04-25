from function import (read_file, write_country_file, write_individual, createCountry,
                      handle_action, production, read_card, card, war, wonder)
from random import shuffle


if __name__ == "__main__":
    countryDict = createCountry()
    actionList = handle_action()
    cardDict = read_card()
    wonderlist = read_file("世界奇觀")

    for i in actionList:
        production(countryDict, i.name, i.produceList, i.occupyMan)
        if i.useCard or i.soldCard:
            card(countryDict, i.name, cardDict, i.useCard, i.soldCard)

    del cardDict

    defeated = {'亞特蘭提斯': False, '阿斯嘉': False, '奧林帕斯': False, '瓦干達': False, '香格里拉': False,
                '瓦拉納西': False, '瑪雅': False, '塔爾塔洛斯': False, '特奧蒂瓦坎': False, '復活節島': False}
    for i in shuffle(actionList):
        if i.war[0] != "不戰爭":
            for j in range(len(i.war)):
                war(countryDict, i.name, i.war[j], i.solider[j], i.resource[j], i.Rspeed[j], defeated)
        else:
            continue

    roundnow = input()
    write_country_file(countryDict)
    countryName = ['亞特蘭提斯', '阿斯嘉', '奧林帕斯', '瓦干達', '香格里拉',
                   '瓦拉納西', '瑪雅', '塔爾塔洛斯', '特奧蒂瓦坎', '復活節島']
    for i in countryName:
        write_individual(countryDict, i, roundnow)
