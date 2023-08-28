import sqlite3

conn = sqlite3.connect("vivino.db")
cursor = conn.cursor()

# We want to highlight 10 wines to increase our sales. Which ones should we choose and why?
# FOR VINTAGE WINES:
cursor.execute('''SELECT DISTINCT vintages.wine_id, vintages.name, wines.ratings_average, wines.ratings_count, vintages.price_euros 
               FROM vintages 
               JOIN wines ON wines.id = vintages.wine_id
               GROUP BY wines.name
               ORDER BY wines.ratings_count DESC, wines.ratings_average DESC, vintages.price_euros ASC 
               LIMIT 10''')
cursor.fetchall()

# We have a marketing budget for this year. Which country should we prioritise and why?
# We would like to give awards to the best wineries. Come up with 3 relevant ones. Which wineries should we choose and why? Be creative ;)
# We have detected that a big cluster of customers like a specific combination of tastes. We have identified a few primary keywords that match this.
# We have detected that a big cluster of customers like a specific combination of tastes. We have identified a few primary keywords that match this. We would like you to find all the wines that have those keywords. To ensure the accuracy of our selection, ensure that more than 10 users confirmed those keywords. Also, identify the group_name related to those keywords.
