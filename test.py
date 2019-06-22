from random import shuffle, randint

resourcePool, warPool, humanPool = [], [], []
loopR = [34, 22, 10, 34, 22, 10, 34, 22, 10, 34, 22, 10, 20, 20, 20, 20, 20, 20, 8, 14, 20, 10]
loopW = [60, 30, 10, 60, 30, 10, 75, 25]
loopH = [15, 25, 10]

resource = ['綠色革命', '神農氏萬歲', '糧食酒', '天降黑森林', '人造林', '榆木椅', '挖礦機器人', '華鐵爐', '熔爐', '找到烏魯魯', '愚公移山', '留遷石', '免洗餐具', '菠菜罐頭', '石板烤肉', '金斧頭銀斧頭',
            '原始人', '鏗鏘鏗鏘', '蟹堡秘方', '國富論', '發小財', '發大財']
war = ['自強運動', '埃癸斯', '葵花寶典', '曼哈頓計畫', '甲不離人', '石中劍', '劍盾在身', '上下其手']
human = ['轉小人', '做中人', '登大人']
countryName = ['亞特蘭提斯', '阿斯嘉', '奧林帕斯', '瓦干達', '香格里拉',
               '瓦拉納西', '瑪雅', '塔爾塔洛斯', '特奧蒂瓦坎', '復活節島']

index = 0
for i in loopR:
    for j in range(i):
        resourcePool.append(resource[index])
    index += 1

index = 0
for i in loopW:
    for j in range(i):
        warPool.append(war[index])
    index += 1

index = 0
for i in loopH:
    for j in range(i):
        humanPool.append(human[index])
    index += 1

shuffle(resourcePool)
shuffle(warPool)
shuffle(humanPool)

Ecountry = {'亞特蘭提斯': [3, 1, 1, 0],
            '阿斯嘉': [3, 1, 1, 0],
            '奧林帕斯': [3, 1, 1, 0],
            '瓦干達': [3, 1, 1, 0],
            '香格里拉': [1, 2, 0, 0],
            '瓦拉納西': [1, 2, 0, 0],
            '瑪雅': [1, 2, 0, 0],
            '塔爾塔洛斯': [1, 2, 0, 0],
            '特奧蒂瓦坎': [1, 2, 0, 0],
            '復活節島': [1, 2, 0, 0],
            }


sumR, sumW, sumH = sum(loopR), sum(loopW), sum(loopH)

for i in countryName:
    print(i, end=": ")
    for j in range(Ecountry[i][0]):
        print(resourcePool[randint(0, sumR - 1)], end=" ")
    for j in range(Ecountry[i][1]):
        print(humanPool[randint(0, sumH - 1)], end=" ")
    for j in range(Ecountry[i][2]):
        print(warPool[randint(0, sumW - 1)], end=" ")
    print()

# resource = ['綠色革命', '神農氏萬歲', '糧食酒', '天降黑森林', '人造林', '榆木椅', '挖礦機器人', '華鐵爐',
#             '熔爐', '找到烏魯魯', '愚公移山', '留遷石', '免洗餐具', '菠菜罐頭', '石板烤肉', '金斧頭銀斧頭', '原始人', '鏗鏘鏗鏘']
# war = ['自強運動', '埃癸斯', '葵花寶典', '曼哈頓計畫', '甲不離人', '石中劍', '劍盾在身', '上下其手']
# human = ['轉小人', '做中人', '登大人']

# index = 0
# for i in loopR:
#     for j in range(i):
#         resourcePool.append(resource[index])
#     index += 1

# index = 0
# for i in loopW:
#     for j in range(i):
#         warPool.append(war[index])
#     index += 1

# index = 0
# for i in loopH:
#     for j in range(i):
#         humanPool.append(human[index])
#     index += 1

# shuffle(resourcePool)
# shuffle(warPool)
# shuffle(humanPool)

# sumR, sumW, sumH = sum(loopR), sum(loopW), sum(loopH)
# cardR, cardW, cardH = 16, 12, 10

# for i in range(cardR):
#     print(resourcePool[randint(0, sumR)])

# print("-" * 100)

# for i in range(cardW):
#     print(warPool[randint(0, sumW)])

# print("-" * 100)

# for i in range(cardH):
#     print(humanPool[randint(0, sumH)])
