from random import shuffle, randint

resourcePool, warPool, humanPool = [], [], []
loopR = [34, 22, 10, 34, 22, 10, 34, 22, 10, 34, 22, 10, 20, 20, 20, 20, 20, 20, 8, 14, 20, 10]
loopW = [60, 30, 10, 60, 30, 10, 75, 25]
loopH = [15, 25, 10]
<<<<<<< HEAD

resource = ['綠色革命', '神農氏萬歲', '糧食酒', '天降黑森林', '人造林', '榆木椅', '挖礦機器人', '華鐵爐', '熔爐', '找到烏魯魯', '愚公移山', '留遷石', '免洗餐具', '菠菜罐頭', '石板烤肉', '金斧頭銀斧頭',
            '原始人', '鏗鏘鏗鏘', '蟹堡秘方', '國富論', '發小財', '發大財']
war = ['自強運動', '埃癸斯', '葵花寶典', '曼哈頓計畫', '甲不離人', '石中劍', '劍盾在身', '上下其手']
human = ['轉小人', '做中人', '登大人']

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

Rcountry = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Hcountry = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
Wcountry = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Scountry = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

sumR, sumW, sumH = sum(loopR), sum(loopW), sum(loopH)
cardR, cardW, cardH = sum(Rcountry), sum(Wcountry), sum(Hcountry)
 
num = 1
for i in Rcountry:
    print(num, end=": ")
    num += 1
    for j in range(i):
        print(resourcePool[randint(0, sumR - 1)], end=" ")
    print()

print("-" * 100)

num = 1
for i in Hcountry:
    print(num, end=": ")
    num += 1
    for j in range(i):
        print(humanPool[randint(0, sumH - 1)], end=" ")
    print()

print("-" * 100)

num = 1
for i in Wcountry:
    print(num, end=": ")
    num += 1
    for j in range(i):
        print(warPool[randint(0, sumW - 1)])
    print()
=======
resource = ['綠色革命', '神農氏萬歲', '糧食酒', '天降黑森林', '人造林', '榆木椅', '挖礦機器人', '華鐵爐',
            '熔爐', '找到烏魯魯', '愚公移山', '留遷石', '免洗餐具', '菠菜罐頭', '石板烤肉', '金斧頭銀斧頭', '原始人', '鏗鏘鏗鏘']
war = ['自強運動', '埃癸斯', '葵花寶典', '曼哈頓計畫', '甲不離人', '石中劍', '劍盾在身', '上下其手']
human = ['轉小人', '做中人', '登大人']

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
a = "123"
print(a)

input()
>>>>>>> 0836f98f512817d3aef2b48311a80c841d61b124
