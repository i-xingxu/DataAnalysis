#coding=utf-8

import numpy as np
from common import conf,mysql,tool,logoutput
import matplotlib.pyplot as plt


class PriceAnaly():

    def __init__(self):
        my=mysql.Mysql()
        my.connect_mysql()
        self.my=my
        self.cur=my.cur
        lg=logoutput.Logger()
        self.lg=lg


    # 获取product_table_name表名称列表
    def get_table_list(self):

        tableLists=[]
        sql="select product_table_name from product_table_list where product=\'显示器\' and id=30;"

        self.cur.execute(sql)
        tableList=self.cur.fetchall()
        for tbname in tableList:
            tableLists.append(tbname[0])
        # self.lg.info(tableLists)
        tableLists=np.array(tableLists)
        return tableLists


    def get_table_data(self,name):
        if len(name)==0:
            return -1
        else:
            for x in np.nditer(name):
                sql='''select * from {tbname};'''.format(tbname=x)
                self.cur.execute(sql)
                datas=np.array(self.cur.fetchall())
                return datas


    def data_analysis(self,datas):

        p1,p2,p3,p4,p5,p6,p7,p8=0,0,0,0,0,0,0,0
        pricrList=datas[:,2]
        pricrList=np.asarray(pricrList,dtype=np.float)
        for price in pricrList:
            if price<500:
                p1+=1
            elif price>=500 and price<1000:
                p2+=1
            elif price>=1000 and price<1500:
                p3+=1
            elif price>=1500 and price<2000:
                p4+=1
            elif price>=2000 and price<2500:
                p5+=1
            elif price>=2500 and price<3000:
                p6+=1
            elif price>=3000 and price<3500:
                p7+=1
            elif price>=3500:
                p8+=1
            else:
                return -1
        result=np.array([["0-499","500-999","1000-1499","1500-1999","2000-2499","2500-2999","3000-3499","3500以上"],[p1,p2,p3,p4,p5,p6,p7,p8]])
        return result
    def draw(self,result):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.figure()
        ylist=np.asarray(result[1],dtype=np.int)
        plt.bar(result[0],ylist)

        plt.show()



if __name__=="__main__":
    p = PriceAnaly()
    try:

        data= p.get_table_data(p.get_table_list())
        r= p.data_analysis(data)
        p.draw(r)
    finally:
        p.my.close_connect()