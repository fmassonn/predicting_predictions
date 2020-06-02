# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 23:16:17 2020

@author: massonnetf
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


months_name = ["January", "February", "March", "April", "May", "June", "July",\
               "August", "September", "October", "November", "December"]


# Sea ice Outlooks
# -------------------

filecsv = "2008_2018_sio.csv"
# Use Pandas to read the file
df = pd.read_csv(filecsv, delimiter = ";", encoding = "latin")

yearb_sio, yeare_sio = 2008, 2018
n_years_sio = yeare_sio - yearb_sio + 1
sio_median = np.zeros(n_years_sio)

years_sio = np.arange(yearb_sio, yeare_sio + 1)
for year in years_sio:
  # defining a label for figures but avoid appearing multiple times

  tmp = df[(df["year"] == year) & \
           (df["month"] == 6)]["sio"]
  # Series of extents converted from string to float (and they appear with
  # comma for separating decimals from integers in the file)
  series = [float(x.replace(",",".")) for x in tmp]

  print(year)
  print("----")
  print("ALL: " + str(np.round(np.median(series), 2)))
  
  
  
  # DYN
  tmp = df[(df["year"] == year) & \
           (df["month"] == 6)   & \
           (df["method4"] == "Dynamical")]["sio"]
  series = [float(x.replace(",",".")) for x in tmp]
  print("DYN: " + str(np.round(np.median(series), 2)))

  # STAT
  tmp = df[(df["year"] == year) & \
           (df["month"] == 6)   & \
           (df["method4"] == "Statistical")]["sio"]
  series = [float(x.replace(",",".")) for x in tmp]
  print("STAT: " + str(np.round(np.median(series), 2)))
  
  # HEUR
  tmp = df[(df["year"] == year) & \
           (df["month"] == 6)   & \
           (df["method4"] == "Heuristic")]["sio"]
  series = [float(x.replace(",",".")) for x in tmp]
  print("HEUR: " + str(np.round(np.median(series), 2)))

  # MIXED
  tmp = df[(df["year"] == year) & \
           (df["month"] == 6)   & \
           (df["method4"] == "Mixed")]["sio"]
  series = [float(x.replace(",",".")) for x in tmp]
  print("MIX: " + str(np.round(np.median(series), 2)))
  print("====")
