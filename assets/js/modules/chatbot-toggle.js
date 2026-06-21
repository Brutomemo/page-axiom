(function initChatbotToggle() {
    const widget = document.getElementById('chatbot-widget');
    const fab = document.getElementById('chatbot-fab');
    const closeBtn = document.getElementById('chatbot-close');
    const cta = document.getElementById('chatbot-cta');
    if (!widget || !fab) return;
  
    function openChat() {
      widget.classList.add('is-open');
      fab.setAttribute('aria-expanded', 'true');
      fab.setAttribute('aria-label', 'Fechar assistente AXIOM');
      document.getElementById('chatbot-input')?.focus({ preventScroll: true });
    }
  
    function closeChat() {
      widget.classList.remove('is-open');
      fab.setAttribute('aria-expanded', 'false');
      fab.setAttribute('aria-label', 'Abrir assistente AXIOM');
    }
  
    function toggleChat() {
      widget.classList.contains('is-open') ? closeChat() : openChat();
    }
  
    fab.addEventListener('click', toggleChat);
    closeBtn?.addEventListener('click', closeChat);
    cta?.addEventListener('click', openChat);
  
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && widget.classList.contains('is-open')) {
        closeChat();
      }
    });
  
    document.addEventListener('click', (event) => {
      if (!widget.classList.contains('is-open')) return;
      if (widget.contains(event.target)) return;
      closeChat();
    });
  })();