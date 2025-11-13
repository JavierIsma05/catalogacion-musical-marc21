// ============================================
// CAMPOS 2XX - TÍTULOS Y PUBLICACIÓN
// ============================================

contadores.registrar("tituloAlternativo", 1);
contadores.registrar("edicion", 1);
contadores.registrar("produccionPublicacion", 1);
contadores.registrar("lugar264", 1);
contadores.registrar("nombreEntidad264", 1);
contadores.registrar("fecha264", 1);

// ============================================
// 246 - TÍTULO ALTERNATIVO (Repetible)
// ============================================

function generarHTMLTituloAlternativo(index) {
    return `
        <div class="campo-repetible" data-campo="titulo-alternativo-${index}">
            <div class="campo-header">
                <span class="campo-label">Título Alternativo #${
                    index + 1
                }</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('titulo-alternativo-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label small">$a Título Alternativo</label>
                    <input type="text" 
                           name="titulo_alternativo_a_${index}" 
                           class="form-control" 
                           placeholder="Ej: Título abreviado, en otro idioma">
                </div>
                <div class="col-md-6">
                    <label class="form-label small">$b Resto del Título Variante</label>
                    <input type="text" 
                           name="titulo_alternativo_b_${index}" 
                           class="form-control" 
                           placeholder="Complemento del título">
                </div>
            </div>
        </div>
    `;
}

window.agregarTituloAlternativo = function () {
    if (!validarContenedor("titulos-alternativos-container")) return;

    const index = contadores.obtener("tituloAlternativo");
    insertarHTML(
        "titulos-alternativos-container",
        generarHTMLTituloAlternativo(index)
    );
    contadores.incrementar("tituloAlternativo");
    console.log(`📝 Título Alternativo agregado (total: ${index + 1})`);
};

// ============================================
// 250 - EDICIÓN (Repetible)
// ============================================

function generarHTMLEdicion(index) {
    return `
        <div class="campo-repetible" data-campo="edicion-${index}">
            <div class="campo-header">
                <span class="campo-label">Edición #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('edicion-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-3">
                <div class="col-12">
                    <label class="form-label small">$a Enunciado de Edición</label>
                    <input type="text" 
                           name="edicion_a_${index}" 
                           class="form-control" 
                           placeholder="Ej: Primera edición, Segunda edición revisada">
                </div>
            </div>
        </div>
    `;
}

window.agregarEdicion = function () {
    if (!validarContenedor("ediciones-container")) return;

    const index = contadores.obtener("edicion");
    insertarHTML("ediciones-container", generarHTMLEdicion(index));
    contadores.incrementar("edicion");
    console.log(`📖 Edición agregada (total: ${index + 1})`);
};

// ============================================
// 264 - PRODUCCIÓN/PUBLICACIÓN (Repetible con subcampos R)
// ============================================

function generarHTMLProduccionPublicacion(index) {
    return `
        <div class="campo-repetible" data-campo="produccion-publicacion-${index}">
            <div class="campo-header">
                <span class="campo-label">Producción/Publicación #${
                    index + 1
                }</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('produccion-publicacion-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            
            <!-- Función (segundo indicador) -->
            <div class="row g-3 mb-3">
                <div class="col-md-4">
                    <label class="form-label small">Función</label>
                    <select name="produccion_publicacion_funcion_${index}" class="form-select">
                        <option value="0">Producción</option>
                        <option value="1" selected>Publicación</option>
                        <option value="2">Distribución</option>
                        <option value="3">Fabricación</option>
                        <option value="4">Copyright</option>
                    </select>
                </div>
            </div>
            
            <!-- Subcampo $a - Lugar (Repetible) -->
            <div class="subcampo-group mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$a Lugar</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarLugar264(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="lugares-264-${index}">
                    <div class="mb-2" data-subcampo="lugar-264-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$a</span>
                            <input type="text" 
                                   name="produccion_publicacion_a_${index}_0" 
                                   class="form-control" 
                                   placeholder="Ej: Quito, Madrid">
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('lugar-264-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Subcampo $b - Nombre de Entidad (Repetible) -->
            <div class="subcampo-group mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$b Nombre de la Entidad</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarNombreEntidad264(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="nombres-264-${index}">
                    <div class="mb-2" data-subcampo="nombre-264-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$b</span>
                            <input type="text" 
                                   name="produccion_publicacion_b_${index}_0" 
                                   class="form-control" 
                                   placeholder="Ej: Editorial Musical">
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('nombre-264-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Subcampo $c - Fecha (Repetible) -->
            <div class="subcampo-group mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$c Fecha</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarFecha264(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="fechas-264-${index}">
                    <div class="mb-2" data-subcampo="fecha-264-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$c</span>
                            <input type="text" 
                                   name="produccion_publicacion_c_${index}_0" 
                                   class="form-control" 
                                   placeholder="Ej: 2023, [2023]">
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('fecha-264-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

window.agregarProduccionPublicacion = function () {
    if (!validarContenedor("producciones-publicaciones-container")) return;

    const index = contadores.obtener("produccionPublicacion");
    insertarHTML(
        "producciones-publicaciones-container",
        generarHTMLProduccionPublicacion(index)
    );
    contadores.incrementar("produccionPublicacion");
    console.log(`🏢 Producción/Publicación agregada (total: ${index + 1})`);
};

// Agregar subcampo $a - Lugar
window.agregarLugar264 = function (parentIndex) {
    const contenedor = document.getElementById(`lugares-264-${parentIndex}`);
    if (!contenedor) return;

    const index = contadores.obtener("lugar264");
    const html = `
        <div class="mb-2" data-subcampo="lugar-264-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$a</span>
                <input type="text" 
                       name="produccion_publicacion_a_${parentIndex}_${index}" 
                       class="form-control" 
                       placeholder="Ej: Quito, Madrid">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('lugar-264-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("lugar264");
    console.log(`📍 Lugar agregado al 264 #${parentIndex + 1}`);
};

// Agregar subcampo $b - Nombre de Entidad
window.agregarNombreEntidad264 = function (parentIndex) {
    const contenedor = document.getElementById(`nombres-264-${parentIndex}`);
    if (!contenedor) return;

    const index = contadores.obtener("nombreEntidad264");
    const html = `
        <div class="mb-2" data-subcampo="nombre-264-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$b</span>
                <input type="text" 
                       name="produccion_publicacion_b_${parentIndex}_${index}" 
                       class="form-control" 
                       placeholder="Ej: Editorial Musical">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('nombre-264-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("nombreEntidad264");
    console.log(`🏢 Nombre de entidad agregado al 264 #${parentIndex + 1}`);
};

// Agregar subcampo $c - Fecha
window.agregarFecha264 = function (parentIndex) {
    const contenedor = document.getElementById(`fechas-264-${parentIndex}`);
    if (!contenedor) return;

    const index = contadores.obtener("fecha264");
    const html = `
        <div class="mb-2" data-subcampo="fecha-264-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$c</span>
                <input type="text" 
                       name="produccion_publicacion_c_${parentIndex}_${index}" 
                       class="form-control" 
                       placeholder="Ej: 2023, [2023]">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('fecha-264-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("fecha264");
    console.log(`📅 Fecha agregada al 264 #${parentIndex + 1}`);
};
