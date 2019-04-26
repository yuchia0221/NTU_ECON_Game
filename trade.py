from function import createCountry, read_file, write_country_file
from math import atan, pi


def trade_function(d, s):
    a, b, c = 2, 1, 0.04

    if d > s:
        return a * (2 / pi) * atan(c * pow((d - s), (1 / 3))) + b
    else:
        return a * (2 / pi) * atan(c * -pow(abs(d - s), (1 / 3))) + b


if __name__ == "__main__":
    trade_info = [list(i) for i in read_file("系統貿易(回應)")]
    countryDict = createCountry()

    print(trade_info)
    # 定價
    price_list = []
    for i in range(4):
        for j in trade_info:
            demand = 0
            supply = 0
            try:
                demand += j[6 + i]
                supply += j[2 + i]
                price_list.append(trade_function(demand, supply))
            except TypeError as e:
                pass

    # 買賣
    for i in trade_info:
        countryDict[i[1]].food -= int(price_list[0] * i[2])
        countryDict[i[1]].wood -= int(price_list[1] * i[3])
        countryDict[i[1]].stone -= int(price_list[2] * i[4])
        countryDict[i[1]].steel -= int(price_list[3] * i[5])
        for j in range(4):
            countryDict[i[1]].gold += int(price_list[j] * i[j + 2])
        for j in range(4):
            countryDict[i[1]].gold -= int(price_list[j] * i[j + 6])

        countryDict[i[1]].food += int(price_list[0] * i[6])
        countryDict[i[1]].wood += int(price_list[1] * i[7])
        countryDict[i[1]].stone += int(price_list[2] * i[8])
        countryDict[i[1]].steel += int(price_list[3] * i[9])

    write_country_file(countryDict)
