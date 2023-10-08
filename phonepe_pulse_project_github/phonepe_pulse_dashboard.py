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

#postgresql connect
import psycopg2
cont=psycopg2.connect(host='localhost',user='postgres',password='basith',port=5432,database='basith')
csr=cont.cursor()

#request geo state
def geo():

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data_geo = json.loads(response.content)
    geo_state = [i['properties']['ST_NM'] for i in data_geo['features']]
    geo_state.sort(reverse=False)
    return geo_state

 # dictof equate geo state and original state
def state_dict(data):
    original=data
    geo_state=geo()
    data = {}
    for i in range(0,len(original)):
      data[original[i]]=geo_state[i]
    return data

def state_list(data):
    original=data
    data_dict=state_dict(data)
    missed = set(original).symmetric_difference(set(data_dict))
    missed = list(missed)

    if len(missed) > 0:
     for i in missed:
        del data_dict[i]
    return list(data_dict.values())

#creating option menu
icon = Image.open("phonepe.jpg")
st.set_page_config(page_title="Phonepe Pulse| by Mohamedbasith",
page_icon= icon,layout='wide',initial_sidebar_state="expanded",menu_items={'About': """# This app is created by *Mohamed Basith!*"""},)
st.header(":violet[Phonepe Pulse Data Visualization!!!:money_with_wings: :chart_with_upwards_trend::rocket:]")
st.title("")

selected = option_menu(
    menu_title = None,
    options = ["Home","Basic Insights","Analysis","About"],
    icons =["house","rocket","bar-chart","toggles"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white","size":"cover"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#B877FC"},
        "nav-link-selected": {"background-color": "#6F36AD"}
    }

)

if selected == "Home":
    col1,col2, = st.columns(2)
    with col1:
        st.image("phn1.png")
        st.markdown("##### ⭐ ***PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India.***")
        st.markdown("##### ⭐***PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer.***")
        st.markdown("##### ⭐***The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016.***")
        st.markdown("##### ⭐***It is owned by Flipkart, a subsidiary of Walmart.***")
        st.info("DOWNLOAD THE APP NOW: 👉[https://www.phonepe.com/app-download/]")
    with col2:
        col1,col2, = st.columns(2)
        with col1:
            st.image("ph22.png")
            st.image("phonepe11.png")
        with col2:
            st.image("ph331.png")
            st.image("phonepe22.png")

