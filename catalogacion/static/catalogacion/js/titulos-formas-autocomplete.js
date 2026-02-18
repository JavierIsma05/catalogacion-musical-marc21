/**
 * Autocomplete editable para campos de Título Uniforme y Forma Musical
 * Campos: 130 $a, 130 $k, 240 $a, 240 $k
 */

(function () {
    "use strict";

    if (!window.CatalogacionAutocomplete) {
        console.warn("Autocomplete base no disponible para títulos/formas");
        return;
    }

    // Nota: forma_130_texto y forma_240_texto ($k) usan selector de botones fijos
    // definido en bloque_1xx.html — no requieren autocomplete aquí.
    const configs = [
        {
            inputId: "id_titulo_uniforme_texto",
            hiddenInputId: "id_titulo_uniforme",
            suggestionsId: "titulo-uniforme-suggestions",
            apiUrl: "/catalogacion/api/autocompletar/titulo/",
            fieldName: "titulo",
            createLabel: "Crear nuevo título",
        },
        {
            inputId: "id_titulo_240_texto",
            hiddenInputId: "id_titulo_240",
            suggestionsId: "titulo-240-suggestions",
            apiUrl: "/catalogacion/api/autocompletar/titulo/",
            fieldName: "titulo",
            createLabel: "Crear nuevo título",
        },
    ];

    configs.forEach((config) => initializeField(config));

    function initializeField(config) {
        const input = document.getElementById(config.inputId);
        const hiddenInput = document.getElementById(config.hiddenInputId);
        const suggestions = document.getElementById(config.suggestionsId);

        if (!input || !suggestions) {
            return;
        }

        if (hiddenInput && hiddenInput.value) {
            preloadValue(config, input, hiddenInput);
        }

        CatalogacionAutocomplete.setup({
            input,
            hiddenInput,
            suggestionsContainer: suggestions,
            endpoint: config.apiUrl,
            minChars: config.minLength || 2,
            transformResults: (data) =>
                (data?.results || []).map((item) => ({
                    id: item.id,
                    label: item[config.fieldName],
                    raw: item,
                })),
            renderItem: (item) => `<strong>${escapeHtml(item.label)}</strong>`,
            renderCreateItem: (query) =>
                `<strong>${config.createLabel}:</strong> “${escapeHtml(
                    query
                )}”`,
            onSelect: (item, elements) => {
                elements.input.value = item.label;
                if (elements.hiddenInput) {
                    elements.hiddenInput.value = item.id || "";
                }
            },
            onCreate: (query, elements) => {
                elements.input.value = query;
                if (elements.hiddenInput) {
                    elements.hiddenInput.value = "";
                }
            },
            onClear: (elements) => {
                if (elements.hiddenInput) {
                    elements.hiddenInput.value = "";
                }
            },
        });
    }

    function preloadValue(config, input, hiddenInput) {
        fetch(`${config.apiUrl}?id=${hiddenInput.value}`)
            .then((response) => response.json())
            .then((data) => {
                const item = data?.results?.[0];
                if (!item) return;
                input.value = item[config.fieldName];
                // Notificar al tracker de campos obligatorios
                // Solo dispatch "change" (no "input" para no disparar búsqueda de autocomplete)
                input.dispatchEvent(new Event("change", { bubbles: true }));
                if (window.RequiredFieldsTracker) {
                    window.RequiredFieldsTracker.updateProgress();
                }
            })
            .catch((error) =>
                console.error(`Error al precargar ${config.fieldName}`, error)
            );
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text || "";
        return div.innerHTML;
    }
})();
