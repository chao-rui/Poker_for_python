import random

poker = []
for i in range(0,52):
    poker.append(i + 1)
random.shuffle(poker)

players = []
for i in range(0,4):
    players.append(poker[i * 13:( i + 1 )*13])         

currcards = [0,]
currPlayer = 0

def ready():
    for player in players:
        sortCards(player)

    index = 0
    for i in poker:
        if i == 13:
            if (index + 1) % 13 == 0:
                currPlayer = (index + 1) // 13
            else:
                currPlayer = (index + 1) // 13 + 1
            return currPlayer
        index += 1

def isEnd():
    for i in players:
        if len(i) == 0:
            return False
    return True

def start():
    global currPlayer
    nextPlayer = currPlayer
    while isEnd():
        print("玩家{}出牌：".format(nextPlayer),end = '')
        if nextPlayer == 4:
            if dealPlayer(players[nextPlayer-1]):
                printName(players[nextPlayer-1])
                currPlayer = nextPlayer
        else:
            if deal(players[nextPlayer-1]):
                printName(players[nextPlayer-1])
                currPlayer = nextPlayer
        

        if nextPlayer == currPlayer:
            nextPlayer = getNextPlayer(currPlayer)
        elif currPlayer == getNextPlayer(nextPlayer):
            currcards.clear()
            currcards.append(0)
            nextPlayer = currPlayer
        else:
            nextPlayer = getNextPlayer(nextPlayer)
        print("")

def bestDeal(cardValues,player):
    currcards.clear()
    minCard = cardValues[0]
    currcards.append(player[0])

    maxSame = 0
    for i in cardValues:
        if i != cardValues[0]:
            break
        maxSame += 1

    if maxSame == 2:
        currcards.append(player[1])
    elif maxSame == 3 or maxSame == 4:
        for i in range(1,5):
            currcards.append(player[i])
    elif maxSame == 1:
        getConnect(cardValues,player,minCard,-1,currcards)

def dealOne(player,playerValues):
    index = 0
    for i in player:
        if compare(i,currcards[0]) > 0:
            currcards.clear()
            currcards.append(i)
            return True
        index += 1
    return False

def isLast(cards,card):
    return cards.index(card) == len(cards) - 1

def dealTwo(player,playerValues):
    index = 0
    for i in player:
        if compare(i,currcards[0]) > 0 and isLast(player,i) == False:
            if compare(player[index + 1],i) == 0:
                currcards.clear()
                currcards.append(i)
                currcards.append(player[index + 1])
                return True
        index += 1
    return False

def getConnect(cardValues,player,min,number,connectCards):
    index = 0
    maxConnect = 0
    connectIndex = 0
    connectCards = []
    for i in range(0,len(players)):
        try:
            connectIndex = cardValues.index(min + i)
        except:
            break
        else:
            maxConnect += 1
            connectCards.append(player[connectIndex])

    if maxConnect >= 3:
        currcards.clear()
        index = 0
        for i in connectCards:
            currcards.append(i)
            if number != -1 and index >= number:
                break
            index += 1

def dealConnect(cardValues,player):
    global currcards
    index = 0
    minCard = convValue(currcards[0])

    connectCards = []
    for i in cardValues:
        if i > minCard:
            getConnect(cardValues,player,i,len(currcards),connectCards)
            if len(connectCards) != 0:
                currcards.clear()
                currcards = connectCards[:]
                return True
    return False

def get3P2MainValue(currcards):
    currValues = convValues(currcards)

    for i in currValues:
        sameValue = 0
        sameTimes = 0
        for j in currValues:
            if i == j:
                sameTimes += 1
        if sameTimes >= 3:
            return i
    return False
    

def deal3Plus2(playerValues,player):
    global currcards
    sameValue = get3P2MainValue(currcards)

    index = 0
    sameIndex = 0
    sameTimes = 0
    isHave3p2 = False
    for i in playerValues:
        if i > sameValue:
            for j in playerValues:
                if i == j:
                    sameTimes += 1
        if sameTimes >= 3:
            sameIndex = index
            isHave3p2 = True
            break
        index += 1
    
    if isHave3p2:
        currcards.clear()
        if sameIndex < 3:
            currcards = player[:5]
        else:
            currcards = player[:2]
            currcards = player[sameIndex : sameIndex + 3]
        return True
    return False

