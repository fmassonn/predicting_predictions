# -*- coding: utf-8 -*-
"""
Created on Fri May 22 17:28:08 2020

@author: massonnetf
"""

#!/usr/bin/python
#
# Time series of sea ice in February


from   netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import wget
import os
import csv
import scipy.stats
import calendar

# Add SIO data (June submissions)
methname = ["All",  "Dynamical", "Statistical", "Heuristic", "Mixed"]
method = 2

#       Year   obs   [ALL,    DYN,    STAT,   HEUR,   MIX]
data = [
        [2007, 4.27, [np.nan, np.nan, np.nan, np.nan, np.nan]],
        [2008, 4.69, [4.3 ,   np.nan,  4.5,    4.1,    3.48 ]], # Value from Larry's file
        [2009, 5.26, [4.74,   4.75,   4.89,   4.67,   np.nan]], # Value from Larry's file
        [2010, 4.87, [4.9 ,   4.9,    4.9,    5.0,    np.nan]], # Value from Larry's file
        [2011, 4.56, [4.7 ,   4.55,   4.7,    4.8,    np.nan]], 
        [2012, 3.57, [4.4 ,   4.8,    4.4,    4.5,    np.nan]],
        [2013, 5.21, [4.1 ,   4.35,   3.9,    4.1,    np.nan]],
        [2014, 5.22, [4.7 ,   4.65,   4.8,    4.4,    4.5   ]],
        [2015, 4.62, [4.94,   5.07,   5.04,   4.1,    3.9   ]],
        [2016, 4.53, [4.28,   4.58,   4.28,   4.0,    np.nan]],
        [2017, 4.82, [4.43,   4.39,   4.69,   4.08,   4.1   ]],
        [2018, 4.79, [4.6 ,   4.78,   4.41,   4.31,   5.04  ]],
        [2019, 4.36, [4.40,   4.56,   4.4 ,   4.09,   np.nan]], # Based on Betsy's Excel sheet
        [2020, 4.00, [4.33, 4.405,  4.26,   4.35,   np.nan  ]],
        #[2021, np.nan,[np.nan, np.nan, np.nan, np.nan, np.nan]] 
       ]
years = [d[0] for d in data]
ssies = [d[1] for d in data]
preds = [d[2][method] for d in data] 

# Prediction of the next SIO

fig, ax = plt.subplots(2, 2, figsize = (8, 8), dpi = 100)
plt.suptitle(methname[method] + " contributions", fontsize = 30)

ax1 = ax[0, 0]
ax1.grid()
ax1.set_ylim(0.0, 6.0)
ax1.set_ylabel("10$^6$ km$^2$")
ax1.set_title("September Arctic sea ice extent")
ax1.plot(years, ssies, marker = "s", color = [0.5, 0.5, 0.5], label = "Observed (NSIDC G02135)")
ax1.plot(years, preds, marker = "s", color = [1.0, 0.5, 0.0], label = "Predicted (" + methname[method] + " SIO median)")
ax1.set_xlim(years[0] - 0.5, years[-1] + 0.5)
ax1.legend(loc = "lower right")

ax2 = ax[0, 1]
ax2.grid()
ax2.set_ylabel("SIO Prediction at year $y$ [10$^6$ km$^2$]")
ax2.set_xlabel("Observation at year $y$ [10$^6$ km$^2$]")
ax2.set_xlim(3.5, 5.5)
ax2.set_ylim(3.5, 5.5)
ax2.plot((0.0, 10.0), (0.0, 10.0), color = "grey", lw = 0.5, label = "y=x")
ax2.set_title("Correspondence")
ax2.scatter(ssies, preds, 50, marker = "s", alpha = 0.5, lw = 0.0, color = [0.0, 0.0, 0.5])
ax2.legend()

