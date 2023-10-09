# Phonepe Pulse Data Visualization from 2018-2023 phonepe data's using SQL,Python,Streamlit,Gitclone,Pandas,Plotly 

### Introduction:
-PhonePe has become one of the most popular digital payment platforms in India, with millions of users relying on it for their day-to-day transactions. The app is known for its simplicity, user-friendly interface, and fast and secure payment processing. It has also won several awards and accolades for its innovative features and contributions to the digital payments industry.

-We create a web app to analyse the Phonepe transaction and users depending on various Years, Quarters, States, and Types of transaction and give a Geographical and Geo visualization output based on given requirements.

-" Disclaimer:-This data between 2018 to 2023 in INDIA only "

#### Importing required libraries
```python
#import libaries
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import requests
import json
```
#### if the module shows any error or module not found it can be overcome by using below command
```python
pip install<module name>
```
### In order to get the data clone the github 
- Inorder to clone the github data into to working environment use below command
```python
!git clone https://github.com/PhonePe/pulse
```
```python
import requests
#aggregated transaction path
path="/content/pulse/data/aggregated/transaction/country/india/state/"
aggr_state_list=os.listdir(path)
```
### Fetch data & Creating csv file 
- after cloning the data from github the dat in the form of json file
- In order to convert json file into data frame we use below code to another 2 folders
```python
#aggregation-->transation---->state--->years--->json data to fetch
aggr_clm={'state':[],'year':[],'quater':[],'transaction_type':[],'transaction_count':[],'transaction_amount':[]}
for i in aggr_state_list:
  p_i=path+i+"/"
  aggr_yr=os.listdir(p_i)
  for j in aggr_yr:
    p_j=p_i+j+"/"
    aggr_yr_list=os.listdir(p_j)
    for k in aggr_yr_list:
      p_k=p_j+k
      data=open(p_k,'r')
      d=json.load(data)
      for z in d['data']['transactionData']:
        name=z['name']
        count=z['paymentInstruments'][0]['count']
        amount=z['paymentInstruments'][0]['amount']
        aggr_clm['state'].append(i)
        aggr_clm['year'].append(j)
        aggr_clm['quater'].append(int(k.strip('.json')))
        aggr_clm['transaction_type'].append(name)
        aggr_clm['transaction_count'].append(count)
        aggr_clm['transaction_amount'].append(amount)
#successfully created usable dict
aggr_trans=pd.DataFrame(aggr_clm)
```
```python
#create CSV file
#df to Csv
aggr_trans.to_csv('aggregated_transaction.csv',index=False)
```
#### Create Table and Insert into Postgresql
- After creating dataframe insert the dataframe into sql  inner server by using postgresql
- To Establish the connection with sql server
- below table to reference another tables 
```python
#postgresql connect
import psycopg2
cont=psycopg2.connect(host='localhost',user='postgres',password='basith',port=5432,database='basith')
csr=cont.cursor()
```

```python
#create tables
csr.execute("""create table if not exists aggregated_transaction(State varchar(--),
            Transaction_Year int,
            Quater int,
            Transaction_Type  varchar(--),
            Transaction_Count bigint,
            Transaction_Amount double precision)""")
```
```python
#insert df to sql
#table aggregated transaction
query="""INSERTINTO aggregated_transaction(State,Transaction_Year,Quater,Transaction_Type,
      Transaction_Count,Transaction_Amount)VALUES(%s,%s,%s,%s,%s,%s)"""
for index, row in df_aggr_trans.iterrows():
  csr.execute(query, tuple(row))
cont.commit()
```
#### Creating Sql Querys and Plot the data to visualization
- Create sql queries to fetch the data as per the user requirement
- plot the data to visualization in streamlit dashboard
```python
SELECT * FROM "Table"
WHERE "Condition"
GROUP BY "Columns"
ORDER BY "Data"
```
### To Ploting code model
-using plotly express
```python
fig = px.bar(df_trans_query_result1, x = 'State', y ='Transaction_amount', color ='Transaction_amount', hover_name = 'Transaction_count',color_continuous_scale = 'sunset',title = 'All Transaction Analysis Chart', height = 700,)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.write("hover_name:(Transaction count)")
                    st.plotly_chart(fig,use_container_width=True)
```
- create the streamlit app with basic tabs [Reference](https://docs.streamlit.io/library/api-reference)
- visualizing the data with plotly and streamlit
- streamlit run <filename.py> to run terminal
#### I hope this project helps you to the understand more about phonepe data

