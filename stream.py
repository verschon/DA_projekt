import streamlit as st
import pandas as pd
import plotly.graph_objects as go

header = st.container()
data_input = st.container()
result_part = st.container()




with header:
    st.title('Dovolenkář')
    st.markdown('Aplikace pro načasování dovolené s ohledem na očekávané pracovní vytížení')

with data_input:
    st.header('Zadání informací')

    #1. promenna
    year = int(st.selectbox('Začínáme! Nejprve si vyber potřebný rok:', options = ['2022', '2023', '2024', '2025']))
    
    #2. promenna
    days_off_no = st.slider('Zadej celkový počet dnů:', min_value = 1, max_value = 25, value=20, step=1)

    #3. promenna
    weeklist = []
    week = int((days_off_no - (days_off_no % 5))/5)
    for i in range(week+1):
        weeklist.append(i)
    whole_week_no = st.selectbox('Zvol si počet celých týdnů (vždy po 5 pracovních dnech) pro lepší regeneraci:', options=weeklist, index = 0)
    
    #4. promenna
    days_rest = days_off_no - whole_week_no
    
    #5. promenna
    mode = st.radio('Už zbývá jen mód. S módem 1 se vyhneš okurkové sezóně, mód 2 tě uchrání před nejvytíženějšími dny:', ['Mód 1','Mód 2'])

with result_part:
    st.header('Výsledek')
    st.markdown('A je to! Ideální týdny a dny jsou připraveny. Neváhej a zabookuj si je, dokud jsou termíny volné.')
    
    tab_1, tab_2 = st.columns(2)

    tab_1.markdown('**Přehled týdnů:**')
    #tab_1.write(data.head(10))

    tab_2.markdown('**Přehled dnů:**')
    #tab_2.write(pd.head(12))

    
    #pocty_dnu = pd.DataFrame(data['Pracovni_den'].value_counts()).head(50)
    #st.bar_chart(pocty_dnu)
    