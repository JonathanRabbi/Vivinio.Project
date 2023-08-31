import sqlite3
import pandas as pd
import plotly.express as px

conn = sqlite3.connect("vivino.db")
cursor = conn.cursor()

# Question 1: We want to highlight 10 wines to increase our sales. Which ones should we choose and why?
# FOR VINTAGE WINES: HIGH PRICE
cursor.execute('''SELECT DISTINCT vintages.name, vintages.ratings_average, vintages.ratings_count, vintages.price_euros 
               FROM vintages 
               WHERE vintages.ratings_count > 500
               ORDER BY  vintages.price_euros DESC, vintages.ratings_average DESC,vintages.ratings_count DESC
               LIMIT 10;''')
data = cursor.fetchall()
cols = ['vintage_name', 'rating_average', 'rating_count', 'price_vintage']
df1 = pd.DataFrame(data, columns=cols)
df1['revenue_vintages'] = df1['rating_count'] * df1['price_vintage']

# TOTAL RATING COUNT OF EXCLUSIVE VINTAGES
df1_sorted = df1.sort_values(by='rating_count', ascending=False)
fig = px.bar(df1_sorted, x='vintage_name', y='rating_count', title='TOP 10: Total rating Count of exclusive Vintages')

fig.update_layout(
    yaxis_title='Rating Count',
    xaxis_title='Vintage Name',
    title_x=0.5
)

# fig.update_traces(text=df1['rating_count'], textposition='inside')
fig.update_traces(
    text=df1_sorted.apply(
        lambda row: f"{row['rating_count']}<br><span style='color: yellow;'>€ {row['price_vintage']:.2f} / unit</span>",
        axis=1
    ),
    textposition='inside'
)

#TOTAL REVENUE OF EXCLUSIVE WINES
df2_sorted = df1.sort_values(by='revenue_vintages', ascending=False)
fig2 = px.bar(df2_sorted, x='vintage_name', y='revenue_vintages', title='TOP 10: Highest revenue to date of highly rated exclusive Vintages')

fig2.update_layout(
    yaxis_title='Total Revenue To Date (million €)',
    xaxis_title='Vintage Name',
    title_x=0.5
)

fig2.update_traces(
    text=df2_sorted.apply(
        lambda row: f"€ {row['revenue_vintages']/1000000:.2f} m<br><span style='color: yellow;'>€ {row['price_vintage']:.2f} / unit</span>",
        axis=1
    ),
    textposition='inside'
)

#ADDING LOW END WINES 
cursor.execute('''SELECT DISTINCT vintages.name, vintages.ratings_average, vintages.ratings_count, vintages.price_euros 
               FROM vintages 
               WHERE vintages.ratings_count > 500
               ORDER BY vintages.ratings_count DESC, vintages.ratings_average DESC
               LIMIT 10;''')
data = cursor.fetchall()
cols = ['vintage_name', 'rating_average', 'rating_count', 'price_vintage']
df3 = pd.DataFrame(data, columns=cols)
df3['revenue_vintages'] = df3['rating_count'] * df3['price_vintage']

merged_df = pd.concat([df1,df3]) 
sorted_df = merged_df.sort_values(by='revenue_vintages', ascending=False)


sorted_df = sorted_df.head(10)
fig3 = px.bar(sorted_df, x='vintage_name', y='revenue_vintages', title='TOP 10: Highest revenue to date of highest rated wines (total ratings > 500)')

fig3.update_layout(
    yaxis_title='Total revenue to date (million €)',
    xaxis_title='Vintage Name',
    title_x=0.5
)

fig3.update_traces(
    text=sorted_df.apply(
        lambda row: f"€ {row['revenue_vintages']/1000000:.2f} m<br><span style='color: yellow;'>€ {row['price_vintage']:.2f} / unit</span>",
        axis=1
    ),
    textposition='inside'
)

# Question 2: What country should we focus on?
# Answer: FOCUS ON FRANCE:given the highest revnue per country
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
df4 = pd.DataFrame(data, columns=cols)
df4['revenue_vintages'] = df4['rating_count'] * df4['price_vintage']

df4_sorted = df4.sort_values(by='revenue_vintages', ascending=False)
fig4 = px.bar(df4_sorted, x='vintage_name', y='revenue_vintages', color='country', title='TOP 10: Highest revenue to date of highest rated wines (total ratings > 500)')

fig4.update_layout(
    yaxis_title='Total Revenue To Date (million €)',
    xaxis_title='Vintage Name',
    title_x=0.5 # Adjust bottom margin to make space for text annotations
)

#fig.update_traces(text=df3_sorted['revenue_vintages'].apply(lambda x: f"€ {x/1000000:.2f} m"), textposition='inside')
for trace in fig4.data:
    text_positions = []
    for i, (y, country) in enumerate(zip(trace.y, df4_sorted['country'])):
        if country == trace.name:
            text_positions.append(y)  # Adjust the value for proper placement
        else:
            text_positions.append(y)  # Adjust the value for proper placement
    trace.text = [f'€ {x/1000000:.2f} m' for x in text_positions]
    trace.textposition = 'inside'

