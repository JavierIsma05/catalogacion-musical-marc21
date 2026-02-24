/**
 * Sistema de seguimiento de campos obligatorios MARC21
 * Actualiza el sidebar de progreso en tiempo real
 */
(function () {
  "use strict";

  const REQUIRED_FIELDS_CONFIG = {
    coleccion_manuscrita: [
      { id: "id_centro_catalogador", label: "040", tabId: "tab-admin" },
      {
        id: "grupo_100_130",
        label: "100/130",
        tabId: "tab-personas",
        group: true,
        fields: ["id_compositor_texto", "id_titulo_uniforme_texto"]
      },
      { id: "id_titulo_principal", label: "245", tabId: "tab-personas" },
      { id: "id_ms_imp", label: "340", tabId: "tab-produccion" },
      {
        id: "id_medio_interpretacion_382",
        label: "382",
        tabId: "tab-datos-musicales",
        special: true
      }
    ],

    obra_en_coleccion_manuscrita: [
      { id: "id_centro_catalogador", label: "040", tabId: "tab-admin" },
      { id: "id_compositor_texto", label: "100", tabId: "tab-personas" },
      { id: "id_titulo_principal", label: "245", tabId: "tab-personas" },
      { id: "id_ms_imp", label: "340", tabId: "tab-produccion" },
      {
        id: "id_medio_interpretacion_382",
        label: "382",
        tabId: "tab-datos-musicales",
        special: true
      }
    ],

    obra_manuscrita_individual: [
      { id: "id_centro_catalogador", label: "040", tabId: "tab-admin" },
      { id: "id_compositor_texto", label: "100", tabId: "tab-personas" },
      { id: "id_titulo_principal", label: "245", tabId: "tab-personas" },
      { id: "id_ms_imp", label: "340", tabId: "tab-produccion" },
      {
        id: "id_medio_interpretacion_382",
        label: "382",
        tabId: "tab-datos-musicales",
        special: true
      }
    ],

    coleccion_impresa: [
      { id: "id_centro_catalogador", label: "040", tabId: "tab-admin" },
      {
        id: "grupo_100_130",
        label: "100/130",
        tabId: "tab-personas",
        group: true,
        fields: ["id_compositor_texto", "id_titulo_uniforme_texto"]
      },
      { id: "id_titulo_principal", label: "245", tabId: "tab-personas" },
      { id: "id_ms_imp", label: "340", tabId: "tab-produccion" },
      {
        id: "id_medio_interpretacion_382",
        label: "382",
        tabId: "tab-datos-musicales",
        special: true
      }
    ],

    obra_en_coleccion_impresa: [
      { id: "id_centro_catalogador", label: "040", tabId: "tab-admin" },
      { id: "id_compositor_texto", label: "100", tabId: "tab-personas" },
      { id: "id_titulo_principal", label: "245", tabId: "tab-personas" },
      { id: "id_ms_imp", label: "340", tabId: "tab-produccion" },
      {
        id: "id_medio_interpretacion_382",
        label: "382",
        tabId: "tab-datos-musicales",
        special: true
      }
    ],

    obra_impresa_individual: [
      { id: "id_centro_catalogador", label: "040", tabId: "tab-admin" },
      { id: "id_compositor_texto", label: "100", tabId: "tab-personas" },
      { id: "id_titulo_principal", label: "245", tabId: "tab-personas" },
      { id: "id_ms_imp", label: "340", tabId: "tab-produccion" },
      {
        id: "id_medio_interpretacion_382",
        label: "382",
        tabId: "tab-datos-musicales",
        special: true
      }
    ]
  };

  let tipoObra = null;
  let requiredFields = [];
  let fieldStates = {};

  function init() {
    tipoObra = getTipoObra();
    if (!tipoObra)
      return console.warn("[RFT] No se pudo determinar tipo de obra");

    requiredFields = REQUIRED_FIELDS_CONFIG[tipoObra] || [];
    if (!requiredFields.length)
      return console.warn("[RFT] Sin config requiredFields para:", tipoObra);

    initFieldStates();
    renderProgressSidebar();
    setupFieldListeners();
    updateProgress();

    // re-check por autocompletados async
    setTimeout(updateProgress, 1500);
  }

  function getTipoObra() {
    // ✅ tu HTML real
    const wrap = document.querySelector(".form-with-progress-sidebar");
    const dataTipo = wrap?.getAttribute("data-tipo-obra");
    if (dataTipo) return dataTipo;

    // fallback
    if (window.TIPO_OBRA_ACTUAL) return window.TIPO_OBRA_ACTUAL;

    const urlParams = new URLSearchParams(window.location.search);
    const urlTipo = urlParams.get("tipo");
    if (urlTipo) return urlTipo;

    return null;
  }

  function initFieldStates() {
    fieldStates = {};
    requiredFields.forEach((f) => {
      fieldStates[f.id] = { complete: false, field: f };
    });
  }

  function renderProgressSidebar() {
    const list = document.getElementById("required-fields-list");
    if (!list) return;

    list.innerHTML = "";

    requiredFields.forEach((field) => {
      const li = document.createElement("li");
      li.className = "required-field-item incomplete";
      li.dataset.fieldId = field.id;
      li.dataset.tabId = field.tabId || "";
      li.title = field.label;

      const fieldCode = field.label.split(" - ")[0];

      li.innerHTML = `
        <div class="required-field-indicator"></div>
        <span class="required-field-code">${fieldCode}</span>
      `;

      li.addEventListener("click", () => {
        // ✅ navegar tab primero
        if (field.tabId && typeof window.switchTabById === "function") {
          window.switchTabById(field.tabId);
        } else {
          console.warn("[RFT] switchTabById no disponible todavía");
          return;
        }

        // ✅ luego scroll/focus
        setTimeout(() => {
          const el = resolveFieldElement(field);
          if (!el)
            return console.warn("[RFT] No se encontró elemento para:", field);

          el.scrollIntoView({ behavior: "smooth", block: "center" });
          if (["INPUT", "SELECT", "TEXTAREA"].includes(el.tagName)) {
            try {
              el.focus({ preventScroll: true });
            } catch (e) {}
          }
        }, 250);
      });

      list.appendChild(li);
    });
  }

  function resolveFieldElement(field) {
    if (field.group) {
      const first = field.fields?.[0];
      return first ? document.getElementById(first) : null;
    }

    if (field.special && field.id === "id_medio_interpretacion_382") {
      // intenta encontrar el primer select real del formset
      return (
        document.querySelector(
          ".medio-select:not(.empty-form .medio-select)"
        ) || document.querySelector('select[name^="medio_interpretacion_382_"]')
      );
    }

    return (
      document.getElementById(field.id) ||
      document.querySelector(`[name="${field.id.replace("id_", "")}"]`)
    );
  }

  function setupFieldListeners() {
    requiredFields.forEach((field) => {
      if (field.group) {
        (field.fields || []).forEach((subId) => {
          const el = document.getElementById(subId);
          if (!el) return;
          ["input", "change", "blur"].forEach((evt) =>
            el.addEventListener(evt, () => checkField(field.id))
          );
        });
        return;
      }

      if (field.special) {
        setupSpecialFieldListener(field);
        return;
      }

      const el =
        document.getElementById(field.id) ||
        document.querySelector(`[name="${field.id.replace("id_", "")}"]`);
      if (!el) return;

      ["input", "change", "blur"].forEach((evt) =>
        el.addEventListener(evt, () => checkField(field.id))
      );
    });

    document.addEventListener("input", debounce(updateProgress, 300));
    document.addEventListener("change", debounce(updateProgress, 300));
  }

  function setupSpecialFieldListener(field) {
    if (field.id !== "id_medio_interpretacion_382") return;

    const container =
      document.querySelector('[id*="medios_382"]') || document.body;
    const observer = new MutationObserver(() => checkField(field.id));
    observer.observe(container, { childList: true, subtree: true });

    container.addEventListener("input", () => checkField(field.id));
    container.addEventListener("change", () => checkField(field.id));
  }

  function checkField(fieldId) {
    const field = requiredFields.find((f) => f.id === fieldId);
    if (!field) return false;

    let complete = false;

    if (field.group) {
      complete = (field.fields || []).some((subId) => {
        const el = document.getElementById(subId);
        return el && el.value && el.value.trim() !== "";
      });
    } else if (field.special) {
      complete = checkSpecialField(field);
    } else {
      const el =
        document.getElementById(fieldId) ||
        document.querySelector(`[name="${fieldId.replace("id_", "")}"]`);
      complete = !!(el && el.value && String(el.value).trim() !== "");
    }

    fieldStates[fieldId].complete = complete;
    updateFieldItemUI(fieldId, complete);
    return complete;
  }

  function checkSpecialField(field) {
    if (field.id === "id_medio_interpretacion_382") {
      const selects = document.querySelectorAll(
        ".medio-select, select[name^='medio_interpretacion_382_']"
      );
      for (const s of selects) {
        if (s.closest(".empty-form") || s.closest(".d-none")) continue;
        if (s.value && s.value.trim() !== "") return true;
      }
      return false;
    }
    return false;
  }

  function updateFieldItemUI(fieldId, complete) {
    const item = document.querySelector(`[data-field-id="${fieldId}"]`);
    if (!item) return;

    item.classList.toggle("complete", complete);
    item.classList.toggle("incomplete", !complete);
  }

  function updateProgress() {
    requiredFields.forEach((f) => checkField(f.id));

    const completed = Object.values(fieldStates).filter(
      (s) => s.complete
    ).length;
    const total = requiredFields.length;
    const percentage = total ? Math.round((completed / total) * 100) : 0;

    updateProgressUI(completed, total - completed, total, percentage);
  }

  function updateProgressUI(completed, pending, total, percentage) {
    const percentEl = document.getElementById("progress-percent");
    if (percentEl) percentEl.textContent = `${percentage}%`;

    const circle = document.getElementById("progress-circle");
    if (circle) {
      const circumference = 226.19;
      const offset = circumference - (percentage / 100) * circumference;
      circle.style.strokeDashoffset = offset;
    }

    const c = document.getElementById("campos-completados");
    const p = document.getElementById("campos-pendientes");
    const t = document.getElementById("campos-totales");
    if (c) c.textContent = completed;
    if (p) p.textContent = pending;
    if (t) t.textContent = total;
  }

  function debounce(fn, wait) {
    let timeout;
    return function (...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => fn.apply(this, args), wait);
    };
  }

  window.RequiredFieldsTracker = {
    init,
    updateProgress,
    checkField,
    getProgress: () => {
      const completed = Object.values(fieldStates).filter(
        (s) => s.complete
      ).length;
      const total = requiredFields.length;
      return {
        completed,
        total,
        percentage: total ? Math.round((completed / total) * 100) : 0
      };
    }
  };

  // ✅ Auto init cuando DOM listo (y ya existen funciones de tabs, porque el script se carga al final)
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
