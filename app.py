import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gestão de Aluguel de Motos", layout="wide")

# --- Carregar dados ---
@st.cache_data
def carregar_dados():
    xls = pd.ExcelFile("Planilha_Aluguel_Motos.xlsx")
    motos = xls.parse("Cadastro de Motos")
    alugueis = xls.parse("Controle de Aluguéis")
    financeiro = xls.parse("Resumo Financeiro")
    manutencao = xls.parse("Agenda Manutenção")
    return motos, alugueis, financeiro, manutencao

motos, alugueis, financeiro, manutencao = carregar_dados()

st.title("🚗 Sistema de Gestão de Aluguel de Motos")

# --- Painel superior ---
st.subheader("Resumo Financeiro")
col1, col2 = st.columns(2)

with col1:
    fig_lucro = px.bar(
        financeiro,
        x="Mês", y="Lucro",
        color="Lucro",
        color_continuous_scale="Greens",
        title="Lucro por Mês"
    )
    st.plotly_chart(fig_lucro, use_container_width=True)

with col2:
    st.metric("Receita Total", f"R$ {financeiro['Receita'].sum():,.2f}".replace(".", ","))
    st.metric("Despesas Totais", f"R$ {financeiro['Despesas'].sum():,.2f}".replace(".", ","))

# --- Cadastro de Motos ---
st.subheader("🚌 Motos Cadastradas")
st.dataframe(motos, use_container_width=True)

# --- Controle de Aluguéis ---
st.subheader("📅 Aluguéis Recentes")
st.dataframe(alugueis.sort_values("Data Retirada", ascending=False), use_container_width=True)

# --- Agenda de Manutenção ---
st.subheader("⚙️ Agenda de Manutenções")
st.dataframe(manutencao, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido para gestão simples e eficiente de frotas de motos. ")
