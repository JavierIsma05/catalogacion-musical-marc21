contadores.registrar("funcionCompositor", 1);
contadores.registrar("atribucionCompositor", 1);
contadores.registrar("forma130", 1);
contadores.registrar("medioInterpretacion130", 1);
contadores.registrar("numeroParteSeccion130", 1);
contadores.registrar("nombreParteSeccion130", 1);
contadores.registrar("forma240", 1);
contadores.registrar("medioInterpretacion240", 1);
contadores.registrar("numeroParteSeccion240", 1);
contadores.registrar("nombreParteSeccion240", 1);

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

// ============ 100 $j - ATRIBUCIÓN COMPOSITOR (Repetible) ============

function generarHTMLAtribucionCompositor(index) {
    return `
        <div class="mb-2" data-subcampo="atribucion-compositor-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$j</span>
                <select name="atribucion_compositor_j_${index}" class="form-select form-select-sm">
                    <option value="atribuida">Atribuida</option>
                    <option value="certificada" selected>Certificada</option>
                    <option value="erronea">Errónea</option>
                </select>
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('atribucion-compositor-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

window.agregarAtribucionCompositor = function () {
    if (!validarContenedor("atribuciones-compositor")) return;

    const index = contadores.obtener("atribucionCompositor");
    insertarHTML(
        "atribuciones-compositor",
        generarHTMLAtribucionCompositor(index)
    );
    contadores.incrementar("atribucionCompositor");
    console.log(`✓ Atribución Compositor agregada (total: ${index + 1})`);
};

// ============================================
// 130 - SUBCAMPOS REPETIBLES
// ============================================

// ============ 130 $k - FORMA (Repetible con autocompletado) ============

function generarHTMLForma130(index) {
    return `
        <div class="mb-2" data-subcampo="forma-130-${index}">
            <div class="input-group input-group-sm position-relative">
                <span class="input-group-text">$k</span>
                <input type="text" 
                       name="forma_130_k_${index}" 
                       class="form-control forma-130-input" 
                       placeholder="Ej: Selección, Fragmento"
                       autocomplete="off"
                       data-index="${index}">
                <div class="forma-130-autocomplete autocomplete-dropdown" data-index="${index}"></div>
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('forma-130-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

window.agregarForma130 = function () {
    if (!validarContenedor("formas-130")) return;

    const index = contadores.obtener("forma130");
    insertarHTML("formas-130", generarHTMLForma130(index));

    // Configurar autocompletado para el nuevo input
    setTimeout(() => {
        const input = document.querySelector(
            `input.forma-130-input[data-index="${index}"]`
        );
        const dropdown = document.querySelector(
            `.forma-130-autocomplete[data-index="${index}"]`
        );

        if (input && dropdown) {
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
                    buscarAutoridades(
                        query,
                        "forma_musical",
                        dropdown,
                        (id, text) => {
                            input.value = id;
                            dropdown.style.display = "none";
                        }
                    );
                }, 300);
            });
        }
    }, 100);

    contadores.incrementar("forma130");
    console.log(`📋 Forma 130 agregada (total: ${index + 1})`);
};

// ============ 130 $m - MEDIO DE INTERPRETACIÓN (Repetible) ============

function generarHTMLMedioInterpretacion130(index) {
    return `
        <div class="mb-2" data-subcampo="medio-interpretacion-130-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$m</span>
                <input type="text" name="medio_interpretacion_130_m_${index}" class="form-control" 
                       placeholder="Ej: piano, orquesta, cuarteto de cuerdas" value="piano">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('medio-interpretacion-130-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

window.agregarMedioInterpretacion130 = function () {
    if (!validarContenedor("medios-interpretacion-130")) return;

    const index = contadores.obtener("medioInterpretacion130");
    insertarHTML(
        "medios-interpretacion-130",
        generarHTMLMedioInterpretacion130(index)
    );
    contadores.incrementar("medioInterpretacion130");
    console.log(
        `🎹 Medio de Interpretación 130 agregado (total: ${index + 1})`
    );
};

// ============ 130 $n - NÚMERO DE PARTE/SECCIÓN (Repetible) ============

function generarHTMLNumeroParteSeccion130(index) {
    return `
        <div class="mb-2" data-subcampo="numero-parte-130-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$n</span>
                <input type="text" name="numero_parte_130_n_${index}" class="form-control" 
                       placeholder="Ej: I, II, III o 1, 2, 3">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('numero-parte-130-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

window.agregarNumeroParteSeccion130 = function () {
    if (!validarContenedor("numeros-parte-130")) return;

    const index = contadores.obtener("numeroParteSeccion130");
    insertarHTML("numeros-parte-130", generarHTMLNumeroParteSeccion130(index));
    contadores.incrementar("numeroParteSeccion130");
    console.log(`🔢 Número de Parte 130 agregado (total: ${index + 1})`);
};

// ============ 130 $p - NOMBRE DE PARTE/SECCIÓN (Repetible) ============

function generarHTMLNombreParteSeccion130(index) {
    return `
        <div class="mb-2" data-subcampo="nombre-parte-130-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$p</span>
                <input type="text" name="nombre_parte_130_p_${index}" class="form-control" 
                       placeholder="Ej: Allegro, Andante, Finale">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('nombre-parte-130-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

window.agregarNombreParteSeccion130 = function () {
    if (!validarContenedor("nombres-parte-130")) return;

    const index = contadores.obtener("nombreParteSeccion130");
    insertarHTML("nombres-parte-130", generarHTMLNombreParteSeccion130(index));
    contadores.incrementar("nombreParteSeccion130");
    console.log(`📄 Nombre de Parte 130 agregado (total: ${index + 1})`);
};

// ============================================
// 240 - SUBCAMPOS REPETIBLES
// ============================================

// ============ 240 $k - FORMA (Repetible con autocompletado) ============

function generarHTMLForma240(index) {
    return `
        <div class="mb-2" data-subcampo="forma-240-${index}">
            <div class="input-group input-group-sm position-relative">
                <span class="input-group-text">$k</span>
                <input type="text" 
                       name="forma_240_k_${index}" 
                       class="form-control forma-240-input" 
                       placeholder="Ej: Selección, Fragmento"
                       autocomplete="off"
                       data-index="${index}">
                <div class="forma-240-autocomplete autocomplete-dropdown" data-index="${index}"></div>
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('forma-240-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

window.agregarForma240 = function () {
    if (!validarContenedor("formas-240")) return;

    const index = contadores.obtener("forma240");
    insertarHTML("formas-240", generarHTMLForma240(index));

    // Configurar autocompletado para el nuevo input
    setTimeout(() => {
        const input = document.querySelector(
            `input.forma-240-input[data-index="${index}"]`
        );
        const dropdown = document.querySelector(
            `.forma-240-autocomplete[data-index="${index}"]`
        );

        if (input && dropdown) {
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
                    buscarAutoridades(
                        query,
                        "forma_musical",
                        dropdown,
                        (id, text) => {
                            input.value = id;
                            dropdown.style.display = "none";
                        }
                    );
                }, 300);
            });

            // Cerrar dropdown al hacer clic fuera
            document.addEventListener("click", function (e) {
                if (e.target !== input && !dropdown.contains(e.target)) {
                    dropdown.style.display = "none";
                }
            });
        }
    }, 100);

    contadores.incrementar("forma240");
    console.log(`📋 Forma 240 agregada (total: ${index + 1})`);
};

