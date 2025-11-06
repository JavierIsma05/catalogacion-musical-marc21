// ============================================
// CAMPOS 3XX - DESCRIPCIÓN FÍSICA
// ============================================

contadores.registrar("descripcionFisica", 1);
contadores.registrar("extension300", 1);
contadores.registrar("dimension300", 1);
contadores.registrar("medioFisico", 1);
contadores.registrar("tecnica340", 1);
contadores.registrar("caracteristicaMusica", 1);
contadores.registrar("formato348", 1);
contadores.registrar("medioInterpretacion382", 1);
contadores.registrar("medio382a", 1);
contadores.registrar("solista382", 1);
contadores.registrar("numeroInterpretes382", 1);
contadores.registrar("designacionNumerica", 1);
contadores.registrar("numeroObra383", 1);
contadores.registrar("opus383", 1);

// ============================================
// 300 - DESCRIPCIÓN FÍSICA (Repetible)
// ============================================

function generarHTMLDescripcionFisica(index) {
    return `
        <div class="campo-repetible" data-campo="descripcion-fisica-${index}">
            <div class="campo-header">
                <span class="campo-label">Descripción Física #${
                    index + 1
                }</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('descripcion-fisica-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            
            <!-- Subcampo $a - Extensión (Repetible) -->
            <div class="subcampo-group mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$a Extensión</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarExtension300(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="extensiones-300-${index}">
                    <div class="mb-2" data-subcampo="extension-300-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$a</span>
                            <input type="text" name="extension_300_a_${index}_0" class="form-control" placeholder="Ej: 1 partitura (24 p.)">
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('extension-300-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row g-3 mb-3">
                <div class="col-md-6">
                    <label class="form-label small">$b Otras Características Físicas</label>
                    <input type="text" name="otras_caracteristicas_300_b_${index}" class="form-control" placeholder="Ej: ilustraciones">
                </div>
                <div class="col-md-6">
                    <label class="form-label small">$e Material Acompañante</label>
                    <input type="text" name="material_acompanante_300_e_${index}" class="form-control" placeholder="Ej: + 1 CD">
                </div>
            </div>
            
            <!-- Subcampo $c - Dimensiones (Repetible) -->
            <div class="subcampo-group">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$c Dimensiones</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarDimension300(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="dimensiones-300-${index}">
                    <div class="mb-2" data-subcampo="dimension-300-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$c</span>
                            <input type="text" name="dimension_300_c_${index}_0" class="form-control" placeholder="Ej: 30 cm">
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('dimension-300-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

window.agregarDescripcionFisica = function () {
    if (!validarContenedor("descripciones-fisicas-container")) return;

    const index = contadores.obtener("descripcionFisica");
    insertarHTML(
        "descripciones-fisicas-container",
        generarHTMLDescripcionFisica(index)
    );
    contadores.incrementar("descripcionFisica");
};

window.agregarExtension300 = function (parentIndex) {
    const contenedor = document.getElementById(
        `extensiones-300-${parentIndex}`
    );
    if (!contenedor) return;

    const index = contadores.obtener("extension300");
    const html = `
        <div class="mb-2" data-subcampo="extension-300-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$a</span>
                <input type="text" name="extension_300_a_${parentIndex}_${index}" class="form-control" placeholder="Ej: 1 partitura (24 p.)">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('extension-300-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("extension300");
};

window.agregarDimension300 = function (parentIndex) {
    const contenedor = document.getElementById(
        `dimensiones-300-${parentIndex}`
    );
    if (!contenedor) return;

    const index = contadores.obtener("dimension300");
    const html = `
        <div class="mb-2" data-subcampo="dimension-300-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$c</span>
                <input type="text" name="dimension_300_c_${parentIndex}_${index}" class="form-control" placeholder="Ej: 30 cm">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('dimension-300-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("dimension300");
};

// ============================================
// 340 - MEDIO FÍSICO (Repetible)
// ============================================

function generarHTMLMedioFisico(index) {
    return `
        <div class="campo-repetible" data-campo="medio-fisico-${index}">
            <div class="campo-header">
                <span class="campo-label">Medio Físico #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('medio-fisico-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            
            <!-- Subcampo $d - Técnica (Repetible) -->
            <div class="subcampo-group">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$d Técnica de Registro</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarTecnica340(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="tecnicas-340-${index}">
                    <div class="mb-2" data-subcampo="tecnica-340-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$d</span>
                            <select name="tecnica_340_d_${index}_0" class="form-select form-select-sm">
                                <option value="autógrafo">Autógrafo</option>
                                <option value="posible autógrafo">Posible autógrafo</option>
                                <option value="manuscrito" selected>Manuscrito</option>
                                <option value="manuscrito de copista no identificado">Manuscrito de copista no identificado</option>
                                <option value="impreso">Impreso</option>
                                <option value="fotocopia de manuscrito">Fotocopia de manuscrito</option>
                                <option value="fotocopia de impreso">Fotocopia de impreso</option>
                            </select>
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('tecnica-340-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

window.agregarMedioFisico = function () {
    if (!validarContenedor("medios-fisicos-container")) return;

    const index = contadores.obtener("medioFisico");
    insertarHTML("medios-fisicos-container", generarHTMLMedioFisico(index));
    contadores.incrementar("medioFisico");
};

window.agregarTecnica340 = function (parentIndex) {
    const contenedor = document.getElementById(`tecnicas-340-${parentIndex}`);
    if (!contenedor) return;

    const index = contadores.obtener("tecnica340");
    const html = `
        <div class="mb-2" data-subcampo="tecnica-340-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$d</span>
                <select name="tecnica_340_d_${parentIndex}_${index}" class="form-select form-select-sm">
                    <option value="autógrafo">Autógrafo</option>
                    <option value="posible autógrafo">Posible autógrafo</option>
                    <option value="manuscrito" selected>Manuscrito</option>
                    <option value="manuscrito de copista no identificado">Manuscrito de copista no identificado</option>
                    <option value="impreso">Impreso</option>
                    <option value="fotocopia de manuscrito">Fotocopia de manuscrito</option>
                    <option value="fotocopia de impreso">Fotocopia de impreso</option>
                </select>
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('tecnica-340-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("tecnica340");
};

// ============================================
// 348 - CARACTERÍSTICAS MÚSICA NOTADA (Repetible)
// ============================================

function generarHTMLCaracteristicaMusica(index) {
    return `
        <div class="campo-repetible" data-campo="caracteristica-musica-${index}">
            <div class="campo-header">
                <span class="campo-label">Característica Música Notada #${
                    index + 1
                }</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('caracteristica-musica-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            
            <div class="alert alert-warning alert-sm" role="alert">
                <i class="bi bi-exclamation-triangle"></i>
                <small>No usar si es piano en doble pauta tradicional</small>
            </div>
            
            <!-- Subcampo $a - Formato (Repetible) -->
            <div class="subcampo-group">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$a Formato de Presentación</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarFormato348(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="formatos-348-${index}">
                    <div class="mb-2" data-subcampo="formato-348-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$a</span>
                            <select name="formato_348_a_${index}_0" class="form-select form-select-sm">
                                <option value="parte">Parte</option>
                                <option value="partitura" selected>Partitura</option>
                                <option value="partitura de coro">Partitura de coro</option>
                                <option value="partitura piano vocal">Partitura piano-vocal</option>
                            </select>
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('formato-348-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

window.agregarCaracteristicaMusica = function () {
    if (!validarContenedor("caracteristicas-musica-container")) return;

    const index = contadores.obtener("caracteristicaMusica");
    insertarHTML(
        "caracteristicas-musica-container",
        generarHTMLCaracteristicaMusica(index)
    );
    contadores.incrementar("caracteristicaMusica");
};

window.agregarFormato348 = function (parentIndex) {
    const contenedor = document.getElementById(`formatos-348-${parentIndex}`);
    if (!contenedor) return;

    const index = contadores.obtener("formato348");
    const html = `
        <div class="mb-2" data-subcampo="formato-348-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$a</span>
                <select name="formato_348_a_${parentIndex}_${index}" class="form-select form-select-sm">
                    <option value="parte">Parte</option>
                    <option value="partitura" selected>Partitura</option>
                    <option value="partitura de coro">Partitura de coro</option>
                    <option value="partitura piano vocal">Partitura piano-vocal</option>
                </select>
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('formato-348-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("formato348");
};

// ============================================
// 382 - MEDIO DE INTERPRETACIÓN (Repetible)
// ============================================

function generarHTMLMedioInterpretacion382(index) {
    return `
        <div class="campo-repetible" data-campo="medio-interpretacion-382-${index}">
            <div class="campo-header">
                <span class="campo-label">Medio de Interpretación #${
                    index + 1
                }</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('medio-interpretacion-382-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            
            <!-- Subcampo $a - Medio (Repetible) -->
            <div class="subcampo-group mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$a Medio de Interpretación</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarMedio382a(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="medios-382a-${index}">
                    <div class="mb-2" data-subcampo="medio-382a-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$a</span>
                            <select name="medio_382_a_${index}_0" class="form-select form-select-sm">
                                <option value="piano" selected>Piano</option>
                                <option value="dos pianos">Dos pianos</option>
                                <option value="piano a cuatro manos">Piano a cuatro manos</option>
                                <option value="piano con acompañamiento">Piano con acompañamiento</option>
                            </select>
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('medio-382a-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Subcampo $b - Solista (Repetible) -->
            <div class="subcampo-group mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$b Solista</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarSolista382(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="solistas-382-${index}">
                    <div class="mb-2" data-subcampo="solista-382-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$b</span>
                            <select name="solista_382_b_${index}_0" class="form-select form-select-sm">
                                <option value="piano" selected>Piano</option>
                            </select>
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('solista-382-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Subcampo $n - Número de Intérpretes (Repetible) -->
            <div class="subcampo-group">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$n Número de Intérpretes</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarNumeroInterpretes382(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="numeros-interpretes-382-${index}">
                    <div class="mb-2" data-subcampo="numero-interpretes-382-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$n</span>
                            <input type="number" min="1" name="numero_interpretes_382_n_${index}_0" class="form-control" placeholder="Ej: 2, 4, 8">
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('numero-interpretes-382-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

window.agregarMedioInterpretacion382 = function () {
    if (!validarContenedor("medios-interpretacion-382-container")) return;

    const index = contadores.obtener("medioInterpretacion382");
    insertarHTML(
        "medios-interpretacion-382-container",
        generarHTMLMedioInterpretacion382(index)
    );
    contadores.incrementar("medioInterpretacion382");
};

window.agregarMedio382a = function (parentIndex) {
    const contenedor = document.getElementById(`medios-382a-${parentIndex}`);
    if (!contenedor) return;

    const index = contadores.obtener("medio382a");
    const html = `
        <div class="mb-2" data-subcampo="medio-382a-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$a</span>
                <select name="medio_382_a_${parentIndex}_${index}" class="form-select form-select-sm">
                    <option value="piano" selected>Piano</option>
                    <option value="dos pianos">Dos pianos</option>
                    <option value="piano a cuatro manos">Piano a cuatro manos</option>
                    <option value="piano con acompañamiento">Piano con acompañamiento</option>
                </select>
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('medio-382a-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("medio382a");
};

window.agregarSolista382 = function (parentIndex) {
    const contenedor = document.getElementById(`solistas-382-${parentIndex}`);
    if (!contenedor) return;

    const index = contadores.obtener("solista382");
    const html = `
        <div class="mb-2" data-subcampo="solista-382-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$b</span>
                <select name="solista_382_b_${parentIndex}_${index}" class="form-select form-select-sm">
                    <option value="piano" selected>Piano</option>
                </select>
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('solista-382-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("solista382");
};

window.agregarNumeroInterpretes382 = function (parentIndex) {
    const contenedor = document.getElementById(
        `numeros-interpretes-382-${parentIndex}`
    );
    if (!contenedor) return;

    const index = contadores.obtener("numeroInterpretes382");
    const html = `
        <div class="mb-2" data-subcampo="numero-interpretes-382-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$n</span>
                <input type="number" min="1" name="numero_interpretes_382_n_${parentIndex}_${index}" class="form-control" placeholder="Ej: 2, 4, 8">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('numero-interpretes-382-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("numeroInterpretes382");
};

// ============================================
// 383 - DESIGNACIÓN NUMÉRICA (Repetible)
// ============================================

function generarHTMLDesignacionNumerica(index) {
    return `
        <div class="campo-repetible" data-campo="designacion-numerica-${index}">
            <div class="campo-header">
                <span class="campo-label">Designación Numérica #${
                    index + 1
                }</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('designacion-numerica-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            
            <!-- Subcampo $a - Número de Obra (Repetible) -->
            <div class="subcampo-group mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$a Número de Obra</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarNumeroObra383(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="numeros-obra-383-${index}">
                    <div class="mb-2" data-subcampo="numero-obra-383-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$a</span>
                            <input type="text" name="numero_obra_383_a_${index}_0" class="form-control" placeholder="Ej: K. 545, BWV 1001">
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('numero-obra-383-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Subcampo $b - Opus (Repetible) -->
            <div class="subcampo-group">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$b Opus</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarOpus383(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="opus-383-${index}">
                    <div class="mb-2" data-subcampo="opus-383-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$b</span>
                            <input type="text" name="opus_383_b_${index}_0" class="form-control" placeholder="Ej: Op. 27, No. 2">
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('opus-383-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

window.agregarDesignacionNumerica = function () {
    if (!validarContenedor("designaciones-numericas-container")) return;

    const index = contadores.obtener("designacionNumerica");
    insertarHTML(
        "designaciones-numericas-container",
        generarHTMLDesignacionNumerica(index)
    );
    contadores.incrementar("designacionNumerica");
};

window.agregarNumeroObra383 = function (parentIndex) {
    const contenedor = document.getElementById(
        `numeros-obra-383-${parentIndex}`
    );
    if (!contenedor) return;

    const index = contadores.obtener("numeroObra383");
    const html = `
        <div class="mb-2" data-subcampo="numero-obra-383-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$a</span>
                <input type="text" name="numero_obra_383_a_${parentIndex}_${index}" class="form-control" placeholder="Ej: K. 545, BWV 1001">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('numero-obra-383-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("numeroObra383");
};

window.agregarOpus383 = function (parentIndex) {
    const contenedor = document.getElementById(`opus-383-${parentIndex}`);
    if (!contenedor) return;

    const index = contadores.obtener("opus383");
    const html = `
        <div class="mb-2" data-subcampo="opus-383-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$b</span>
                <input type="text" name="opus_383_b_${parentIndex}_${index}" class="form-control" placeholder="Ej: Op. 27, No. 2">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('opus-383-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("opus383");
};
