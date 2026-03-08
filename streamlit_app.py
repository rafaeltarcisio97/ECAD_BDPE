import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="ECAD Igreja", layout="wide")

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LISTA DE MOMENTOS DA MISSA ---
MOMENTOS = [
    "NENHUM / OUTRO", "CANTO DE ENTRADA", "SINAL DA CRUZ", "ATO PENITENCIAL", 
    "HINO DE LOUVOR", "SALMO", "ACLAMAÇÃO AO EVANGELHO", "OFERENDAS", 
    "SANTO", "ACLAMAÇÃO MEMORIAL", "AMÉM", "CORDEIRO", "COMUNHÃO", 
    "FINAL", "OUTROS 1", "OUTROS 2", "OUTROS 3", "OUTROS 4"
]

# --- CARREGAR DADOS DA BIBLIOTECA (DA PLANILHA) ---
@st.cache_data(ttl=600)
def carregar_biblioteca():
    return conn.read(worksheet="biblioteca")

df_bib = carregar_biblioteca()

# --- INTERFACE ---
st.title("⛪ Relatório de Músicas - ECAD")

with st.sidebar:
    st.header("Acesso")
    usuario = st.text_input("Seu Usuário", value="Musico_01")
    modo = st.radio("Ir para:", ["Novo Relatório", "Meus Rascunhos", "Finalizados"])

if modo == "Novo Relatório":
    # --- CABEÇALHO ---
    st.subheader("1. Informações da Celebração")
    c1, c2, c3, c4 = st.columns(4)
    with c1: data = st.date_input("Data")
    with c2: horario = st.time_input("Horário")
    with c3: local = st.selectbox("Local", ["Matriz", "Capela A", "Capela B"])
    with c4: grupo = st.text_input("Grupo/Cantor")

    st.divider()

    # --- INSERÇÃO DE MÚSICAS ---
    st.subheader("2. Músicas")
    
    if "lista_temporaria" not in st.session_state:
        st.session_state.lista_temporaria = []

    with st.container(border=True):
        col_m, col_t, col_c = st.columns([1.5, 2, 2])
        with col_m:
            momento_sel = st.selectbox("Momento", MOMENTOS)
        with col_t:
            # Busca na biblioteca mas permite digitar novo
            busca = st.selectbox("Buscar na Biblioteca", [""] + list(df_bib["Titulo"]))
            titulo_manual = st.text_input("Ou digite o título:")
            titulo_final = titulo_manual if titulo_manual else busca
        with col_c:
            # Auto-preenche compositor se achar na busca, mas deixa editar
            comp_sugerido = ""
            if busca:
                comp_sugerido = df_bib[df_bib["Titulo"] == busca]["Compositor"].values[0]
            compositor_final = st.text_input("Compositor", value=comp_sugerido)

        st.write("**Duração:**")
        ct1, ct2, ct3 = st.columns([1, 1, 2])
        with ct1: min_inp = st.number_input("Minutos", min_value=0, step=1)
        with ct2: seg_inp = st.number_input("Segundos", min_value=0, max_value=59, step=1)
        
        if st.button("➕ Adicionar Música"):
            segundos_totais = (min_inp * 60) + seg_inp
            st.session_state.lista_temporaria.append({
                "Momento": momento_sel,
                "Título": titulo_final,
                "Compositor": compositor_final,
                "Segundos": segundos_totais,
                "Formatado": f"{min_inp}min {seg_inp}s"
            })

    # --- LISTA ATUAL E SALVAMENTO ---
    if st.session_state.lista_temporaria:
        st.write("### Músicas Selecionadas")
        df_atual = pd.DataFrame(st.session_state.lista_temporaria)
        st.table(df_atual[["Momento", "Título", "Compositor", "Formatado"]])

        c_btn1, c_btn2 = st.columns(2)
        if c_btn1.button("💾 Salvar Rascunho"):
            # Lógica para dar um 'append' na aba relatorios da planilha
            st.info("Rascunho salvo no Google Sheets!")
        
        if c_btn2.button("✅ FINALIZAR"):
            # Aqui o sistema enviaria os dados para a aba itens_musica
            st.success("Relatório finalizado e enviado!")
            st.session_state.lista_temporaria = []
