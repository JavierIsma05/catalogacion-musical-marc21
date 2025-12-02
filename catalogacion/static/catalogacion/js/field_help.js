/**
 * field_help.js
 * Sistema de ayuda dinámica para campos MARC21
 * Los textos de ayuda se cargan desde field_help_texts.json
 */

(function () {
    "use strict";

    // Cache de textos de ayuda
    let helpTexts = null;

    /**
     * Carga los textos de ayuda desde el archivo JSON
     */
    async function loadHelpTexts() {
        if (helpTexts) return helpTexts;

        try {
            const basePath =
                document.querySelector('script[src*="field_help.js"]')?.src ||
                "";
            const jsonPath = basePath.replace(
                "field_help.js",
                "field_help_texts.json"
            );

            const response = await fetch(jsonPath);
            if (!response.ok)
                throw new Error("No se pudo cargar el archivo de ayuda");

            helpTexts = await response.json();
            return helpTexts;
        } catch (error) {
            console.warn("Error cargando textos de ayuda:", error);
            return { campos: {} };
        }
    }

    /**
     * Obtiene el texto de ayuda para un campo específico
     */
    function getHelpText(fieldCode) {
        if (!helpTexts || !helpTexts.campos || !helpTexts.campos[fieldCode]) {
            return "";
        }
        return helpTexts.campos[fieldCode].ayuda || "";
    }

    /**
     * Inicializa los tooltips de ayuda
     */
    async function initHelpTooltips() {
        await loadHelpTexts();

        const helpButtons = document.querySelectorAll(".campo-help-btn");

        helpButtons.forEach((btn) => {
            const fieldCode = btn.getAttribute("data-field-code");
            if (!fieldCode) return;

            // Crear tooltip si no existe
            if (!btn.querySelector(".campo-help-tooltip")) {
                const tooltip = document.createElement("div");
                tooltip.className = "campo-help-tooltip";

                const helpText = getHelpText(fieldCode);
                if (helpText) {
                    tooltip.textContent = helpText;
                } else {
                    tooltip.textContent = "Información de ayuda no disponible.";
                    tooltip.classList.add("campo-help-tooltip-empty");
                }

                btn.appendChild(tooltip);
            }
        });
    }

    /**
     * Actualiza los textos de ayuda (útil si se cargan dinámicamente nuevos campos)
     */
    function refreshHelpTooltips() {
        initHelpTooltips();
    }

    // Inicializar cuando el DOM esté listo
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initHelpTooltips);
    } else {
        initHelpTooltips();
    }

    // Exponer función para refrescar tooltips
    window.refreshFieldHelp = refreshHelpTooltips;

    // Observador para detectar cambios dinámicos en el DOM
    const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            if (mutation.addedNodes.length) {
                const hasNewHelpBtns = Array.from(mutation.addedNodes).some(
                    (node) =>
                        node.nodeType === 1 &&
                        (node.classList?.contains("campo-help-btn") ||
                            node.querySelector?.(".campo-help-btn"))
                );
                if (hasNewHelpBtns) {
                    initHelpTooltips();
                    break;
                }
            }
        }
    });

    // Observar cambios en el contenido principal
    document.addEventListener("DOMContentLoaded", () => {
        const mainContent = document.querySelector("main") || document.body;
        observer.observe(mainContent, { childList: true, subtree: true });
    });
})();
