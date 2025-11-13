contadores.registrar("funcionCompositor", 1);
// ============================================
// SISTEMA DE AUTOCOMPLETADO
// ============================================

/**
 * Configura el autocompletado para un input
 * @param {string} inputId - ID del input
 * @param {string} dropdownId - ID del dropdown de sugerencias
 * @param {string} modelType - Tipo de modelo ('compositor', 'titulo_uniforme', 'forma_musical')
 * @param {function} onSelect - Callback cuando se selecciona una opción
 */
function configurarAutocompletado(inputId, dropdownId, modelType, onSelect) {
    const input = document.getElementById(inputId);
    const dropdown = document.getElementById(dropdownId);

    if (!input || !dropdown) {
        console.warn(
            `⚠️ No se encontró input (${inputId}) o dropdown (${dropdownId})`
        );
        return;
    }

    let debounceTimer;

    input.addEventListener("input", function () {
        clearTimeout(debounceTimer);
        const query = this.value.trim();

        if (query.length < 2) {
            dropdown.innerHTML = "";
            dropdown.style.display = "none";
            return;
        }

        debounceTimer = setTimeout(() => {
            buscarAutoridades(query, modelType, dropdown, onSelect);
        }, 300);
    });

    // Cerrar dropdown al hacer clic fuera
    document.addEventListener("click", function (e) {
        if (e.target !== input && !dropdown.contains(e.target)) {
            dropdown.style.display = "none";
        }
    });
}

/**
 * Busca autoridades en el servidor
 */
async function buscarAutoridades(query, modelType, dropdown, onSelect) {
    try {
        const response = await fetch(
            `/api/autoridades/?model=${modelType}&q=${encodeURIComponent(
                query
            )}`
        );
        const data = await response.json();

        if (data.results && data.results.length > 0) {
            mostrarSugerencias(data.results, dropdown, onSelect);
        } else {
            dropdown.innerHTML =
                '<div class="autocomplete-item no-results">No se encontraron resultados</div>';
            dropdown.style.display = "block";
        }
    } catch (error) {
        console.error("Error al buscar autoridades:", error);
        dropdown.style.display = "none";
    }
}

/**
 * Muestra las sugerencias en el dropdown
 */
function mostrarSugerencias(results, dropdown, onSelect) {
    dropdown.innerHTML = results
        .map((item) => {
            return `<div class="autocomplete-item" data-id="${
                item.id
            }" data-text="${item.text}" data-fechas="${item.fechas || ""}">
            ${item.text}
        </div>`;
        })
        .join("");

    dropdown.style.display = "block";

    // Agregar eventos click a cada item
    dropdown.querySelectorAll(".autocomplete-item").forEach((item) => {
        item.addEventListener("click", function () {
            const id = this.getAttribute("data-id");
            const text = this.getAttribute("data-text");
            const fechas = this.getAttribute("data-fechas");

            if (onSelect) {
                onSelect(id, text, fechas);
            }

            dropdown.style.display = "none";
        });
    });
}

// ============================================
// 100 - COMPOSITOR (Autocompletado con autoridades)
// ============================================