# Question 4-5: specific combination of tastes
test = '''
SELECT 
    GROUP_CONCAT(DISTINCT keywords.name) AS mixed_tastes,
    GROUP_CONCAT(DISTINCT keywords_wine.group_name) AS taste_group,
    COUNT(DISTINCT keywords.name) AS count_of_tastes
FROM 
    wines
JOIN 
    regions ON wines.region_id = regions.id
JOIN 
    countries ON regions.country_code = countries.code
JOIN 
    keywords_wine ON wines.id = keywords_wine.wine_id
JOIN 
    keywords ON keywords_wine.keyword_id = keywords.id
WHERE 
    keywords.name IN ('coffee', 'toast', 'green apple', 'cream', 'citrus')
AND 
    keywords_wine.count > 10  -- More than 10 users confirmed the keywords
AND 
    keywords_wine.keyword_type = 'primary'
GROUP BY
    wines.name
HAVING 
    COUNT(DISTINCT keywords.name) >= 2
ORDER BY count_of_tastes DESC, mixed_tastes DESC
'''
cursor.execute(test)
data = cursor.fetchall()

cols = ['mixed_tastes', 'taste_groups', 'count_mixed_tastes']
df_13 = pd.DataFrame(data, columns=cols)
# pd.set_option('display.max_rows', None)  # Display all rows
# df_13.head(3)
# Assuming you already have the DataFrame named df
# Calculate the percentage of items for each count
count_percentage = df_13['taste_groups'].value_counts(normalize=True) * 100

# Filter labels and percentages for slices with percentage > 2.5%
filtered_data = count_percentage[count_percentage > 2.5]

# Create a DataFrame for the filtered data
filtered_df = pd.DataFrame({'Taste Groups': filtered_data.index, 'Percentage': filtered_data.values})

# Create a pie chart using Plotly Express
fig5 = px.pie(
    data_frame=filtered_df,
    values='Percentage',
    names='Taste Groups',
    title='Percentage of each taste group',
    labels={'Taste Groups': 'Taste Groups'},
    hover_data={'Percentage': ':.1f%'}
)

# Center the legend to the right of the pie chart
fig5.update_layout(legend_title_text='Taste Groups', legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1))


# pd.set_option('display.max_rows', None)

# Question 5:    Find the top 3 most common grape all over the world and for each grape. Give us the 5 best rated wines. - IGNORE CANNOT BE ANSWERED
query1 = """SELECT most_used_grapes_per_country.grape_id, grapes.name, most_used_grapes_per_country.wines_count, COUNT(most_used_grapes_per_country.grape_id) AS grapeCount
             FROM most_used_grapes_per_country
             JOIN grapes ON most_used_grapes_per_country.grape_id = grapes.id
             GROUP BY grape_id
             ORDER BY grapeCount DESC, wines_count DESC
             LIMIT 5
             """ 
cursor.execute(query1)
data = cursor.fetchall()
cols = ['grape_id', 'grape_name', 'wines_count', 'count']
df5 = pd.DataFrame(data, columns=cols)

# Question 6: We would to give create a country leaderboard, give us a visual that shows the average wine rating for each country. Do the same for the vintages.
cursor.execute( """
SELECT 
    countries.name, 
    ROUND(AVG( vintages.ratings_average),2) AS average_rating_vintage,
    ROUND(AVG(wines.ratings_average),2) AS average_rating_wine
    
FROM 
    vintages
    JOIN wines ON vintages.wine_id = wines.id
    JOIN regions ON wines.region_id = regions.id
    JOIN countries ON regions.country_code = countries.code

GROUP BY countries.name
ORDER BY average_rating_vintage DESC, average_rating_wine DESC;


    """)
data = cursor.fetchall()
cols = ['countries', 'rating_average_vintage','rating_average_wine']
df_1 = pd.DataFrame(data, columns=cols)


# BONUS QUESTION 1:

# One of our VIP client likes Cabernet Sauvignon and would like our top 5 recommendations. Which wines would you recommend to him?

cursor.execute( """SELECT vintages.name, vintages.ratings_average, vintages.ratings_count, vintages.price_euros
               FROM vintages
               JOIN wines ON wines.id = vintages.wine_id
               WHERE wines.name = 'Cabernet Sauvignon'
               AND vintages.ratings_average > 4.5
               ORDER BY vintages.price_euros DESC, vintages.ratings_average DESC,  vintages.ratings_count DESC
               LIMIT 5
             """ )

data = cursor.fetchall() 

# SCARECROW 2015 IS RANKED NUMBER ONE 
# ------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import plotly.express as px

# Create a DataFrame from the sample data

df = pd.DataFrame(data, columns=['Name', 'Rating', 'Rating Count', 'Price'])

# Sort the DataFrame by Rating Count in descending order
df = df.sort_values(by='Rating Count', ascending=False)

# Create a bar plot using Plotly Express
fig6 = px.bar(
    df,
    x='Name',
    y='Rating Count',
    color='Rating',
    hover_data=['Price'],
    text=df['Price'].apply(lambda x: f'€ {x:.2f} / unit'),  # Display the formatted price on the bars
    title='Top Cabernet Sauvignon by Rating',
    labels={'Rating Count': 'Rating Count', 'Name': 'Wine Name'}
)

# Rotate x-axis labels for better readability
fig6.update_xaxes(tickangle=-45)

# Update the positioning of the price text on the bars
fig6.update_traces(textposition='inside')


