class ContadoresCampos {
    constructor() {
        this.contadores = {
            isbn: 1,
            ismn: 1,
            numeroEditor: 1,
            incipit: 1,
            codigoLengua: 1,
            codigoPais: 1,
        };

        // Contadores para subcampos anidados
        this.subcontadores = {
            incipitURLs: { 0: 1 },
            codigoLenguaIdiomas: { 0: 1 },
        };
    }

    obtener(tipo) {
        return this.contadores[tipo] || 0;
    }

    incrementar(tipo) {
        if (this.contadores[tipo] !== undefined) {
            this.contadores[tipo]++;
        }
        return this.contadores[tipo];
    }

    obtenerSubcontador(tipo, indice) {
        if (!this.subcontadores[tipo]) {
            this.subcontadores[tipo] = {};
        }
        return this.subcontadores[tipo][indice] || 0;
    }

    incrementarSubcontador(tipo, indice) {
        if (!this.subcontadores[tipo]) {
            this.subcontadores[tipo] = {};
        }
        if (this.subcontadores[tipo][indice] === undefined) {
            this.subcontadores[tipo][indice] = 0;
        }
        this.subcontadores[tipo][indice]++;
        return this.subcontadores[tipo][indice];
    }

    inicializarSubcontador(tipo, indice, valor = 1) {
        if (!this.subcontadores[tipo]) {
            this.subcontadores[tipo] = {};
        }
        this.subcontadores[tipo][indice] = valor;
    }
}

// Instancia global
const contadores = new ContadoresCampos();

// ============================================
// FUNCIONES GENÉRICAS
// ============================================

/**
 * Elimina un campo repetible del DOM
 */
function eliminarCampo(campoId) {
    const campo = document.querySelector(`[data-campo="${campoId}"]`);
    if (campo) {
        campo.remove();
    }
}

/**
 * Elimina un subcampo del DOM
 */
function eliminarSubcampo(subcampoId) {
    const subcampo = document.querySelector(`[data-subcampo="${subcampoId}"]`);
    if (subcampo) {
        subcampo.remove();
    }
}

/**
 * Inserta HTML en un contenedor
 */
function insertarHTML(containerId, html) {
    const container = document.getElementById(containerId);
    if (container) {
        container.insertAdjacentHTML("beforeend", html);
    } else {
        console.error(`Contenedor no encontrado: ${containerId}`);
    }
}

// ============================================
// CAMPOS 0XX - SIMPLES
// ============================================

/**
 * 020 - ISBN
 */
function generarHTMLISBN(index) {
    return `
        <div class="campo-repetible" data-campo="isbn-${index}">
            <div class="campo-header">
                <span class="campo-label">ISBN #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('isbn-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-2">
                <div class="col-md-6">
                    <label class="subcampo-label">$a ISBN</label>
                    <input type="text" name="isbn_a_${index}" class="form-control" placeholder="978-0-123456-78-9">
                </div>
                <div class="col-md-6">
                    <label class="subcampo-label">$q Calificador</label>
                    <input type="text" name="isbn_q_${index}" class="form-control" placeholder="Ej: rústica">
                </div>
            </div>
        </div>
    `;
}

function agregarISBN() {
    const index = contadores.obtener("isbn");
    insertarHTML("isbn-container", generarHTMLISBN(index));
    contadores.incrementar("isbn");
}

/**
 * 024 - ISMN
 */
function generarHTMLISMN(index) {
    return `
        <div class="campo-repetible" data-campo="ismn-${index}">
            <div class="campo-header">
                <span class="campo-label">ISMN #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('ismn-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-2">
                <div class="col-md-12">
                    <label class="subcampo-label">$a ISMN</label>
                    <input type="text" name="ismn_a_${index}" class="form-control" placeholder="M-001-12345-6-7">
                </div>
            </div>
        </div>
    `;
}

function agregarISMN() {
    const index = contadores.obtener("ismn");
    insertarHTML("ismn-container", generarHTMLISMN(index));
    contadores.incrementar("ismn");
}

/**
 * 028 - Número de Editor
 */
function generarHTMLNumeroEditor(index) {
    return `
        <div class="campo-repetible" data-campo="numero-editor-${index}">
            <div class="campo-header">
                <span class="campo-label">Número de Editor #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('numero-editor-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-2 mb-2">
                <div class="col-md-12">
                    <label class="subcampo-label">$a Número de Editor</label>
                    <input type="text" name="numero_editor_a_${index}" class="form-control" placeholder="Ej: B. & H. 8797">
                </div>
            </div>
            <div class="row g-2">
                <div class="col-md-6">
                    <label class="subcampo-label">Indicador 1 - Tipo de Número</label>
                    <select name="numero_editor_tipo_${index}" class="form-select">
                        <option value="0">0 - Número de publicación</option>
                        <option value="1">1 - Número de matriz</option>
                        <option value="2" selected>2 - Número de plancha</option>
                        <option value="3">3 - Otro número de música</option>
                        <option value="4">4 - Número de videograbación</option>
                        <option value="5">5 - Otro número de editor</option>
                    </select>
                </div>
                <div class="col-md-6">
                    <label class="subcampo-label">Indicador 2 - Control de Nota</label>
                    <select name="numero_editor_control_${index}" class="form-select">
                        <option value="0" selected>0 - No hay nota ni punto de acceso adicional</option>
                        <option value="1">1 - Nota, hay punto de acceso adicional</option>
                        <option value="2">2 - Nota, no hay punto de acceso adicional</option>
                        <option value="3">3 - No hay nota, hay punto de acceso adicional</option>
                    </select>
                </div>
            </div>
        </div>
    `;
}

