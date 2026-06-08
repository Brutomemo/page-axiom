import streamlit as st
import pandas as pd
from supabase import create_client
import plotly.express as px
from streamlit_functions import (
    carregar_pipeline,
    carregar_clientes,
    carregar_projetos,
    carregar_chat_history,
    carregar_automacoes,
    carregar_relatorios,
    carregar_metricas_pipeline,
    inserir_cliente,
    inserir_projeto
)

# Config
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="AXIOM Dashboard", layout="wide")

# AUTENTICAÇÃO
cliente_id = st.sidebar.text_input("Cliente ID")

if not cliente_id:
    st.error("Informe seu Cliente ID")
    st.stop()

# MENU PRINCIPAL
menu = st.sidebar.radio("Menu", [
    "Dashboard Principal",
    "Análise Diagnóstica",
    "Projetos",
    "Automações",
    "Relatórios",
    "Chat IA",
    "🎯 Pipeline Integrado",
    "🧪 Testes - Adicionar Dados"
])

# ═══════════════════════════════════════════════════════════════
# PÁGINA 1: Dashboard Principal
# ═══════════════════════════════════════════════════════════════

if menu == "Dashboard Principal":
    st.title("📊 Dashboard Principal")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Projetos", "12")
    col2.metric("Dados Processados", "2.5 GB")
    col3.metric("Qualidade Dados", "94%")
    col4.metric("Automações Ativas", "8")

# ═══════════════════════════════════════════════════════════════
# PÁGINA 2: Análise Diagnóstica
# ═══════════════════════════════════════════════════════════════

elif menu == "Análise Diagnóstica":
    st.title("🔬 Análise Diagnóstica de Dados")
    
    uploaded_file = st.file_uploader("Envie seu arquivo de dados")
    
    if uploaded_file:
        st.write("Processando análise...")

# ═══════════════════════════════════════════════════════════════
# PÁGINA 3: Projetos
# ═══════════════════════════════════════════════════════════════

