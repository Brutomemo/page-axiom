/**
 * Formulário de diagnóstico / leads (#leadForm).
 * Configure window.AXIOM.leadForm.endpoint para enviar à API.
 */
(function initLeadForm() {
  const form = document.getElementById("leadForm");
  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const endpoint =
      window.AXIOM?.leadForm?.endpoint ||
      form.dataset.endpoint ||
      "";

    const payload = {
      nome: document.getElementById("nome")?.value?.trim(),
      email: document.getElementById("email")?.value?.trim(),
      telefone: document.getElementById("telefone")?.value?.trim(),
      empresa: document.getElementById("empresa")?.value?.trim(),
      interesse: document.getElementById("interesse")?.value,
      mensagem: document.getElementById("mensagem")?.value?.trim(),
    };

    if (!endpoint) {
      console.info("[AXIOM] leadForm: endpoint não configurado.", payload);
      return;
    }

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error("Falha ao enviar formulário");
    } catch (err) {
      console.error("[AXIOM] leadForm:", err);
    }
  });
})();
