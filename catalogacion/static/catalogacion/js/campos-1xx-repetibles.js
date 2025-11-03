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
// 100 - COMPOSITOR (Campo NO repetible, pero con subcampos repetibles)
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
// 130 - TÍTULO UNIFORME (Campo NO repetible, pero con subcampos repetibles)
// ============================================

// ============ 130 $k - FORMA (Repetible) ============

function generarHTMLForma130(index) {
    return `
        <div class="mb-2" data-subcampo="forma-130-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$k</span>
                <input type="text" name="forma_130_k_${index}" class="form-control" 
                       placeholder="Ej: Selección, Fragmento, Adaptación">
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
    contadores.incrementar("forma130");
    console.log(`📝 Forma 130 agregada (total: ${index + 1})`);
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
// 240 - TÍTULO UNIFORME CON COMPOSITOR (Campo NO repetible, pero con subcampos repetibles)
// ============================================

// ============ 240 $k - FORMA (Repetible) ============

function generarHTMLForma240(index) {
    return `
        <div class="mb-2" data-subcampo="forma-240-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$k</span>
                <select name="forma_240_k_${index}" class="form-select form-select-sm">
                    <option value="adaptación">Adaptación</option>
                    <option value="boceto">Boceto</option>
                    <option value="fragmento">Fragmento</option>
                    <option value="selección" selected>Selección</option>
                    <option value="tema con variaciones">Tema con variaciones</option>
                </select>
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
    contadores.incrementar("forma240");
    console.log(`📝 Forma 240 agregada (total: ${index + 1})`);
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

console.log("✅ campos-1xx-repetibles.js cargado correctamente");
console.log("📦 Funciones 1XX disponibles:");
console.log("   - agregarFuncionCompositor()");
console.log("   - agregarAtribucionCompositor()");
console.log("   - agregarForma130()");
console.log("   - agregarMedioInterpretacion130()");
console.log("   - agregarNumeroParteSeccion130()");
console.log("   - agregarNombreParteSeccion130()");
console.log("   - agregarForma240()");
console.log("   - agregarMedioInterpretacion240()");
console.log("   - agregarNumeroParteSeccion240()");
console.log("   - agregarNombreParteSeccion240()");
