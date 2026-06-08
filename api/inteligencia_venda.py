"""
Sistema inteligente de venda integrada
Detecta oportunidades de cross-sell e upsell
"""

from enum import Enum
from typing import List, Dict

class TipoEixo(str, Enum):
    STRATEGIC = "strategic"
    HUMAN = "human"
    INTEGRADO = "integrado"

class ServicoDisponivel(str, Enum):
    # Strategic
    WEB_APP = "web_development"
    ANALISE_DADOS = "data_analysis"
    AUTOMACAO_IA = "automacao_ia"
    
    # Human
    TRAINING_NEGOCIACAO = "training_negotiation"
    GROWTH_MINDSET = "growth_mindset"
    PSICOLOGIA_ESPORTE = "psychology_sport"
    COACHING_PESSOAL = "coaching_pessoal"

class InteligenciaVenda:
    """Detecta intencoes e sugere serviços integrados"""
    
    def __init__(self):
        self.palavra_chave_strategic = {
            'web': [WEB_APP],
            'app': [WEB_APP],
            'dashboard': [WEB_APP, ANALISE_DADOS],
            'relatorio': [ANALISE_DADOS],
            'dados': [ANALISE_DADOS],
            'analise': [ANALISE_DADOS],
            'automat': [AUTOMACAO_IA],
            'integracao': [AUTOMACAO_IA],
        }
        
        self.palavra_chave_human = {
            'treina': [TRAINING_NEGOCIACAO, GROWTH_MINDSET],
            'negociacao': [TRAINING_NEGOCIACAO],
            'crise': [TRAINING_NEGOCIACAO],
            'equipe': [TRAINING_NEGOCIACAO, GROWTH_MINDSET],
            'coach': [COACHING_PESSOAL],
            'psicolog': [PSICOLOGIA_ESPORTE],
            'desempen': [PSICOLOGIA_ESPORTE, GROWTH_MINDSET],
        }
    
    def detectar_intencao(self, mensagem: str) -> Dict:
        """
        Analisa mensagem e detecta o que cliente quer
        """
        msg_lower = mensagem.lower()
        
        servicos_estrategicos = []
        servicos_humanos = []
        
        # Detecta Strategic
        for palavra, servicos in self.palavra_chave_strategic.items():
            if palavra in msg_lower:
                servicos_estrategicos.extend(servicos)
        
        # Detecta Human
        for palavra, servicos in self.palavra_chave_human.items():
            if palavra in msg_lower:
                servicos_humanos.extend(servicos)
        
        # Remove duplicatas
        servicos_estrategicos = list(set(servicos_estrategicos))
        servicos_humanos = list(set(servicos_humanos))
        
        # Determina tipo de eixo
        if servicos_estrategicos and servicos_humanos:
            tipo_eixo = TipoEixo.INTEGRADO
        elif servicos_estrategicos:
            tipo_eixo = TipoEixo.STRATEGIC
        elif servicos_humanos:
            tipo_eixo = TipoEixo.HUMAN
        else:
            tipo_eixo = None
        
        return {
            'tipo_eixo': tipo_eixo,
            'servicos_strategic': servicos_estrategicos,
            'servicos_human': servicos_humanos,
            'confianca': min(len(servicos_estrategicos) + len(servicos_humanos), 100)
        }
    
    def sugerir_integracao(self, 
                          servicos_detectados: List[str],
                          tipo_eixo: TipoEixo) -> Dict:
        """
        Sugere complementos integrados
        """
        sugestoes = []
        
        if tipo_eixo == TipoEixo.STRATEGIC:
            # Se pediu web app, sugere training
            if WEB_APP in servicos_detectados:
                sugestoes.append({
                    'tipo': TipoEixo.HUMAN,
                    'servico': TRAINING_NEGOCIACAO,
                    'motivo': 'Treinar equipe para usar a ferramenta',
                    'aumento_valor': 5000,
                })
            
            # Se pediu análise, sugere coaching
            if ANALISE_DADOS in servicos_detectados:
                sugestoes.append({
                    'tipo': TipoEixo.HUMAN,
                    'servico': COACHING_PESSOAL,
                    'motivo': 'Coaching executivo em tomada de decisão',
                    'aumento_valor': 3000,
                })
        
        elif tipo_eixo == TipoEixo.HUMAN:
            # Se pediu training, sugere automação
            if TRAINING_NEGOCIACAO in servicos_detectados:
                sugestoes.append({
                    'tipo': TipoEixo.STRATEGIC,
                    'servico': AUTOMACAO_IA,
                    'motivo': 'Automação para testar técnicas em tempo real',
                    'aumento_valor': 8000,
                })
            
            # Se pediu growth, sugere análise
            if GROWTH_MINDSET in servicos_detectados:
                sugestoes.append({
                    'tipo': TipoEixo.STRATEGIC,
                    'servico': ANALISE_DADOS,
                    'motivo': 'Dashboard para acompanhar evolução',
                    'aumento_valor': 6000,
                })
        
        return sugestoes
    
    def calcular_desconto_integracao(self, 
                                     servicos: List[str],
                                     tipo_eixo: TipoEixo) -> Dict:
        """
        Calcula desconto por integração (para fechar mais)
        """
        if tipo_eixo == TipoEixo.INTEGRADO:
            quantidade_servicos = len(servicos)
            
            if quantidade_servicos >= 3:
                desconto_percentual = 12  # 12% para 3+
            elif quantidade_servicos == 2:
                desconto_percentual = 8   # 8% para 2
            else:
                desconto_percentual = 0
            
            return {
                'eh_integrado': True,
                'desconto_percentual': desconto_percentual,
                'motivo': 'Desconto por solução integrada',
            }
        
        return {
            'eh_integrado': False,
            'desconto_percentual': 0,
        }
    
    def gerar_prompt_inteligente(self, 
                                 intencao: Dict,
                                 cliente_existing: bool = False) -> str:
        """
        Gera prompt personalizado baseado na intencão
        """
        tipo = intencao['tipo_eixo']
        servicos = intencao['servicos_strategic'] + intencao['servicos_human']
        
        base = """Você é vendedor especialista AXIOM.

Cliente quer: {tipo}
Serviços: {servicos}

ESTRATÉGIA:
1. Validar necessidade
2. Fazer perguntas diagnósticas
3. Sugerir integração (se aplicável)
4. Descrever benefícios específicos
5. Oferecer proposta"""
        
        if cliente_existing:
            base += """

⭐ CLIENTE EXISTENTE
Este cliente já comprou conosco.
Cross-sell / Upsell opportunity!
Mencione projetos anteriores naturalmente."""
        
        if tipo == TipoEixo.INTEGRADO:
            base += """

🔗 INTEGRAÇÃO DETECTADA
Cliente quer AMBOS os serviços.
Enfatize os benefícios de ter tudo integrado.
Sugira pacote especial."""
        
        return base.format(
            tipo=tipo.value,
            servicos=", ".join(servicos)
        )