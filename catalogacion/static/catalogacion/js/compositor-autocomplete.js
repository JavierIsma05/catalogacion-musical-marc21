/**
 * Autocomplete editable para campo Compositor (100 $a)
 * Permite buscar compositores existentes o crear nuevos
 */

(function () {
    "use strict";

    const compositorInput = document.getElementById("id_compositor_texto");
    const coordenadasInput = document.getElementById(
        "id_compositor_coordenadas"
    );
    const compositorIdInput = document.getElementById("id_compositor");
    const suggestionsContainer = document.getElementById(
        "compositor-suggestions"
    );

    if (!compositorInput || !suggestionsContainer) {
        console.warn("Compositor autocomplete: elementos no encontrados");
        return;
    }

    let debounceTimer = null;
    let currentSuggestions = [];
    let selectedIndex = -1;

    // Inicializar - si hay un compositor seleccionado, cargar sus datos
    if (compositorIdInput.value) {
        loadCompositorData(compositorIdInput.value);
    }

    // Evento de escritura en el input
    compositorInput.addEventListener("input", function (e) {
        const query = e.target.value.trim();

        if (query.length < 2) {
            hideSuggestions();
            return;
        }

        // Debounce para evitar demasiadas peticiones
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            searchCompositors(query);
        }, 300);
    });

    // Navegación con teclado
    compositorInput.addEventListener("keydown", function (e) {
        if (!suggestionsContainer.classList.contains("show")) return;

        const items =
            suggestionsContainer.querySelectorAll(".autocomplete-item");

        switch (e.key) {
            case "ArrowDown":
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
                updateSelection(items);
                break;

            case "ArrowUp":
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, -1);
                updateSelection(items);
                break;

            case "Enter":
                e.preventDefault();
                if (selectedIndex >= 0 && items[selectedIndex]) {
                    items[selectedIndex].click();
                }
                break;

            case "Escape":
                e.preventDefault();
                hideSuggestions();
                break;
        }
    });

    // Cerrar al hacer click fuera
    document.addEventListener("click", function (e) {
        if (
            !compositorInput.contains(e.target) &&
            !suggestionsContainer.contains(e.target)
        ) {
            hideSuggestions();
        }
    });

    // Buscar compositores
    function searchCompositors(query) {
        fetch(
            `/catalogacion/api/autocompletar/persona/?q=${encodeURIComponent(
                query
            )}`
        )
            .then((response) => response.json())
            .then((data) => {
                currentSuggestions = data.results || [];
                showSuggestions(currentSuggestions, query);
            })
            .catch((error) => {
                console.error("Error al buscar compositores:", error);
            });
    }

    // Mostrar sugerencias
    function showSuggestions(suggestions, query) {
        suggestionsContainer.innerHTML = "";
        selectedIndex = -1;

        if (suggestions.length === 0) {
            // Mostrar opción para crear nuevo
            const createItem = createSuggestionItem({
                apellidos_nombres: query,
                coordenadas_biograficas: "",
                isNew: true,
            });
            suggestionsContainer.appendChild(createItem);
        } else {
            // Mostrar sugerencias existentes
            suggestions.forEach((suggestion) => {
                const item = createSuggestionItem(suggestion);
                suggestionsContainer.appendChild(item);
            });

            // Agregar opción para crear nuevo al final
            const createItem = createSuggestionItem({
                apellidos_nombres: query,
                coordenadas_biograficas: "",
                isNew: true,
            });
            suggestionsContainer.appendChild(createItem);
        }

        suggestionsContainer.classList.add("show");
    }

    // Crear elemento de sugerencia
    function createSuggestionItem(data) {
        const item = document.createElement("div");
        item.className = "autocomplete-item";

        if (data.isNew) {
            item.classList.add("autocomplete-item-new");
            item.innerHTML = `
                <i class="bi bi-plus-circle me-2"></i>
                <strong>Crear nuevo:</strong> "${escapeHtml(
                    data.apellidos_nombres
                )}"
            `;
        } else {
            item.innerHTML = `
                <div><strong>${escapeHtml(
                    data.apellidos_nombres
                )}</strong></div>
                ${
                    data.coordenadas_biograficas
                        ? `<small class="text-muted">${escapeHtml(
                              data.coordenadas_biograficas
                          )}</small>`
                        : ""
                }
            `;
        }

        item.addEventListener("click", function () {
            selectCompositor(data);
        });

        return item;
    }

    // Seleccionar compositor
    function selectCompositor(data) {
        if (data.isNew) {
            // Crear nuevo - dejar el ID vacío para que Django lo cree
            compositorInput.value = data.apellidos_nombres;
            coordenadasInput.value = "";
            compositorIdInput.value = "";
        } else {
            // Seleccionar existente
            compositorInput.value = data.apellidos_nombres;
            coordenadasInput.value = data.coordenadas_biograficas || "";
            compositorIdInput.value = data.id;
        }

        hideSuggestions();
    }

    // Cargar datos de compositor existente
    function loadCompositorData(compositorId) {
        fetch(`/catalogacion/api/autocompletar/persona/?id=${compositorId}`)
            .then((response) => response.json())
            .then((data) => {
                if (data.results && data.results.length > 0) {
                    const compositor = data.results[0];
                    compositorInput.value = compositor.apellidos_nombres;
                    coordenadasInput.value =
                        compositor.coordenadas_biograficas || "";
                }
            })
            .catch((error) => {
                console.error("Error al cargar compositor:", error);
            });
    }

    // Actualizar selección visual
    function updateSelection(items) {
        items.forEach((item, index) => {
            if (index === selectedIndex) {
                item.classList.add("selected");
                item.scrollIntoView({ block: "nearest" });
            } else {
                item.classList.remove("selected");
            }
        });
    }

    // Ocultar sugerencias
    function hideSuggestions() {
        suggestionsContainer.classList.remove("show");
        suggestionsContainer.innerHTML = "";
        selectedIndex = -1;
    }

    // Escapar HTML
    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }
})();
