!git clone https://github.com/PhonePe/pulse

#required libaries and module
import pandas as pd
import json
import os

import requests

def get_district_from_pincode(pincode):
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    response = requests.get(url)
    data = response.json()

    if data[0]['Status'] == 'Success':
        district = data[0]['PostOffice'][0]['District']
        return district
    else:
        return None
    
#-------------------------------------------------------------aggregated--------------------------------------------------------------------

#aggregated transaction path
path="/content/pulse/data/aggregated/transaction/country/india/state/"
aggr_state_list=os.listdir(path)
#print(aggr_state_list)

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

#aggregated user path
path_u="/content/pulse/data/aggregated/user/country/india/state/"
aggU_state_list=os.listdir(path_u)
#print(aggU_state_list)

#aggregation-->user---->state--->years--->json data to fetch
aggU_clm={'state':[],'transaction_year':[],'quater':[],'mobile_brand':[],'count':[],'percentage':[]}
for i in aggU_state_list:
  p_i=path_u+i+"/"
  aggU_yr=os.listdir(p_i)
  for j in aggU_yr:
    p_j=p_i+j+"/"
    aggU_yr_list=os.listdir(p_j)
    for k in aggU_yr_list:
      p_k=p_j+k
      data=open(p_k,'r')
      d=json.load(data)
      Data=d['data']['usersByDevice']
      if Data is not None:
        for z in Data:
          brand=z['brand']
          count=int(z['count'])
          percentage=float(z['percentage'])
          aggU_clm['state'].append(i)
          aggU_clm['transaction_year'].append(int(j))
          aggU_clm['quater'].append(int(k.strip('.json')))
          aggU_clm['mobile_brand'].append(brand)
          aggU_clm['count'].append(count)
          aggU_clm['percentage'].append(percentage)
#successfully created usable dict
aggr_user=pd.DataFrame(aggU_clm)

#---------------------------------------------------------------map-------------------------------------------------------------------------

#map transaction path
path1="/content/pulse/data/map/transaction/hover/country/india/state/"
map_state_list=os.listdir(path1)
#print(map_state_list)

#map-->transation---->state--->years--->json data to fetch
map_clm={'state':[],'transaction_year':[],'quater':[],'transaction_places':[],'transaction_count':[],'transaction_amount':[]}
for i in map_state_list:
  p1_i=path1+i+"/"
  map_yr=os.listdir(p1_i)
  for j in map_yr:
    p1_j=p1_i+j+"/"
    map_yr_list=os.listdir(p1_j)
    for k in map_yr_list:
      p1_k=p1_j+k
      data=open(p1_k,'r')
      d=json.load(data)
      for z in d['data']['hoverDataList']:
        name=z['name']
        count=int(z['metric'][0]['count'])
        amount=int(z['metric'][0]['amount'])
        map_clm['state'].append(i)
        map_clm['transaction_year'].append(int(j))
        map_clm['quater'].append(int(k.strip('.json')))
        map_clm['transaction_places'].append(name)
        map_clm['transaction_count'].append(count)
        map_clm['transaction_amount'].append(amount)
#successfully created usable dict
map_trans=pd.DataFrame(map_clm)

#map user path
path_u1="/content/pulse/data/map/user/hover/country/india/state/"
mapU_state_list=os.listdir(path_u1)
#print(mapU_state_list)

#map-->user---->state--->years--->json data to fetch
mapU_clm={'state':[],'transaction_year':[],'quater':[],'district':[],'registered_user':[],'app_opens':[]}
for i in mapU_state_list:
  p_i=path_u1+i+"/"
  mapU_yr=os.listdir(p_i)
  for j in mapU_yr:
    p_j=p_i+j+"/"
    mapU_yr_list=os.listdir(p_j)
    for k in mapU_yr_list:
      p_k=p_j+k
      data=open(p_k,'r')
      d=json.load(data)
      for district,values in d['data']['hoverData'].items():
        District=district
        registered_user=values['registeredUsers']
        app_opens=values['appOpens']
        mapU_clm['state'].append(i)
        mapU_clm['transaction_year'].append(j)
        mapU_clm['quater'].append(int(k.strip('.json')))
        mapU_clm['district'].append(District)
        mapU_clm['registered_user'].append(registered_user)
        mapU_clm['app_opens'].append(app_opens)
