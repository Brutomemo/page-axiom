from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key="SUA_API_KEY"
)

class Pergunta(BaseModel):
    pergunta:str

@app.post("/chat")

def chat(data:Pergunta):

    resposta = client.chat.completions.create(

        model="gpt-5",

        messages=[

            {
                "role":"system",
                "content":"""

Você é o assistente comercial da Axiom.

Serviços:

- Dashboards
- KPI
- OKR
- Analytics
- IA
- Automação

Objetivo:

Explicar serviços.
Identificar necessidades.
Captar leads.

Nunca invente preços.

"""
            },

            {
                "role":"user",
                "content":data.pergunta
            }

        ]

    )

    return {

        "resposta":
        resposta.choices[0]
        .message.content

    }
