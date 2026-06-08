"""
Funções para extrair dados do Supabase
Integração limpa entre dashboard e banco de dados
"""

import streamlit as st
import pandas as pd
from supabase import create_client
import os

# Inicializar Supabase (reutiliza secrets do Streamlit)
@st.cache_resource
def get_supabase():
    """Conecta ao Supabase uma única vez"""
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro ao conectar Supabase: {e}")
        return None

# ═══════════════════════════════════════════════════════════════
# FUNÇÕES DE EXTRAÇÃO DO BANCO
# ═══════════════════════════════════════════════════════════════

def carregar_clientes():
    """
    Carrega todos os clientes do banco
    Retorna: DataFrame com clientes
    """
    supabase = get_supabase()
    
    if not supabase:
        return pd.DataFrame()
    
    try:
        response = supabase.table('clientes').select('*').execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Erro ao carregar clientes: {e}")
        return pd.DataFrame()


def carregar_projetos(cliente_id=None):
    """
    Carrega projetos (filtrado por cliente se informado)
    
    Args:
        cliente_id: UUID do cliente (opcional)
    
    Retorna: DataFrame com projetos
    """
    supabase = get_supabase()
    
    if not supabase:
        return pd.DataFrame()
    
    try:
        if cliente_id:
            # Busca apenas projetos deste cliente
            response = supabase.table('projetos')\
                .select('*')\
                .eq('cliente_id', cliente_id)\
                .execute()
        else:
            # Busca todos os projetos
            response = supabase.table('projetos').select('*').execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Erro ao carregar projetos: {e}")
        return pd.DataFrame()


def carregar_pipeline():
    """
    Carrega pipeline de vendas com contexto completo
    Junta: clientes + projetos + informações de vendas
    
    Retorna: DataFrame preparado para visualização
    """
    supabase = get_supabase()
    
    if not supabase:
        return pd.DataFrame()
    
    try:
        # Carrega projetos com toda informação
        response = supabase.table('projetos')\
            .select('*')\
            .execute()
        
        projetos = response.data
        
        if not projetos:
            return pd.DataFrame()
        
        # Processa os dados
        dados_processados = []
        
        for projeto in projetos:
            # Busca cliente relacionado
            try:
                cliente_response = supabase.table('clientes')\
                    .select('nome_empresa')\
                    .eq('id', projeto.get('cliente_id'))\
                    .execute()
                
                nome_cliente = cliente_response.data[0]['nome_empresa'] if cliente_response.data else 'N/A'
            except:
                nome_cliente = 'N/A'
            
            # Processa tipo de eixo
            tipo_eixo = projeto.get('tipo_eixo', 'N/A')
            
            # Processa status
            status = projeto.get('status', 'lead')
            
            # Processa valor
            valor = projeto.get('valor_contrato') or projeto.get('valor_proposto') or 0
            
            # Monta linha da tabela
            dados_processados.append({
                'Cliente': nome_cliente,
                'Projeto': projeto.get('nome', 'S/N'),
                'Tipo': tipo_eixo,
                'Valor (R$)': f"R$ {valor:,.0f}",
                'Status': status.capitalize(),
                'Data Criação': projeto.get('data_criacao', ''),
                'projeto_id': projeto.get('id')  # ID oculto para ações
            })
        
        df = pd.DataFrame(dados_processados)
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar pipeline: {e}")
        return pd.DataFrame()


def carregar_chat_history(cliente_id=None, projeto_id=None):
    """
    Carrega histórico de chat
    
    Args:
        cliente_id: Filtrar por cliente (opcional)
        projeto_id: Filtrar por projeto (opcional)
    
    Retorna: DataFrame com histórico
    """
    supabase = get_supabase()
    
    if not supabase:
        return pd.DataFrame()
    
    try:
        query = supabase.table('chat_history').select('*')
        
        if cliente_id:
            query = query.eq('cliente_id', cliente_id)
        
        if projeto_id:
            query = query.eq('projeto_id', projeto_id)
        
        # Ordenar por data (mais recente primeiro)
        response = query.order('created_at', desc=True).execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Erro ao carregar chat: {e}")
        return pd.DataFrame()


