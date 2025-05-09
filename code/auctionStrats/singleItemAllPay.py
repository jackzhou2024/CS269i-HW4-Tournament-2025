import random
import numpy as np

# return the name of the strategy
def get_name():
    return "All-Pay Auction"

# auctionStrategy receives the biding prices from the two auto-bidders
# In addition, it also receives their history, i.e., auctionHistory1 and auctionHistory2
# auctionHistory1/auctionHistory2 is a list of 3-tuples, (bid, result, payment), recording
# the bid price, allocation result and the bidder's payment in the last rounds

# Receive the bid price from player 1 and player 2

# Return a 2x2 list, 
# each 2-tuple includes the allocation result (i.e., a flag indicating whether you win the item), and your payment

# If there is a tie, make a random winner 


def auctionStrategy(bid1, bid2, auctionHistory1, auctionHistory2):
    if bid1 > bid2:
        return [[1, bid1],[0,bid2]]
    elif bid1 < bid2:
        return [[0,bid1],[1, bid2]]
    else:
        if random.uniform(0,1) <0.5:
            return [[1, bid1], [0,bid2]]
        else:
            return [[0,bid1], [1, bid2]]
