# Auction-Design Tournament

This tournament code was originally developed by Jinkun Geng and modified by Jack Zhou.

## How It Works:

Your task is to develop an auction strategy following the provided template in the `auctionStrats` folder. Specifically, you will implement a function called `auctionStrategy`, which takes two bid prices as input and returns a 2x2 list representing the auction results. Please refer to the examples provided for guidance.

We will utilize the bidding strategies submitted by you and your classmates for HW3. Your auction strategy will be tested against randomly sampled pairs of your classmates' auto-bidders. For each pair:

- Each auto-bidder is assigned a random ROI factor sampled from the range $$[1, 2]$$.
- Your auction strategy is executed for 10,000 rounds.

Your goal is to maximize the **total revenue** generated while trying to help bidders meet their ROI constraints.

### Scoring:

Your score is the sum of payments from both bidders who satisfy their ROI constraints. For example:

- If bidder 1 and bidder 2 both satisfy their ROI constraint, your score the total payment from both bidders.
- If bidder 1 violates the ROI constraint but bidder 2 satisfies it, your score is the total payment from bidder 2.
- If bidder 1 and bidder 2 both violate the ROI constraints, your score is $$0$$.

**Note:**
- You do not know the exact ROI factors of the bidders; you only know they are randomly sampled from $$[1, 2]$$.
- You may infer bidder strategies and ROI factors from history auction data, which is part of input to your strategy.

### Auction Format Requirements:

Your auction strategy must:
- Never charge a bidder more than their bid in any round.
- Allocate the item deterministically to at most one bidder per round.


## Tasks:

- Write a Python file named `strategy.py`. (Please maintain this exact filename!)
- Implement the function named `auctionStrategy` within this file.
- Place your `strategy.py` file into the `auctionStrats` folder.
- Run the tournament script using `game_run.py`.

Three examples are provided in `auctionStrats`:
- First-price auction
- Second-price auction
- All-pay auction

These examples can guide you in developing your auction strategy.

**Important:** _No hacking: your code should behave like a legitimate auction strategy, and should not attempt to exploit unauthorized data or manipulate the system itself._


## Tips

To start from a clean Python enviornment, I suggest you use conda 

https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html

First, install conda

Second, create a clean python enviornment (say python 3.7) with conda

Third, install any deps and execute your script in that conda enviornment 

The major commands are as below. 

```
conda create --name [NAME]

conda activate [NAME]

conda install pip

pip install -r requirements.txt
```

After you have successfully create the environment, enter the code environment, and run game_run.py

```
cd code 

python game_run.py
```


## Note

All you need to do is to write a strategy.py file and add it to auctionStrats. No need to change any existing files.

When submitting to gradescope, you only submit strategy.py, no other files are needed.

For any questions, feel free to make a post on edstem.
