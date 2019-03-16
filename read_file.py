import csv
from collections import namedtuple


country_info = namedtuple("country_info",
                          "id name asset gold population solider weapon air food_speed wood_speed steel_speed oil_speed food wood steel oil")

nameDict = {"亞特蘭提斯": "Atlantis", "阿斯嘉": "Asgard", "奧林帕斯": "Olympus", "瓦干達": "Wakanda", "香格里拉": "ShangriLa",
            "瓦拉納西": "Varanasi", "瑪雅": "Maya", "塔爾塔洛斯": "Tartarus", "特奧蒂瓦坎": "Teotihuacan", "復活節島": "EasterIsland"}

with open("國家資訊.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    country_list = [country_info(*i) for i in csv_reader]