if selected == "Basic Insights":
        st.image("phn11.png")
        st.title("BASIC INSIGHTS")
        st.title("")
        st.subheader("Let's know some basic insights about the data")
        options = ["--select--","Which brand has more phonepe users?  Show its top 10  brand and its user counts",
                   "What are the type of transaction and its corresponding number and amount",
                   "Top 10 average transaction_amount and corresponding year and district",
                   "Lowest 10  app opens average and their corresponding year, amount of registered users and state",
                   "Top 10 average transaction amount and their corresponding  district,quater and transaction year",
                   "Top most sum of registered user and their corresponding states"]
        select = st.selectbox("Select the option",options)
        if select=="What are the type of transaction and its corresponding number and amount":
            csr.execute("""select transaction_type,sum(transaction_amount) as transaction_amount,sum(transaction_count)as transaction_count from aggregated_transaction group by transaction_type""")
            df = pd.DataFrame(csr.fetchall(),columns=['Transaction_type','Transaction_amount','Transaction_count'])
            tab1, tab2 = st.tabs(["DATAFRAME","PLOTLY"])
            with tab1:
                st.write(df)
            with tab2:
                st.subheader("What are the type of transaction and its corresponding number and amount")
                fig = px.bar(df, x = 'Transaction_type', y = 'Transaction_amount', color = 'Transaction_type')
                fig.update_layout(width=600, height=500)
                tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
                with tab1:
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                with tab2:
                    st.plotly_chart(fig, theme=None, use_container_width=True)

        elif select=="Which brand has more phonepe users?  Show its top 10  brand and its user counts":
            csr.execute("""select mobile_brand,max(count) as user_count from aggregated_user group by mobile_brand order by user_count desc limit 10""")
            df = pd.DataFrame(csr.fetchall(),columns=['Mobile_brand','User_count'])
            tab1, tab2 = st.tabs(["DATAFRAME","PLOTLY"])
            with tab1:
                st.write(df)
            with tab2:
                st.subheader("Which brand has more phonepe users?  Show its top 10  brand and its user counts")
                #fig = px.histogram(df,x = 'User_count',color = 'Mobile_brand')
                fig = px.pie(df, names = 'Mobile_brand', values = 'User_count', hole = 0.4)
                fig.update_layout(width=800, height=600)
                tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
                with tab1:
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                with tab2:
                    st.plotly_chart(fig, theme=None, use_container_width=True)

        elif select=="Top 10 average transaction_amount and corresponding year and district":
            csr.execute("""select district,transaction_year,avg(transaction_amount)as total_transaction_amount from map_transaction group by district,transaction_year order by total_transaction_amount desc limit 10""")
            df = pd.DataFrame(csr.fetchall(),columns=['District','Transaction_year','Total_transaction_amount'])
            tab1, tab2 = st.tabs(["DATAFRAME","PLOTLY"])
            with tab1:
                st.write(df)
            with tab2:
                st.subheader("Top 10 average transaction_amount and corresponding year and district")
                fig = px.sunburst(df, path = ["District","Transaction_year"], values = 'Total_transaction_amount')
                fig.update_layout(width=800, height=600)
                tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
                with tab1:
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                with tab2:
                    st.plotly_chart(fig, theme=None, use_container_width=True)

        elif select=="Lowest 10  app opens average and their corresponding year, amount of registered users and state":
            csr.execute("""select state,transaction_year,avg(app_opens) as app_opens,sum(registered_user) as registered_user from map_user  group by state,transaction_year order by app_opens asc limit 10""")
            df = pd.DataFrame(csr.fetchall(),columns=['State','Transaction_year','App_opens','Registered_user'])
            tab1, tab2 = st.tabs(["DATAFRAME","PLOTLY"])
            with tab1:
                st.write(df)
            with tab2:
                st.subheader("Lowest 10  app opens average and their corresponding year, amount of registered users and state")
                fig = px.bar(df, x = 'State', y = 'Registered_user',color ='State',hover_name = 'App_opens')
                fig.update_layout(width=800, height=500)
                fig.layout.title.text = "APP_OPENS(represent no: 0 / above 1)"
                tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
                with tab1:
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                with tab2:
                    st.plotly_chart(fig, theme=None, use_container_width=True)

        elif select=="Top 10 average transaction amount and their corresponding  district,quater and transaction year":
            csr.execute("""select district,quater,transaction_year,avg(transaction_amount) as avg_transaction_amount from top_transaction group by district,quater,transaction_year order by avg_transaction_amount desc limit 10""")
            df = pd.DataFrame(csr.fetchall(),columns=['District','Quater','Transaction_year','Avg_transaction_amount'])
            tab1, tab2 = st.tabs(["DATAFRAME","PLOTLY"])
            with tab1:
                st.write(df)
            with tab2:
                st.subheader("Top 10 average transaction amount and their corresponding  district,quater and transaction year")
                fig = px.pie(df, names = 'District', values = 'Avg_transaction_amount',hole=0.4)
                fig.update_layout(width=800, height=600)
                tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
                with tab1:
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                with tab2:
                    st.plotly_chart(fig, theme=None, use_container_width=True)

        elif select=="Top most sum of registered user and their corresponding states":
            csr.execute("""select state,sum(registered_user) as registered_user from top_user group by state order by registered_user desc limit 10""")
            df = pd.DataFrame(csr.fetchall(),columns=['State','Registered_user'])
            tab1, tab2 = st.tabs(["DATAFRAME","PLOTLY"])
            with tab1:
                st.write(df)
            with tab2:
                st.subheader("Top most sum of registered user and their corresponding states")
                fig=px.bar(df,x="State",y="Registered_user",color="State")
                fig.update_layout(width=800, height=500)
                tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
                with tab1:
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                with tab2:
                    st.plotly_chart(fig, theme=None, use_container_width=True)

