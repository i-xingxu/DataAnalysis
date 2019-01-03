#coding=utf-8

import numpy as np
import time
from datetime import datetime
import datetime
import pandas as pd
from common import conf,mysql,tool,logoutput
import matplotlib.pyplot as plt

class AnalysisMoney():

    def __init__(self):
        # my=mysql.Mysql()
        # my.connect_mysql()
        # self.my=my
        # self.cur=my.cur
        lg=logoutput.Logger()
        self.lg=lg
        self.cf=conf.Conf()
        f=self.cf.get_conf_data("File")
        self.df=pd.read_csv(f["path"],encoding='utf-8',index_col=False)
        byTime=self.df
        byTime["时间"]=pd.to_datetime(byTime["时间"])
        self.byTime=byTime.set_index(byTime["时间"])


    def get_csv(self):
        # print(self.df)
        pass

    def get_year(self,year):
        '''
        返回年的所有数据
        :param year:
        :return:
        '''
        return self.byTime[str(year)]

    def get_year_spend(self,year):
        data=self.get_year(year)
        data=data.groupby("类型")

        spend=data.get_group("支出")
        # income=data.get_group("收入")
        return spend["金额"].sum()

    def get_year_income(self,year):

        data=self.get_year(year)
        data=data.groupby("类型")

        income=data.get_group("收入")
        # income=data.get_group("收入")
        return income["金额"].sum()

    def get_month_income(self,year):

        month=range(1,13)
        data=self.byTime[str(year)].groupby("类型")
        income=data.get_group("收入")
        timeLst=[]
        incomeLst=[]
        for t in month:
            timeLst.append(str(year) + '-' + str(t))
            incomeLst.append(income[str(year)+'-'+str(t)]["金额"].sum().round(decimals=2))

        monthIncome=pd.DataFrame({
            "时间":timeLst,
            "金额":incomeLst
        },dtype=float)
        monthIncome["时间"]=pd.to_datetime(monthIncome["时间"])
        monthIncome.set_index(monthIncome["时间"],inplace=True)

        return monthIncome


    def get_month_spend(self,year):


        month=range(1,13)
        data=self.byTime[str(year)].groupby("类型")
        spend=data.get_group("支出")

        timeLst=[]
        spendLst=[]
        for t in month:
            timeLst.append(str(year)+'-'+str(t))
            spendLst.append(spend[str(year)+'-'+str(t)]["金额"].sum().round(decimals=2))

        monthSpend = pd.DataFrame({"时间":timeLst,
                                   "金额":spendLst
                                   },dtype=float)
        monthSpend["时间"]=pd.to_datetime(monthSpend["时间"])
        monthSpend.set_index(monthSpend["时间"],inplace=True)
        return monthSpend



    def dram_month_spend(self,year):

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        spendMondy_2017=self.get_month_spend(year)
        incomeMoney_2017=self.get_month_income(year)
        allData=pd.DataFrame({
            "收入":incomeMoney_2017["金额"],
            "支出":spendMondy_2017["金额"],
        },dtype=float,index=incomeMoney_2017["时间"])
        plt.figure()
        allData.plot()
        plt.show()

    def draw_year_money(self,yearList):

        incomList=[]
        for y in yearList:
            # y=datetime(y,1,1,0).strftime("%Y")
            incomList.append(self.get_year_income(y).round(decimals=2))
        spendList=[]
        for y in yearList:
            spendList.append(a.get_year_spend(y).round(decimals=2))

        datas=pd.DataFrame({
            # "年份":yearList,
            "收入":incomList,
            "支出":spendList,
        },dtype=float,index=[int(x) for x in yearList])
        # datas.index.name="年份"
        # datas.sort_index(ascending=False)

        plt.figure()
        ax=datas.plot.barh()
        ax.invert_yaxis()
        plt.show()


    def average_month(self):
        datasIncome=pd.DataFrame({
            "平均月收入":[self.get_month_income(2017)["金额"].mean(),self.get_month_income(2018)["金额"].mean()],
        },index=[2017,2018])
        datasSpend=pd.DataFrame({

            "平均月支出":[self.get_month_spend(2017)["金额"].mean(),self.get_month_spend(2018)["金额"].mean()],
        },index=[2017,2018])


        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.figure(1)
        fig, axes = plt.subplots(2, 1)
        # plt.subplot(211)
        datasIncome.plot.barh(ax=axes[0]).invert_yaxis()
        # plt.barh(datasSpend,width=1.0)
        # plt.subplot(212)
        datasSpend.plot.barh(ax=axes[1]).invert_yaxis()
        plt.show()

    def growth_rate(self):

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        incomePate=(self.get_year_income(2018).round(decimals=2)-self.get_year_income(2017).round(decimals=2))/self.get_year_income(2017).round(decimals=2)
        spendRate=(self.get_year_spend(2018).round(decimals=2)-self.get_year_spend(2017).round(decimals=2))/self.get_year_spend(2017).round(decimals=2)
        dataRate=pd.DataFrame({
            "增长率":[incomePate,spendRate]
        },index=["收入增长率","消费增长率"])
        dataRate.plot.bar()
        plt.show()

    def gather(self):

        result={
            "2017年总收入":self.get_year_income(2017).round(decimals=2),
            "2018年总收入":self.get_year_income(2018).round(decimals=2),
            "2017年总支出":self.get_year_spend(2017).round(decimals=2),
            "2018年总支出":self.get_year_spend(2018).round(decimals=2),
        }


        print("2016收入:{}".format(a.get_year_income(2016).round(decimals=2)))
        print("2016支出:{}".format(a.get_year_spend(2016).round(decimals=2)))
        print("2017收入:{}".format(a.get_year_income(2017).round(decimals=2)))
        print("2018收入:{}".format(a.get_year_income(2018).round(decimals=2)))
        print("2017支出:{}".format(a.get_year_spend(2017).round(decimals=2)))
        print("2018支出:{}".format(a.get_year_spend(2018).round(decimals=2)))



if __name__=="__main__":
    a=AnalysisMoney()
    a.get_csv()
    # print(a.get_year(2017))
    # a.get_month_income(2018)
    a.dram_month_spend(2018)
    a.dram_month_spend(2017)
    a.draw_year_money([2017,2018])
    a.average_month()
    a.growth_rate()



