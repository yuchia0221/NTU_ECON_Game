from function import createCountry, read_file, write_country_file
from math import atan, pi


def trade_function(d, s):
    a, b, c = 2, 2, 0.04

    if d > s:
        return a * (2 / pi) * atan(c * pow((d - s), (1 / 3))) + b
    else:
        return a * (2 / pi) * atan(c * -pow(abs(d - s), (1 / 3))) + b


def print_indo(countryDict):
    for i in countryDict.values():
        print(i.to_list())


if __name__ == "__main__":
    resources = ["糧食", "木頭", "鐵礦", "石頭"]
    trade_info = read_file("系統貿易(回應)")              # [時間, 國家名, 賣糧, 賣木, 賣鐵, 賣石, 買糧, 買木, 買鐵, 買石]
    countryDict = createCountry()

    # 定價
    price_list, demand, supply = [], [0] * 4, [0] * 4   # [糧食, 木頭, 鐵礦, 石頭], 物資的總需求，總供給 [糧食, 木頭, 鐵礦, 石頭]

    for j in trade_info:
        if countryDict[j[1]].food < j[2]:               # 如果物資不夠賣，將當回賣的物資量等同現有物資存量，並顯示錯誤
            j[2] = countryDict[j[1]].food
            print(f"{j[1]} doesn't have enough resources of food")
        if countryDict[j[1]].wood < j[3]:
            j[3] = countryDict[j[1]].wood
            print(f"{j[1]} doesn't have enough resources of wood")
        if countryDict[j[1]].steel < j[4]:
            j[4] = countryDict[j[1]].steel
            print(f"{j[1]} doesn't have enough resources of steel")
        if countryDict[j[1]].stone < j[5]:
            j[5] = countryDict[j[1]].stone
            print(f"{j[1]} doesn't have enough resources of stone")

        for i in range(4):                          # 加總供給與需求
            supply[i] += j[i + 2]
            demand[i] += j[i + 6]

    for i, j in zip(demand, supply):
        price_list.append(trade_function(i, j))     # 算出均衡價格

    for i in range(4):
        print(f"{resources[i]}的價格為{price_list[i]:.2f}")

    # 買賣
    for i in trade_info:
        # 執行賣物資的動作
        countryDict[i[1]].food -= i[2]
        countryDict[i[1]].wood -= i[3]
        countryDict[i[1]].steel -= i[4]
        countryDict[i[1]].stone -= i[5]
        print(f"{i[1]} 賣出了 {i[2]} 糧食 {i[3]} 木頭 {i[4]} 鐵礦 {i[5]} 石頭")
        for j in range(4):
            countryDict[i[1]].gold += price_list[j] * i[j + 2]

        # 執行買物資的動作
        for j in range(4):
            if countryDict[i[1]].gold < price_list[j] * i[j + 6]:                                   # 如果黃金不夠買當項物資
                print(f"{i[1]} doesn't have enough resources of gold to buy {resources[j]}")        # 顯示錯誤訊息
                i[j + 6] = 0
                while(countryDict[i[1]].gold > price_list[j] * (i[j + 6] + 500)):  # 以500為間隔，從0開始，直到他買得起結束
                    i[j + 6] += 500

            countryDict[i[1]].gold -= price_list[j] * i[j + 6]

        countryDict[i[1]].food += i[6]
        countryDict[i[1]].wood += i[7]
        countryDict[i[1]].steel += i[8]
        countryDict[i[1]].stone += i[9]
        print(f"{i[1]} 買進了 {i[6]} 糧食 {i[7]} 木頭 {i[8]} 鐵礦 {i[9]} 石頭")

    write_country_file(countryDict)
