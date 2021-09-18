# 这是一个文字冒险游戏
# 作者：孙健
# 联系方式:QQ 28472517
# 开始创建于2018.09.26
# 修改人：WangScaler
# 修改时间：2021.09.17
import math
import random


class Player:
    def __init__(self):
        self.name = '后羿'
        self.hp = 10  # 血量
        self.maxHp = 10
        self.moonCake = 0  # 月饼数
        self.maxMoonCake = 10
        self.allMoonCake = 0
        self.level = 1  # 等级
        self.xp = 0  # 经验
        self.xpForNextLevel = 30
        self.locationX = 0
        self.locationY = 0
        self.locationID = 0  # 当前位置
        self.exploredAreas = 1  # 探索的数量
        print("\n你叫后羿. 你的生命值是满的 (%s 点), 你有 %s个月饼. 你的任务就是找到100个月饼，带着月饼寻找你心目中的嫦娥." % (self.hp, self.moonCake))
        print("\n你现在是一个一级角色, 需要获得 %s 点经验才能升级. 这样做我们会获得更多最大生命值. 你可以在探索和战斗中获得经验." % self.xpForNextLevel)
        print("\n你的冒险开始于地球，每移动一步就会掉一滴血哦，注意血量变化，偷偷告诉你，找到惊喜bug,就能快速通关啦...")

    def initPlayer(self, mapSize):
        self.locationX = math.floor((mapSize - 1) / 2)
        self.locationY = math.floor((mapSize - 1) / 2)
        self.locationID = math.floor(math.pow(mapSize, 2) / 2) + 1
        # 初始化当前关卡的月饼数
        self.moonCake = 0

    def initMaxMoonCake(self):
        self.maxMoonCake = 0
        for i in range(0, mapSize):
            for j in range(map_Num - (i + 1) * mapSize, map_Num - i * mapSize):
                if (gameMap[j + 1].type == '月球'):
                    self.maxMoonCake = self.maxMoonCake + 1
        if self.maxMoonCake == 0:
            Map(mapSize, mapSize, self.locationID)
            self.exploredAreas = 1
            self.initMaxMoonCake()

    def hitEnter(self):
        input("\n回车键继续.")

    def getAction(self):
        print('\n可用命令')
        actionString = ""
        if gameMap[self.locationID].explored == False:
            actionString += "\nx = 寻找月饼。"
        if gameMap[self.locationID].type == '地球' and self.hp < self.maxHp:
            actionString += "\nr = 坐禅恢复。"
        print(actionString)
        print('w = 去北面  s = 去南面  a = 去西边  d = 去东边.')
        print('i = 查看月饼')
        print('c = 查看角色状态')
        choice = input('请输入命令并回车').lower()
        print("---------------------------wangscaler----------后羿逐月-----------------------------\n\n")
        if choice == "i":
            print("你目前一共携带: %s 个月饼" % self.allMoonCake)
            print("当前地图拾取 %s 个月饼: " % self.moonCake)
        # 移动
        elif choice == "w" or choice == "a" or choice == "d" or choice == "s":
            self.movePlayer(choice)
        # 探索地区
        elif choice == "x":
            if gameMap[self.locationID].explored == False:
                self.exploredAreas += 1
                if gameMap[self.locationID].type == '月球':
                    print('\n你找到了一个月饼，离嫦娥更近一步了哦')
                    self.addMoonCake(1)
                    self.addXp(self.level)
                sumNum = random.randrange(1, 4)
                if sumNum == 1:
                    print("天哪，你遇到了怪物!")
                    aMonster = monster()
                    damage = aMonster.hitBlood
                    print("你受到了 " + str(damage) + " 点伤害.")
                    self.hp -= damage
                    if self.hp > 0:
                        self.addXp(aMonster.xp)
                elif sumNum == 2:
                    luck = random.randrange(1, 3)
                    aGod = god()
                    if luck == 1:
                        print("哇哦，太幸运了!\n")
                        recovery = aGod.restoreBlood
                        if (self.maxHp - self.hp >= recovery):
                            print(" %s 帮你你恢复了 " + str(recovery) + " 点伤害." % aGod.type)
                            self.hp += recovery
                        elif (self.maxHp == self.hp):
                            print('获得 %s 的祝福，妖魔鬼怪更加忌惮你了。\n' % aGod.type)
                        else:
                            print(' %s 帮你恢复至满血了。\n' % aGod.type)
                            self.hp = self.maxHp
                    else:
                        print('不幸的是 %s 并没有理你。\n' % aGod.type)
                else:
                    print('这是块贫瘠的土地，连个鸟屎都没有！')
                    self.addXp(1)
                gameMap[self.locationID].explored = True
            else:
                print('土地老儿蹦了出来：“土地都被你挖空了，这里没有月饼了”')
        elif choice == "r" and gameMap[self.locationID].type == '地球' and self.hp < self.maxHp:
            self.healHp()
        elif choice == 'c':
            print(self.name + ' /等级: ' + str(self.level) + "级  经验值: " + str(self.xp) + "点 (还需要" + str(
                self.xpForNextLevel - self.xp) + "点升级)")
            print("生命值: " + str(self.hp) + " 点 (最大生命值: " + str(self.maxHp) + " 点)")
        elif choice == 'map':
            print('完了，被你发现了隐藏的bug!可以顺利通关了！\n')
            for i in range(0, mapSize):
                for j in range(map_Num - (i + 1) * mapSize, map_Num - i * mapSize):
                    print(gameMap[j + 1].type + '(' + str(gameMap[j + 1].mapID).zfill(2) + '号)  ', end='')
                print('\n')
        else:
            print('抱歉，我不知道你在说什么。')

    # 绕地图移动.
    def movePlayer(self, direction):
        if direction == 'w':
            if self.locationY + 1 <= mapSize - 1:
                self.locationY += 1
                self.locationID += mapSize
            else:
                self.locationY = 0
                self.locationID = (self.locationID + mapSize) - map_Num
        elif direction == 's':
            if self.locationY - 1 >= 0:
                self.locationY -= 1
                self.locationID -= mapSize
            else:
                self.locationY = mapSize - 1
                self.locationID = (self.locationID - mapSize) + map_Num
        elif direction == "d":
            if self.locationX + 1 <= mapSize - 1:
                self.locationX += 1
                self.locationID += 1
            else:
                self.locationX = 0
                self.locationID -= mapSize - 1

        else:
            if self.locationX - 1 >= 0:
                self.locationX -= 1
                self.locationID -= 1
            else:
                self.locationX = mapSize - 1
                self.locationID += mapSize - 1
        map.description()
        if gameMap[self.locationID].explored == False:
            self.hp -= 1

    # 添加经验
    def addXp(self, num):
        self.xp += num
        print('\n你获得了 %s 点经验值。' % (num))
        if self.xp >= self.xpForNextLevel:
            self.level += 1
            self.maxHp += 5
            self.xpForNextLevel = (self.level) * 20
            print('恭喜你，升级了 -- 现在是 %s 级了！血量上限增加5，记得及时回到地球坐禅恢复哦' % self.level)

    def addMoonCake(self, num):
        self.moonCake += num
        self.allMoonCake += num
        print('\n%s 已经拾取了 %s 个月饼。还需要拾取%s 个月饼' % (self.name, num, self.maxMoonCake - self.moonCake))

    def healHp(self):
        print('你增加了 %s 点生命值。' % (self.maxHp - self.hp))
        self.hp = self.maxHp


