from RFM import RFM
import pandas as pd
from datetime import datetime as dt
from tqdm import tqdm
import numpy as np
from mpl_toolkits import mplot3d
import numpy as np
import random
import matplotlib.pyplot as plt

class data:

    def __init__(self,fold='data',year_ini=2017,year_end=2018):
        self.cliente = pd.read_csv(fold+'/olist_customers_dataset.csv')
        self.payments = pd.read_csv(fold+'/olist_order_payments_dataset.csv')
        self.orders = pd.read_csv(fold+'/olist_orders_dataset.csv')

        self.orders = self.orders[self.orders['customer_id'].isin(self.cliente['customer_id'].to_numpy())]
        self.orders = self.orders[self.orders['order_status']=='delivered']
        self.orders = self.orders[(self.orders['order_approved_at'] >= str(
            year_ini)+'-01-01') & (self.orders['order_approved_at'] < str(year_end+1)+'-01-01')]
        self.payments = self.payments[self.payments['order_id'].isin(self.orders['order_id'].to_numpy())]
        self.payments = pd.merge(self.orders[['customer_id','order_id','order_approved_at']],self.payments,how='left', on='order_id')
    
    def get_RFM(self,year_end=2018):
        R = []
        F = []
        M = []
        vetor_cli = []
        str_d1 = str(year_end+1)+'-1-1'
        d1 = dt.strptime(str_d1, "%Y-%m-%d")

        for cli in tqdm(self.payments['customer_id'].to_numpy()):
            vetor_cli.append(cli)
            F.append(len(self.payments[self.payments['customer_id']==cli]))

            M.append(np.sum(self.payments[self.payments['customer_id']==cli]['payment_value']))

            df_r = self.payments[self.payments['customer_id']==cli].sort_values(by='payment_value')
            str_d2 = df_r.iloc[0]['order_approved_at']
            d2 = dt.strptime(str_d2[0:10], "%Y-%m-%d")
            R.append((d1-d2).days)

            self.data_RFM = pd.DataFrame({'customer_id':vetor_cli,'R':R,'F':F,'M':M})

if __name__ == '__main__':
    ecommerce = data()
    #ecommerce.get_RFM()
    ecommerce.data_RFM = pd.read_csv('data/RFM.csv')
    ecommerce.data_RFM.columns = ['customer_id','R','F','M']
    
    # fig = plt.figure()
    # ax = plt.axes()
    # ecommerce.data_RFM[['customer_id','R']].boxplot(showfliers=False)
    # ax.set_title('Distribuição de Recência')
    # ax.set_ylabel('Recência')
    # plt.show()

    # fig = plt.figure()
    # ax = plt.axes()
    # ecommerce.data_RFM[['customer_id','F']].boxplot(showfliers=True)
    # ax.set_title('Distribuição de Frequência')
    # ax.set_ylabel('Frequência')
    # plt.show()

    # fig = plt.figure()
    # ax = plt.axes()
    # ecommerce.data_RFM[['customer_id','M']].boxplot(showfliers=False)
    # ax.set_title('Distribuição de Monetário')
    # ax.set_ylabel('Monetário')
    # plt.show()
    
    # fig = plt.figure()
    # ax = plt.axes(projection ='3d')

    # x = ecommerce.data_RFM['R'].to_numpy() / max(ecommerce.data_RFM['R'].to_numpy())
    # y = ecommerce.data_RFM['F'].to_numpy() / max(ecommerce.data_RFM['F'].to_numpy())
    # z = ecommerce.data_RFM['M'].to_numpy() / max(ecommerce.data_RFM['M'].to_numpy())
    # c = np.arange(len(x)) / len(x)  

    # p = ax.scatter(x, y, z, c=plt.cm.viridis(0.5*c))
    # ax.set_title('Distribuição RFM normalizada de '+str(len(ecommerce.data_RFM['R']))+' clientes')
    
    # ax.set_xlabel('R', fontsize=20, rotation=60)
    # ax.set_ylabel('F', fontsize=20, rotation=60)
    # ax.set_zlabel('M', fontsize=20, rotation=60)

    # fig.colorbar(p, ax=ax)
    # plt.show()

    seg_RFM = RFM(ID=ecommerce.data_RFM['customer_id'].to_numpy(),recency=ecommerce.data_RFM['R'].to_numpy(),frequency=ecommerce.data_RFM['F'].to_numpy(),monetary=ecommerce.data_RFM['M'].to_numpy(),n_quantis=4)
    RFM_segment = seg_RFM.evaluate_RFM_quantis(plot_data=True)
    seg_RFM.boxplot_RFM(opt_RFM=0)
    seg_RFM.boxplot_RFM(opt_RFM=1)
    seg_RFM.boxplot_RFM(opt_RFM=2)

    print('Finish')
