from math import atan, pi
from function import createCountry, read_file, write_country_file, write_individual


def trade_function(d, s):
    return (1.2) * (2 / pi) * atan((d - s) * (1 / 5000)) + 1.2


if __name__ == "__main__":
    print("開始執行程式")

    resources = ["糧食", "木頭", "鐵礦", "石頭"]
    trade_info = read_file("系統貿易(回應)")              # [時間, 國家名, 賣糧, 賣木, 賣鐵, 賣石, 買糧, 買木, 買鐵, 買石]
    countryDict = createCountry()

    print("讀檔完成\n")

    # 定價
    price_list, demand, supply = [], [0] * 4, [0] * 4   # [糧食, 木頭, 鐵礦, 石頭], 物資的總需求，總供給 [糧食, 木頭, 鐵礦, 石頭]

    for j in trade_info:
        name = j[1]
        if countryDict[name].food < j[2]:               # 如果物資不夠賣，將當回賣的物資量等同現有物資存量，並顯示錯誤
            j[2] = countryDict[name].food
            print(f"{name}沒有足夠的糧食去貿易")
        if countryDict[name].wood < j[3]:
            j[3] = countryDict[name].wood
            print(f"{name}沒有足夠的木頭去貿易")
        if countryDict[name].steel < j[4]:
            j[4] = countryDict[name].steel
            print(f"{name}沒有足夠的鐵礦去貿易")
        if countryDict[name].stone < j[5]:
            j[5] = countryDict[name].stone
            print(f"{name}沒有足夠的石頭去貿易")

        for i in range(4):                          # 加總供給與需求
            supply[i] += j[i + 2]
            demand[i] += j[i + 6]

    for i, j in zip(demand, supply):
        price_list.append(trade_function(i, j))     # 算出均衡價格

    for i in range(4):
        print(f"{resources[i]}的價格為{price_list[i]:.2f}")

    # 買賣
    for i in trade_info:
        name = i[1]
        # 執行賣物資的動作
        countryDict[name].food -= i[2]
        countryDict[name].wood -= i[3]
        countryDict[name].steel -= i[4]
        countryDict[name].stone -= i[5]
        print(f"{name} 賣出了 {i[2]} 糧食 {i[3]} 木頭 {i[4]} 鐵礦 {i[5]} 石頭")
        for j in range(4):
            countryDict[name].gold += price_list[j] * i[j + 2]

        # 執行買物資的動作
        for j in range(4):
            if countryDict[name].gold < price_list[j] * i[j + 6]:                   # 如果黃金不夠買當項物資
                print(f"{name}沒有足夠的黃金去購買{resources[j]}")                    # 顯示錯誤訊息
                i[j + 6] = 0
                while(countryDict[name].gold > price_list[j] * (i[j + 6] + 500)):   # 以500為間隔，從0開始，直到他買得起結束
                    i[j + 6] += 500

            countryDict[name].gold -= price_list[j] * i[j + 6]

        countryDict[name].food += i[6]
        countryDict[name].wood += i[7]
        countryDict[name].steel += i[8]
        countryDict[name].stone += i[9]
        print(f"{name} 買進了 {i[6]} 糧食 {i[7]} 木頭 {i[8]} 鐵礦 {i[9]} 石頭")

    print("\n貿易結束\n開始寫檔")

    loop = "一"
    write_country_file(countryDict)
    countryName = ['亞特蘭提斯', '阿斯嘉', '奧林帕斯', '瓦干達', '香格里拉',
                   '瓦拉納西', '瑪雅', '塔爾塔洛斯', '特奧蒂瓦坎', '復活節島']
    for i in countryName:
        write_individual(countryDict, i, loop)
