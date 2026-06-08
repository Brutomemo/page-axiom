-- AXIOM Database Schema - Multi-Tenant
-- Para suportar múltiplos clientes

-- 1. TABELA DE CLIENTES (Tenants)
CREATE TABLE IF NOT EXISTS clientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_empresa VARCHAR(255) NOT NULL UNIQUE,
    email_admin VARCHAR(255) NOT NULL,
    plano VARCHAR(50) NOT NULL, -- 'starter', 'professional', 'enterprise'
    status VARCHAR(50) NOT NULL DEFAULT 'ativo', -- 'ativo', 'suspenso', 'cancelado'
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_expiracao TIMESTAMP,
    limite_usuarios INT DEFAULT 5,
    limite_dados_gb INT DEFAULT 10,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABELA DE USUÁRIOS (por cliente)
CREATE TABLE IF NOT EXISTS usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'admin', 'analyst', 'viewer'
    senha_hash VARCHAR(255),
    ativo BOOLEAN DEFAULT TRUE,
    ultimo_acesso TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cliente_id, email)
);

-- 3. TABELA DE PROJETOS (Análises)
CREATE TABLE IF NOT EXISTS projetos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50) NOT NULL, -- 'analise_dados', 'dashboard', 'automacao'
    status VARCHAR(50) DEFAULT 'em_desenvolvimento',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_ultimo_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES usuarios(id),
    metadata JSONB
);

-- 4. TABELA DE DADOS BRUTOS (Uploads/ETL)
CREATE TABLE IF NOT EXISTS dados_brutos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    projeto_id UUID NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
    nome_arquivo VARCHAR(255),
    tipo_arquivo VARCHAR(50), -- 'csv', 'json', 'xlsx', 'api'
    tamanho_bytes BIGINT,
    linhas INT,
    colunas INT,
    data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_processamento VARCHAR(50), -- 'pendente', 'processando', 'concluido', 'erro'
    erro_mensagem TEXT,
    storage_path VARCHAR(255),
    metadata JSONB
);

-- 5. TABELA DE ANÁLISE DIAGNÓSTICA
CREATE TABLE IF NOT EXISTS analise_diagnostica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    projeto_id UUID NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
    dados_brutos_id UUID REFERENCES dados_brutos(id),
    tipo_analise VARCHAR(50), -- 'descritiva', 'exploratoria', 'preditiva', 'prescritiva'
    
    -- Estatísticas Básicas
    total_registros INT,
    total_colunas INT,
    percentual_completude FLOAT,
    valores_faltantes INT,
    
    -- Qualidade de Dados
    outliers_detectados INT,
    anomalias_encontradas INT,
    qualidade_score FLOAT, -- 0-100
    
    -- Insights Automáticos
    variaveis_importante TEXT[], -- array de colunas
    correlacoes JSONB, -- correlações encontradas
    padroes_identificados TEXT,
    recomendacoes TEXT,
    
    -- Processamento
    tempo_processamento_ms INT,
    modelo_ia_usado VARCHAR(50), -- 'groq', 'openai', 'claude'
    confianca_score FLOAT,
    
    data_analise TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- 6. TABELA DE DASHBOARDS
CREATE TABLE IF NOT EXISTS dashboards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    projeto_id UUID REFERENCES projetos(id),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50), -- 'executivo', 'operacional', 'estrategico'
    url_streamlit VARCHAR(500),
    status VARCHAR(50) DEFAULT 'ativo',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    criado_por UUID REFERENCES usuarios(id)
);

-- 7. TABELA DE AUTOMAÇÕES (ETL/Webhooks)
CREATE TABLE IF NOT EXISTS automacoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    projeto_id UUID REFERENCES projetos(id),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50), -- 'webhook', 'agendado', 'evento'
    
    -- Configuração
    source_tipo VARCHAR(50), -- 'api', 'banco', 'arquivo', 'webhook'
    source_url VARCHAR(500),
    frequencia VARCHAR(50), -- 'tempo_real', 'horaria', 'diaria', 'semanal'
    
    -- Transformação
    transformacao_script TEXT, -- código de transformação
    
    -- Destino
    destino_tipo VARCHAR(50), -- 'supabase', 'api', 'arquivo'
    destino_config JSONB,
    
    -- Status
    ativo BOOLEAN DEFAULT TRUE,
    proxima_execucao TIMESTAMP,
    ultima_execucao TIMESTAMP,
    ultima_execucao_sucesso BOOLEAN,
    erro_mensagem TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. TABELA DE HISTÓRICO DE CHATS (IA Integrada)
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    projeto_id UUID REFERENCES projetos(id),
    session_id VARCHAR(255),
    user_email VARCHAR(255),
    user_message TEXT NOT NULL,
    assistant_message TEXT NOT NULL,
    model VARCHAR(50), -- 'groq', 'openai', 'claude'
    complexidade INT, -- 1, 2, 3
    tokens_usados INT,
    tempo_resposta_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. TABELA DE RELATÓRIOS
CREATE TABLE IF NOT EXISTS relatorios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    projeto_id UUID REFERENCES projetos(id),
    nome VARCHAR(255) NOT NULL,
    tipo VARCHAR(50), -- 'executivo', 'tecnico', 'automatizado'
    conteudo TEXT,
    formato VARCHAR(20), -- 'pdf', 'html', 'markdown'
    data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    gerado_por UUID REFERENCES usuarios(id),
    storage_path VARCHAR(255)
);

-- 10. TABELA DE LOGS DE AUDITORIA
CREATE TABLE IF NOT EXISTS auditoria_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    usuario_id UUID REFERENCES usuarios(id),
    acao VARCHAR(100),
    recurso VARCHAR(100),
    recurso_id VARCHAR(255),
    detalhes JSONB,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ÍNDICES para performance
CREATE INDEX idx_usuarios_cliente ON usuarios(cliente_id);
CREATE INDEX idx_projetos_cliente ON projetos(cliente_id);
CREATE INDEX idx_dados_brutos_projeto ON dados_brutos(projeto_id);
CREATE INDEX idx_analise_projeto ON analise_diagnostica(projeto_id);
CREATE INDEX idx_chat_cliente ON chat_history(cliente_id);
CREATE INDEX idx_auditoria_cliente ON auditoria_logs(cliente_id);

-- Row Level Security (RLS) - Segurança multi-tenant
ALTER TABLE clientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE projetos ENABLE ROW LEVEL SECURITY;
ALTER TABLE dados_brutos ENABLE ROW LEVEL SECURITY;
ALTER TABLE analise_diagnostica ENABLE ROW LEVEL SECURITY;