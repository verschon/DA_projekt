import pandas as pd
import streamlit as st
import plotly.graph_objects as go
#import matplotlib.pyplot as plt

df_shipments = pd.read_csv("sql_query_shipments.csv", encoding='utf-8')
df_working_days = pd.read_csv("sql_query_working_days.csv", encoding='utf-8')
df_shipments['Datum zpracování'] = pd.to_datetime(df_shipments['Datum zpracování'])
df_working_days['Datum'] = pd.to_datetime(df_working_days['Datum'])

df_shipments = df_shipments.rename(columns={'Číslo zásilky': 'Shipments_no', 'Datum zpracování': 'Processing_date'})
df_shipments = df_shipments.groupby('Processing_date')[['Shipments_no']].count().reset_index()
df_shipments['Month/day'] = df_shipments['Processing_date'].dt.strftime('%m/%d')
df_shipments = df_shipments.groupby('Month/day')[['Shipments_no']].mean().round(2).reset_index()

header = st.container()
data_input = st.container()
result_part = st.container()

with header:
    st.title('Dovolenkář')
    st.markdown('Aplikace pro načasování dovolené s ohledem na očekávané pracovní vytížení')

with data_input:
    st.header('Zadání informací')

    #1. input
    year = int(st.selectbox('Začínáme! Nejprve si vyber potřebný rok:', options = ['2022', '2023', '2024', '2025']))
    
    df_working_days['Year'] = pd.DatetimeIndex(df_working_days['Datum']).year
    df_working_days['Month/day'] = df_working_days['Datum'].dt.strftime('%m/%d')
    df_working_days['Week_no'] = df_working_days['Datum'].dt.isocalendar().week
    df_wd_year = df_working_days[(df_working_days['Year'] == year)]

    df_final_day = pd.merge(df_wd_year, df_shipments, on=['Month/day'])
    
    df_final_week = df_final_day.groupby('Week_no')[['Shipments_no']].mean().round(2)
    
    #vyselektování kompletních týdnů v roce
    week_count = df_final_day['Week_no'].value_counts().sort_index()
    df_final_wholeweek = df_final_week.assign(Week_count = week_count)
    df_final_wholeweek = df_final_wholeweek[df_final_wholeweek['Week_count'] == 5]

    #2. input
    days_off_no = st.slider('Zadej celkový počet dnů:', min_value = 1, max_value = 25, value=20, step=1)

    #3. input
    weeklist = []
    week = int((days_off_no - (days_off_no % 5))/5)
    for i in range(week+1):
        weeklist.append(i)
    whole_week_no = st.selectbox('Zvol si počet celých týdnů tzn. 5 pracovních dnů od pondělí do pátku pro delší regeneraci:', options=weeklist, index = 0)
    
    #4. input
    mode = st.radio('Už zbývá jen mód. S módem 1 se vyhneš okurkové sezóně, mód 2 tě uchrání před nejvytíženějšími dny:', ['Mód 1','Mód 2'])

    #kopie pro urceni dnů a týdnů
    df_final_wholeweek_copy = df_final_wholeweek.copy()
    df_final_day_copy = df_final_day.copy()

    #urceni týdnů - vysledne df
    df_result_week = pd.DataFrame()

    for i in range(whole_week_no):
        if mode =='Mód 1':
            result_week = df_final_wholeweek_copy['Shipments_no'].idxmin()
            df_final_wholeweek_copy = df_final_wholeweek_copy.drop(result_week)
            df_final_day_copy.drop(df_final_day_copy[df_final_day_copy['Week_no'] == result_week].index, inplace = True)
            df1 = df_final_day[(df_final_day['Week_no'] == result_week)][['Datum', 'Week_no']]
            df_result_week = pd.concat([df_result_week, df1], ignore_index = True).sort_values(by='Datum')    
        else:
            result_week = df_final_wholeweek_copy['Shipments_no'].idxmax()
            df_final_wholeweek_copy = df_final_wholeweek_copy.drop(result_week)
            df_final_day_copy.drop(df_final_day_copy[df_final_day_copy['Week_no'] == result_week].index, inplace = True)
            df1 = df_final_day[(df_final_day['Week_no'] == result_week)][['Datum', 'Week_no']]
            df_result_week = pd.concat([df_result_week, df1], ignore_index = True).sort_values(by='Datum')
    
    
    #urceni dnů - vysledne df
    df_result_days = pd.DataFrame()
    days_rest = days_off_no - (whole_week_no*5)

    for i in range(days_rest):
        if mode =='Mód 1':
            result_day_index = df_final_day_copy['Shipments_no'].idxmin()
            result_day = df_final_day_copy.at[result_day_index, 'Datum']
            df_final_day_copy.drop(df_final_day_copy[df_final_day_copy['Datum'] == result_day].index, inplace = True)
            row = df_final_day.loc[result_day_index, ['Datum','Week_no']].to_dict()
            df_row = pd.DataFrame([row])
            df_result_days = pd.concat([df_result_days, df_row], ignore_index = True).sort_values(by='Datum')
        else:
            result_day_index = df_final_day_copy['Shipments_no'].idxmax()
            result_day = df_final_day_copy.at[result_day_index, 'Datum']
            df_final_day_copy.drop(df_final_day_copy[df_final_day_copy['Datum'] == result_day].index, inplace = True)
            row = df_final_day.loc[result_day_index, ['Datum','Week_no']].to_dict()
            df_row = pd.DataFrame([row])
            df_result_days = pd.concat([df_result_days, df_row], ignore_index = True).sort_values(by='Datum')