def deal(player):
    global currcards
    playerValues = []
    for i in player:
        playerValues.append(convValue(i))

    if currcards[0] == 0:
        bestDeal(playerValues,player)
        return True
    
    if len(currcards) == 1:
        return dealOne(player,playerValues)
    elif len(currcards) == 2:
        return dealTwo(player,playerValues)
    elif len(currcards) == 5:
        return deal3Plus2(playerValues,player)                                                                   
    else:
        return dealConnect(playerValues,player)

#parm:x,y
#return:0:x=y 1:x>y -1:x<y
def compare(x,y):
    if y == 0:
        return -1

    x = convValue(x)
    y = convValue(y)
    if x == y:
        return 0 

    if x >= 4 and y >= 4:
        return x - y
    elif x < 4 and y < 4:
        return x - y
    elif x < 4:
        return 1
    else:
        return -1

def convValue(x):
    if x % 4 != 0:
        return x // 4 + 1
    else:
        return x // 4

def convName(x):
    if x % 4 == 1:
        name = "红桃"
    elif x % 4 == 2:
        name = "方块"
    elif x % 4 == 3:
        name = "梅花"
    else:
        name = "黑桃"
    
    if convValue(x) == 11:
        name += "J"
    elif convValue(x) == 12:
        name += "Q"
    elif convValue(x) == 13:
        name += "K"
    elif convValue(x) == 1:
        name += "A"
    else:
        name += "{}".format(convValue(x))

    return name

def convValues(player):
    cardValues = []
    for i in player:
        cardValues.append(convValue(i))
    return cardValues

def sortCards(cards):
    maxcards = []
    cards.sort()
    for i in cards:
        if convValue(i) < 4:
            maxcards.append(i)

    for i in maxcards:
        cards.remove(i)
        cards.append(i)

def getNextPlayer(playerNo):
    if (playerNo + 1) % 4 == 0:
        return 4
    else:
        return (playerNo + 1) % 4

def getWinner():
    index = 0
    for i in players:
        if len(i) == 0:
            print("玩家{}获胜".format(index + 1))
        index += 1

def printName(player):
    for i in currcards:
        player.remove(i)
        print(convName(int(i)),end = ',')

def isVailed(currcards,cards,player):
    length = len(currcards)
    sortCards(cards)

    for i in cards:
        try:
            player.index(i)
        except:
            return False

    if currcards[0] == 0:
        if len(cards) == 1:
            return True
        elif len(cards) == 2:
            return compare(cards[0],cards[1]) == 0
        elif len(cards) == 5:
            return get3P2MainValue(cards)
        else:
            index = 0
            for i in cards:
                if compare(cards[index],cards[index - 1] + 4) != 0:
                    return False
    elif length == 1:
        return compare(cards[0],currcards[0]) > 0
    elif length == 2:
        return compare(cards[0],cards[1]) == 0 and compare(cards[0] ,currcards[0]) > 0
    elif length == 5:
        return compare(get3P2MainValue(cards),get3P2MainValue(currcards)) > 0
    else:      
        if compare(cards[0] , currcards[0]) > 0:
            index = 0
            for i in cards:
                if compare(cards[index] , cards[index - 1] + 4) != 0:
                    return False
    return True
                
def dealPlayer(player):
    global currcards
    print("\n手牌：",end = "")
    for i in player:
        print("{}({})".format(convName(i),i),end=" ")
    
    number = len(currcards)
    if currcards[0] != 0:
        while True:
            card = ""
            cards = []
            inValue = input("\n是否跳过本环节：（Y/N）：")
            if inValue == "Y":
                return False       
            for i in range(0,number):
                card = input("出牌（{}/{}）:".format(i+1,number))
                try:
                    cards.append(int(card))
                except:
                    print("无效输入，请重试")
            if isVailed(currcards,cards,player):
                currcards.clear()
                currcards = cards[:]
                break
            else:
                print("无效组合，请重新出牌")
    else:
        cards = []
        print("")
        while True:
            card = input("出牌（按0结束）:")
            if card == "0":
                if isVailed(currcards,cards,player):
                    currcards.clear()
                    currcards = cards[:]
                    break
            else:
                try:
                    cards.append(int(card))
                except:
                    print("无效输入，请重试")
    

    return True

currPlayer = ready()
start()
getWinner()