// Inicializar autocompletado para compositor cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", function () {
    configurarAutocompletado(
        "compositor_apellidos_nombres",
        "compositor-autocomplete",
        "compositor",
        function (id, text, fechas) {
            // Separar apellidos_nombres del texto completo
            const apellidosNombres = id; // El id ES el apellidos_nombres
            document.getElementById("compositor_apellidos_nombres").value =
                apellidosNombres;

            // Llenar el campo de fechas si existe
            if (fechas) {
                document.getElementById("compositor_fechas").value = fechas;
            }
        }
    );

    // Autocompletado para Título Uniforme 130
    configurarAutocompletado(
        "titulo_uniforme_130",
        "titulo-130-autocomplete",
        "titulo_uniforme",
        function (id, text, fechas) {
            document.getElementById("titulo_uniforme_130").value = id;
        }
    );

    // Autocompletado para Título 240
    configurarAutocompletado(
        "titulo_240",
        "titulo-240-autocomplete",
        "titulo_uniforme",
        function (id, text, fechas) {
            document.getElementById("titulo_240").value = id;
        }
    );

    // Configurar autocompletado para el primer campo 130 $k que ya existe
    const primeraForma130 = document.querySelector(
        'input.forma-130-input[data-index="0"]'
    );
    const dropdownForma130 = document.querySelector(
        '.forma-130-autocomplete[data-index="0"]'
    );

    if (primeraForma130 && dropdownForma130) {
        let debounceTimer130;
        primeraForma130.addEventListener("input", function () {
            clearTimeout(debounceTimer130);
            const query = this.value.trim();

            if (query.length < 2) {
                dropdownForma130.innerHTML = "";
                dropdownForma130.style.display = "none";
                return;
            }

            debounceTimer130 = setTimeout(() => {
                buscarAutoridades(
                    query,
                    "forma_musical",
                    dropdownForma130,
                    (id, text) => {
                        primeraForma130.value = id;
                        dropdownForma130.style.display = "none";
                    }
                );
            }, 300);
        });

        // Cerrar dropdown al hacer clic fuera
        document.addEventListener("click", function (e) {
            if (
                e.target !== primeraForma130 &&
                !dropdownForma130.contains(e.target)
            ) {
                dropdownForma130.style.display = "none";
            }
        });
    }

    // Configurar autocompletado para el primer campo 240 $k que ya existe
    const primeraForma240 = document.querySelector(
        'input.forma-240-input[data-index="0"]'
    );
    const dropdownForma240 = document.querySelector(
        '.forma-240-autocomplete[data-index="0"]'
    );

    if (primeraForma240 && dropdownForma240) {
        let debounceTimer;
        primeraForma240.addEventListener("input", function () {
            clearTimeout(debounceTimer);
            const query = this.value.trim();

            if (query.length < 2) {
                dropdownForma240.innerHTML = "";
                dropdownForma240.style.display = "none";
                return;
            }

            debounceTimer = setTimeout(() => {
                buscarAutoridades(
                    query,
                    "forma_musical",
                    dropdownForma240,
                    (id, text) => {
                        primeraForma240.value = id;
                        dropdownForma240.style.display = "none";
                    }
                );
            }, 300);
        });

        // Cerrar dropdown al hacer clic fuera
        document.addEventListener("click", function (e) {
            if (
                e.target !== primeraForma240 &&
                !dropdownForma240.contains(e.target)
            ) {
                dropdownForma240.style.display = "none";
            }
        });
    }
});

// ============================================
// 100 - SUBCAMPOS REPETIBLES
// ============================================

// ============ 100 $e - FUNCIÓN COMPOSITOR (Repetible) ============

function generarHTMLFuncionCompositor(index) {
    return `
        <div class="mb-2" data-subcampo="funcion-compositor-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$e</span>
                <select name="funcion_compositor_e_${index}" class="form-select form-select-sm">
                    <option value="arreglista">Arreglista</option>
                    <option value="coeditor">Coeditor</option>
                    <option value="compilador">Compilador</option>
                    <option value="compositor" selected>Compositor</option>
                    <option value="copista">Copista</option>
                    <option value="dedicatario">Dedicatario</option>
                    <option value="editor">Editor</option>
                    <option value="prologuista">Prologuista</option>
                </select>
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('funcion-compositor-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

window.agregarFuncionCompositor = function () {
    if (!validarContenedor("funciones-compositor")) return;

    const index = contadores.obtener("funcionCompositor");
    insertarHTML("funciones-compositor", generarHTMLFuncionCompositor(index));
    contadores.incrementar("funcionCompositor");
    console.log(`🎼 Función Compositor agregada (total: ${index + 1})`);
};