with result_part:
    st.header('Výsledek')
    st.markdown('A je to! Ideální týdny a dny jsou připraveny. Neváhej a zabookuj si je, dokud jsou termíny volné.')
    
    #zobrazení tabulek
    tab_1, tab_2 = st.columns(2)
    tab_1.markdown('**Seznam celých týdnů:**')
    if df_result_week.empty:
        fig = go.Figure(data=[go.Table(
            header=dict(values=[['<b>Datum</b>'], ['<b>Týden</b>']],
                font=dict(color='white',size=12),
                fill_color='red',
                align='left'),
            cells=dict(values=[0, 0],
               fill_color='ghostwhite',
               align='left'))
               ])
        fig.update_layout(width=400, height=300, margin=dict(l=0,r=50,b=0,t=0))
    else:
        fig = go.Figure(data=[go.Table(
            header=dict(values=[['<b>Datum</b>'], ['<b>Týden</b>']],
                font=dict(color='white',size=12),
                fill_color='red',
                align='left'),
            cells=dict(values=[df_result_week['Datum'].dt.strftime('%d/%m/%y'), df_result_week['Week_no']],
                fill_color='ghostwhite',
                align='left'))
        ])
        fig.update_layout(width=400, height=300, margin=dict(l=0,r=50,b=0,t=0))
    tab_1.write(fig)

    tab_2.markdown('**Seznam jednotlivých dnů:**')
    if df_result_days.empty:
        fig = go.Figure(data=[go.Table(
            header=dict(values=[['<b>Datum</b>'], ['<b>Týden</b>']],
                font=dict(color='white',size=12),
                fill_color='lightpink',
                align='left'),
            cells=dict(values=[0, 0],
               fill_color='ghostwhite',
               align='left'))
               ])
        fig.update_layout(width=350, height=300, margin=dict(l=0,r=0,b=0,t=0))    
    else:
        fig = go.Figure(data=[go.Table(
            header=dict(values=[['<b>Datum</b>'], ['<b>Týden</b>']],
                font=dict(color='white',size=12),
                fill_color='lightpink',
                align='left'),
            cells=dict(values=[df_result_days['Datum'].dt.strftime('%d/%m/%y'), df_result_days['Week_no']],
                fill_color='ghostwhite',
                align='left'))
        ])
        fig.update_layout(width=350, height=300, margin=dict(l=0,r=0,b=0,t=0))
    tab_2.write(fig)

    #zobrazení grafu
    st.markdown('**Přehled vybraných termínů v roce:**')
    colors = ['darkgrey',] * 52
    if df_result_week.empty:
        go_week = 0
    else:
        go_week = df_result_week['Week_no'].unique().tolist()
        for i in range(len(go_week)):
            colors[go_week[i]-1] = 'red'
    if df_result_days.empty:
        go_days = 0
    else:
        go_days = df_result_days['Week_no'].unique().tolist()
        for i in range(len(go_days)):
            colors[go_days[i]-1] = 'lightpink'

    fig_chart = go.Figure(data=[go.Bar(
        x=df_final_week.index.values.tolist(),
        y=df_final_week['Shipments_no'].tolist(),
        marker_color=colors,
        text = df_final_week['Shipments_no'].astype(int).tolist(),
        textposition='outside',
    )])
    fig_chart.update_xaxes(tickmode='linear')
    fig_chart.update_layout(width=1000,height=500, margin=dict(l=0,r=0,b=0,t=0),
        xaxis=dict(title='Číslo týdne',titlefont_size=16),
        yaxis=dict(title='Počet zásilek',titlefont_size=16),
    )
    st.write(fig_chart)