elif menu == "Projetos":
    st.title("📋 Projetos")
    
    df_projetos = carregar_projetos()
    
    if df_projetos.empty:
        st.info("📭 Nenhum projeto encontrado.")
    else:
        st.dataframe(df_projetos, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# PÁGINA 4: Automações
# ═══════════════════════════════════════════════════════════════

elif menu == "Automações":
    st.title("⚙️ Automações")
    
    df_automacoes = carregar_automacoes()
    
    if df_automacoes.empty:
        st.info("📭 Nenhuma automação encontrada.")
    else:
        st.dataframe(df_automacoes, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# PÁGINA 5: Relatórios
# ═══════════════════════════════════════════════════════════════

elif menu == "Relatórios":
    st.title("📄 Relatórios")
    
    df_relatorios = carregar_relatorios()
    
    if df_relatorios.empty:
        st.info("📭 Nenhum relatório encontrado.")
    else:
        st.dataframe(df_relatorios, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# PÁGINA 6: Chat IA
# ═══════════════════════════════════════════════════════════════

elif menu == "Chat IA":
    st.title("💬 Chat com IA")
    
    df_chat = carregar_chat_history()
    
    if df_chat.empty:
        st.info("📭 Nenhuma conversa encontrada.")
    else:
        st.dataframe(df_chat, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# PÁGINA 7: Pipeline Integrado (PRINCIPAL!)
# ═══════════════════════════════════════════════════════════════

elif menu == "🎯 Pipeline Integrado":
    st.title("🎯 Pipeline Vendas - Strategic + Human Integrado")
    
    # FILTROS
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_tipo = st.selectbox(
            "Filtrar por tipo",
            ["Todos", "strategic", "human", "integrado"]
        )
    with col2:
        filtro_status = st.selectbox(
            "Filtrar por status",
            ["Todos", "lead", "qualificado", "proposta", "em_progresso", "finalizado"]
        )
    with col3:
        filtro_busca = st.text_input("Buscar cliente")
    
    st.divider()
    
    # CARREGAR DADOS DO SUPABASE
    df_pipeline = carregar_pipeline()
    
    # APLICAR FILTROS
    if not df_pipeline.empty:
        if filtro_tipo != "Todos":
            df_pipeline = df_pipeline[
                df_pipeline['Tipo'].str.lower() == filtro_tipo.lower()
            ]
        
        if filtro_status != "Todos":
            df_pipeline = df_pipeline[
                df_pipeline['Status'].str.lower() == filtro_status.lower()
            ]
        
        if filtro_busca:
            df_pipeline = df_pipeline[
                df_pipeline['Cliente'].str.contains(
                    filtro_busca, case=False, na=False
                )
            ]
    
    # MOSTRAR TABELA
    st.subheader("📊 Pipeline Atual")
    if df_pipeline.empty:
        st.info("📭 Nenhum projeto encontrado. Adicione dados para começar!")
    else:
        st.dataframe(
            df_pipeline.drop('projeto_id', axis=1, errors='ignore'),
            use_container_width=True
        )
    
    st.divider()
    
    # MÉTRICAS DO PIPELINE
    st.subheader("📈 Métricas de Performance")
    
    metricas = carregar_metricas_pipeline()
    
    if metricas and metricas.get('receita_total', 0) > 0:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(
            "Receita Strategic",
            f"R$ {metricas.get('receita_strategic', 0):,.0f}"
        )
        col2.metric(
            "Receita Human",
            f"R$ {metricas.get('receita_human', 0):,.0f}"
        )
        col3.metric(
            "Receita Integrada",
            f"R$ {metricas.get('receita_integrada', 0):,.0f}"
        )
        col4.metric(
            "Total",
            f"R$ {metricas.get('receita_total', 0):,.0f}"
        )
    else:
        st.info("⏳ Adicione projetos para ver métricas.")
    
    st.divider()
    
    # GRÁFICO DO FUNIL
    st.subheader("📊 Distribuição por Tipo")
    
    if not df_pipeline.empty:
        tipo_counts = df_pipeline['Tipo'].value_counts()
        
        fig = px.pie(
            values=tipo_counts.values,
            names=tipo_counts.index,
            title="Projetos por Tipo de Serviço"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📭 Nenhum dado para exibir gráfico.")

# ═══════════════════════════════════════════════════════════════
# PÁGINA 8: Testes - Adicionar Dados
# ═══════════════════════════════════════════════════════════════

elif menu == "🧪 Testes - Adicionar Dados":
    st.title("🧪 Seção de Testes - Adicionar Dados")
    st.write("Use esta seção para adicionar dados de teste ao banco Supabase")
    
    st.divider()
    
    # ADICIONAR CLIENTE
    st.subheader("➕ Adicionar Cliente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_empresa = st.text_input("Nome da Empresa", placeholder="Ex: Acme Corporation")
        email = st.text_input("Email", placeholder="Ex: contato@empresa.com")
        telefone = st.text_input("Telefone", placeholder="Ex: 11 98765-4321")
    
    with col2:
        setor = st.selectbox(
            "Setor",
            ["Tech", "Finance", "Saúde", "Educação", "Consultoria", "Outro"]
        )
        tamanho = st.selectbox(
            "Tamanho",
            ["Startup", "PME", "Grande Empresa"]
        )
    
    if st.button("➕ Adicionar Cliente", key="add_cliente"):
        if nome_empresa and email:
            if inserir_cliente(nome_empresa, email, telefone, setor, tamanho):
                st.success(f"✅ Cliente '{nome_empresa}' adicionado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Erro ao adicionar cliente")
        else:
            st.warning("⚠️ Preencha nome e email!")
    
    st.divider()
    
    # ADICIONAR PROJETO
    st.subheader("➕ Adicionar Projeto")
    
    df_clientes = carregar_clientes()
    
    if df_clientes.empty:
        st.warning("⚠️ Nenhum cliente registrado. Adicione um cliente primeiro!")
    else:
        cliente_selecionado = st.selectbox(
            "Selecione Cliente",
            df_clientes['nome_empresa'].tolist(),
            key="cliente_select"
        )
        
        cliente_id = df_clientes[
            df_clientes['nome_empresa'] == cliente_selecionado
        ]['id'].values[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome_projeto = st.text_input(
                "Nome do Projeto",
                placeholder="Ex: Web App de Vendas"
            )
            tipo_eixo = st.selectbox(
                "Tipo de Serviço",
                ["strategic", "human", "integrado"]
            )
        
        with col2:
            valor = st.number_input(
                "Valor (R$)",
                min_value=0,
                value=10000,
                step=1000
            )
            status = st.selectbox(
                "Status",
                ["lead", "qualificado", "proposta", "em_progresso", "finalizado"]
            )
        
        if st.button("➕ Adicionar Projeto", key="add_projeto"):
            if nome_projeto:
                if inserir_projeto(cliente_id, nome_projeto, tipo_eixo, valor, status):
                    st.success(f"✅ Projeto '{nome_projeto}' adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao adicionar projeto")
            else:
                st.warning("⚠️ Preencha o nome do projeto!")
    
    st.divider()
    
    # VISUALIZAR DADOS
    st.subheader("📊 Dados Adicionados no Banco")
    
    st.write("**🏢 Clientes:**")
    df_clientes_view = carregar_clientes()
    if df_clientes_view.empty:
        st.info("Nenhum cliente adicionado ainda.")
    else:
        st.dataframe(df_clientes_view, use_container_width=True)
    
    st.write("**📋 Projetos:**")
    df_projetos_view = carregar_projetos()
    if df_projetos_view.empty:
        st.info("Nenhum projeto adicionado ainda.")
    else:
        st.dataframe(df_projetos_view, use_container_width=True)