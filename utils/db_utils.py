# ==============================================================================
# ARQUIVO: utils/db_utils.py (CORRIGIDO)
# DESCRIÇÃO: Funções para conectar e interagir com o banco de dados.
# ==============================================================================
import streamlit as st
import pandas as pd
from sqlalchemy import text

@st.cache_resource
def get_db_connection():
    """Estabelece e cacheia a conexão com o banco de dados usando st.connection."""
    return st.connection("mysql_db", type="sql")

@st.cache_data(ttl=600)
def fetch_data(query: str, params: dict = None):
    """
    Executa uma query de LEITURA (SELECT) usando o método .query() da conexão,
    que é a forma recomendada e mais robusta para retornar um DataFrame.
    """
    conn = get_db_connection()
    # Usa o método .query() do objeto de conexão do Streamlit, que lida
    # com os parâmetros e retorna um DataFrame diretamente.
    df = conn.query(query, params=params)
    return df

def execute_query(query: str, params: dict = None):
    """Executa uma query de ESCRITA (INSERT, UPDATE, DELETE)."""
    conn = get_db_connection()
    with conn.session as s:
        s.execute(text(query), params=params)
        s.commit()
    # Limpa todos os caches de dados para garantir que as novas informações sejam exibidas
    st.cache_data.clear()