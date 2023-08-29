import streamlit as st
import plotly
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px
conn = sqlite3.connect("vivino.db")
cursor = conn.cursor()

cursor.execute('''SELECT DISTINCT countries.name, vintages.name, vintages.ratings_average, vintages.ratings_count, vintages.price_euros 
               FROM wines
               JOIN vintages ON wine_id == wines.id
               JOIN regions ON region_id == regions.id
               JOIN countries ON regions.country_code == countries.code 
               WHERE vintages.ratings_count > 500
               ORDER BY  vintages.price_euros DESC, vintages.ratings_average DESC,vintages.ratings_count DESC
               LIMIT 10;''')
data = cursor.fetchall()
cols = ['country', 'vintage_name', 'rating_average', 'rating_count', 'price_vintage']
df3 = pd.DataFrame(data, columns=cols)
df3['revenue_vintages'] = df3['rating_count'] * df3['price_vintage']

fig = px.bar(df3, x='vintage_name', y='price_vintage', color='country', barmode='group')

# Adjust the X-axis labels
fig.update_xaxes(tickangle=65, tickmode='array', tickvals=list(range(len(df3['vintage_name'].unique()))),
                 ticktext=df3['vintage_name'].unique())

st.title('Vivinio Wine Recommendation')

st.image('images/Vivino_logo.jpg', use_column_width=False, output_format="jpg")

st.title('QUESTION 2: What country should we focus on?')
st.plotly_chart(fig, use_container_width=False)
