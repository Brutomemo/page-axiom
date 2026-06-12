/**
 * Formulários de diagnóstico / leads (#leadForm, #hpLeadForm).
 * Configure window.AXIOM.leadForm.endpoint para enviar à API.
 */
(function initLeadForms() {
  const forms = document.querySelectorAll("[data-lead-form], #leadForm, #hpLeadForm");
  if (!forms.length) return;

  let toastEl = null;
  let toastTimer = null;

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

  function clearChoiceErrors(form) {
    form.querySelectorAll("[data-choice-feedback]").forEach((feedback) => {
      feedback.classList.remove("is-error");
      if (!feedback.textContent || feedback.classList.contains("is-error")) {
        feedback.hidden = true;
      }
    });
  }

  function resetChoiceCards(form) {
    form.querySelectorAll(".choice-card.is-selected").forEach((card) => {
      card.classList.remove("is-selected");
      card.setAttribute("aria-pressed", "false");
      const input = card.querySelector('input[type="checkbox"]');
      if (input) input.checked = false;
    });
    form.querySelectorAll("[data-choice-cards]").forEach((container) => {
      const feedback = container.parentElement?.querySelector("[data-choice-feedback]");
      if (feedback) {
        feedback.hidden = true;
        feedback.textContent = "";
        feedback.classList.remove("is-error");
      }
    });
  }

  function resetForm(form) {
    form.reset();
    resetChoiceCards(form);
    form.classList.remove("is-submitted");
    updateProgress(form);
  }

  function setButtonState(btn, state) {
    if (!btn) return;
    btn.classList.remove("is-loading", "is-success", "is-error");
    if (state) btn.classList.add(state);
    btn.disabled = state === "is-loading";
  }

  function getToast() {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "axiom-form-toast";
      toastEl.setAttribute("role", "status");
      toastEl.setAttribute("aria-live", "polite");
      toastEl.innerHTML = `
        <span class="axiom-form-toast__icon" aria-hidden="true"></span>
        <div class="axiom-form-toast__body">
          <strong class="axiom-form-toast__title"></strong>
          <p class="axiom-form-toast__text"></p>
        </div>
      `;
      document.body.appendChild(toastEl);
    }
    return toastEl;
  }

  function showToast({ title, text, type = "success", accent = "strategic" }) {
    const toast = getToast();
    clearTimeout(toastTimer);

    toast.className = `axiom-form-toast axiom-form-toast--${type} axiom-form-toast--${accent}`;
    toast.querySelector(".axiom-form-toast__title").textContent = title;
    toast.querySelector(".axiom-form-toast__text").textContent = text;

    const iconMap = { success: "✓", error: "!" };
    toast.querySelector(".axiom-form-toast__icon").textContent = iconMap[type] || "✓";

    requestAnimationFrame(() => toast.classList.add("is-visible"));

    toastTimer = setTimeout(() => {
      toast.classList.remove("is-visible");
    }, 4200);
  }

  function preserveScroll(action) {
    const scrollY = window.scrollY;
    const result = action();
    if (result && typeof result.then === "function") {
      return result.finally(() => {
        requestAnimationFrame(() => {
          window.scrollTo({ top: scrollY, left: 0, behavior: "auto" });
        });
      });
    }
    requestAnimationFrame(() => {
      window.scrollTo({ top: scrollY, left: 0, behavior: "auto" });
    });
    return result;
  }

  function bindForm(form) {
    form.addEventListener("input", () => updateProgress(form));
    form.addEventListener("choicechange", () => updateProgress(form));
    updateProgress(form);

    form.addEventListener("submit", (event) => {
      event.preventDefault();

      const scrollY = window.scrollY;
      const choiceField = form.dataset.choiceField || "interesse";
      const choices = window.AXIOM?.getChoiceValues?.(form, choiceField) || [];
      const minChoices = Number(form.dataset.choiceMin || 0);

      clearChoiceErrors(form);

      if (minChoices > 0 && choices.length < minChoices) {
        showChoiceError(
          form,
          choiceField,
          `Selecione pelo menos ${minChoices} opção${minChoices > 1 ? "ões" : ""}.`
        );
        window.scrollTo({ top: scrollY, left: 0, behavior: "auto" });
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
        interesse: choices,
        servicos: choices,
      };

      const submitBtn = form.querySelector('[type="submit"]');
      const isHp = form.classList.contains("axiom-form--hp");
      const accent = isHp ? "hp" : "strategic";

      if (!endpoint) {
        console.info("[AXIOM] leadForm: endpoint não configurado.", payload);
        setButtonState(submitBtn, "is-success");
        resetForm(form);
        showToast({
          title: "Solicitação registrada",
          text: "Endpoint não configurado — dados apenas no console.",
          type: "success",
          accent,
        });
        window.scrollTo({ top: scrollY, left: 0, behavior: "auto" });
        setTimeout(() => setButtonState(submitBtn, null), 1600);
        return;
      }

      setButtonState(submitBtn, "is-loading");

      preserveScroll(
        fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        })
          .then(async (response) => {
            const data = await response.json().catch(() => ({}));
            if (!response.ok || data.success === false) {
              throw new Error(data.error || "Falha ao enviar formulário");
            }
            return data;
          })
          .then(() => {
            setButtonState(submitBtn, "is-success");
            resetForm(form);
            showToast({
              title: "Solicitação recebida",
              text: "Obrigado pelo interesse. Nossa equipe entrará em contato em breve.",
              type: "success",
              accent,
            });
            setTimeout(() => setButtonState(submitBtn, null), 1800);
          })
          .catch((err) => {
            console.error("[AXIOM] leadForm:", err);
            setButtonState(submitBtn, "is-error");
            showToast({
              title: "Não foi possível enviar",
              text: "Tente novamente em instantes ou fale com o assistente virtual.",
              type: "error",
              accent,
            });
            setTimeout(() => setButtonState(submitBtn, null), 2200);
          })
      );
    });
  }

  forms.forEach(bindForm);
})();
