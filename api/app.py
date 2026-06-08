from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from supabase import create_client
from openai import OpenAI
from groq import Groq
import anthropic

load_dotenv()

app = FastAPI()

# CORS para permitir requisições do Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

class ChatMessage(BaseModel):
    mensagem: str
    session_id: str
    user_email: str = None

class WarmupRequest(BaseModel):
    session_id: str = "warmup"

@app.get("/")
def root():
    return {"status": "AXIOM API rodando!", "version": "1.0"}

@app.post("/warmup")
def warmup(request: WarmupRequest):
    """Endpoint para acordar a API (warm-up)"""
    return {"status": "API acordada", "ready": True}

@app.post("/chat")
def chat(data: ChatMessage):
    """Endpoint principal do chatbot com Groq → OpenAI → Claude"""
    try:
        # Tenta Groq primeiro (mais rápido)
        resposta = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": """Você é o assistente comercial da AXIOM.

Serviços:
- Dashboards e Analytics
- Agentes de IA
- Automação de Processos
- Consultoria Estratégica

Objetivo:
- Explicar serviços com clareza
- Identificar necessidades do cliente
- Ser profissional e direto

Nunca invente preços."""
                },
                {"role": "user", "content": data.mensagem}
            ],
            max_tokens=500,
            temperature=0.7
        )
        texto_resposta = resposta.choices[0].message.content
        modelo_usado = "groq"
        
    except Exception as e:
        try:
            # Fallback para OpenAI
            resposta = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """Você é o assistente comercial da AXIOM.

Serviços:
- Dashboards e Analytics
- Agentes de IA
- Automação de Processos
- Consultoria Estratégica

Nunca invente preços."""
                    },
                    {"role": "user", "content": data.mensagem}
                ],
                max_tokens=500,
                temperature=0.7
            )
            texto_resposta = resposta.choices[0].message.content
            modelo_usado = "openai"
        except Exception as openai_error:
            try:
                # Fallback para Claude (melhor qualidade)
                client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                resposta = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=500,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""Você é o assistente comercial da AXIOM.

Serviços:
- Dashboards e Analytics
- Agentes de IA
- Automação de Processos
- Consultoria Estratégica

Responda de forma clara e profissional.
Nunca invente preços.

Pergunta: {data.mensagem}"""
                        }
                    ]
                )
                texto_resposta = resposta.content[0].text
                modelo_usado = "claude"
            except Exception as claude_error:
                return {"erro": str(claude_error), "resposta": "Desculpe, estou com dificuldades no momento."}

# Adicione estas rotas (além do chat):

@app.post("/api/projetos")
def criar_projeto(cliente_id: str, nome: str, descricao: str):
    """Criar novo projeto de análise"""
    # Salva no Supabase
    pass

@app.post("/api/upload-dados")
def upload_dados(cliente_id: str, arquivo):
    """Upload de dados para análise"""
    # ETL automático
    pass

@app.post("/api/analise-diagnostica")
def analise_diagnostica(projeto_id: str):
    """Executa análise diagnóstica automática"""
    # Usa IA para detectar padrões
    pass

@app.get("/api/dashboard/{cliente_id}")
def get_dashboard(cliente_id: str):
    """Retorna dados para dashboard Streamlit"""
    pass

@app.post("/api/automacao")
def criar_automacao(cliente_id: str, config: dict):
    """Criar pipeline de automação ETL"""
    pass

    
    # Salva no Supabase
    try:
        supabase.table("chat_history").insert({
            "session_id": data.session_id,
            "user_message": data.mensagem,
            "assistant_message": texto_resposta,
            "model": modelo_usado,
            "user_email": data.user_email
        }).execute()
    except Exception as db_error:
        print(f"Erro ao salvar: {db_error}")
    
    return {
        "resposta": texto_resposta,
        "modelo": modelo_usado,
        "session_id": data.session_id
    }
    
    
    # Salva no Supabase
    try:
        supabase.table("chat_history").insert({
            "session_id": data.session_id,
            "user_message": data.mensagem,
            "assistant_message": texto_resposta,
            "model": modelo_usado,
            "user_email": data.user_email
        }).execute()
    except Exception as db_error:
        print(f"Erro ao salvar: {db_error}")
    
    return {
        "resposta": texto_resposta,
        "modelo": modelo_usado,
        "session_id": data.session_id
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
