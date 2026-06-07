/**
 * Menu mobile AXIOM — toggle, acessibilidade e fechamento ao navegar.
 */
(function initNavMobile() {
  const navConfig = window.AXIOM?.navigation || {};
  const nav = document.querySelector("[data-nav-mobile]");
  if (!nav) return;

  const toggle = nav.querySelector(".nav-toggle");
  const panel = nav.querySelector(".nav-panel");
  if (!toggle || !panel) return;

  const labelOpen = navConfig.toggleLabelOpen || "Abrir menu";
  const labelClose = navConfig.toggleLabelClose || "Fechar menu";
  const closeOnNavigate = navConfig.closeOnNavigate !== false;
  const lockBodyScroll = navConfig.lockBodyScroll !== false;

  const mq = window.matchMedia(
    `(max-width: ${navConfig.mobileBreakpoint || 768}px)`
  );

  function isMobileView() {
    return mq.matches;
  }

  function setOpen(open) {
    nav.classList.toggle("nav--open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? labelClose : labelOpen);

    if (lockBodyScroll && isMobileView()) {
      document.body.classList.toggle("nav-menu-open", open);
    }
  }

  function closeMenu() {
    if (nav.classList.contains("nav--open")) {
      setOpen(false);
    }
  }

  function syncDesktopState() {
    if (!isMobileView()) {
      document.body.classList.remove("nav-menu-open");
      nav.classList.remove("nav--open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", labelOpen);
    }
  }

  toggle.addEventListener("click", () => {
    setOpen(!nav.classList.contains("nav--open"));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeMenu();
    }
  });

  if (closeOnNavigate) {
    panel.querySelectorAll(".nav-link").forEach((link) => {
      link.addEventListener("click", () => {
        if (isMobileView()) {
          closeMenu();
        }
      });
    });
  }

  mq.addEventListener("change", syncDesktopState);
  syncDesktopState();
})();
