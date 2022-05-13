import streamlit as st
import pandas as pd

header = st.container()
dataset = st.container()
model = st.container()
jk = st.container()

with header:
    st.title('Dovolenkář')
    st.text('vítejte u dovolenkáře')

with dataset:
    st.header('2. část')
    st.text('další informace')
    
    st.subheader('Ukázka tabulky')
    data = pd.read_csv('Pracovni_dny.csv')
    st.write(data.head(10))
    #pocty_dnu = pd.DataFrame(data['Pracovni_den'].value_counts()).head(50)
    #st.bar_chart(pocty_dnu)

with model:
    st.header('3. část')
    st.markdown('* **First feature:** I create')

    prvni_sl, druhy_sl = st.columns(2)

    year = int(prvni_sl.radio('Rok dovolené:', ["2022", '2023', '2024','2025']))
    
    days_off_no = prvni_sl.slider('Kolik dnů dovolené máš:', min_value = 1, max_value = 25, value=20, step=1)

    weeklist = []
    week = int((days_off_no - (days_off_no % 5))/5)
    for i in range(week+1):
        weeklist.append(i)

    whole_week_no = prvni_sl.selectbox('Kolik týdnů dovolené potřenuješ v kuse', options=weeklist, index = 0)


    mode = prvni_sl.radio('zvol si mod:', ['Mod1', 'Mod2', 'Mod3"'])

with jk:
    st.header('4. část')
    st.text('halo, haloi hahahaha ahahaha ahahaha ahaha ahaha ahaha ahjaa \n djjdjdjd\n shshshshs')

    