if selected == "Analysis":
        st.image("phn11.png")
        st.title("ANALYSIS")
        st.info('**(Note)**:-This data between **2018** to **2023** in **INDIA**')
        option = st.radio('**Select your option**',('All India(aggregated)', 'State wise(map)','Top Ten categories(top)'),horizontal=True)
        if option == 'All India(aggregated)':
            tab111, tab222 = st.tabs(['Transaction','User'])
            # ---------------------------------------       /     All India Transaction        /        ------------------------------------ #
            with tab111:
                col1, col2, col3 = st.columns(3)
                with col1:
                    trans_year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='trans_year')
                with col2:
                    trans_quarter = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='trans_quarter')
                with col3:
                    trans_tr_type = st.selectbox('**Select Transaction type**', ('Recharge & bill payments','Peer-to-peer payments',
                    'Merchant payments','Financial Services','Others'),key='trans_tr_type')

                # SQL Query
                # Aggregated Transaction Analysis Bar chart query
                csr.execute(f"SELECT State,Transaction_amount,Transaction_count FROM aggregated_transaction WHERE Transaction_year = '{trans_year}' AND Quater = '{trans_quarter}' AND Transaction_type = '{trans_tr_type}';")
                trans_query_result = csr.fetchall()
                df_trans_query_result = pd.DataFrame(np.array(trans_query_result), columns=['State','Transaction_amount','Transaction_count'])
                df_trans_query_result1 = df_trans_query_result.set_index(pd.Index(range(1, len(df_trans_query_result)+1)))
                
                tab11,tab12,tab13 = st.tabs(['GEO Visual-plotly','PIE Chart-Plotly','BAR Chart-Plotly'])
                with tab11:
                    tab1, tab2, = st.tabs(['Geo Visualization of India','Live Geo Visualization of India'])
                    with tab1:
                        # ------    /  Geo visualization dashboard for  User Analysis Bar chart  /   ---- #
                        df_trans_query_result1['State']=state_list(data=[i for i in df_trans_query_result1['State']])
                        fig = px.choropleth(df_trans_query_result1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM',
                                    locations='State',
                                    color='Transaction_amount',
                                    color_continuous_scale='sunset',
                                    hover_name='Transaction_count',
                                    title="Geo Visualization of India & 'All Transaction Analysis Chart'",
                                    height=900,width=700)
                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                        st.write("hover_name:(Transaction count)")
                        st.plotly_chart(fig,use_container_width=True)
                    with tab2:
                        fig =px.choropleth(df_trans_query_result1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM', 
                                    locations="State",
                                    color='Transaction_amount',
                                    hover_name='Transaction_count',
                                    color_continuous_scale=px.colors.diverging.RdYlGn,
                                    height=900,width=700,
                        title="Live Geo Visualization of India & 'All Transaction Analysis Chart'")
                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                        st.write("hover_name:(Transaction count)")
                        st.plotly_chart(fig,use_container_width=True)

                with tab12:
                    # ---------   /   All India Transaction Analysis Bar chart  /  ----- #
                    fig = px.pie(df_trans_query_result1, names = 'State', values = 'Transaction_amount',hover_name='Transaction_count',hole=0.4,title = 'All Transaction Analysis Chart')
                    fig.update_layout(width=800, height=600)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.write("hover_name:(Transaction count)")
                    st.plotly_chart(fig,use_container_width=True)
                with tab13:
                    fig = px.bar(df_trans_query_result1, x = 'State', y ='Transaction_amount', color ='Transaction_amount', hover_name = 'Transaction_count',color_continuous_scale = 'sunset',title = 'All Transaction Analysis Chart', height = 700,)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.write("hover_name:(Transaction count)")
                    st.plotly_chart(fig,use_container_width=True)

            # ---------------------------------------       /     All India User        /        ------------------------------------ #
            with tab222:
                col1, col2,col3, = st.columns(3)
                with col1:
                    user_trans_year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='user_trans_year')
                with col2:
                    user_quarter = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='user_quarter')
                with col3:
                    user_mobile_brand = st.selectbox('**Select Brand**', ("Xiaomi","Vivo","Samsung","Oppo","Realme","Others","Apple","OnePlus","Motorola","Tecno"),key='user_mobile_brand')
                
                # SQL Query
                # Aggregated User Analysis Bar chart query
                csr.execute(f"SELECT State, SUM(Count),SUM(Percentage) FROM aggregated_user WHERE Transaction_year = '{user_trans_year}' AND Quater = '{user_quarter}' AND Mobile_brand = '{user_mobile_brand}' GROUP BY State;")
                user_query_result = csr.fetchall()
                df_user_query_result = pd.DataFrame(np.array(user_query_result), columns=['State','User_Count','Percentage'])
                df_user_query_result1 = df_user_query_result.set_index(pd.Index(range(1, len(df_user_query_result)+1)))

                tab1,tab2,tab3 = st.tabs(['GEO Visual-plotly','PIE Chart-Plotly','BAR Chart-Plotly'])
                with tab1:
                    tab11, tab22, = st.tabs(['Geo Visualization of India','Live Geo Visualization of India'])
                    with tab11:
                        # ------    /  Geo visualization dashboard for  User Analysis Bar chart  /   ---- #
                        df_user_query_result1['State']=state_list(data=[i for i in df_user_query_result1['State']])
                        fig = px.choropleth(df_user_query_result1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM',
                                    locations='State',
                                    color='User_Count',
                                    hover_name='Percentage',
                                    color_continuous_scale='thermal',
                                    title="Geo Visualization of India & 'All User Analysis Chart'",
                                    height=900,width=700)
                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                        st.write("hover_name:(Percentage)")
                        st.plotly_chart(fig,use_container_width=True)
                    with tab22:
                        fig =px.choropleth(df_user_query_result1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                    featureidkey='properties.ST_NM', 
                                    locations="State",
                                    color='User_Count',
                                    hover_name='Percentage',
                                    color_continuous_scale=px.colors.diverging.RdYlGn,
                                    height=900,width=700,
                        title="Live Geo Visualization of India & 'All User Analysis Chart'")
                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                        st.write("hover_name:(Percentage)")
                        st.plotly_chart(fig,use_container_width=True)

                # ----   /   All India User Analysis Bar chart   /     -------- #
                with tab2:
                    fig = px.pie(df_user_query_result1, names = 'State', values = 'User_Count',hole=0.4,hover_name='Percentage',title = 'All User Analysis Chart')
                    fig.update_layout(width=800, height=600)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.write("hover_name:(Percentage)")
                    st.plotly_chart(fig,use_container_width=True)
                with tab3:
                    fig = px.bar(df_user_query_result1 , x = 'State', y ='User_Count', color ='User_Count',hover_name ='Percentage', color_continuous_scale = 'thermal', title = 'All User Analysis Chart', height = 700,)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.write("hover_name:(Percentage)")
                    st.plotly_chart(fig,use_container_width=True)

        elif option =='State wise(map)':
            tab3, tab4 = st.tabs(['Transaction','User'])
            # ---------------------------------       /     State wise Transaction        /        ------------------------------- # 
            with tab3:
                col1,col2,col3 = st.columns(3)
                with col1:
                    state_trans = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                    'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                    'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                    'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                    'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='state_trans')
                with col2:
                    state_trans_year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='state_trans_year')
                with col3:
                    state_trans_quarter = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='state_trans_quarter')
                
                # SQL Query
                # Map Transaction Analysis bar chart query
                csr.execute(f"SELECT District, Transaction_count,Transaction_amount FROM map_transaction WHERE State = '{state_trans}' AND Transaction_year = '{state_trans_year}' AND Quater = '{state_trans_quarter}';")
                trans_dist_query_result = csr.fetchall()
                df_trans_dist_query_result = pd.DataFrame(np.array(trans_dist_query_result), columns=['District', 'Transaction_count','Transaction_amount'])
                df_trans_dist_query_result1 = df_trans_dist_query_result.set_index(pd.Index(range(1, len(df_trans_dist_query_result)+1)))

                # -----    /   State wise Transaction Analysis bar chart   /   ------ #
                tab1, tab2 = st.tabs(['PIE Chart-Plotly','BAR Chart-Plotly'])
                with tab1:
                    fig = px.pie(df_trans_dist_query_result1, names = 'District', values = 'Transaction_count',hover_name='Transaction_amount',hole=0.4,title =' Map Transaction Analysis Chart')
                    fig.update_layout(width=800, height=600)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.write("hover_name:(Transaction amount)")
                    st.plotly_chart(fig,use_container_width=True)
                with tab2:
                    fig = px.bar(df_trans_dist_query_result1 , x = 'District', y ='Transaction_count',hover_name='Transaction_amount',color ='District', color_continuous_scale = 'sunset', title = 'Map Transaction Analysis Chart', height = 700,)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.write("hover_name:(Transaction amount)")
                    st.plotly_chart(fig,use_container_width=True)

            # -----------------------------------------       /     State wise User        /        ---------------------------------- # 
            with tab4:
                col1,col2,col3 = st.columns(3)
                with col1:
                    state_user = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                    'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                    'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                    'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                    'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='state_user')
                with col2:
                    state_user_year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='state_user_year')
                with col3:
                    state_user_quarter = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='state_user_quarter')
                
                # SQL Query
                # Map User Analysis bar chart query
                csr.execute(f"SELECT District, Registered_user,App_opens FROM map_user WHERE State = '{state_user}' AND Transaction_year = '{state_user_year}' AND Quater = '{state_user_quarter}';")
                user_dist_query_result = csr.fetchall()
                df_user_dist_query_result = pd.DataFrame(np.array(user_dist_query_result), columns=['District', 'Registered_user','App_opens'])
                df_user_dist_query_result1 = df_user_dist_query_result.set_index(pd.Index(range(1, len(df_user_dist_query_result)+1)))

                # -----    /   State wise Transaction Analysis bar chart   /   ------ #
                tab1, tab2 = st.tabs(['PIE Chart-Plotly','BAR Chart-Plotly'])
                with tab1:
                    fig = px.pie(df_user_dist_query_result1, names = 'District', values = 'Registered_user',hover_name='App_opens',hole=0.4,title = 'Map User Analysis Chart')
                    fig.update_layout(width=800, height=600)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.write("hover_name:(App_opens)")
                    st.plotly_chart(fig,use_container_width=True)
                with tab2:
                    fig = px.bar(df_user_dist_query_result1 , x = 'District', y ='Registered_user',hover_name = 'App_opens', color ='District', color_continuous_scale = 'thermal', title = 'Map User Analysis Chart', height = 700,)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.write("hover_name:(App_opens)")
                    st.plotly_chart(fig,use_container_width=True)

        # ==============================================          /     Top categories       /             =========================================== #
        else:
            tab5, tab6 = st.tabs(['Transaction','User'])
            # ---------------------------------------       /     All India Top Transaction        /        ---------------------------- #
            with tab5:
                col1,col2,col3 = st.columns(3)
                with col1:
                    top_trans_state = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                    'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                    'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                    'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                    'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='top_trans_state')
                with col2:
                    top_trans_year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='top_trans_year')
                with col3:
                    top_trans_quarter = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='top_trans_quarter')
                
                # SQL Query
                # Top Transaction Analysis bar chart query
                csr.execute(f"SELECT District, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM top_transaction WHERE State = '{top_trans_state}' AND Transaction_year = '{top_trans_year}' AND Quater = '{top_trans_quarter}' GROUP BY District ORDER BY Transaction_amount desc limit 10;")
                top_trans_query_result = csr.fetchall()
                df_top_trans_query_result = pd.DataFrame(np.array(top_trans_query_result), columns=['District', 'Top_transaction_amount','Total_transaction_count'])
                df_top_trans_query_result1 = df_top_trans_query_result.set_index(pd.Index(range(1, len(df_top_trans_query_result)+1)))

                # -----   /   All India Top Transaction Analysis Bar chart   /   ----- #
                tab1, tab2 = st.tabs(['PIE Chart-Plotly','BAR Chart-Plotly'])
                with tab1:
                    fig = px.pie(df_top_trans_query_result1, names = 'District', values = 'Top_transaction_amount',hover_name='Total_transaction_count',hole=0.4,title = 'Top Transaction Analysis Chart')
                    fig.update_layout(width=800, height=600)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.write("hover_name:(Total Transaction count)")
                    st.plotly_chart(fig,use_container_width=True)
                with tab2:
                    fig = px.bar(df_top_trans_query_result1 , x = 'District', y ='Top_transaction_amount', color ='Top_transaction_amount',hover_name='Total_transaction_count',color_continuous_scale = 'sunset', title = 'Top Transaction Analysis Chart', height = 700,)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.write("hover_name:(Total Transaction count)")
                    st.plotly_chart(fig,use_container_width=True)

            # -------------------------       /     All India Top User        /        ------------------ #
            with tab6:
                col1,col2,col3 = st.columns(3)
                with col1:
                    top_user_state = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                    'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                    'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                    'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                    'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='top_user_state')
                with col2:
                    top_user_year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023'),key='top_user_year')
                with col3:
                    top_user_quarter = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='top_user_quarter')
                
                # SQL Query
                # Top User Analysis bar chart query
                csr.execute(f"SELECT District, SUM(Registered_user) AS Top_user FROM top_user WHERE State = '{top_user_state}' AND Transaction_year = '{top_user_year}' AND Quater = '{top_user_quarter}' GROUP BY District ORDER BY Top_user DESC LIMIT 10;")
                top_user_query_result = csr.fetchall()
                df_top_user_query_result = pd.DataFrame(np.array(top_user_query_result), columns=['District', 'Top_user_count'])
                df_top_user_query_result1 = df_top_user_query_result.set_index(pd.Index(range(1, len(df_top_user_query_result)+1)))

                # -----   /   All India User Analysis Bar chart   /   ----- #
                tab1, tab2 = st.tabs(['PIE Chart-Plotly','BAR Chart-Plotly'])
                with tab1:
                    fig = px.pie(df_top_user_query_result1, names = 'District', values = 'Top_user_count',hole=0.4,title = 'Top User Analysis Chart')
                    fig.update_layout(width=800, height=600)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.plotly_chart(fig,use_container_width=True)
                with tab2:
                    fig = px.bar(df_top_user_query_result1 , x = 'District', y ='Top_user_count', color ='District', color_continuous_scale = 'thermal', title = 'Top User Analysis Chart', height = 700,)
                    fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                    st.plotly_chart(fig,use_container_width=True)

if selected == "About":
    col1,col2,col3, = st.columns(3)
    with col1:
        st.info("DOWNLOAD THE APP NOW: 👉[https://www.phonepe.com/app-download/]")
        st.image("ph22.png")

    with col2:
        st.markdown("### ***:violet[About:]***")
        st.markdown("##### ⭐ ***The Indian digital payments story has truly captured the world's imagination.***")
        st.markdown("##### ⭐ ***From the largest towns to the remotest villages.***") 
        st.markdown("##### ⭐ ***There is a payments revolution being driven by the penetration of mobile phones.***")
        st.markdown("##### ⭐ ***Mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government.***")
    with col3:
        st.markdown("##### ⭐ ***Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India.***")
        st.markdown("##### ⭐ ***PhonePe Pulse is our way of giving back to the digital payments ecosystem.***")
        st.markdown("##### ⭐ ***Phonepe Now Everywhere..!***")
        st.image("phonepe11.png")
        st.image("phonepe22.png")