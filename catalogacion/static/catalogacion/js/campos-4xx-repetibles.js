// ============================================
// CAMPOS 4XX - SERIES
// ============================================

contadores.registrar("mencionSerie", 1);
contadores.registrar("tituloSerie490", 1);
contadores.registrar("volumenSerie490", 1);

// ============================================
// 490 - MENCIÓN DE SERIE (Repetible)
// ============================================

function generarHTMLMencionSerie(index) {
    return `
        <div class="campo-repetible" data-campo="mencion-serie-${index}">
            <div class="campo-header">
                <span class="campo-label">Mención de Serie #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('mencion-serie-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            
            <!-- Relación de serie (primer indicador) -->
            <div class="row g-3 mb-3">
                <div class="col-md-12">
                    <label class="form-label small">Relación de la Serie (Primer Indicador)</label>
                    <select name="mencion_serie_relacion_${index}" class="form-select">
                        <option value="0" selected>0 - No relacionado (sin entrada secundaria)</option>
                        <option value="1">1 - Relacionado (con entrada secundaria 800-830)</option>
                    </select>
                    <small class="form-text text-muted">
                        Indica si se crea o no una entrada secundaria de serie en los campos 800-830.
                    </small>
                </div>
            </div>
            
            <!-- Subcampo $a - Título de Serie (Repetible) -->
            <div class="subcampo-group mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$a Título de Serie</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarTituloSerie490(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="titulos-serie-490-${index}">
                    <div class="mb-2" data-subcampo="titulo-serie-490-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$a</span>
                            <input type="text" 
                                   name="titulo_serie_490_a_${index}_0" 
                                   class="form-control" 
                                   placeholder="Ej: Colección Támesis. Serie A">
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('titulo-serie-490-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Subcampo $v - Volumen/Número (Repetible) -->
            <div class="subcampo-group">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$v Designación de Volumen/Número</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarVolumenSerie490(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="volumenes-serie-490-${index}">
                    <div class="mb-2" data-subcampo="volumen-serie-490-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$v</span>
                            <input type="text" 
                                   name="volumen_serie_490_v_${index}_0" 
                                   class="form-control" 
                                   placeholder="Ej: 260, Vol. 5, Tomo III">
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('volumen-serie-490-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Ejemplo de formato MARC -->
            <div class="mt-3">
                <small class="text-muted">
                    <strong>Ejemplo:</strong> 490 1# $aColección Támesis. Serie A $v260
                </small>
            </div>
        </div>
    `;
}

window.agregarMencionSerie = function () {
    if (!validarContenedor("menciones-serie-container")) return;

    const index = contadores.obtener("mencionSerie");
    insertarHTML("menciones-serie-container", generarHTMLMencionSerie(index));
    contadores.incrementar("mencionSerie");
    console.log(`📚 Mención de Serie agregada (total: ${index + 1})`);
};

// ============================================
// SUBCAMPO $a - TÍTULO DE SERIE (Repetible)
// ============================================

window.agregarTituloSerie490 = function (parentIndex) {
    const contenedor = document.getElementById(
        `titulos-serie-490-${parentIndex}`
    );
    if (!contenedor) {
        console.error(
            `❌ No se encontró el contenedor titulos-serie-490-${parentIndex}`
        );
        return;
    }

    const index = contadores.obtener("tituloSerie490");
    const html = `
        <div class="mb-2" data-subcampo="titulo-serie-490-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$a</span>
                <input type="text" 
                       name="titulo_serie_490_a_${parentIndex}_${index}" 
                       class="form-control" 
                       placeholder="Ej: Colección Támesis. Serie A">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('titulo-serie-490-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("tituloSerie490");
    console.log(`📖 Título de Serie agregado a Mención #${parentIndex + 1}`);
};

// ============================================
// SUBCAMPO $v - VOLUMEN/NÚMERO (Repetible)
// ============================================

window.agregarVolumenSerie490 = function (parentIndex) {
    const contenedor = document.getElementById(
        `volumenes-serie-490-${parentIndex}`
    );
    if (!contenedor) {
        console.error(
            `❌ No se encontró el contenedor volumenes-serie-490-${parentIndex}`
        );
        return;
    }

    const index = contadores.obtener("volumenSerie490");
    const html = `
        <div class="mb-2" data-subcampo="volumen-serie-490-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$v</span>
                <input type="text" 
                       name="volumen_serie_490_v_${parentIndex}_${index}" 
                       class="form-control" 
                       placeholder="Ej: 260, Vol. 5, Tomo III">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('volumen-serie-490-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("volumenSerie490");
};