ax3 = ax[1, 0]
ax3.grid()
ax3.set_ylim(0.0, 6.0)
ax3.set_ylabel("10$^6$ km$^2$")
ax3.set_title("September Arctic sea ice extent")
ax3.plot(years[1:], ssies[:-1], marker = "s", color = [0.5, 0.5, 0.5], label = "Observed last year (NSIDC G02135)")
ax3.plot(years, preds, marker = "s", color = [1.0, 0.5, 0.0], label = "Predicted (" + methname[method] + " SIO median)")
ax3.set_xlim(years[0] - 0.5, years[-1] + 0.5)
ax3.legend(loc = "lower right")


ax4 = ax[1, 1]
ax4.grid()
ax4.set_ylabel("SIO Prediction at year $y + 1$ [10$^6$ km$^2$]")
ax4.set_xlabel("Observation at year $y$ [10$^6$ km$^2$]")
ax4.set_xlim(3.5, 5.5)
ax4.set_ylim(3.5, 5.5)
ax4.plot((0.0, 10.0), (0.0, 10.0), color = "grey", lw = 0.5, label = "y=x")
ax4.set_title("Correspondence")
ax4.scatter(ssies[:-1], preds[1:], 50, marker = "s", alpha = 0.5, lw = 0.0, color = [0.0, 0.0, 0.5])
ax4.legend()

fig.tight_layout()
plt.subplots_adjust(top = 0.85)
plt.savefig("./fig1_" + methname[method] + ".png")

# Prediction of prediction
x = np.array(ssies[:-1])
xnew = ssies[-1]

y = np.array(preds[1:])

# Exclude nans
x = x[~np.isnan(y)]
y = y[~np.isnan(y)]

n = len(x)


fig, ax = plt.subplots(1, 1, figsize = (4, 4), dpi = 200)
ax.grid()
ax.set_xlim(3.5, 5.5)
ax.set_ylim(3.5, 5.5)


xx = np.linspace(-10, 10, 1000)

xbar = np.mean(x)
ybar = np.mean(y)
xtil = x - xbar
ytil = y - ybar

ax.scatter(x, y, 50, marker = "s", color = "k", alpha = 0.5)
for j in np.arange(len(x)):
    ax.text(x[j], y[j], str(years[j])[:], color = "white", ha = "center", va = "center", fontsize = 3)
    
ax.plot((xnew, xnew), (-1e9, 1e9), color = "green", label = str(years[-1]))
ax.set_xlabel("Observation at year $y$ [10$^6$ km$^2$]")
ax.set_ylabel(methname[method] + " SIO Prediction at year $y + 1$ [10$^6$ km$^2$]")

ax.text(5.05, 5.3, "$r^2$ = " + str(np.round(np.corrcoef(x, y)[0, 1], 2)))

# Estimation of regression coefficients
ahat = np.sum(xtil * ytil) / np.sum(xtil ** 2)
bhat = ybar - ahat * xbar
yhat = ahat * x + bhat

res = y - yhat

se2 = 1.0 / (n - 2) * np.sum(res ** 2)

fit = ahat * xx + bhat

ax.plot(xx, fit, color = "red", label = "Regression line")
spred = np.sqrt(se2 * (1 + 1 / n + (xx - xbar) ** 2 / np.sum(xtil ** 2)))

myzs = [50, 90]

zs = [scipy.stats.norm.ppf((100 - (100 - q) / 2 ) / 100) for q in myzs]

for j, z in enumerate(zs):
    ax.fill_between(xx, fit - z * spred, fit + z * spred, color = "orange", 
                 alpha = 0.8 / (j + 1), edgecolor = "none", zorder = 0, 
                 label = str(myzs[j]) + "% pred. interval", lw = 0)

ax.legend()
ynew = ahat * xnew + bhat
snew = np.sqrt(se2 * (1 + 1 / n + (xnew - xbar) ** 2 / np.sum(xtil ** 2)))

ax.set_title("Prediction of " + str(years[-1] + 1) + " June SIO median (" + methname[method].lower() + "):\n" + str(np.round(ynew, 2)) + " +/- " \
             + str(np.round(zs[-1] * snew, 2)) + " million km²")
plt.tight_layout()
plt.savefig("fig2_" + methname[method] + ".png")


