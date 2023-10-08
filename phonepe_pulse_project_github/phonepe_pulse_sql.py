#importing packages and libaries
import pandas as pd
import numpy as np

#postgresql connect
import psycopg2
cont=psycopg2.connect(host='localhost',user='postgres',password='basith',port=5432,database='basith')
csr=cont.cursor()

#read csv in using pandas 
df_aggr_trans=pd.read_csv("aggregated_transaction.csv")

df_aggr_user=pd.read_csv("aggregated_user.csv")

df_map_trans=pd.read_csv("map_transaction.csv")

df_map_user=pd.read_csv("map_user.csv")

df_top_trans=pd.read_csv("top_transaction.csv")

df_top_user=pd.read_csv("top_user.csv")


#create tables
csr.execute("""create table if not exists aggregated_transaction(State varchar(40),
            Transaction_Year int,
            Quater int,
            Transaction_Type  varchar(50),
            Transaction_Count bigint,
            Transaction_Amount double precision)""")
cont.commit()

csr.execute("""create table if not exists aggregated_user(State varchar(40),
            Transaction_Year int,
            Quater int,
            Mobile_Brand  varchar(50),
            Count bigint,
            Percentage double precision)""")
cont.commit()

csr.execute("""create table if not exists map_transaction(State varchar(40),
            Transaction_Year int,
            Quater int,
            District  varchar(50),
            Transaction_Count bigint,
            Transaction_Amount double precision)""")
cont.commit()

csr.execute("""create table if not exists map_user(State varchar(40),
            Transaction_Year int,
            Quater int,
            District varchar(50),
            Registered_user bigint,
            App_opens bigint)""")
cont.commit()

csr.execute("""create table if not exists top_transaction(State varchar(40),
            Transaction_Year int,
            District  varchar(50),
            Quater int,
            Transaction_Count bigint,
            Transaction_Amount double precision)""")
cont.commit()

csr.execute("""create table if not exists top_user(State varchar(40),
            Transaction_Year int,
            Quater int,
            District varchar(50),
            Registered_user bigint)""")
cont.commit()


#insert df to sql
def insert_sql():
    #table aggregated transaction
    query = """INSERT INTO aggregated_transaction (State, Transaction_Year, Quater, Transaction_Type, Transaction_Count, Transaction_Amount)VALUES (%s, %s, %s, %s, %s, %s)"""
    for index, row in df_aggr_trans.iterrows():
        csr.execute(query, tuple(row))
    cont.commit()

    #table aggregated user
    query = """INSERT INTO aggregated_user (State, Transaction_Year, Quater, Mobile_Brand, Count, Percentage)VALUES (%s, %s, %s, %s, %s, %s)"""
    for index, row in df_aggr_user.iterrows():
        csr.execute(query, tuple(row))
    cont.commit()

    #table map transaction
    query = """INSERT INTO map_transaction (State, Transaction_Year, Quater, District, Transaction_Count, Transaction_Amount)VALUES (%s, %s, %s, %s, %s, %s)"""
    for index, row in df_map_trans.iterrows():
        csr.execute(query, tuple(row))
    cont.commit()

    #table map user
    query = """INSERT INTO map_user (State, Transaction_Year, Quater, District, Registered_user, App_opens)VALUES (%s, %s, %s, %s, %s, %s)"""
    for index, row in df_map_user.iterrows():
        csr.execute(query, tuple(row))
    cont.commit()

    #table top transaction
    query = """INSERT INTO top_transaction (State, Transaction_Year,  District, Quater, Transaction_Count, Transaction_Amount)VALUES (%s, %s, %s, %s, %s, %s)"""
    for index, row in df_top_trans.iterrows():
        csr.execute(query, tuple(row))
    cont.commit()

    #table top user
    query = """INSERT INTO top_user (State, Transaction_Year, Quater, District, Registered_user)VALUES (%s, %s, %s, %s, %s)"""
    for index, row in df_top_user.iterrows():
        csr.execute(query, tuple(row))
    cont.commit()
#sql=insert_sql()