// ============ 240 $m - MEDIO DE INTERPRETACIÓN (Repetible) ============

function generarHTMLMedioInterpretacion240(index) {
    return `
        <div class="mb-2" data-subcampo="medio-interpretacion-240-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$m</span>
                <input type="text" name="medio_interpretacion_240_m_${index}" class="form-control" 
                       placeholder="Ej: piano, orquesta, cuarteto de cuerdas" value="piano">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('medio-interpretacion-240-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

window.agregarMedioInterpretacion240 = function () {
    if (!validarContenedor("medios-interpretacion-240")) return;

    const index = contadores.obtener("medioInterpretacion240");
    insertarHTML(
        "medios-interpretacion-240",
        generarHTMLMedioInterpretacion240(index)
    );
    contadores.incrementar("medioInterpretacion240");
    console.log(
        `🎹 Medio de Interpretación 240 agregado (total: ${index + 1})`
    );
};

// ============ 240 $n - NÚMERO DE PARTE/SECCIÓN (Repetible) ============

function generarHTMLNumeroParteSeccion240(index) {
    return `
        <div class="mb-2" data-subcampo="numero-parte-240-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$n</span>
                <input type="text" name="numero_parte_240_n_${index}" class="form-control" 
                       placeholder="Ej: I, II, III o 1, 2, 3">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('numero-parte-240-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

window.agregarNumeroParteSeccion240 = function () {
    if (!validarContenedor("numeros-parte-240")) return;

    const index = contadores.obtener("numeroParteSeccion240");
    insertarHTML("numeros-parte-240", generarHTMLNumeroParteSeccion240(index));
    contadores.incrementar("numeroParteSeccion240");
    console.log(`🔢 Número de Parte 240 agregado (total: ${index + 1})`);
};

// ============ 240 $p - NOMBRE DE PARTE/SECCIÓN (Repetible) ============

function generarHTMLNombreParteSeccion240(index) {
    return `
        <div class="mb-2" data-subcampo="nombre-parte-240-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$p</span>
                <input type="text" name="nombre_parte_240_p_${index}" class="form-control" 
                       placeholder="Ej: Allegro, Andante, Finale">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('nombre-parte-240-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

window.agregarNombreParteSeccion240 = function () {
    if (!validarContenedor("nombres-parte-240")) return;

    const index = contadores.obtener("nombreParteSeccion240");
    insertarHTML("nombres-parte-240", generarHTMLNombreParteSeccion240(index));
    contadores.incrementar("nombreParteSeccion240");
    console.log(`📄 Nombre de Parte 240 agregado (total: ${index + 1})`);
};

// ============================================
// CONFIRMACIÓN DE CARGA
// ============================================

console.log(
    "✅ campos-1xx-repetibles.js cargado correctamente (con autocompletado)"
);
console.log("📦 Funciones 1XX disponibles:");
console.log("   - agregarFuncionCompositor()");
console.log("   - agregarAtribucionCompositor()");
console.log("   - agregarForma130() [con autocompletado]");
console.log("   - agregarMedioInterpretacion130()");
console.log("   - agregarNumeroParteSeccion130()");
console.log("   - agregarNombreParteSeccion130()");
console.log("   - agregarForma240()");
console.log("   - agregarMedioInterpretacion240()");
console.log("   - agregarNumeroParteSeccion240()");
console.log("   - agregarNombreParteSeccion240()");
