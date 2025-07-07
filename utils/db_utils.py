# ==============================================================================
# ARQUIVO: utils/db_utils.py
# DESCRIÇÃO: Funções para conectar e interagir com o banco de dados.
# ==============================================================================
import streamlit as st
import pandas as pd
from sqlalchemy import text

@st.cache_resource
def get_db_connection():
    """Estabelece e cacheia a conexão com o banco de dados usando st.connection."""
    return st.connection("mysql_db", type="sql")

def fetch_data(query, params=None):
    """
    Executa uma query de LEITURA (SELECT) e retorna os resultados como um DataFrame.
    Utiliza cache para otimizar o desempenho.
    """
    conn = get_db_connection()
    # Cacheia os resultados por 10 minutos (600s) para queries de leitura frequentes
    df = conn.query(sql=query, params=params, ttl=600)
    return df

def execute_query(query, params=None):
    """Executa uma query de ESCRITA (INSERT, UPDATE, DELETE)."""
    conn = get_db_connection()
    with conn.session as s:
        s.execute(text(query), params)
        s.commit()
    # Limpa todos os caches de dados para garantir que as novas informações sejam exibidas
    st.cache_data.clear()