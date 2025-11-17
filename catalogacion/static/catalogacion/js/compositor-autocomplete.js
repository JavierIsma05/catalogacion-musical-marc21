/**
 * Autocomplete mejorado para compositor con opción de crear nuevo
 */

class CompositorAutocomplete {
    constructor(inputId) {
        this.input = document.getElementById(inputId);
        this.hiddenInput = document.getElementById(
            inputId.replace("_display", "")
        );
        this.suggestionsList = null;
        this.debounceTimer = null;
        this.selectedIndex = -1;

        if (this.input) {
            this.init();
        }
    }

    init() {
        // Crear contenedor de sugerencias
        this.suggestionsList = document.createElement("ul");
        this.suggestionsList.className = "autocomplete-suggestions";
        this.suggestionsList.style.display = "none";
        this.input.parentNode.appendChild(this.suggestionsList);

        // Event listeners
        this.input.addEventListener("input", (e) => this.handleInput(e));
        this.input.addEventListener("keydown", (e) => this.handleKeydown(e));
        this.input.addEventListener("blur", (e) => this.handleBlur(e));

        // Si hay valor inicial, mostrarlo
        if (this.hiddenInput && this.hiddenInput.value) {
            this.loadInitialValue();
        }
    }

    handleInput(e) {
        const query = e.target.value.trim();

        // Limpiar el hidden input cuando el usuario escribe
        if (this.hiddenInput) {
            this.hiddenInput.value = "";
        }

        clearTimeout(this.debounceTimer);

        if (query.length < 2) {
            this.hideSuggestions();
            return;
        }

        // Debounce: esperar 300ms después de que el usuario deje de escribir
        this.debounceTimer = setTimeout(() => {
            this.searchCompositors(query);
        }, 300);
    }

    handleKeydown(e) {
        const items = this.suggestionsList.querySelectorAll("li");

        if (items.length === 0) return;

        switch (e.key) {
            case "ArrowDown":
                e.preventDefault();
                this.selectedIndex = Math.min(
                    this.selectedIndex + 1,
                    items.length - 1
                );
                this.updateSelection(items);
                break;

            case "ArrowUp":
                e.preventDefault();
                this.selectedIndex = Math.max(this.selectedIndex - 1, 0);
                this.updateSelection(items);
                break;

            case "Enter":
                e.preventDefault();
                if (this.selectedIndex >= 0 && items[this.selectedIndex]) {
                    items[this.selectedIndex].click();
                } else {
                    // Si no hay selección, crear nuevo
                    this.createNew();
                }
                break;

            case "Escape":
                this.hideSuggestions();
                break;
        }
    }

    handleBlur(e) {
        // Esperar un poco antes de ocultar para permitir clic en sugerencias
        setTimeout(() => {
            // Si el input está vacío o no hay ID, intentar crear nuevo
            if (this.input.value.trim() && !this.hiddenInput.value) {
                // El usuario escribió algo pero no seleccionó nada
                // Lo dejamos para que se cree al guardar el formulario
            }
            this.hideSuggestions();
        }, 200);
    }

    async searchCompositors(query) {
        try {
            const response = await fetch(
                `/catalogacion/api/autocompletar/persona/?q=${encodeURIComponent(
                    query
                )}`
            );

            if (!response.ok) {
                throw new Error("Error en la búsqueda");
            }

            const data = await response.json();
            this.displaySuggestions(data.results);
        } catch (error) {
            console.error("Error al buscar compositores:", error);
            this.hideSuggestions();
        }
    }

    displaySuggestions(results) {
        this.suggestionsList.innerHTML = "";
        this.selectedIndex = -1;

        if (results.length === 0) {
            // Mostrar opción para crear nuevo
            const li = document.createElement("li");
            li.className = "autocomplete-suggestion-item create-new";
            li.innerHTML = `<i class="bi bi-plus-circle"></i> Crear "${this.input.value}"`;
            li.addEventListener("click", () => this.createNew());
            this.suggestionsList.appendChild(li);
        } else {
            results.forEach((result, index) => {
                const li = document.createElement("li");
                li.className = "autocomplete-suggestion-item";
                li.textContent = result.text;
                li.dataset.id = result.id;
                li.dataset.apellidosNombres = result.apellidos_nombres;
                li.dataset.fechas = result.fechas;

                li.addEventListener("click", () =>
                    this.selectSuggestion(result)
                );
                this.suggestionsList.appendChild(li);
            });

            // Agregar opción "Crear nuevo" al final
            const li = document.createElement("li");
            li.className = "autocomplete-suggestion-item create-new";
            li.innerHTML = `<i class="bi bi-plus-circle"></i> Crear nuevo compositor`;
            li.addEventListener("click", () => this.createNew());
            this.suggestionsList.appendChild(li);
        }

        this.suggestionsList.style.display = "block";
    }

    selectSuggestion(result) {
        this.input.value = result.text;
        this.hiddenInput.value = result.id;
        this.hideSuggestions();
    }

    createNew() {
        // Marcar que se debe crear un nuevo registro
        // El formulario Django manejará la creación
        this.hiddenInput.value = ""; // Dejar vacío para que Django cree uno nuevo
        this.input.setAttribute("data-create-new", "true");
        this.hideSuggestions();
    }

    updateSelection(items) {
        items.forEach((item, index) => {
            if (index === this.selectedIndex) {
                item.classList.add("selected");
                item.scrollIntoView({ block: "nearest" });
            } else {
                item.classList.remove("selected");
            }
        });
    }

    hideSuggestions() {
        this.suggestionsList.style.display = "none";
        this.selectedIndex = -1;
    }

    async loadInitialValue() {
        // Si ya hay un ID, cargar el nombre
        try {
            const response = await fetch(
                `/catalogacion/api/autocompletar/persona/?q=${this.hiddenInput.value}`
            );
            const data = await response.json();

            if (data.results.length > 0) {
                this.input.value = data.results[0].text;
            }
        } catch (error) {
            console.error("Error al cargar valor inicial:", error);
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", function () {
    new CompositorAutocomplete("id_compositor_display");
});
