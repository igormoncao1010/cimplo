const WHATSAPP_NUMBER = "5532999935590";

const leadForm = document.querySelector("#leadForm");
const phoneInput = document.querySelector("#phone");
const animatedElements = document.querySelectorAll(
  ".trust-bar div, .section-heading, .highlight-grid article, .intro-copy, .treatment-grid article, .feature-grid article, .steps div, .faq-list details, .contact-band"
);

animatedElements.forEach((element) => element.classList.add("reveal"));

if ("IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.14 }
  );

  animatedElements.forEach((element) => revealObserver.observe(element));
} else {
  animatedElements.forEach((element) => element.classList.add("is-visible"));
}

function onlyDigits(value) {
  return value.replace(/\D/g, "");
}

function formatPhone(value) {
  const digits = onlyDigits(value).slice(0, 11);

  if (digits.length <= 2) {
    return digits;
  }

  if (digits.length <= 6) {
    return `(${digits.slice(0, 2)}) ${digits.slice(2)}`;
  }

  if (digits.length <= 10) {
    return `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`;
  }

  return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`;
}

phoneInput.addEventListener("input", (event) => {
  event.target.value = formatPhone(event.target.value);
});

leadForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const formData = new FormData(leadForm);
  const name = String(formData.get("name") || "").trim();
  const phone = String(formData.get("phone") || "").trim();
  const treatment = String(formData.get("treatment") || "").trim();
  const message = String(formData.get("message") || "").trim();

  if (onlyDigits(phone).length < 10) {
    phoneInput.focus();
    phoneInput.setCustomValidity("Informe um telefone válido com DDD.");
    phoneInput.reportValidity();
    phoneInput.setCustomValidity("");
    return;
  }

  const leadMessage = [
    "Olá, equipe Cimplo! Quero agendar uma consulta.",
    "",
    `Nome: ${name}`,
    `Telefone: ${phone}`,
    `Interesse: ${treatment}`,
    message ? `Mensagem: ${message}` : "",
    "",
    "Vim pelo site."
  ].filter(Boolean).join("\n");

  const whatsappUrl = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(leadMessage)}`;
  window.open(whatsappUrl, "_blank", "noopener,noreferrer");
});
