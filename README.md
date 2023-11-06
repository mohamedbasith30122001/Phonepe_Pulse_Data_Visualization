# Phonepe Pulse Data Visualization Fintech (from 2018-2023 phonepe data's using SQL,Python,Streamlit,Gitclone,Pandas,Plotly)

## Table of Contents
- [Introduction](#introduction)
- [Domain](#Domain)
- [Problem_Statement ](#Problem_Statement )
- [Libraries](#Libraries)
-  [Problem_solution](#Problem_solution)
- [Conclusion](#Conclusion)
- 
# Introduction:
- PhonePe has become one of the most popular digital payment platforms in India, with millions of users relying on it for their day-to-day transactions. The app is known for its simplicity, user-friendly interface, and fast and secure payment processing. It has also won several awards and accolades for its innovative features and contributions to the digital payments industry.

- We create a web app to analyse the Phonepe transaction and users depending on various Years, Quarters, States, and Types of transaction and give a Geographical and Geo visualization output based on given requirements.

- " Disclaimer:-This data between 2018 to 2023 in INDIA only "
# Domain 
- Fintech
# Problem_Statement:
- The Phonepe pulse Github repository contains a large amount of data related to
various metrics and statistics. The goal is to extract this data and process it to obtain
insights and information that can be visualized in a user-friendly manner.
# Libraries
### Libraries/Modules needed for the project!
- Streamlit - (To Create Graphical user Interface)
- Psycopg2 - (To Create local database and interact with data)
- Json - (To read the data or Json files and convert Json format)
- PIL - (To Insert and Use Image)
- Pandas - (To Clean and manipulate the data)
- Numpy - (To use array and statistical value)
- Plotly - (To Create the plot)
- Requests - (To use request the another data)
# Problem_solution:
### what i did for project solution:
## workflow:
#### Step 1 :
- Python environment (Python 3.x recommended) Streamlit, Pandas,Numpy,Json,Requests,Plotly,PIL,Psycopg2 libraries installed postgresql server setup and running Features **Home**: Displays an overview of the app including technologies used and a brief description of the app. 
#### Step 2 :
- **Basic Insights**: This section allows the user to click top questions and about data informations.its displayed about data basic insights.
#### Step 3 : 
- **Analysis**: This section allows users to select which type of data information we see.To click  transaction tab in selected year,state,Transaction_type,user_mobile,state,quarter,user will click user tab in selected year,quarter,brand,state to see insights.
#### Step 4 : 
- **About** :This section allows users to knows as the phonepe company about.
## Importing required libraries
### Import Data Handling libraries
```python
import pandas as pd
import numpy as np
```
### Import Dashboard libraries
```python
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
```
### Import Clone libraries
```python
import requests
import json
```
### if the module shows any error or module not found it can be overcome by using below command
```python
pip install<module name>
```
```python
#aggregated transaction path
path="/content/pulse/data/aggregated/transaction/country/india/state/"
aggr_state_list=os.listdir(path)
```
# E T L Process

## a) Extract data

* Initially, we Clone the data from the Phonepe GitHub repository by using Python libraries.
### In order to get the data clone the github 
- Inorder to clone the github data into to working environment use below command
```python
!git clone https://github.com/PhonePe/pulse
```
## b) Process and Transform the data
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
## c) Load  data
### Create Table and Insert into Postgresql
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

# E D A Process and Frame work

## a) Access PostgreSQL DB 

* Create a connection to the postgreSQL server and access the specified postgreSQL DataBase by using **psycopg2** library
  
```python
#insert df to sql
#table aggregated transaction
query="""INSERTINTO aggregated_transaction(State,Transaction_Year,Quater,Transaction_Type,
      Transaction_Count,Transaction_Amount)VALUES(%s,%s,%s,%s,%s,%s)"""
for index, row in df_aggr_trans.iterrows():
  csr.execute(query, tuple(row))
cont.commit()
```

## b) Filter the data

* Filter and process the collected data depending on the given requirements by using SQL queries
### Creating Sql Querys and Plot the data to visualization
- Create sql queries to fetch the data as per the user requirement
- plot the data to visualization in streamlit dashboard
```python
SELECT * FROM "Table"
WHERE "Condition"
GROUP BY "Columns"
ORDER BY "Data"
```
## c) Visualization 

* Finally, create a Dashboard by using Streamlit and applying selection and dropdown options on the Dashboard and show the output are Geo visualization, bar chart, and Dataframe Table
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

# Conculsion
## Geo-visualization of Transaction datas
- To see detailed code to use plotly for Geo visualization see phonepe_pulse_dashboard.py (Geo-visualization of transacion data section)
- ### Aggregated All India T & U:
![Outlook](https://github.com/mohamedbasith30122001/Phonepe_Pulse_Data_Visualization/blob/main/phonepe_pulse_project_github/outputs_insights/all_india_data.png)
![Outlook](https://github.com/mohamedbasith30122001/Phonepe_Pulse_Data_Visualization/blob/main/phonepe_pulse_project_github/outputs_insights/all_india_user.png)

- This image insights to increase user to peer to peer payments and recharge payments.the uttar pradesh has high transaction amount and jharkand has high transaction count and lower than uttar pradesh transaction amount and uttar pradesh has transaction count was lower than jharkand

## User device analysis of Phonepe data
- ### BAR CHART ANALYSIS T & U:
![Outlook](https://github.com/mohamedbasith30122001/Phonepe_Pulse_Data_Visualization/blob/main/phonepe_pulse_project_github/outputs_insights/map_user.png)
- ### PIE CHART ANALYSIS T & U:
![Outlook](https://github.com/mohamedbasith30122001/Phonepe_Pulse_Data_Visualization/blob/main/phonepe_pulse_project_github/outputs_insights/map_pie.png)

## Top user analysis of phonepe data
- ### PIE CHART ANALYSIS T & U:
![Outlook](https://github.com/mohamedbasith30122001/Phonepe_Pulse_Data_Visualization/blob/main/phonepe_pulse_project_github/outputs_insights/top_pie.png)
- ### BAR CHART ANALYSIS T & U: 
![Outlook](https://github.com/mohamedbasith30122001/Phonepe_Pulse_Data_Visualization/blob/main/phonepe_pulse_project_github/outputs_insights/top_user.png)
- I hope this project helps you to the understand more about phonepe data
