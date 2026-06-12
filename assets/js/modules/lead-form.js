/**
 * Formulários de diagnóstico / leads (#leadForm, #hpLeadForm).
 * Configure window.AXIOM.leadForm.endpoint para enviar à API.
 */
(function initLeadForms() {
  const forms = document.querySelectorAll("[data-lead-form], #leadForm, #hpLeadForm");
  if (!forms.length) return;

  function countProgress(form) {
    const fields = form.querySelectorAll(
      ".axiom-field__input[required], .axiom-field__textarea[required]"
    );
    const choiceContainers = form.querySelectorAll("[data-choice-cards]");
    let total = fields.length + choiceContainers.length;
    let filled = 0;

    fields.forEach((field) => {
      if (field.value.trim()) filled += 1;
    });

    choiceContainers.forEach((container) => {
      if (container.querySelector(".choice-card.is-selected")) filled += 1;
    });

    return total ? Math.round((filled / total) * 100) : 0;
  }

  function updateProgress(form) {
    const bar = form.querySelector(".axiom-form-progress__bar");
    if (bar) bar.style.width = `${countProgress(form)}%`;
  }

  function showChoiceError(form, fieldName, message) {
    const container = form.querySelector(`[data-choice-cards][data-field="${fieldName}"]`);
    const feedback = container?.parentElement?.querySelector("[data-choice-feedback]");
    if (feedback) {
      feedback.hidden = false;
      feedback.textContent = message;
      feedback.classList.add("is-error");
    }
  }

  function bindForm(form) {
    form.addEventListener("input", () => updateProgress(form));
    form.addEventListener("choicechange", () => updateProgress(form));
    updateProgress(form);

    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      const choiceField = form.dataset.choiceField || "interesse";
      const choices = window.AXIOM?.getChoiceValues?.(form, choiceField) || [];
      const minChoices = Number(form.dataset.choiceMin || 0);

      if (minChoices > 0 && choices.length < minChoices) {
        showChoiceError(
          form,
          choiceField,
          `Selecione pelo menos ${minChoices} opção${minChoices > 1 ? "ões" : ""}.`
        );
        return;
      }

      const endpoint =
        form.dataset.endpoint ||
        window.AXIOM?.leadForm?.endpoint ||
        "";

      const payload = {
        nome: form.querySelector("#nome, [name='nome']")?.value?.trim(),
        email: form.querySelector("#email, [name='email']")?.value?.trim(),
        telefone: form.querySelector("#telefone, [name='telefone']")?.value?.trim(),
        empresa: form.querySelector("#empresa, [name='empresa']")?.value?.trim(),
        mensagem: form.querySelector("#mensagem, [name='mensagem']")?.value?.trim(),
        origem: form.dataset.origem || "strategic-intelligence",
      };

      payload[choiceField] = choices;

      const submitBtn = form.querySelector('[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;

      if (!endpoint) {
        console.info("[AXIOM] leadForm: endpoint não configurado.", payload);
        form.classList.add("is-submitted");
        if (submitBtn) submitBtn.disabled = false;
        return;
      }

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        if (!response.ok) throw new Error("Falha ao enviar formulário");
        form.classList.add("is-submitted");
      } catch (err) {
        console.error("[AXIOM] leadForm:", err);
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  forms.forEach(bindForm);
})();
