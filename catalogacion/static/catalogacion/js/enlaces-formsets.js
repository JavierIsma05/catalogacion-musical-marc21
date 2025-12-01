(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        document
            .querySelectorAll('[data-enlace-formset="true"]')
            .forEach(setupEnlaceFormset);
    });

    function setupEnlaceFormset(container) {
        const prefix = container.dataset.formsetPrefix;
        const numeroPrefix = container.dataset.numeroPrefix || "773";
        const personaEndpoint =
            container.dataset.personaEndpoint ||
            "/catalogacion/api/autocompletar/persona/";

        if (!prefix) {
            return;
        }

        const formsWrapper = container.querySelector(".formset-forms");
        const emptyForm = container.querySelector(".empty-form");
        const addButton = container.querySelector(".add-form-row");
        const totalFormsInput =
            container.querySelector(`#id_${prefix}-TOTAL_FORMS`) ||
            container.querySelector(`[name="${prefix}-TOTAL_FORMS"]`);
        const numeroTemplate = container.querySelector(
            "[data-numero-template]"
        );

        if (!formsWrapper || !emptyForm) {
            console.warn("Formset 7XX: estructura incompleta para", prefix);
            return;
        }

        reindexForms();

        if (addButton) {
            addButton.addEventListener("click", function (event) {
                event.preventDefault();
                const clone = emptyForm.cloneNode(true);
                clone.classList.remove("empty-form", "d-none");
                formsWrapper.appendChild(clone);
                reindexForms();
            });
        }

        container.addEventListener("click", function (event) {
            if (event.target.closest(".delete-row-btn")) {
                handleDeleteRow(event);
                return;
            }

            if (event.target.closest(".add-numero-btn")) {
                handleAddNumero(event);
                return;
            }

            if (event.target.closest(".delete-numero-btn")) {
                handleDeleteNumero(event);
            }
        });

        function handleDeleteRow(event) {
            const row = event.target.closest(".formset-row");
            if (!row || row.classList.contains("empty-form")) {
                return;
            }

            const deleteField = row.querySelector('[name$="-DELETE"]');
            if (deleteField && row.classList.contains("existing-form")) {
                deleteField.checked = !deleteField.checked;
                row.classList.toggle("marked-for-delete", deleteField.checked);
            } else {
                row.remove();
                reindexForms();
            }
        }

        function handleAddNumero(event) {
            event.preventDefault();
            const row = event.target.closest(".formset-row");
            if (!row || row.classList.contains("empty-form")) {
                return;
            }

            const target = row.querySelector("[data-numeros-container]");
            if (!target || !numeroTemplate) {
                return;
            }

            const clone = numeroTemplate.cloneNode(true);
            clone.classList.remove("d-none");
            clone.removeAttribute("data-numero-template");

            const input = clone.querySelector(".numero-w-input");
            const rowIndex = row.dataset.formIndex || "0";
            if (input) {
                input.name = `numero_${numeroPrefix}_${rowIndex}_${Date.now()}`;
            }

            target.appendChild(clone);

            const placeholder = target.querySelector(".numero-placeholder");
            if (placeholder) {
                placeholder.remove();
            }
        }

        function handleDeleteNumero(event) {
            event.preventDefault();
            const numeroRow = event.target.closest(".numero-form-row");
            if (!numeroRow || numeroRow.hasAttribute("data-numero-template")) {
                return;
            }
            numeroRow.remove();
        }

        function reindexForms() {
            const rows = formsWrapper.querySelectorAll(
                ".formset-row:not(.empty-form)"
            );

            rows.forEach(function (row, index) {
                row.dataset.formIndex = String(index);

                row.querySelectorAll("input, select, textarea").forEach(
                    function (field) {
                        updateIndexedAttribute(field, "name", index);
                        updateIndexedAttribute(field, "id", index);
                    }
                );

                row.querySelectorAll("label").forEach(function (label) {
                    updateIndexedAttribute(label, "for", index);
                });

                const numerosContainer = row.querySelector(
                    "[data-numeros-container]"
                );
                if (numerosContainer) {
                    numerosContainer.dataset.numerosContainer = String(index);
                }

                initAutoridadAutocomplete(row);
            });

            if (totalFormsInput) {
                totalFormsInput.value = rows.length;
            }
        }

        function updateIndexedAttribute(element, attribute, index) {
            const value = element.getAttribute(attribute);
            if (!value) {
                return;
            }

            if (value.includes("__prefix__")) {
                element.setAttribute(
                    attribute,
                    value.replace(/__prefix__/g, index)
                );
                return;
            }

            const regex = new RegExp(`(${prefix}-)(\d+)`);
            if (regex.test(value)) {
                element.setAttribute(
                    attribute,
                    value.replace(regex, `$1${index}`)
                );
            }
        }

        function initAutoridadAutocomplete(row) {
            row.querySelectorAll("[data-autoridad-input]").forEach(function (
                input
            ) {
                if (input.dataset.autocompleteInit === "1") {
                    return;
                }
                input.dataset.autocompleteInit = "1";

                const wrapper = input.closest(".autocomplete-wrapper");
                const suggestions = wrapper
                    ? wrapper.querySelector(".autocomplete-suggestions")
                    : null;
                const hiddenFieldName =
                    input.dataset.hiddenField || "encabezamiento_principal";
                const hiddenField = row.querySelector(
                    `input[name$="-${hiddenFieldName}"]`
                );

                if (!wrapper || !suggestions || !hiddenField) {
                    return;
                }

                let debounceTimer = null;
                let abortController = null;

                input.addEventListener("input", function () {
                    const query = input.value.trim();
                    if (query.length < 2) {
                        hideSuggestions();
                        hiddenField.value = "";
                        return;
                    }

                    clearTimeout(debounceTimer);
                    debounceTimer = setTimeout(function () {
                        searchPersonas(query);
                    }, 250);
                });

                document.addEventListener("click", function (event) {
                    if (!wrapper.contains(event.target)) {
                        hideSuggestions();
                    }
                });

                function searchPersonas(query) {
                    if (abortController) {
                        abortController.abort();
                    }
                    abortController = new AbortController();

                    fetch(`${personaEndpoint}?q=${encodeURIComponent(query)}`, {
                        signal: abortController.signal,
                    })
                        .then((response) => response.json())
                        .then((data) =>
                            renderSuggestions(data.results || [], query)
                        )
                        .catch((error) => {
                            if (error.name !== "AbortError") {
                                console.error("Autocomplete 7XX:", error);
                            }
                        });
                }

                function renderSuggestions(results, query) {
                    suggestions.innerHTML = "";

                    results.forEach(function (result) {
                        const option = document.createElement("div");
                        option.className = "autocomplete-item";
                        option.innerHTML = `
                            <strong>${escapeHtml(
                                result.apellidos_nombres || result.text || ""
                            )}</strong>
                            ${
                                result.coordenadas_biograficas
                                    ? `<small class="text-muted d-block">${escapeHtml(
                                          result.coordenadas_biograficas
                                      )}</small>`
                                    : ""
                            }
                        `;
                        option.addEventListener("click", function () {
                            input.value =
                                result.apellidos_nombres || result.text || "";
                            hiddenField.value = result.id || "";
                            hideSuggestions();
                        });
                        suggestions.appendChild(option);
                    });

                    const createOption = document.createElement("div");
                    createOption.className =
                        "autocomplete-item autocomplete-item-new";
                    createOption.innerHTML = `<i class="bi bi-plus-circle me-2"></i> Crear nuevo: "${escapeHtml(
                        query
                    )}"`;
                    createOption.addEventListener("click", function () {
                        hiddenField.value = "";
                        input.value = query;
                        hideSuggestions();
                    });
                    suggestions.appendChild(createOption);

                    suggestions.classList.add("is-visible");
                }

                function hideSuggestions() {
                    suggestions.classList.remove("is-visible");
                    suggestions.innerHTML = "";
                }
            });
        }
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text || "";
        return div.innerHTML;
    }
})();
