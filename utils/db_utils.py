# ==============================================================================
# ARQUIVO: utils/db_utils.py
# DESCRIÇÃO: Funções para conectar e interagir com o banco de dados.
# ==============================================================================
import streamlit as st
import pandas as pd
from sqlalchemy import text
from typing import Optional, Dict, Any

@st.cache_resource(show_spinner="Conectando ao banco de dados...")
def get_db_connection():
    """Estabelece e cacheia a conexão com o banco de dados usando st.connection."""
    try:
        return st.connection("mysql_db", type="sql")
    except Exception as e:
        st.error(f"Falha ao conectar ao banco de dados: {str(e)}")
        raise

@st.cache_data(ttl=600, show_spinner="Carregando dados...")
def fetch_data(query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Executa uma query de LEITURA (SELECT) e retorna um DataFrame.
    """
    if not query or not isinstance(query, str):
        st.error("A query SQL deve ser uma string não vazia.")
        return pd.DataFrame()
    
    try:
        conn = get_db_connection()
        # Usa text() apenas para queries com parâmetros
        if params:
            return conn.session.execute(text(query), params).fetchall()
        return conn.query(query)
    except Exception as e:
        st.error(f"Erro ao executar query: {str(e)}")
        return pd.DataFrame()

def execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> bool:
    """
    Executa uma query de ESCRITA (INSERT, UPDATE, DELETE).
    """
    if not query or not isinstance(query, str):
        st.error("A query SQL deve ser uma string não vazia.")
        return False
    
    try:
        conn = get_db_connection()
        with conn.session as session:
            session.execute(text(query), params or {})
            session.commit()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro ao executar query: {str(e)}")
        return False