
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Float
import sqlalchemy
import pyodbc

#import IB_API
from datetime import date

#print(pyodbc.drivers())


def get_company_ticker(name, ticker_df):
    import numpy as np
    name=name.upper()
    #ticker_df=read_tickers()
    if name in ticker_df['Ticker'].values:
        return name
    results =[]
    for alias in ticker_df['Alias'].values:
        if name in alias:
            results.append(1)
        else:
            results.append(np.nan)
    ticker_df['Query'] = pd.Series(results, index=ticker_df.index)
    ticker_df=ticker_df.dropna(subset=['Query'])
    if len(ticker_df.index)==0:
        return [None]
    elif len(ticker_df.index)==1:
        return ticker_df['Ticker'].values
    elif len(ticker_df.index)>1:
        return ticker_df['Ticker'].values

class sql():
    def __init__(self):
        #self.engine = sqlalchemy.create_engine("mssql+pyodbc://sa:Growlif123@192.168.1.24:1433/StockTips?driver={}".format(pyodbc.drivers()[0]),echo=False)
        self.engine = sqlalchemy.create_engine("mssql+pymssql://sa:Growlif123@192.168.1.108/StockTips")
        self.table_path = r'/Users/tom/Documents/StockSharks/history.csv'
        self.table = pd.read_csv(self.table_path, encoding='utf-8')
    def read_table(self, name=None):
        self.sql_table = pd.read_sql('{}'.format(name), con=self.engine, index_col=0)
        return self.sql_table
    def merge_table(self, name=None):

        #if len(self.sql_table.index) >0:
        #    self.table = pd.concat([self.table, self.sql_table], axis=0)
        #    print(self.table)
        self.table = self.table.dropna(how='all', axis=0)#.drop(columns=['index'])
        #self.table = self.table.set_index(keys='Time', drop=True)
        self.table.to_sql(name, con=self.engine, if_exists='replace')

    def insert_row(self, table_name=None, params=None):
        self.sql_table = pd.read_sql('{}'.format(table_name), con=self.engine, index_col=0)
        row_table = pd.DataFrame(columns=self.sql_table.columns, index=[0])
        for ind, col in enumerate(list(params.keys())):
            if col !='index':
                row_table[col].iloc[0] = params[col]
        self.sql_table = (pd.concat([self.sql_table, row_table], axis=0, ignore_index=True)).reset_index(drop=True)
        self.sql_table.to_sql(table_name, con=self.engine, if_exists='replace', index=False)


    def identify_live_post_ticker(self, organisations):
        import ast
        import numpy as np
        import json
        print(organisations, type(organisations))
        if organisations==set([]):
            print('bingo')
            return [None]
        self.ticker_table = pd.read_sql('Tickers', con=self.engine)

        new_alias = [ast.literal_eval(alias) for alias in self.ticker_table['Alias'].values]
        self.ticker_table['Alias'] = pd.Series(new_alias, index=self.ticker_table.index)
        tickers =[]
        if organisations == 'set()':
            tickers.append(np.nan)
        else:

            orgs=ast.literal_eval((str(organisations).strip('}')).strip('{'))
            if isinstance(orgs[0], str):
                ticker = get_company_ticker(orgs[0], self.ticker_table)
                if isinstance(ticker, np.ndarray):
                    for t in ticker:
                        tickers.append(t)
                else:
                    tickers.append(ticker)
            else:
                multi=[]
                for suborgs in orgs:
                    ticker = get_company_ticker(suborgs[0], self.ticker_table)
                    multi.append(ticker)
                for i in multi:
                    if isinstance(i, np.ndarray):
                        for subi in i:
                            tickers.append(subi)
                    else:
                        tickers.append(i)
        return tickers


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        