#successfully created usable dict
map_users=pd.DataFrame(mapU_clm)

#-------------------------------------------------------------top--------------------------------------------------------------------------

#top transaction path
path2="/content/pulse/data/top/transaction/country/india/state/"
top_state_list=os.listdir(path2)
top_state_list

#top-->transation---->state--->years--->json data to fetch
top_clm={'state':[],'transaction_year':[],'districts':[],'quater':[],'transaction_count':[],'transaction_amount':[]}
for i in top_state_list:
  p2_i=path2+i+"/"
  top_yr=os.listdir(p2_i)
  for j in top_yr:
    p2_j=p2_i+j+"/"
    top_yr_list=os.listdir(p2_j)
    for k in top_yr_list:
      p2_k=p2_j+k
      data=open(p2_k,'r')
      d=json.load(data)
      for z in d['data']['districts']:
        districts=z['entityName']
        count=z['metric']['count']
        amount=z['metric']['amount']
        top_clm['state'].append(i)
        top_clm['transaction_year'].append(j)
        top_clm['quater'].append(int(k.strip('.json')))
        top_clm['districts'].append(districts)
        top_clm['transaction_count'].append(count)
        top_clm['transaction_amount'].append(amount)
      data=d['data']['pincodes']
      if  data is not None:
        for z in d['data']['pincodes']:
          pincode=get_district_from_pincode(z['entityName'])
          count=z['metric']['count']
          amount=z['metric']['amount']
          top_clm['state'].append(i)
          top_clm['transaction_year'].append(j)
          top_clm['quater'].append(int(k.strip('.json')))
          top_clm['districts'].append(pincode)
          top_clm['transaction_count'].append(count)
          top_clm['transaction_amount'].append(amount)
#successfully created usable dict
top_trans=pd.DataFrame(top_clm)

#top user path
path_u2="/content/pulse/data/top/user/country/india/state/"
topU_state_list=os.listdir(path_u2)
topU_state_list

#top-->user---->state--->years--->json data to fetch
topU_clm={'state':[],'transaction_year':[],'quater':[],'district':[],'registered_user':[]}
for i in topU_state_list:
  p_i=path_u2+i+"/"
  topU_yr=os.listdir(p_i)
  for j in topU_yr:
    p_j=p_i+j+"/"
    topU_yr_list=os.listdir(p_j)
    for k in topU_yr_list:
      p_k=p_j+k
      data=open(p_k,'r')
      d=json.load(data)
      for z in d['data']['districts']:
        district=z['name']
        registered_user=z['registeredUsers']
        topU_clm['state'].append(i)
        topU_clm['transaction_year'].append(j)
        topU_clm['quater'].append(int(k.strip('.json')))
        topU_clm['district'].append(district)
        topU_clm['registered_user'].append(registered_user)
      data=d['data']['pincodes']
      if  data is not None:
        for z in d['data']['pincodes']:
          pincode=get_district_from_pincode(z['name'])
          topU_clm['state'].append(i)
          topU_clm['transaction_year'].append(j)
          topU_clm['quater'].append(int(k.strip('.json')))
          topU_clm['district'].append(pincode)
          topU_clm['registered_user'].append(registered_user)
#successfully created usable dict
top_users=pd.DataFrame(topU_clm)

#create CSV file
#df to Csv
aggr_trans.to_csv('aggregated_transaction.csv',index=False)

aggr_user.to_csv("aggregated_user.csv",index=False)

map_trans.to_csv("map_transaction.csv",index=False)

map_users.to_csv("map_user.csv",index=False)

top_trans.to_csv("top_transaction.csv",index=False)

top_users.to_csv("top_user.csv",index=False)