function agregarNumeroEditor() {
    const index = contadores.obtener("numeroEditor");
    insertarHTML("numero-editor-container", generarHTMLNumeroEditor(index));
    contadores.incrementar("numeroEditor");
}

/**
 * 044 - Código de País
 */
function generarHTMLCodigoPais(index) {
    const paises = [
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

    const options = paises
        .map(
            (p) =>
                `<option value="${p.value}" ${p.selected ? "selected" : ""}>${
                    p.text
                }</option>`
        )
        .join("");

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
                        ${options}
                    </select>
                </div>
            </div>
        </div>
    `;
}

function agregarCodigoPais() {
    const index = contadores.obtener("codigoPais");
    insertarHTML("codigo-pais-container", generarHTMLCodigoPais(index));
    contadores.incrementar("codigoPais");
}

// ============================================
// CAMPOS 0XX - COMPLEJOS (CON SUBCAMPOS)
// ============================================

/**
 * 031 - Incipit Musical (con URLs repetibles)
 */
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
                    <input type="number" name="incipit_a_${index}" class="form-control" placeholder="1" value="1" min="1">
                </div>
                <div class="col-md-4">
                    <label class="subcampo-label">$b Número de Movimiento</label>
                    <input type="number" name="incipit_b_${index}" class="form-control" placeholder="1" value="1" min="1">
                </div>
                <div class="col-md-4">
                    <label class="subcampo-label">$c Número de Pasaje</label>
                    <input type="number" name="incipit_c_${index}" class="form-control" placeholder="1" value="1" min="1">
                </div>
            </div>
            
            <div class="row g-2 mb-2">
                <div class="col-md-6">
                    <label class="subcampo-label">$d Título o Encabezamiento (opcional)</label>
                    <input type="text" name="incipit_d_${index}" class="form-control" placeholder="Ej: Aria, Allegro, Andante">
                </div>
                <div class="col-md-6">
                    <label class="subcampo-label">$m Voz/Instrumento (opcional)</label>
                    <input type="text" name="incipit_m_${index}" class="form-control" placeholder="Ej: V (solo si NO es piano)">
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

function agregarIncipit() {
    const index = contadores.obtener("incipit");
    insertarHTML("incipit-container", generarHTMLIncipit(index));
    contadores.inicializarSubcontador("incipitURLs", index, 1);
    contadores.incrementar("incipit");
}

function agregarURLIncipit(incipitIndex) {
    const urlIndex = contadores.obtenerSubcontador("incipitURLs", incipitIndex);
    insertarHTML(
        `incipit-${incipitIndex}-urls`,
        generarHTMLURLIncipit(incipitIndex, urlIndex)
    );
    contadores.incrementarSubcontador("incipitURLs", incipitIndex);
}

/**
 * 041 - Código de Lengua (con idiomas repetibles)
 */
function generarHTMLIdioma(codigoIndex, idiomaIndex) {
    return `
        <div class="mb-2" data-subcampo="idioma-${codigoIndex}-${idiomaIndex}">
            <div class="input-group input-group-sm">
                <select name="codigo_lengua_a_${codigoIndex}_${idiomaIndex}" class="form-select form-select-sm">
                    <option value="ger">Alemán</option>
                    <option value="spa" selected>Español</option>
                    <option value="fre">Francés</option>
                    <option value="eng">Inglés</option>
                    <option value="ita">Italiano</option>
                    <option value="por">Portugués</option>
                </select>
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('idioma-${codigoIndex}-${idiomaIndex}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
}

function generarHTMLCodigoLengua(index) {
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
                        <option value="#"># - No se proporciona información</option>
                        <option value="0" selected>0 - No es traducción</option>
                        <option value="1">1 - Es traducción</option>
                    </select>
                </div>
                <div class="col-md-6">
                    <label class="subcampo-label">Indicador 2 - Código de Fuente</label>
                    <select name="codigo_lengua_ind2_${index}" class="form-select">
                        <option value="#" selected># - Código MARC de lengua</option>
                        <option value="7">7 - Fuente especificada en $2</option>
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

function agregarCodigoLengua() {
    const index = contadores.obtener("codigoLengua");
    insertarHTML("codigo-lengua-container", generarHTMLCodigoLengua(index));
    contadores.inicializarSubcontador("codigoLenguaIdiomas", index, 1);
    contadores.incrementar("codigoLengua");
}

function agregarIdiomaObra(codigoIndex) {
    const idiomaIndex = contadores.obtenerSubcontador(
        "codigoLenguaIdiomas",
        codigoIndex
    );
    insertarHTML(
        `codigo-lengua-${codigoIndex}-idiomas`,
        generarHTMLIdioma(codigoIndex, idiomaIndex)
    );
    contadores.incrementarSubcontador("codigoLenguaIdiomas", codigoIndex);
}

// ============================================
// EXPONER FUNCIONES GLOBALMENTE
// ============================================

window.eliminarCampo = eliminarCampo;
window.eliminarSubcampo = eliminarSubcampo;
window.agregarISBN = agregarISBN;
window.agregarISMN = agregarISMN;
window.agregarNumeroEditor = agregarNumeroEditor;
window.agregarCodigoPais = agregarCodigoPais;
window.agregarIncipit = agregarIncipit;
window.agregarURLIncipit = agregarURLIncipit;
window.agregarCodigoLengua = agregarCodigoLengua;
window.agregarIdiomaObra = agregarIdiomaObra;
