(function initAxiomChatbot() {
      const chatbot = document.getElementById('axiom-chatbot');
      if (!chatbot) return;

      const form = document.getElementById('chatbot-form');
      const input = document.getElementById('chatbot-input');
      const messagesEl = document.getElementById('chatbot-messages');
      const endpoint =
        chatbot.dataset.chatbotEndpoint ||
        window.AXIOM?.chatbot?.endpoint ||
        '';
      const welcomeMessage = chatbot.dataset.chatbotWelcome || 'Olá! Como posso ajudar?';

      function formatTime(date = new Date()) {
        return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
      }

      function appendMessage(text, role = 'bot') {
        const message = document.createElement('div');
        message.className = `chatbot-message chatbot-message--${role}`;
        message.innerHTML = `<p>${text}</p><time>${formatTime()}</time>`;
        messagesEl.appendChild(message);
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }

      function setTyping(isVisible) {
        const existing = messagesEl.querySelector('.chatbot-message--typing');
        if (!isVisible) {
          existing?.remove();
          return;
        }
        if (existing) return;

        const typing = document.createElement('div');
        typing.className = 'chatbot-message chatbot-message--typing';
        typing.textContent = 'AXIOM Assistant está digitando...';
        messagesEl.appendChild(typing);
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }

      const pageId = document.body.dataset.axiomPage;
      const origem = pageId === "human-performance" ? "human-performance" : "strategic-intelligence";

      // session_id simples, persistente durante a sessão do navegador
      let sessionId = sessionStorage.getItem('axiom-session-id');
      if (!sessionId) {
        sessionId = 'sess-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8);
        sessionStorage.setItem('axiom-session-id', sessionId);
      }
      
      async function requestBotReply(userText) {
        if (endpoint) {
          const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userText, session_id: sessionId, origem: origem })
          });

          if (!response.ok) {
            throw new Error('Falha na API do chatbot');
          }

          const data = await response.json();
          return data.reply || data.message || 'Recebi sua mensagem. Em breve retornaremos o contato.';
        }

        const isHumanPerformance =
          document.body.classList.contains("page-human-performance") ||
          document.body.dataset.axiomPage === "human-performance";

        const replies = isHumanPerformance
          ? {
              "o que é axiom human performance?":
                "AXIOM Human Performance une people analytics, OKRs, KPIs de equipe e dashboards para decisões sobre performance humana e resultados.",
              "como funcionam okrs para times?":
                "Estruturamos objetivos, rituais de check-in e painéis de progresso por time, alinhados à estratégia do negócio.",
              "quero um diagnóstico de performance humana":
                "Excelente. Acesse o formulário em Strategic Intelligence (Diagnóstico) ou descreva aqui seu contexto e tamanho do time.",
              "falar com um consultor humano":
                "Encaminharei ao time comercial. Informe e-mail ou telefone na próxima mensagem.",
            }
          : {
              "quais serviços a axiom oferece?":
                "Oferecemos análise de dados, inteligência artificial, automação, dashboards, diagnóstico estratégico e soluções web orientadas a performance.",
              "como funciona o diagnóstico estratégico?":
                "O diagnóstico mapeia indicadores, processos e oportunidades de melhoria. Você pode solicitar uma avaliação na seção Diagnóstico Estratégico.",
              "quero solicitar um orçamento":
                "Perfeito. Informe seu nome, empresa e principal desafio. Nossa equipe comercial preparará uma proposta personalizada.",
              "falar com um consultor humano":
                "Vou encaminhar seu interesse ao time comercial. Deixe seu e-mail ou telefone na próxima mensagem.",
            };

        const normalized = userText.trim().toLowerCase();
        const fallback = isHumanPerformance
          ? "Obrigado pelo contato. Nossa equipe Human Performance retornará em breve."
          : "Obrigado pelo contato. Nossa equipe comercial analisará sua mensagem e retornará em breve.";
        return replies[normalized] || fallback;
      }

      async function sendMessage(text) {
        const trimmed = text.trim();
        if (!trimmed) return;

        appendMessage(trimmed, 'user');
        input.value = '';
        setTyping(true);

        try {
          const reply = await requestBotReply(trimmed);
          setTyping(false);
          appendMessage(reply, 'bot');
        } catch (error) {
          setTyping(false);
          appendMessage('Não foi possível conectar ao assistente no momento. Tente novamente em instantes.', 'bot');
        }
      }

      appendMessage(welcomeMessage, 'bot');

      form.addEventListener('submit', (event) => {
        event.preventDefault();
        sendMessage(input.value);
      });

      chatbot.querySelectorAll('.chatbot-suggestion').forEach((button) => {
        button.addEventListener('click', () => {
          sendMessage(button.dataset.prompt || button.textContent);
        });
      });
    })();
