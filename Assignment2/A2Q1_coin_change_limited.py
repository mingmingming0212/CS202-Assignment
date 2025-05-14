import random

# random generate 10 denominations
# the next denomination ~= the previous * 2, or plus/minus 1
# for each denomination, generate a quantity between 10 and 20 inclusive

random.seed('coin')
curr = 1
denom = [(curr, random.randint(10, 20))]
for i in range(9):
    curr = 2 * curr + 1 - random.randrange(3)
    denom.append((curr, random.randint(1, 2)))
    # what if you change it to denom.append((curr, random.randint(1, 2)))
print(denom)

# denom.sort(reverse=True, key=lambda x: x[0])

# solution to each subproblem, contain (1) the min number of coins, and (2) all plans with sum of coins being the min num of coins, this is because there is limited supply for each coin, one plan of x cents may allow us to reach x+5 cents, another plan may allow us to reach x+10 cents, depending on whether we have extra coins of 5 cents or 10 cents

class MinCoinPlan:
    def __init__(self, n, p):
        self.num_coin = n
        self.plan = [p]
    def add_plan(self, p):
        self.plan.append(p)

m = len(denom)
n = 10

min_coin_plan = [None] * (n + 1)
min_coin_plan[0] = MinCoinPlan(0, [0] * m)
for i in range(m): # suppose we already obtained solutions to the sub-problems using denom[0], denom[1], ..., denom[i-1], now we consider using denom[i], e.g., when considering 5c, solutions to sub-problems that use 1c and 2c only are available.
    for j in range(1, n+1): # consider the min-coin sub-problem sum to j cents, e.g., 11c
        if j >= denom[i][0] and min_coin_plan[j - denom[i][0]] is not None: # is it possible to use denom[i][0]? if yes, we can make j cents by adding 1 coin of denom[i][0] to a min-coin plan of j-denom[i][0] cents. E.g., when making 11c, consider add 1 coin of 5c to all possible ways to make 6c.
            for p in min_coin_plan[j - denom[i][0]].plan: # for each possible plan of making j-denom[i][0], e.g., 6c
                if p[i] < denom[i][1]: # must check if there is enough supply of denom[i][0], e.g., there are still 5c coins
                    if min_coin_plan[j] is None or min_coin_plan[j - denom[i][0]].num_coin + 1 < min_coin_plan[j].num_coin: # now I have a better solution, remove all existing plans, and build a new MinCoinPlan object as a solution for j cents
                        p_new = p.copy()
                        p_new[i] += 1 # add one coin of denom[i][0]
                        min_coin_plan[j] = MinCoinPlan(min_coin_plan[j - denom[i][0]].num_coin + 1, p_new)
                    elif min_coin_plan[j - denom[i][0]].num_coin + 1 == min_coin_plan[j].num_coin: # now I have an equally good solution, only need to add this plan
                        p_new = p.copy()
                        p_new[i] += 1 # add one coin of denom[i][0]
                        min_coin_plan[j].add_plan(p_new)


# may print out and check
for i in range(1, n+1):
    if min_coin_plan[i] is not None:
        print(i, min_coin_plan[i].num_coin, min_coin_plan[i].plan)


# if we only consider the minimum number of coins without considering the plans, this is the algorithm discussed in class

denom.insert(0, 0) # insert at position 0, so that each row i considers using denom[i] (cents: denom[i][0]; limit: denom[i][1])
minCoin = [[float('inf')] * (n+1) for _ in range(m+1)]
for i in range(m+1):
    minCoin[i][0] = 0
for i in range(1, m+1):
    for j in range(1, n+1):
        minCoin[i][j] = minCoin[i-1][j] # if do not use denom[i][0] cents
        for k in range(1, denom[i][1]+1): # using k pieces of denom[i][0] cents
            if j >= k * denom[i][0]:
                minCoin[i][j] = min(minCoin[i][j], minCoin[i-1][j - k*denom[i][0]] + k)

for i in range(1, n+1):
    if min_coin_plan[i] is None:
        if minCoin[m][i] > 0:
            print('inconsistent result at %d cents, no min_coin_plan, but MinCoin = %d' % (i, minCoin[m][i]))
    elif min_coin_plan[i].num_coin != minCoin[m][i]:
        print('inconsistent result at %d cents, min_coin_plan give minimum %d coins, but MinCoin = %d' % (i, min_coin_plan[i].num_coin, minCoin[m][i]))
