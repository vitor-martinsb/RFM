import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class RFM:
    '''
    
    Class to evaluate and calculate RFM for segment group of database

    '''
    
    def __init__(self,ID=[],recency=[],frequency=[],monetary=[],n_quantis=4):
        
        '''
        Configure the database of RFM

        Parameters:
                ID (numpy.array): Number of ID of each person from database
                recency (numpy.array): Time of person will be away from segmetation
                frequency (numpy.array): Number of times the person gets in the store
                monetary (numpy.array): Monetary value for each person from the bae
                n_quantis (numpy.array): Number of quantis to separate RFM
        '''

        self.n_quantis = n_quantis
        self.quantis = np.linspace(0,1,n_quantis+1)
        Data = {'Recency':recency,'Frequency':frequency,'Monetary':monetary}
        if len(ID) == 0:
            self.RFM_segment = pd.DataFrame(Data)
        else:
            self.RFM_segment = pd.DataFrame(Data,ID)

        quantiles = self.RFM_segment.quantile(q=self.quantis[1:-1])    
        self.quantiles = quantiles.to_dict()

    def RFMScore(self,x,p,d):
        score = 1
        for q in self.quantis[1:-1]:
            if x <= d[p][q]:
                return score
            else:
                score = score + 1

        return score

    def join_rfm(self,x):
        '''

        Merge columns value of quantis

        Parameters:
            x (Dataframe): Value for each pareameter of RFM
        
        returns:
            Unique column of RFM

        '''
        return str(x['R']) + str(x['F']) + str(x['M'])

    def evaluate_RFM_quantis(self,plot_data=False):
        '''

        Calculate RFM based on quantis configuration

        Parameters:
            plot_data (bool): Define if will plot the results
        
        returns:
            Return dataframe with the results of RFM

        '''

        segt_map = {
            r'11': 'Novo',
            r'12': 'Novo',
            r'13': 'Campeão',
            r'14': 'Campeão',

            r'21': 'Novo',
            r'22': 'Promissor',
            r'23': 'Promissor',
            r'24': 'Campeão',

            r'31': 'Hibernando',
            r'32': 'Sonolento',
            r'33': 'Campeão',
            r'34': 'Campeão',

            r'41': 'Hibernando',
            r'42': 'Sonolento',
            r'43': 'Campeão Ausente',
            r'44': 'Campeão Ausente'
        }

        self.RFM_segment['R'] = self.RFM_segment['Recency'].apply(self.RFMScore, args=('Recency',self.quantiles,))
        self.RFM_segment['F'] = self.RFM_segment['Frequency'].apply(self.RFMScore, args=('Frequency',self.quantiles,))
        self.RFM_segment['M'] = self.RFM_segment['Monetary'].apply(self.RFMScore, args=('Monetary',self.quantiles,))
        self.RFM_segment['RFM_Segment'] = self.RFM_segment.apply(self.join_rfm, axis=1)
        self.RFM_segment['RFM_Score'] = self.RFM_segment[['R','F','M']].sum(axis=1)

        vetor_media_FM = np.round(self.RFM_segment[['F','M']].mean(axis=1).to_numpy(),decimals=0)
        vetor_media_FM = {'FM':vetor_media_FM.astype(int)}
        df_vetor_media_FM = pd.DataFrame(vetor_media_FM,self.RFM_segment.index)

        self.RFM_segment['RFM_Segment'] = self.RFM_segment['R'].map(str) + self.RFM_segment['M'].map(str)
        self.RFM_segment['RFM_Segment'] = self.RFM_segment['RFM_Segment'].replace(segt_map, regex=True)
           
        if plot_data:
            results_segments = pd.DataFrame(self.RFM_segment['RFM_Segment'].value_counts())
            label = list(results_segments.index.values)

            y = results_segments['RFM_Segment'].to_numpy()
            y = 100 * (y/(np.sum(y)))
            fig1, ax1 = plt.subplots()
            try:
                wedges, texts, autotexts = ax1.pie(y, autopct='%1.1f%%', startangle=90,textprops=dict(color="w"))
            except:
                wedges, texts, autotexts = ax1.pie(y, autopct='%1.1f%%', startangle=90,textprops=dict(color="w"))

            ax1.legend(bbox_to_anchor=(1, 0, 0.25, 1),loc="center right", title="Classes de Clientes", labels=label,borderaxespad=0)
            ax1.set_title("Classes de Clientes")
            figManager = plt.get_current_fig_manager()
            #figManager.window.showMaximized()
            #plt.savefig(fold+pie_title+'_pie'+'.png', dpi=500)

            plt.show()
        
        return self.RFM_segment
    
    def boxplot_RFM(self, opt_RFM=0, column_name = 'RFM_Segment',filliers = False):
        '''

        Boxplot of R or F or M based in subgroups of dataframe

        Parameters:
            opt_RFM (int): Define if will plot the results
            column_name (str): Column to base the subplot
            filliers (bool): Consider (True) or not (False) filliers

        '''

        if (opt_RFM < 0) & (opt_RFM > 2):
            print('opt_RFM erro: \n opt_RFM == 0 -> Recency \n opt_RFM == 1 -> Frequency \n opt_RFM == 2 -> Monetary ')
            opt_RFM = 0

        class_name = self.RFM_segment[column_name].value_counts().index.values
        df_plot = []

        for cl in class_name:
            x_label = column_name
            if opt_RFM == 0:
                df_plot.append(self.RFM_segment[self.RFM_segment[column_name] == cl]['Recency'].to_numpy())
                y_label = 'Recency'

            elif opt_RFM == 1:
                df_aux = self.RFM_segment
                df_aux = df_aux[df_aux['Frequency']>1]
                df_plot.append(df_aux[df_aux[column_name] == cl]['Frequency'].to_numpy())
                y_label = 'Frequency'

            elif opt_RFM == 2:
                df_plot.append(self.RFM_segment[self.RFM_segment[column_name] == cl]['Monetary'].to_numpy())
                y_label = 'Monetary'

        fig,ax = plt.subplots()
        ax.set_title(y_label)
        bplot1 = ax.boxplot(df_plot,
        vert=True,  # vertical box alignment
        patch_artist=True,  # fill with color
        labels=class_name,
        showfliers=filliers)  # will be used to label x-ticks
        ax.set_xticklabels(class_name,rotation=45)
        plt.show()


    def violin_RFM(self, opt_RFM=0, column_name = 'RFM_Segment'):
        '''

        Plot violin of R or F or M based in subgroups of dataframe

        Parameters:
            opt_RFM (int): Define if will plot the results
            column_name (str): Column to base the subplot

        '''

        if (opt_RFM < 0) & (opt_RFM > 2):
            print('opt_RFM warning: \n opt_RFM == 0 -> Recency \n opt_RFM == 1 -> Frequency \n opt_RFM == 2 -> Monetary ')
            opt_RFM = 0

        class_name = self.RFM_segment[column_name].value_counts().index.values
        df_plot = []

        for cl in class_name:
            x_label = column_name
            if opt_RFM == 0:
                df_plot.append(self.RFM_segment[self.RFM_segment[column_name] == cl]['Recency'].to_numpy())
                y_label = 'Recency'

            elif opt_RFM == 1:
                df_plot.append(self.RFM_segment[self.RFM_segment[column_name] == cl]['Frequency'].to_numpy())
                y_label = 'Frequency'

            elif opt_RFM == 2:
                df_plot.append(self.RFM_segment[self.RFM_segment[column_name] == cl]['Monetary'].to_numpy())
                y_label = 'Monetary'

        fig,ax = plt.subplots()
        bplot1 = ax.violinplot(df_plot)
        ax.set_title(y_label)
        ax.set_xticks(np.linspace(1,len(class_name),len(class_name)))
        ax.set_xticklabels(class_name,rotation=45)
        plt.show()
