/**
 * Configuração global AXIOM — páginas, Unicorn, APIs.
 */
(function defineAxiomConfig() {
  const pages = {
    home: {
      id: "home",
      path: "index.html",
      title: "AXIOM Strategic Intelligence | Apresentação Executiva",
      navLabel: "Strategic Intelligence",
      unicornProjectId: "yWZ2Tbe094Fsjgy9NRnD",
      unicornVariant: "strategic",
    },
    humanPerformance: {
      id: "human-performance",
      path: "pages/human-performance.html",
      title: "AXIOM Human Performance | Performance Humana & People Analytics",
      navLabel: "Human Performance",
      /** Efeito Unicorn distinto da home (projeto seção contato / alternativo) */
      unicornProjectId: "UtvhDctN8AjL6tvf1yKd",
      unicornVariant: "human-performance",
    },
  };

  window.AXIOM = Object.freeze({
    siteName: "AXIOM Strategic Intelligence",
    lang: "pt-BR",

    chatbot: {
      endpoint: "https://axiombackend-production-25d9.up.railway.app/api/chat",
      welcome:
        "Olá! Sou o assistente comercial da AXIOM. Posso apresentar nossos serviços, explicar soluções de dados e IA, ou encaminhar seu contato.",
    },

    leadForm: {
      endpoint: "https://axiombackend-production-25d9.up.railway.app/api/lead",
    },

    /** Navegação mobile — breakpoint, rótulos e comportamento do menu */
    navigation: {
      mobileBreakpoint: 1024,
      toggleLabelOpen: "Abrir menu",
      toggleLabelClose: "Fechar menu",
      panelLabel: "Menu de navegação",
      closeOnNavigate: true,
      lockBodyScroll: true,
      showStatusInPanel: true,
    },

    pages,

    unicorn: {
      mainProjectId: pages.home.unicornProjectId,
      contatoProjectId: pages.humanPerformance.unicornProjectId,
      humanPerformanceProjectId: pages.humanPerformance.unicornProjectId,
    },

    /**
     * @param {string} pageId — ex.: "home" | "human-performance"
     */
    getPageConfig(pageId) {
      const entry = Object.values(pages).find(
        (p) => p.id === pageId || p.id === pageId?.replace(/_/g, "-")
      );
      return entry || null;
    },
  });
})();
