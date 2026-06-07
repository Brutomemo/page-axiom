/**
 * Inicialização por página — título, classe body, links ativos no nav.
 */
(function bootstrapAxiomPage() {
  const pageId = document.body?.dataset?.axiomPage;
  if (!pageId || !window.AXIOM?.getPageConfig) return;

  const config = window.AXIOM.getPageConfig(pageId);
  if (!config) return;

  if (config.title) {
    document.title = config.title;
  }

  document.querySelectorAll("[data-nav-page]").forEach((link) => {
    const target = link.getAttribute("data-nav-page");
    if (target === pageId) {
      link.classList.add("nav-link--active");
      link.setAttribute("aria-current", "page");
    }
  });
})();
