import os
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from sqlalchemy import create_engine

# =============================
# CONFIGURAÇÃO INICIAL
# =============================

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Tema visual customizado
st.markdown("""
    <style>
        .main {
            background-color: #0E1117;
            color: white;
        }
        .stMetric {
            background-color: #AD85FF;
            padding: 15px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Sales Dashboard")
st.markdown("Análise interativa de vendas conectada ao Supabase (PostgreSQL)")

# =============================
# CONEXÃO COM SUPABASE
# =============================

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    st.error("DATABASE_URL não encontrada no .env")
    st.stop()

engine = create_engine(DATABASE_URL)

@st.cache_data
def load_data():
    query = "SELECT id, sale_date, seller_name, sale_code, sale_value FROM sales"
    df = pd.read_sql(query, engine)
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    return df

df = load_data()

# =============================
# SIDEBAR - FILTROS
# =============================

st.sidebar.header("🔎 Filtros")

# Filtro por vendedor
sellers = st.sidebar.multiselect(
    "Selecione o(s) vendedor(es):",
    options=df["seller_name"].unique(),
    default=df["seller_name"].unique()
)

# Filtro por data
date_range = st.sidebar.date_input(
    "Selecione o período:",
    [df["sale_date"].min(), df["sale_date"].max()]
)

# Aplicar filtros
filtered_df = df[
    (df["seller_name"].isin(sellers)) &
    (df["sale_date"] >= pd.to_datetime(date_range[0])) &
    (df["sale_date"] <= pd.to_datetime(date_range[1]))
]

# =============================
# MÉTRICAS PRINCIPAIS
# =============================

total_sales = filtered_df["sale_value"].sum()
total_transactions = filtered_df.shape[0]
avg_ticket = filtered_df["sale_value"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total de Vendas", f"R$ {total_sales:,.2f}")
col2.metric("🧾 Total de Transações", total_transactions)
col3.metric("📈 Ticket Médio", f"R$ {avg_ticket:,.2f}")

st.markdown("---")

# =============================
# GRÁFICO - VENDAS AO LONGO DO TEMPO
# =============================

sales_over_time = (
    filtered_df
    .groupby(filtered_df["sale_date"].dt.date)["sale_value"]
    .sum()
    .reset_index()
)

fig_time = px.line(
    sales_over_time,
    x="sale_date",
    y="sale_value",
    title="📈 Vendas ao longo do tempo",
    markers=True,
    template="plotly_dark"
)

st.plotly_chart(fig_time, use_container_width=True)

# =============================
# GRÁFICO - VENDAS POR VENDEDOR
# =============================

sales_by_seller = (
    filtered_df
    .groupby("seller_name")["sale_value"]
    .sum()
    .reset_index()
)

fig_seller = px.bar(
    sales_by_seller,
    x="seller_name",
    y="sale_value",
    title="🏆 Vendas por vendedor",
    template="plotly_dark"
)

st.plotly_chart(fig_seller, use_container_width=True)

# =============================
# TABELA DETALHADA
# =============================

st.subheader("📋 Dados detalhados")

st.dataframe(filtered_df, use_container_width=True)

# =============================
# EXPORTAÇÃO CSV
# =============================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Exportar dados filtrados (CSV)",
    data=csv,
    file_name="sales_export.csv",
    mime="text/csv"
)
