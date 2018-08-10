#coding:utf-8
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

class ModelEvaluator():
    def __init__(self,station):
        self.station = station

    def getPR(self):
     predict_file = "test" + self.station + ".csv"
     P = pd.read_csv(predict_file, index_col=0, parse_dates=True)

     real_file = "real" + self.station + ".csv"
     R = pd.read_csv(real_file, index_col=0, parse_dates=True)

     self.P = P
     self.R = R
     self.var = P.columns

    def prePR(self, P, R, var):
        dataset = pd.concat([P[var], R[var]], axis=1)
        dataset.dropna(axis=0, how="any", inplace=True)
        P=dataset.iloc[:,:1]
        R=dataset.iloc[:,1:]
        return P, R

    def calcNMB(self, P, R, var, time):
        P = P[:time]
        R = R[:time]
        P, R = self.prePR(P, R, var)
        x = 0
        y = 0
        for i in range(0,P.shape[0]):
         x = x + P[var].iloc[i]
         y = y + R[var].iloc[i]
        return (x/y - 1)*100

    def calcNME(self, P, R, var, time):
        P = P[:time]
        R = R[:time]
        P, R = self.prePR(P, R, var)
        x = 0
        y = 0
        for i in range(0, P.shape[0]):
            x = x + abs(P[var].iloc[i] - R[var].iloc[i])
            y = y + R[var].iloc[i]
        return (x / y)*100

    def calccorr(self, P, R, var, time):
        df = pd.concat([P[var], R[var]], axis=1)
        df = df[:time]
        df.dropna(axis=0, how="any", inplace=True)
        return df.corr().iloc[0,1]

    def calcRMSE(self, P, R, var, time):
        P = P[:time]
        R = R[:time]
        P, R = self.prePR(P, R, var)
        x = 0
        y = 0
        for i in range(0, P.shape[0]):
            x = x + (P[var].iloc[i] - R[var].iloc[i])**2
        return (x / P.shape[0])**0.5

    def BasicStat(self, vartypes, time):
        self.getPR()

        self.Po = pd.DataFrame()
        self.Ro = pd.DataFrame()

        for var in vartypes:

          self.Po = pd.concat([self.Po, self.prePR(self.P,self.R,var)[0]], axis=1)
          self.Ro = pd.concat([self.Ro, self.prePR(self.P,self.R,var)[1]], axis=1)

        self.P = self.Po
        self.R = self.Ro

        NMB = {}
        NME = {}
        corr = {}
        RMSE = {}

        for var in vartypes:
          NMB[var] = self.calcNMB(self.P, self.R, var, time)

        self.NMB = NMB

        for var in vartypes:
          NME[var] = self.calcNME(self.P, self.R, var, time)

        self.NME = NME

        for var in vartypes:
          corr[var] = self.calccorr(self.P, self.R, var, time)

        self.corr = corr

        for var in vartypes:
          RMSE[var] = self.calcRMSE(self.P, self.R, var, time)

        self.RMSE = RMSE





BJN = ModelEvaluator("1011A")
vartypes=["pm2_5", "pm10", "o3"]

times = [12, 24, 48, 72, 120, 168]  #评价前t个时次预报平均质量
for time in times:
  BJN.BasicStat(vartypes, time)
  print "NMB in",time,"hours:", BJN.NMB,"\n" #NMB越接近0越好，正值表示高估，负值表示低估，20%以下可以满意
  print "NME in",time,"hours:", BJN.NME,"\n"  #NME越接近0越好，为正值，50%以下可以满意

  print "corr in",time,"hours:", BJN.corr,"\n" #corr越接近1越好
  print "RMSE in", time, "hours:", BJN.RMSE, "\n\n"  # corr越接近1越好



