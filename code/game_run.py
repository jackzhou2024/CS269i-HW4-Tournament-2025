import os
import itertools
import importlib
import numpy as np
import random
import json

AUCTION_FOLDER = "auctionStrats"
STRATEGY_FOLDER = "exampleStrats"
CONTEXT_FILE = "context.json"


NUM_ROUNDS = 10000 # You can reduce the num round when you debug

def gen_context():
    f = open(CONTEXT_FILE, 'w')
    jsonArr = []
    valueArr1 = []
    valueArr2 = []
    for i in range(NUM_ROUNDS):
        v1 = random.uniform(0,1)
        valueArr1.append(v1)
        v2 = random.uniform(0,1)
        valueArr2.append(v2)  

    for i in range(NUM_ROUNDS):
        jsonItem = {}
        jsonItem["v1"] = valueArr1[i]
        jsonItem["v2"] = valueArr2[i]
        jsonArr.append(jsonItem)
    
    json.dump(jsonArr, f, indent=4)


gen_context()       
# exit(0)




def calcScore(value, allocationResult):
    if allocationResult == 1:
        # winner, score is value
        return value
    else:
        # loser:  score 0
        return 0
    
def calcRevenue():
    pass

def runRound(pair, auction):
    # print("modulea:",STRATEGY_FOLDER+"."+pair[0])
    moduleA = importlib.import_module(STRATEGY_FOLDER+"."+pair[0])
    moduleB = importlib.import_module(STRATEGY_FOLDER+"."+pair[1])
    moduleAuction = importlib.import_module(AUCTION_FOLDER +"."+auction)
    contextJson = json.load(open(CONTEXT_FILE, 'r'))
    
    LENGTH_OF_GAME =len(contextJson)
    totalScore1, totalScore2 = 0, 0
    totalPayment1, totalPayment2 = 0, 0

    history1 = []
    history2 = []
    ROI1 = random.random() + 1
    ROI2 = random.random() + 1

    auctionHistory1 = []
    auctionHistory2 = []
    for turn in range(NUM_ROUNDS):
        contextItem = contextJson[turn]
        v1 = contextItem["v1"]
        v2 = contextItem["v2"]

        v1 = random.random()
        v2 = random.random()
        bid1 = moduleA.strategy(v1, totalScore1, totalPayment1, ROI1, history1)
        bid2 = moduleB.strategy(v2, totalScore2, totalPayment2, ROI2, history2)
        bid1 = max(bid1, 0)
        bid2 = max(bid2, 0)


    
        # print("bid1=", bid1, " bid2=",bid2)
        # The auction strategy can also see the history of bids, payments, and allocations (but not values)
        auctionResult = moduleAuction.auctionStrategy(bid1, bid2, auctionHistory1, auctionHistory2)
        result1 = auctionResult[0][0]
        result2 = auctionResult[1][0]
        payment1 = auctionResult[0][1]
        payment2 = auctionResult[1][1]
        if payment1 >bid1 or payment2 >bid2:
            raise Exception("Bidder's payment cannot be larger than the bid price, please check your auction strategy")
        if not ((result1==1 and result2 ==0) or (result1 == 0 and result2 ==1) or (result1 == 0 and result2 ==0)):
            raise Exception("At most one bidder can win, and it is allowed that neither wins")
        # if auctionResult[0][0]==1:
        #     cnt1 +=1
        # if auctionResult[1][0]==1:
        #     cnt2 += 1
        # print(bid1," vs ", bid2, " win ", cnt1, " vs ", cnt2)

        score1 = calcScore(v1, result1)
        score2 = calcScore(v2, result2)

        totalPayment1 += payment1
        totalPayment2 += payment2
        totalScore1 += score1
        totalScore2 += score2
        history1.append([v1, bid1, result1, payment1 ])
        history2.append([v2, bid2, result2, payment2 ])

        
        auctionHistory1.append([bid1, result1, payment1])
        auctionHistory2.append([bid2, result2, payment2])

    if (totalPayment1 > 0 and totalScore1 / totalPayment1 < ROI1):
        totalScore1 = 0
        totalPayment1 = 0
    if (totalPayment2 > 0 and totalScore2 / totalPayment2 < ROI2):
        totalScore2 = 0
        totalPayment2 = 0

    return totalScore1, totalScore2, totalPayment1 + totalPayment2


def pad(stri, leng):
    result = stri
    for i in range(len(stri),leng):
        result = result+" "
    return result
    
def runFullPairingTournament(auctionFolder, stratsFolder):
    print("Starting tournament, reading files from "+stratsFolder)
    scoreKeeper = {}
    STRATEGY_LIST = []
    for file in os.listdir(stratsFolder):
        if file.endswith(".py"):
            STRATEGY_LIST.append(file[:-3])

    print("Reading Auction modes from "+auctionFolder)
    AUCTION_LIST = []
    for file in os.listdir(auctionFolder):
        if file.endswith(".py"):
            AUCTION_LIST.append(file[:-3])
            
    for strategy in STRATEGY_LIST:
        scoreKeeper[strategy] = 0

    auctionScore = {}
    for auction in AUCTION_LIST:
        auctionScore[auction] = 0
    for auction in AUCTION_LIST:
        totalRevenue = 0
        pairNum = 0
        for pair in itertools.combinations(STRATEGY_LIST, r=2):
            score0, score1, revenue = runRound(pair, auction)
            totalRevenue += revenue
            scoreKeeper[pair[0]] += score0
            scoreKeeper[pair[1]] += score1
            pairNum +=1
        auctionScore[auction] = totalRevenue / pairNum
        
    
        
    scoresNumpy = np.zeros(len(auctionScore))
    for i in range(len(AUCTION_LIST)):
        scoresNumpy[i] = auctionScore[AUCTION_LIST[i]]
    rankings = np.argsort(scoresNumpy)

    print("\n\nAVERAGE SCORES\n")
    
    for rank in range(len(AUCTION_LIST)):
        i = rankings[-1-rank]
        score = scoresNumpy[i]
        print("#"+str(rank+1)+": "+pad(AUCTION_LIST[i]+":",16)+' %.3f'%score+" \n")
    print("Done with everything!")
    
    
runFullPairingTournament(AUCTION_FOLDER, STRATEGY_FOLDER)
