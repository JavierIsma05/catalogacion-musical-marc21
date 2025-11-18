/**
 * Autocomplete editable para campos de Título Uniforme y Forma Musical
 * Campos: 130 $a, 130 $k, 240 $a, 240 $k
 */

(function () {
    "use strict";

    // Configuración de autocompletes
    const autocompletes = [
        {
            inputId: "id_titulo_uniforme_texto",
            hiddenInputId: "id_titulo_uniforme",
            suggestionsId: "titulo-uniforme-suggestions",
            apiUrl: "/catalogacion/api/autocompletar/titulo/",
            fieldName: "titulo",
            createLabel: "Crear nuevo título:",
            minLength: 2,
        },
        {
            inputId: "id_forma_130_texto",
            hiddenInputId: "id_forma_130",
            suggestionsId: "forma-130-suggestions",
            apiUrl: "/catalogacion/api/autocompletar/forma-musical/",
            fieldName: "forma",
            createLabel: "Crear nueva forma musical:",
            minLength: 2,
        },
        {
            inputId: "id_titulo_240_texto",
            hiddenInputId: "id_titulo_240",
            suggestionsId: "titulo-240-suggestions",
            apiUrl: "/catalogacion/api/autocompletar/titulo/",
            fieldName: "titulo",
            createLabel: "Crear nuevo título:",
            minLength: 2,
        },
        {
            inputId: "id_forma_240_texto",
            hiddenInputId: "id_forma_240",
            suggestionsId: "forma-240-suggestions",
            apiUrl: "/catalogacion/api/autocompletar/forma-musical/",
            fieldName: "forma",
            createLabel: "Crear nueva forma musical:",
            minLength: 2,
        },
    ];

    // Inicializar cada autocomplete
    autocompletes.forEach((config) => {
        initAutocomplete(config);
    });

    function initAutocomplete(config) {
        const input = document.getElementById(config.inputId);
        const hiddenInput = document.getElementById(config.hiddenInputId);
        const suggestionsContainer = document.getElementById(
            config.suggestionsId
        );

        if (!input || !suggestionsContainer) {
            // Debug silencioso - estos campos pueden no existir según el tipo de obra
            return;
        }

        let debounceTimer = null;
        let selectedIndex = -1;

        // Cargar datos iniciales si hay un ID
        if (hiddenInput && hiddenInput.value) {
            loadInitialData(config, input, hiddenInput);
        }

        // Evento de escritura
        input.addEventListener("input", function (e) {
            const query = e.target.value.trim();

            if (query.length < config.minLength) {
                hideSuggestions(suggestionsContainer);
                return;
            }

            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                searchItems(config, query, suggestionsContainer);
            }, 300);
        });

        // Navegación con teclado
        input.addEventListener("keydown", function (e) {
            if (!suggestionsContainer.classList.contains("show")) return;

            const items =
                suggestionsContainer.querySelectorAll(".autocomplete-item");

            switch (e.key) {
                case "ArrowDown":
                    e.preventDefault();
                    selectedIndex = Math.min(
                        selectedIndex + 1,
                        items.length - 1
                    );
                    updateSelection(items, selectedIndex);
                    break;

                case "ArrowUp":
                    e.preventDefault();
                    selectedIndex = Math.max(selectedIndex - 1, -1);
                    updateSelection(items, selectedIndex);
                    break;

                case "Enter":
                    e.preventDefault();
                    if (selectedIndex >= 0 && items[selectedIndex]) {
                        items[selectedIndex].click();
                    }
                    break;

                case "Escape":
                    e.preventDefault();
                    hideSuggestions(suggestionsContainer);
                    break;
            }
        });

        // Cerrar al hacer click fuera
        document.addEventListener("click", function (e) {
            if (
                !input.contains(e.target) &&
                !suggestionsContainer.contains(e.target)
            ) {
                hideSuggestions(suggestionsContainer);
            }
        });
    }

    function searchItems(config, query, suggestionsContainer) {
        fetch(`${config.apiUrl}?q=${encodeURIComponent(query)}`)
            .then((response) => response.json())
            .then((data) => {
                const results = data.results || [];
                showSuggestions(config, results, query, suggestionsContainer);
            })
            .catch((error) => {
                console.error(`Error al buscar ${config.fieldName}:`, error);
            });
    }

    function showSuggestions(config, results, query, suggestionsContainer) {
        suggestionsContainer.innerHTML = "";

        if (results.length === 0) {
            const createItem = createSuggestionItem(config, {
                [config.fieldName]: query,
                isNew: true,
            });
            suggestionsContainer.appendChild(createItem);
        } else {
            results.forEach((result) => {
                const item = createSuggestionItem(config, result);
                suggestionsContainer.appendChild(item);
            });

            // Agregar opción para crear nuevo
            const createItem = createSuggestionItem(config, {
                [config.fieldName]: query,
                isNew: true,
            });
            suggestionsContainer.appendChild(createItem);
        }

        suggestionsContainer.classList.add("show");
    }

    function createSuggestionItem(config, data) {
        const item = document.createElement("div");
        item.className = "autocomplete-item";

        if (data.isNew) {
            item.classList.add("autocomplete-item-new");
            item.innerHTML = `
                <i class="bi bi-plus-circle me-2"></i>
                <strong>${config.createLabel}</strong> "${escapeHtml(
                data[config.fieldName]
            )}"
            `;
        } else {
            item.innerHTML = `
                <div><strong>${escapeHtml(
                    data[config.fieldName]
                )}</strong></div>
            `;
        }

        item.addEventListener("click", function () {
            selectItem(config, data);
        });

        return item;
    }

    function selectItem(config, data) {
        const input = document.getElementById(config.inputId);
        const hiddenInput = document.getElementById(config.hiddenInputId);
        const suggestionsContainer = document.getElementById(
            config.suggestionsId
        );

        if (data.isNew) {
            input.value = data[config.fieldName];
            if (hiddenInput) hiddenInput.value = "";
        } else {
            input.value = data[config.fieldName];
            if (hiddenInput) hiddenInput.value = data.id;
        }

        hideSuggestions(suggestionsContainer);
    }

    function loadInitialData(config, input, hiddenInput) {
        fetch(`${config.apiUrl}?id=${hiddenInput.value}`)
            .then((response) => response.json())
            .then((data) => {
                if (data.results && data.results.length > 0) {
                    const item = data.results[0];
                    input.value = item[config.fieldName];
                }
            })
            .catch((error) => {
                console.error(`Error al cargar ${config.fieldName}:`, error);
            });
    }

    function updateSelection(items, selectedIndex) {
        items.forEach((item, index) => {
            if (index === selectedIndex) {
                item.classList.add("selected");
                item.scrollIntoView({ block: "nearest" });
            } else {
                item.classList.remove("selected");
            }
        });
    }

    function hideSuggestions(suggestionsContainer) {
        suggestionsContainer.classList.remove("show");
        suggestionsContainer.innerHTML = "";
    }

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }
})();
