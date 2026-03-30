import streamlit as st 
import requests
import base64

st.set_page_config(
    page_title= 'Teams', 
    page_icon='⚽', 
    layout='wide'
)

@st.cache_data ## adicionando porque teve uma atualização e apenas utilizando st.image não estava sendo possível renderizar a imagem do jogador. 
## foi necessário criar esse função de load para poder carregar a imagem e disponibilizar. 
def load_image_64(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    data = requests.get(url, headers=headers).content
    return "data:image/png;base64," + base64.b64encode(data).decode()


def preprocess_row(url):
    if isinstance(url, str) and url.startswith("http"):
        return load_image_64(url)
    return url

df_data = st.session_state['data']

clubes = df_data['Club'].unique() 
club = st.sidebar.selectbox('Club', clubes)
df_club = df_data[df_data['Club'] == club].set_index('Name')

st.image(load_image_64(df_club["Club Logo"].iloc[0]))
st.title(df_club['Club'].iloc[0])

columns = ["Age", "Club Logo", "Photo", "Flag", "Overall", 'Value(£)', 'Wage(£)', 'Joined', 
           'Height(cm.)', 'Weight(lbs.)', 
           'Contract Valid Until', 'Release Clause(£)']

df_filter = df_club[columns]

df_filter["Photo"] = df_filter["Photo"].apply(preprocess_row)
df_filter["Flag"] = df_filter["Flag"].apply(preprocess_row)
df_filter["Club Logo"] = df_filter["Club Logo"].apply(preprocess_row)

st.dataframe(df_filter, 
             column_config={
                "Overall" : st.column_config.ProgressColumn(
                    'Overall', format = '%d', min_value= 0, max_value=100),
                "Club Logo" : st.column_config.ImageColumn(),
                "Photo" : st.column_config.ImageColumn(),
                'Flag' : st.column_config.ImageColumn("Nationality"), 
                "Wage(£)" : st.column_config.ProgressColumn(
                    'Weekly Wage', format = '£%f', min_value= 0, max_value=df_filter['Wage(£)'].max())
             }
             
             )

