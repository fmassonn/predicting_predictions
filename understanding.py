# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:10:16 2020

@author: massonnetf
"""

import numpy as np
import matplotlib.pyplot as plt

#np.random.seed(0)
# Understanding the origin of correlation between previous year observed
# and next year forecasted extent

# Strategy: 1/ generate a synthetic time series of length N
#           2/ Extrapolate the time series linearly or quadratically to N + 1
#           3/ Correlate the extrapolation with the Nth element of the series
#           4/ Repeat many times

# Order for trend extrapolation
order = 0 

# First year of time series
yearb  = 1979

# First year an outlook was collected
yearbo = 2008 
# Last year an outlook was collected
yeareo = 2022

# Number of years
N = yeareo - yearb + 1
# Number of Monte Carlo Runs
nMC = 1000


correlations = list()
for jMC in range(nMC):
    
    # Generating synthetic time series of observations from start to end
    historicalSeries = np.random.randn(N)
    
    # Generate a prediction each year by simple extrapolation of the trend
    # up to previous year
    
    # Initializing the year of prediction to the first outlook year
    yearpred = yearbo
    
    currentOutlooks = list()
    while yearpred <=  yeareo:
        
        # series of observations up to then (ignoring the current year)
        # Note that PYthon stops indexing at the last but one value of the
        # range
        myYears = np.arange(yearb, yearpred)
        
        seriesObs = historicalSeries[yearb - yearb: yearpred - yearb]
        
        extrapolPrediction = np.polyval( \
                            np.polyfit(myYears, seriesObs, order), \
                            yearpred)
    
        currentOutlooks.append([extrapolPrediction, seriesObs[-1]])
        
        yearpred += 1
     
    currentOutlooks = np.array(currentOutlooks)    
    # Correlate the time series
    correlations.append(np.corrcoef(currentOutlooks[:, 0], currentOutlooks[:, 1])[0, 1])


    
    
fig, ax = plt.subplots(1, 1, dpi = 150, figsize = (6, 4))
ax.set_title("Distribution of " + str(nMC) + " correlations between artificial observations\n \
             at year $y$ and linear extrapolation to year $y+1$,\n \
             for $y$ ranging from " + str(yearbo) + " to " + str(yeareo - 1))
h = ax.hist(correlations, bins = np.arange(-1, 1, 0.1), color = "black", \
            alpha = 0.5, edgecolor = "white")
ax.plot((0.0, 0.0), (0.0, 1000), color = "k")
ax.grid()
ax.set_ylabel("Count")
ax.set_xlabel("Sample Pearson correlation")
ax.set_ylim(0.0, 1.05 * np.max(h[0]))
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig("./fig.png")



x = list()
y = list()
for jMC in range(nMC):
    tmp = np.random.randn(N)
    x.append(tmp[-1])
    y.append(np.polyval(np.polyfit(np.arange(1, N + 1), tmp, 1), N + 1))


print(np.corrcoef(x, y)[0, 1])

t = np.arange(1, N + 1); 
tnp1t = N + 1 - np.mean(t); 
k = N; 
tkt = k - np.mean(t); 
sti2 = np.sum((t - np.mean(t)) ** 2); 
tnp1t = N + 1 - np.mean(t); 
tnp1t2 = tnp1t ** 2; 
r = (tnp1t * tkt / sti2 + 1 / N) / (tnp1t2 / sti2 + 1 / N) ** 0.5
print(r)
