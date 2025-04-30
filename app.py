import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import BytesIO

st.set_page_config(page_title="Gestão de Aluguel de Motos", layout="wide")

# --- Carregar dados do Google Drive ---
@st.cache_data
def carregar_dados(link_google_drive):
    # Extrair o ID do arquivo do link público
    file_id = link_google_drive.split("/d/")[1].split("/")[0]
    # Montar o link de exportação do arquivo em formato Excel
    download_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    
    # Baixar o arquivo
    response = requests.get(download_url)
    response.raise_for_status()  # Verificar se o download foi bem-sucedido

    # Ler o arquivo Excel em um objeto pandas
    xls = pd.ExcelFile(BytesIO(response.content))
    motos = xls.parse("Cadastro de Motos")
    alugueis = xls.parse("Controle de Aluguéis")
    financeiro = xls.parse("Resumo Financeiro")
    manutencao = xls.parse("Agenda Manutenção")
    return motos, alugueis, financeiro, manutencao

# Solicitar o link do usuário
link_google_drive = "https://docs.google.com/spreadsheets/d/1-CsTh0IZOUKbmm1TchFxj-IyVMEPw2upbjRsu-4q5OQ/edit?usp=sharing"

if link_google_drive:
    try:
        motos, alugueis, financeiro, manutencao = carregar_dados(link_google_drive)
        
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

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os dados: {e}")
