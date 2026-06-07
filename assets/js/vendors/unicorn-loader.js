/**
 * Carrega UnicornStudio e inicializa projetos [data-us-project].
 * ID do projeto: atributo no HTML ou AXIOM.getPageConfig().unicornProjectId
 */
(function loadAxiomUnicorn() {
  const pageId = document.body?.dataset?.axiomPage;
  const pageConfig =
    pageId && window.AXIOM?.getPageConfig
      ? window.AXIOM.getPageConfig(pageId)
      : null;

  document.querySelectorAll("[data-us-project]").forEach((el) => {
    if (!el.getAttribute("data-us-project") && pageConfig?.unicornProjectId) {
      el.setAttribute("data-us-project", pageConfig.unicornProjectId);
    }
  });

  function initStudio() {
    if (typeof UnicornStudio === "undefined") return;
    try {
      UnicornStudio.init();
      window.UnicornStudio.isInitialized = true;
    } catch (e) {
      console.warn("[AXIOM] UnicornStudio.init:", e);
    }
  }

  if (window.UnicornStudio?.isInitialized) {
    initStudio();
    return;
  }

  window.UnicornStudio = window.UnicornStudio || { isInitialized: false };

  const existing = document.querySelector('script[data-axiom-unicorn-sdk]');
  if (existing) {
    existing.addEventListener("load", initStudio);
    return;
  }

  const script = document.createElement("script");
  script.src =
    "https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.29/dist/unicornStudio.umd.js";
  script.dataset.axiomUnicornSdk = "true";
  script.onload = function () {
    if (!window.UnicornStudio.isInitialized) initStudio();
  };
  (document.head || document.body).appendChild(script);
})();