def carregar_automacoes(cliente_id=None):
    """
    Carrega automações/ETL configuradas
    
    Args:
        cliente_id: Filtrar por cliente (opcional)
    
    Retorna: DataFrame com automações
    """
    supabase = get_supabase()
    
    if not supabase:
        return pd.DataFrame()
    
    try:
        query = supabase.table('automacoes').select('*')
        
        if cliente_id:
            query = query.eq('cliente_id', cliente_id)
        
        response = query.execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Erro ao carregar automações: {e}")
        return pd.DataFrame()


def carregar_relatorios(cliente_id=None):
    """
    Carrega relatórios gerados
    
    Args:
        cliente_id: Filtrar por cliente (opcional)
    
    Retorna: DataFrame com relatórios
    """
    supabase = get_supabase()
    
    if not supabase:
        return pd.DataFrame()
    
    try:
        query = supabase.table('relatorios').select('*')
        
        if cliente_id:
            query = query.eq('cliente_id', cliente_id)
        
        response = query.order('data_geracao', desc=True).execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Erro ao carregar relatórios: {e}")
        return pd.DataFrame()


def carregar_metricas_pipeline():
    """
    Calcula métricas do pipeline
    
    Retorna: Dict com métricas
    """
    supabase = get_supabase()
    
    if not supabase:
        return {}
    
    try:
        response = supabase.table('projetos').select('*').execute()
        projetos = response.data or []
        
        # Calcula métricas
        total_projetos = len(projetos)
        
        receita_strategic = sum([
            p.get('valor_contrato', 0) or p.get('valor_proposto', 0)
            for p in projetos
            if p.get('tipo_eixo') == 'strategic'
        ])
        
        receita_human = sum([
            p.get('valor_contrato', 0) or p.get('valor_proposto', 0)
            for p in projetos
            if p.get('tipo_eixo') == 'human'
        ])
        
        receita_integrada = sum([
            p.get('valor_contrato', 0) or p.get('valor_proposto', 0)
            for p in projetos
            if p.get('tipo_eixo') == 'integrado'
        ])
        
        receita_total = receita_strategic + receita_human + receita_integrada
        
        projetos_ativos = len([p for p in projetos if p.get('status') == 'em_progresso'])
        
        return {
            'total_projetos': total_projetos,
            'receita_strategic': receita_strategic,
            'receita_human': receita_human,
            'receita_integrada': receita_integrada,
            'receita_total': receita_total,
            'projetos_ativos': projetos_ativos,
        }
        
    except Exception as e:
        st.error(f"Erro ao calcular métricas: {e}")
        return {}


def inserir_cliente(nome_empresa, email, telefone, setor, tamanho):
    """
    Insere novo cliente no banco
    (para testes manuais)
    """
    supabase = get_supabase()
    
    if not supabase:
        return False
    
    try:
        data = {
            'nome_empresa': nome_empresa,
            'email_principal': email,
            'telefone': telefone,
            'setor_industria': setor,
            'tamanho_empresa': tamanho,
            'ativo': True
        }
        
        response = supabase.table('clientes').insert(data).execute()
        return True
        
    except Exception as e:
        st.error(f"Erro ao inserir cliente: {e}")
        return False


def inserir_projeto(cliente_id, nome, tipo_eixo, valor, status='lead'):
    """
    Insere novo projeto no banco
    (para testes manuais)
    """
    supabase = get_supabase()
    
    if not supabase:
        return False
    
    try:
        data = {
            'cliente_id': cliente_id,
            'nome': nome,
            'tipo_eixo': tipo_eixo,
            'valor_proposto': valor,
            'status': status,
        }
        
        response = supabase.table('projetos').insert(data).execute()
        return True
        
    except Exception as e:
        st.error(f"Erro ao inserir projeto: {e}")
        return False