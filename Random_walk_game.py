# -*- coding: utf-8 -*-
"""
game that determines probability that you will reach height of 60 steps given
steps taken by roll of dice and clumsinesss. Start at 0 height and roll dice
100 times, simulate 10000 times. Display results. Calculate probability of
reaching height of 60 steps
"""

import matplotlib.pyplot as plt
import numpy as np
# set seed
np.random.seed(123)
all_walks = []
# number of interations
for i in range(500) :
    random_walk = [0]
    # roll dice range() times per iteration
    for x in range(100) :
        step = random_walk[-1]
        dice = np.random.randint(1, 7)
        if dice <= 2:
            step = max(0, step - 1)
        elif dice <= 5:
            step += 1
        else:
            step = step + np.random.randint(1, 7)
        if np.random.rand() <= 0.001 :
            step = 0
        random_walk.append(step)
    all_walks.append(random_walk)

# Create and plot np_aw_t
np_aw_t = np.transpose(np.array(all_walks))

# Select last row from np_aw_t: ends
ends = np_aw_t[-1]

# Plot histogram of ends, display plot
plt.hist(ends)
plt.title("Number of Steps Taken Per Iteration")
plt.xlabel("Height")
plt.ylabel("Number of times Height reached")
plt.show()
plt.clf()

# winning percentage
wp = (sum(ends >= 60) / len(ends)) * 100
print(wp)