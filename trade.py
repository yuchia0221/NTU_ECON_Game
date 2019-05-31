from function import createCountry, read_file, write_country_file
from math import atan, pi


def trade_function(d, s):
    return (1.2) * (2 / pi) * atan((d - s) * (1 / 5000)) + 1.2


def print_indo(countryDict):
    for i in countryDict.values():
        print(i.to_list())


if __name__ == "__main__":
    # print("a = 5, c = 0.001")
    # print(trade_function(0, 10000), "d = 0, s = 10000")
    # print(trade_function(0, 5000), "d = 0, s = 5000")
    # print(trade_function(0, 2500), "d = 0, s = 2500")
    # print(trade_function(0, 1000), "d = 0, s = 1000")
    # print(trade_function(0, 500), "d = 0, s = 500")
    # print(trade_function(0, 0), "d = 0, s = 0")
    # print(trade_function(500, 0), "d = 500, s = 0")
    # print(trade_function(1000, 0), "d = 1000, s = 0")
    # print(trade_function(2500, 0), "d = 2500, s = 0")
    # print(trade_function(5000, 0), "d = 5000, s = 0")
    # print(trade_function(10000, 0), "d = 10000, s = 0")

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
