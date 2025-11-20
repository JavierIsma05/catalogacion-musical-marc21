/*
 * AUTOCOMPLETE PARA:
 *  - 650 $a  (AutoridadMateria)
 *  - 655 $a  (AutoridadFormaMusical)
 *
 * Para cada input debes tener:
 *   <input type="hidden" class="materia-id"> (o genero-id)
 *   <input type="text" class="materia-input" ...>
 *   <div class="materia-suggestions"></div>
 */

console.log("📌 Autocomplete 650/655 cargado correctamente.");

function initMateriaAutocomplete(input, config) {
    const suggestionsBox = input.parentElement.querySelector(config.suggestionsClass);
    const hiddenId = input.parentElement.querySelector(config.hiddenClass);

    let debounceTimer = null;
    let selectedIndex = -1;

    /* ---------------- INPUT ---------------- */
    input.addEventListener("input", () => {
        const query = input.value.trim();

        if (query.length < 1) {
            hide();
            return;
        }

        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => buscar(query), 200);
    });

    /* ---------------- TECLAS ↑ ↓ ENTER ---------------- */
    input.addEventListener("keydown", (e) => {
        const items = suggestionsBox.querySelectorAll(".autocomplete-item");
        if (!items.length) return;

        if (e.key === "ArrowDown") {
            e.preventDefault();
            selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
            marcar(items);
        }

        if (e.key === "ArrowUp") {
            e.preventDefault();
            selectedIndex = Math.max(selectedIndex - 1, 0);
            marcar(items);
        }

        if (e.key === "Enter") {
            e.preventDefault();
            if (items[selectedIndex]) items[selectedIndex].click();
        }
    });

    /* ---------------- BUSCAR ---------------- */
    function buscar(query) {
        fetch(`${config.url}?q=${encodeURIComponent(query)}`)
            .then(r => r.json())
            .then(data => mostrar(data.results, query))
            .catch(err => console.error("Error en autocomplete:", err));
    }

    /* ---------------- MOSTRAR RESULTADOS ---------------- */
    function mostrar(resultados, query) {
        suggestionsBox.innerHTML = "";
        selectedIndex = -1;

        if (resultados.length === 0) {
            suggestionsBox.innerHTML = `
                <div class="autocomplete-item autocomplete-item-new">
                    <i class="bi bi-plus-circle me-2"></i> Crear: "${query}"
                </div>`;
        } else {
            resultados.forEach(r => {
                const item = document.createElement("div");
                item.className = "autocomplete-item";
                item.innerHTML = `<strong>${r.text || r.termino}</strong>`;
                item.addEventListener("click", () => seleccionar(r));
                suggestionsBox.appendChild(item);
            });

            const crear = document.createElement("div");
            crear.className = "autocomplete-item autocomplete-item-new";
            crear.innerHTML = `<i class="bi bi-plus-circle me-2"></i> Crear: "${query}"`;
            crear.addEventListener("click", () =>
                seleccionar({ id: "", text: query, nuevo: true })
            );
            suggestionsBox.appendChild(crear);
        }

        suggestionsBox.classList.add("show");
    }

    /* ---------------- SELECCIONAR ---------------- */
    function seleccionar(item) {
        input.value = item.text || item.termino;
        hiddenId.value = item.id || "";
        hide();
    }

    /* ---------------- OCULTAR ---------------- */
    function hide() {
        suggestionsBox.classList.remove("show");
        suggestionsBox.innerHTML = "";
        selectedIndex = -1;
    }

    function marcar(items) {
        items.forEach((el, i) => {
            el.classList.toggle("selected", i === selectedIndex);
        });
    }
}

/* ============================================================
   INICIALIZACIÓN PARA 650 Y 655
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {

    // 650 $a
    document.querySelectorAll(".materia-input").forEach(el =>
        initMateriaAutocomplete(el, {
            url: "/catalogacion/api/autocompletar/materia/",
            suggestionsClass: ".materia-suggestions",
            hiddenClass: ".materia-id"
        })
    );

    // 655 $a
    document.querySelectorAll(".genero-input").forEach(el =>
        initMateriaAutocomplete(el, {
            url: "/catalogacion/api/autocompletar/forma-musical/",
            suggestionsClass: ".genero-suggestions",
            hiddenClass: ".genero-id"
        })
    );
});

/* ============================================================
   REINICIALIZAR TRAS AGREGAR FORMS 650/655
   ============================================================ */
document.addEventListener("click", (e) => {
    if (e.target.closest(".add-form-row")) {
        setTimeout(() => {
            document.querySelectorAll(".materia-input").forEach(el =>
                initMateriaAutocomplete(el, {
                    url: "/catalogacion/api/autocompletar/materia/",
                    suggestionsClass: ".materia-suggestions",
                    hiddenClass: ".materia-id"
                })
            );

            document.querySelectorAll(".genero-input").forEach(el =>
                initMateriaAutocomplete(el, {
                    url: "/catalogacion/api/autocompletar/forma-musical/",
                    suggestionsClass: ".genero-suggestions",
                    hiddenClass: ".genero-id"
                })
            );
        }, 150);
    }
});
