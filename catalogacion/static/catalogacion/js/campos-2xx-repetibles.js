// ============================================
// CAMPOS 2XX - TÍTULOS Y PUBLICACIÓN
// ============================================

contadores.registrar("tituloAlternativo", 1);
contadores.registrar("edicion", 1);
contadores.registrar("produccionPublicacion", 1);

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
// 264 - PRODUCCIÓN/PUBLICACIÓN (Repetible)
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
            <div class="row g-3">
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
                <div class="col-md-4">
                    <label class="form-label small">$a Lugar</label>
                    <input type="text" 
                           name="produccion_publicacion_a_${index}" 
                           class="form-control" 
                           placeholder="Ej: Quito, Madrid">
                </div>
                <div class="col-md-4">
                    <label class="form-label small">$b Nombre de la Entidad</label>
                    <input type="text" 
                           name="produccion_publicacion_b_${index}" 
                           class="form-control" 
                           placeholder="Ej: Editorial Musical">
                </div>
            </div>
            <div class="row g-3 mt-2">
                <div class="col-md-4">
                    <label class="form-label small">$c Fecha</label>
                    <input type="text" 
                           name="produccion_publicacion_c_${index}" 
                           class="form-control" 
                           placeholder="Ej: 2023, [2023]">
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