class monster:
    monsterType = ["孙悟空", "猪八戒", "沙僧", "白骨精", "金角大王", "银角大王", "牛魔王", "红孩儿"]

    def __init__(self):
        self.type = random.choice(self.monsterType)
        self.hitBlood = random.randrange(1, 5 * player.level)
        self.xp = random.randrange(0, 5 * player.level)
        print('\n%s 出现在你的面前。\n' % self.type)
        if self.type == "猪八戒":
            self.hitBlood = self.hitBlood * 2


class god:
    godType = ["观音菩萨", "金蝉子", "玉皇大帝", "如来佛祖", "上帝"]

    def __init__(self):
        self.type = random.choice(self.godType)
        self.restoreBlood = random.randrange(1, 3 * player.level)
        print('\n%s 出现在你的面前。\n' % self.type)


class Area:
    areaTpye = ["金星", "木星", "水星", "火星", "土星", "月球", "天王星", "海王星"]
    explored = False
    mapID = 0
    x = 0
    y = 0
    type = "月球"

    def __init__(self, id, x, y):
        self.mapID = id
        self.x = x
        self.y = y
        self.type = random.choice(self.areaTpye)


class Map:
    def __init__(self, rows, columns, locationID):
        row = 0
        col = 0
        area = 1
        for r in range(0, rows):
            for c in range(0, columns):
                theArea = Area(area, col, row)
                gameMap[area] = theArea
                if gameMap[area].mapID == locationID:
                    gameMap[area].type = '地球'
                    gameMap[area].explored = True
                area += 1
                area += 1
            row += 1
            col = 0

    def description(self):
        isExplored = "已探索"
        if gameMap[player.locationID].explored == False:
            isExplored = "未探索"
        if gameMap[player.locationID].type == '地球':
            print("\n当前位置: " + gameMap[player.locationID].type)
        print("(X: " + str(player.locationX) + ", Y: " + str(
            player.locationY) + ") 该区域状态： " + isExplored + "." + str(
            player.locationID) + "号地区")


if __name__ == '__main__':
    # 初始化游戏地图和游戏区域
    gameMap = {}
    mapSize = 3
    map_Num = math.floor(math.pow(mapSize, 2))
    player = Player()
    player.initPlayer(mapSize)
    map = Map(mapSize, mapSize, player.locationID)
    still_alive = True
    player.initMaxMoonCake()
    map.description()
    player.hitEnter()
    while still_alive:
        player.getAction()
        if player.exploredAreas == map_Num or player.moonCake >= player.maxMoonCake:
            print("该地图所有的月饼都被你找到了!\n现在进入一个全新的地图继续寻找月饼吧...")
            player.hitEnter()
            mapSize = mapSize + 2
            map_Num = math.floor(math.pow(mapSize, 2))
            player.initPlayer(mapSize)
            gamemap = {}
            map = Map(mapSize, mapSize, player.locationID)
            player.exploredAreas = 1
            player.initMaxMoonCake()
            map.description()
            if player.hp <= 0:  # 玩家死亡
                print("\n很遗憾，还到达了西天极乐世界，没能与嫦娥相聚.")
                still_alive = False
            if player.allMoonCake >= 100:
                print("\n你终于和你的嫦娥相聚了.")
                still_alive = False
        if player.hp <= 0:  # 玩家死亡
            print("\n很遗憾，你到达了西天极乐世界，没能与嫦娥相聚.")
            still_alive = False
        if player.allMoonCake >= 100:
            print("\n你终于和你的嫦娥相聚了.")
            still_alive = False
