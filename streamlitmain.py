import streamlitdata
import streamlit as st
import streamlit.components.v1 as components
# st.set_page_config(layout="wide") 

header = st.container()
plots = st.container()

with header: 
    st.title('Vivino Market Analysis TITLE?')
    # st.header('THIS IS HEADER')
with plots:
    st.subheader('We want to highlight 10 wines to increase our sales. Which ones should we choose and why?')
    # st.write(streamlitdata.df1)
    # st.write(streamlitdata.fig)
    # st.write(streamlitdata.fig2)
    st.write(streamlitdata.sorted_df.head(10))
    st.write(streamlitdata.fig3)
    st.subheader('We have a marketing budget for this year. Which country should we prioritise and why?')
    st.write(streamlitdata.df4)
    st.write(streamlitdata.fig4)
    st.subheader('We have detected that a big cluster of customers like a specific combination of tastes. We have identified a few primary keywords that match this. We would like you to find all the wines that have those keywords. To ensure the accuracy of our selection, ensure that more than 10 users confirmed those keywords. Also, identify the group_name related to those keywords.')
    # st.write(streamlitdata.df_3)
    st.write(streamlitdata.df_13.head(3))
    st.write(streamlitdata.fig5)
    st.subheader('We would like to select wines that are easy to find all over the world. Find the top 3 most common grape all over the world and for each grape, give us the the 5 best rated wines.')
    st.write(streamlitdata.df5)
    components.html("""<div class='tableauPlaceholder' id='viz1693473688539' style='position: relative'><noscript><a href='#'><img alt='&lt;Grape Count &gt; ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Gr&#47;Grape_LeaderBoard&#47;Sheet3&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Grape_LeaderBoard&#47;Sheet3' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Gr&#47;Grape_LeaderBoard&#47;Sheet3&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1693473688539');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>""", width=800, height=800)
    st.caption("""There is a clear link between the wines and the countries: wines.region_id --> regions.id > regions.country_code --> countries.code > most_used_grapes_per_country.country_code > grapes.name.  
        Unfortunately we cannot link the wines to grapes name because the link ends at the "most_used_grapes_per_country" node. This only shows the most_used_grapes per country (every wine from that country will have these same grapes listed even though it would not necessarily mean that one of these grapes is used to produce the wine)""")
    st.subheader('We would to give create a country leaderboard, give us a visual that shows the average wine rating for each country. Do the same for the vintages.')
    st.write(streamlitdata.df_1)
    components.html("""<div class='tableauPlaceholder' id='viz1693474804322' style='position: relative'><noscript><a href='#'><img alt='&lt;Ratings of Wine vs Vintage&gt; ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Country_LeaderBoardandGrape_LeaderBoard&#47;Sheet2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Country_LeaderBoardandGrape_LeaderBoard&#47;Sheet2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Country_LeaderBoardandGrape_LeaderBoard&#47;Sheet2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1693474804322');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>""", width=1000, height=1000)
    st.subheader("BONUS QUESTION: One of our VIP client likes Cabernet Sauvignon and would like our top 5 recommendations. Which wines would you recommend to him?")
    st.write(streamlitdata.fig6)
   