(function () {
    "use strict";

    if (!window.CatalogacionAutocomplete) {
        console.warn(
            "CatalogacionAutocomplete no está disponible para títulos."
        );
        return;
    }

    const SELECTOR = '[data-autocomplete="titulo"]';
    const initialized = new WeakSet();

    const observer = new MutationObserver(() => {
        scan(document.body);
    });

    function scan(root) {
        const scope = root || document;
        scope.querySelectorAll(SELECTOR).forEach(initAutocomplete);
    }

    function initAutocomplete(input) {
        if (initialized.has(input)) {
            return;
        }

        const wrapper = input.closest(".autocomplete-wrapper");
        if (!wrapper) {
            return;
        }

        const suggestions = wrapper.querySelector(".autocomplete-suggestions");
        if (!suggestions) {
            return;
        }

        const hiddenInput = resolveHiddenInput(input);
        let ignoreNextInput = false;

        input.addEventListener("input", () => {
            if (ignoreNextInput) {
                ignoreNextInput = false;
                return;
            }
            if (hiddenInput) {
                hiddenInput.value = "";
            }
        });

        function syncValues(text, hiddenValue) {
            ignoreNextInput = true;
            input.value = text;
            if (hiddenInput) {
                hiddenInput.value = hiddenValue || "";
            }
        }

        CatalogacionAutocomplete.setup({
            input,
            suggestionsContainer: suggestions,
            endpoint: "/catalogacion/api/autocompletar/titulo/",
            minChars: 2,
            allowCreate: true,
            hiddenInput,
            transformResults: (data) =>
                (data?.results || []).map((item) => ({
                    id: item.id,
                    label: item.titulo || item.text || "",
                })),
            renderItem: (item) => `<strong>${escapeHtml(item.label)}</strong>`,
            renderCreateItem: (query) =>
                `<strong>Crear título:</strong> “${escapeHtml(query)}”`,
            onSelect: (item) => {
                syncValues(item.label, item.id);
            },
            onCreate: (query) => {
                syncValues(query, "");
            },
            onClear: () => {
                syncValues("", "");
            },
        });

        initialized.add(input);
    }

    function resolveHiddenInput(input) {
        const scope =
            input.closest(".formset-row") || input.closest("form") || document;
        const selector = input.dataset.hiddenFieldSelector;
        if (selector) {
            const scoped = scope.querySelector(selector);
            if (scoped) {
                return scoped;
            }
        }

        const fieldId = input.dataset.hiddenFieldId;
        if (fieldId) {
            const byId = document.getElementById(fieldId);
            if (byId) {
                return byId;
            }
        }

        const fieldName = input.dataset.hiddenField;
        if (!fieldName) {
            return null;
        }

        const endings = [`[name$="-${fieldName}"]`, `[name="${fieldName}"]`];
        for (const ending of endings) {
            const found = scope.querySelector(ending) || document.querySelector(ending);
            if (found) {
                return found;
            }
        }

        return null;
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text || "";
        return div.innerHTML;
    }

    document.addEventListener("DOMContentLoaded", () => {
        scan(document);
        observer.observe(document.body, { childList: true, subtree: true });
    });
})();
