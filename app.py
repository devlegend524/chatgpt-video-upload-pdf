import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.environ["OPENAI_API_KEY"]


import streamlit as st
from streamlit_chat import message
from langchain.llms import OpenAI
import validators
from youtube    import find_videos
from aprender   import ai_aprender
from conversar  import setup, chat


st.set_page_config(page_title="buildChat", page_icon=":robot:")
st.header("Build Chat")

# Define as variaveis de sessao persistencia
if 'base' not in st.session_state:
    st.session_state['base'] = ''

if 'urls' not in st.session_state:
    st.session_state['urls'] = []

if 'lista_video' not in st.session_state:
    st.session_state['lista_video'] = []

if 'aprendido' not in st.session_state:
    st.session_state['aprendido'] = False

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def buscar_yt(tema, nro_videos):
    st.session_state['lista_video'] = find_videos(tema, nro_videos)


tab1, tab2 = st.tabs(["Aprender", "Conversar"])

# Tabela com o formulario para aprender um assunto
with tab1:
    # Obtem o nome da base de dados (a ser salvo)
    def get_base():
            input_text = st.text_input(label="Nome Base", label_visibility='collapsed',
                                    placeholder="Base de dados...", key="base_input")
            return input_text
    st.session_state['base'] = get_base()
    
    col1, col2 = st.columns(2)
    # Obtenção do termo de busca do youtube
    with col1:
        def get_text():
            input_text = st.text_area(label="Busca youtube", label_visibility='collapsed', placeholder="Conteudo...", key="email_input")
            return input_text
        tema_input = get_text()
    # Quantidade de videos retornadas
    with col2:
        nro_videos = st.slider( 'Numero videos youtube', 1, 5)
        if tema_input:
            st.button('Buscar', on_click=buscar_yt, args=[tema_input, nro_videos])

    # Barra lateral que carrega os videos do youtube
    with st.sidebar:
        if st.session_state['lista_video']:
            for vd in st.session_state['lista_video']:
                st.video("https://youtu.be/" + vd['videos'])
                st.write(vd)
        
    # Escolha dos PDF que deve fazer parte do processo de treino
    uploaded_files = st.file_uploader("Escolha seus PDFs", type=['pdf'], accept_multiple_files=True)
    
    # URLs de Sites que devem ser parte tambem do conteudo
    """ Escolhas suas URLS """
    def get_url():
        st.empty()
        input_text = st.text_input(label="Sites com conteudo",
                                label_visibility='collapsed',
                                placeholder="Sites...",
                                key="url_input")
        return input_text
    nova_url = get_url()
    if nova_url:    
        if nova_url not in st.session_state['urls']:
            if not validators.url(nova_url):
                st.warning('URL inválida')
            else:
                st.session_state['urls'].append(nova_url)
                nova_url = st.empty()
    options = st.multiselect('sites',st.session_state['urls'],st.session_state['urls'])


    # Funcao para iniciar o aprendizado do conteudo
    def aprender():
        with st.spinner('Aprendendo...'):
            st.session_state['aprendido'] = ai_aprender(
                st.session_state['base'],
                st.session_state['lista_video'],
                uploaded_files,
                st.session_state['urls']
            )
    if st.session_state['base']:
        st.button("*Aprender*", type='secondary', help="Aqui comeco a aprender os conteudos.",
                on_click=aprender
        )

# Tabela para conversar com um assunto aprendido
with tab2:
    st.markdown("### Conversar:")
    
    # Selecao so aprendizados existente (nome da colection no chomadb)
    option = st.selectbox(
        'Qual aprendizado gostaria de utilizar?',
        os.listdir('./db/chroma')
    )

    if option:
        # Objeto de conversa para utilizar no chat
        qa = setup(option)
        # Mostra o resumo obtido no treinamento sobre o conteudo
        f = open('./resumos/'+ option +'.txt', 'r', encoding="utf8")
        st.write(f.read())
        
        # Entradas de texto do usuario
        def get_text():
            input_text = st.text_input("U Mano: ","", key="input")
            return input_text 
        user_input = get_text()
        
        if user_input:
            # Obtem resposta do modelo
            output = chat(qa, user_input)
            # Salvar o retorno no array de historico da conversa
            st.session_state.past.append(user_input)
            st.session_state.generated.append(output)
        
        # Mostra o chat
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state["generated"][i], key=str(i))
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')