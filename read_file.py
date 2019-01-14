import csv
from collections import namedtuple


with open("國家資訊.csv", "r") as csv_file:
    country_info = namedtuple("country_info",
                              "id name asset gold population solider weapon food_speed wood_speed mineral_speed oil_speed food wood mineral oil")
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    country_list = [country_info(*i) for i in csv_reader]
