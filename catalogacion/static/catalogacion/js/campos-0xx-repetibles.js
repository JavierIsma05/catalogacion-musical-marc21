contadores.registrar("incipit", 1);
contadores.registrar("codigoLengua", 1);
contadores.registrar("codigoPais", 1);

// ============================================
// 031 - Incipit Musical (CON SUBCAMPOS: URLs)
// ============================================

function generarHTMLURLIncipit(incipitIndex, urlIndex) {
    return `
        <div class="mb-2" data-subcampo="url-${incipitIndex}-${urlIndex}">
            <div class="input-group input-group-sm">
                <input type="url" name="incipit_u_${incipitIndex}_${urlIndex}" class="form-control" placeholder="https://...">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('url-${incipitIndex}-${urlIndex}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

function generarHTMLIncipit(index) {
    // Obtener valores predeterminados desde variable global o usar fallback
    const defaults = window.INCIPIT_DEFAULTS || {
        numero_obra: 1,
        numero_movimiento: 1,
        numero_pasaje: 1,
        voz_instrumento: "piano",
    };

    return `
        <div class="campo-repetible" data-campo="incipit-${index}">
            <div class="campo-header">
                <span class="campo-label">Incipit #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('incipit-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            
            <div class="row g-2 mb-2">
                <div class="col-md-4">
                    <label class="subcampo-label">$a Número de Obra</label>
                    <input type="number" name="incipit_a_${index}" class="form-control" placeholder="${
        defaults.numero_obra
    }" value="${defaults.numero_obra}" min="1">
                </div>
                <div class="col-md-4">
                    <label class="subcampo-label">$b Número de Movimiento</label>
                    <input type="number" name="incipit_b_${index}" class="form-control" placeholder="${
        defaults.numero_movimiento
    }" value="${defaults.numero_movimiento}" min="1">
                </div>
                <div class="col-md-4">
                    <label class="subcampo-label">$c Número de Pasaje</label>
                    <input type="number" name="incipit_c_${index}" class="form-control" placeholder="${
        defaults.numero_pasaje
    }" value="${defaults.numero_pasaje}" min="1">
                </div>
            </div>
            
            <div class="row g-2 mb-2">
                <div class="col-md-6">
                    <label class="subcampo-label">$d Título o Encabezamiento (opcional)</label>
                    <input type="text" name="incipit_d_${index}" class="form-control" placeholder="Ej: Aria, Allegro, Andante">
                </div>
                <div class="col-md-6">
                    <label class="subcampo-label">$m Voz/Instrumento</label>
                    <input type="text" name="incipit_m_${index}" class="form-control" placeholder="${
        defaults.voz_instrumento
    }" value="${defaults.voz_instrumento}">
                    <small class="text-muted">Predeterminado: ${
                        defaults.voz_instrumento
                    }</small>
                </div>
            </div>
            
            <div class="row g-2 mb-3">
                <div class="col-md-12">
                    <label class="subcampo-label">$p Notación Musical (opcional)</label>
                    <textarea name="incipit_p_${index}" class="form-control" rows="2" placeholder="Código de incipit musical (Plaine & Easie, MusicXML, ABC)"></textarea>
                </div>
            </div>

            <div class="subcampo-group">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$u URL Uniforme de Recursos</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarURLIncipit(${index})">
                        <i class="bi bi-plus"></i> URL
                    </button>
                </div>
                <div id="incipit-${index}-urls">
                    ${generarHTMLURLIncipit(index, 0)}
                </div>
            </div>
        </div>
    `;
}

window.agregarIncipit = function () {
    if (!validarContenedor("incipit-container")) return;

    const index = contadores.obtener("incipit");
    insertarHTML("incipit-container", generarHTMLIncipit(index));
    contadores.inicializarSubcontador("incipitURLs", index, 1);
    contadores.incrementar("incipit");
    console.log(`🎼 Incipit agregado (total: ${index + 1})`);
};

window.agregarURLIncipit = function (incipitIndex) {
    const urlIndex = contadores.obtenerSubcontador("incipitURLs", incipitIndex);
    insertarHTML(
        `incipit-${incipitIndex}-urls`,
        generarHTMLURLIncipit(incipitIndex, urlIndex)
    );
    contadores.incrementarSubcontador("incipitURLs", incipitIndex);
    console.log(`🔗 URL agregada al Incipit ${incipitIndex}`);
};

// ============================================
// 041 - Código de Lengua (CON SUBCAMPOS: Idiomas)
// ============================================

function generarHTMLIdioma(codigoIndex, idiomaIndex) {
    const idiomas = window.CODIGOS_IDIOMA || [
        { value: "ger", text: "Alemán" },
        { value: "spa", text: "Español", selected: true },
        { value: "fre", text: "Francés" },
        { value: "eng", text: "Inglés" },
        { value: "ita", text: "Italiano" },
        { value: "por", text: "Portugués" },
    ];

    return `
        <div class="mb-2" data-subcampo="idioma-${codigoIndex}-${idiomaIndex}">
            <div class="input-group input-group-sm">
                <select name="codigo_lengua_a_${codigoIndex}_${idiomaIndex}" class="form-select form-select-sm">
                    ${generarOpciones(idiomas)}
                </select>
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('idioma-${codigoIndex}-${idiomaIndex}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

function generarHTMLCodigoLengua(index) {
    const indicacionTraduccion = window.INDICACION_TRADUCCION || [
        { value: "#", text: "# - No se proporciona información" },
        { value: "0", text: "0 - No es traducción", selected: true },
        { value: "1", text: "1 - Es traducción" },
    ];

    const fuentes = window.FUENTE_CODIGO || [
        { value: "#", text: "# - Código MARC de lengua", selected: true },
        { value: "7", text: "7 - Fuente especificada en $2" },
    ];

    return `
        <div class="campo-repetible" data-campo="codigo-lengua-${index}">
            <div class="campo-header">
                <span class="campo-label">Código de Lengua #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('codigo-lengua-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            
            <div class="row g-2 mb-3">
                <div class="col-md-6">
                    <label class="subcampo-label">Indicador 1 - Código de Traducción</label>
                    <select name="codigo_lengua_ind1_${index}" class="form-select">
                        ${generarOpciones(indicacionTraduccion)}
                    </select>
                </div>
                <div class="col-md-6">
                    <label class="subcampo-label">Indicador 2 - Código de Fuente</label>
                    <select name="codigo_lengua_ind2_${index}" class="form-select">
                        ${generarOpciones(fuentes)}
                    </select>
                </div>
            </div>

            <div class="subcampo-group">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$a Código de Lengua del Texto/Banda Sonora</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarIdiomaObra(${index})">
                        <i class="bi bi-plus"></i> Idioma
                    </button>
                </div>
                <div id="codigo-lengua-${index}-idiomas">
                    ${generarHTMLIdioma(index, 0)}
                </div>
            </div>
        </div>
    `;
}

window.agregarCodigoLengua = function () {
    if (!validarContenedor("codigo-lengua-container")) return;

    const index = contadores.obtener("codigoLengua");
    insertarHTML("codigo-lengua-container", generarHTMLCodigoLengua(index));
    contadores.inicializarSubcontador("codigoLenguaIdiomas", index, 1);
    contadores.incrementar("codigoLengua");
    console.log(`🌐 Código de Lengua agregado (total: ${index + 1})`);
};

window.agregarIdiomaObra = function (codigoIndex) {
    const idiomaIndex = contadores.obtenerSubcontador(
        "codigoLenguaIdiomas",
        codigoIndex
    );
    insertarHTML(
        `codigo-lengua-${codigoIndex}-idiomas`,
        generarHTMLIdioma(codigoIndex, idiomaIndex)
    );
    contadores.incrementarSubcontador("codigoLenguaIdiomas", codigoIndex);
    console.log(`🗣️ Idioma agregado al Código de Lengua ${codigoIndex}`);
};

// ============================================
// 044 - Código de País
// ============================================

function generarHTMLCodigoPais(index) {
    // Usar lista de países desde variable global (definida en el template)
    const paises = window.CODIGOS_PAIS || [
        { value: "ar", text: "Argentina" },
        { value: "bo", text: "Bolivia" },
        { value: "br", text: "Brasil" },
        { value: "cl", text: "Chile" },
        { value: "co", text: "Colombia" },
        { value: "cr", text: "Costa Rica" },
        { value: "cu", text: "Cuba" },
        { value: "ec", text: "Ecuador", selected: true },
        { value: "sv", text: "El Salvador" },
        { value: "gt", text: "Guatemala" },
        { value: "ho", text: "Honduras" },
        { value: "mx", text: "México" },
        { value: "nq", text: "Nicaragua" },
        { value: "pa", text: "Panamá" },
        { value: "pe", text: "Perú" },
        { value: "pr", text: "Puerto Rico" },
        { value: "dr", text: "República Dominicana" },
        { value: "uy", text: "Uruguay" },
        { value: "ve", text: "Venezuela" },
    ];

    return `
        <div class="campo-repetible" data-campo="codigo-pais-${index}">
            <div class="campo-header">
                <span class="campo-label">Código de País #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('codigo-pais-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-2">
                <div class="col-md-12">
                    <label class="subcampo-label">$a Código de País</label>
                    <select name="codigo_pais_a_${index}" class="form-select">
                        ${generarOpciones(paises)}
                    </select>
                </div>
            </div>
        </div>
    `;
}

window.agregarCodigoPais = function () {
    if (!validarContenedor("codigo-pais-container")) return;

    const index = contadores.obtener("codigoPais");
    insertarHTML("codigo-pais-container", generarHTMLCodigoPais(index));
    contadores.incrementar("codigoPais");
    console.log(`🌍 Código de País agregado (total: ${index + 1})`);
};

// ============================================
// CONFIRMACIÓN DE CARGA
// ============================================
