import streamlit as st 
import requests
import base64

st.set_page_config(
    page_title= 'Players', 
    page_icon='🏃‍♂️', 
    layout='wide'
)

@st.cache_data ## adicionando porque teve uma atualização e apenas utilizando st.image não estava sendo possível renderizar a imagem do jogador. 
## foi necessário criar esse função de load para poder carregar a imagem e disponibilizar. 
def load_image_64(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    data = requests.get(url, headers=headers).content
    return "data:image/png;base64," + base64.b64encode(data).decode()

df_data = st.session_state['data']

clubes = df_data['Club'].unique() 
club = st.sidebar.selectbox('Club', clubes)


df_players = df_data[df_data['Club'] == club]
players = df_players['Name'].unique() 
player = st.sidebar.selectbox('Players', players)

player_stats = df_data[df_data['Name'] == player].iloc[0]

st.image(load_image_64(player_stats["Photo"]))
st.title(player_stats['Name'])

st.markdown(f'__Clube:__ {player_stats["Club"]}')
st.markdown(f'__Posição:__ {player_stats["Position"]}')

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'__Idade:__ {player_stats["Age"]}')
col2.markdown(f'__Altura:__ {player_stats["Height(cm.)"] / 100}')
col3.markdown(f'__Peso:__ {player_stats["Weight(lbs.)"] * 0.45:.2f}')

st.divider() 

st.subheader(f'__Overall:__ {player_stats["Overall"]}')
st.progress(int(player_stats["Overall"]))

col1, col2, col3, col4 = st.columns(4)
col1.metric(label= 'Valor de Mercado', value=f"£ {player_stats['Value(£)']:,}")
col2.metric(label= 'Remuneração semanal', value=f"£ {player_stats['Wage(£)']:,}")
col3.metric(label= 'Claúsula de Rescisão', value=f"£ {player_stats['Release Clause(£)']:,}")
