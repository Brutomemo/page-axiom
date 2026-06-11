/**
 * Choice cards estilo Typeform — seleção múltipla com feedback visual.
 */
(function initChoiceCards() {
  const CHECK_ICON =
    '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8.5L6.5 12L13 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function getFeedbackEl(container) {
    const id = container.dataset.feedbackId;
    if (id) return document.getElementById(id);
    return container.parentElement?.querySelector("[data-choice-feedback]");
  }

  function updateFeedback(container) {
    const feedback = getFeedbackEl(container);
    if (!feedback) return;

    const selected = container.querySelectorAll(".choice-card.is-selected").length;
    const label = container.dataset.choiceLabel || "opção";
    const plural = selected === 1 ? label : `${label}s`;

    feedback.classList.remove("is-error");
    feedback.hidden = selected === 0;
    if (selected > 0) {
      feedback.textContent = `${selected} ${plural} selecionada${selected === 1 ? "" : "s"}`;
    }
  }

  function setSelected(card, selected) {
    card.classList.toggle("is-selected", selected);
    card.setAttribute("aria-pressed", selected ? "true" : "false");
    const input = card.querySelector('input[type="checkbox"]');
    if (input) input.checked = selected;
  }

  function toggleCard(card) {
    const container = card.closest("[data-choice-cards]");
    if (!container) return;

    const isMultiple = container.dataset.multiple !== "false";
    if (!isMultiple) {
      container.querySelectorAll(".choice-card.is-selected").forEach((other) => {
        if (other !== card) setSelected(other, false);
      });
    }

    setSelected(card, !card.classList.contains("is-selected"));
    updateFeedback(container);
    container.dispatchEvent(new CustomEvent("choicechange", { bubbles: true }));
  }

  function ensureCheckIcon(card) {
    let check = card.querySelector(".choice-card__check");
    if (!check) {
      check = document.createElement("span");
      check.className = "choice-card__check";
      check.setAttribute("aria-hidden", "true");
      const input = card.querySelector('input[type="checkbox"]');
      if (input) {
        card.insertBefore(check, input);
      } else {
        card.appendChild(check);
      }
    }
    if (!check.innerHTML.trim()) {
      check.innerHTML = CHECK_ICON;
    }
  }

  function bindContainer(container) {
    const cards = container.querySelectorAll(".choice-card");
    cards.forEach((card, index) => {
      ensureCheckIcon(card);

      if (!card.hasAttribute("tabindex")) card.tabIndex = 0;
      if (!card.hasAttribute("role")) card.role = "button";
      if (!card.hasAttribute("aria-pressed")) card.setAttribute("aria-pressed", "false");
      if (!card.getAttribute("type")) card.type = "button";

      const keyEl = card.querySelector(".choice-card__key");
      if (keyEl && !keyEl.textContent.trim()) {
        keyEl.textContent = String.fromCharCode(65 + index);
      }

      card.addEventListener("click", () => toggleCard(card));
      card.addEventListener("keydown", (event) => {
        if (event.key === " " || event.key === "Enter") {
          event.preventDefault();
          toggleCard(card);
        }
      });
    });

    updateFeedback(container);
  }

  function init() {
    document.querySelectorAll("[data-choice-cards]").forEach(bindContainer);
  }

  window.AXIOM = window.AXIOM || {};
  window.AXIOM.getChoiceValues = function getChoiceValues(containerOrForm, fieldName) {
    let container = containerOrForm;
    if (containerOrForm?.querySelector) {
      container = containerOrForm.querySelector(
        `[data-choice-cards][data-field="${fieldName}"]`
      );
    }
    if (!container) return [];
    return Array.from(container.querySelectorAll(".choice-card.is-selected")).map(
      (card) => card.dataset.value || card.querySelector("input")?.value || ""
    );
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
