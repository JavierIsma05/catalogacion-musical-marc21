// ============================================================
// 📘 BLOQUE 5XX - Notas, Contenido, Sumario, Biografía
// ============================================================

// Aseguramos que existan los contadores globales
if (typeof window.contadores === "undefined") window.contadores = {
    data: {},
    obtener: function (clave) {
        return this.data[clave] || 0;
    },
    incrementar: function (clave) {
        this.data[clave] = (this.data[clave] || 0) + 1;
    }
};

// ========================================
// 🧩 Función utilitaria para insertar HTML
// ========================================
function insertarHTML(contenedorId, html) {
    const contenedor = document.getElementById(contenedorId);
    if (contenedor) contenedor.insertAdjacentHTML("beforeend", html);
}

function validarContenedor(id) {
    return document.getElementById(id) !== null;
}

// ============================================================
// 500 ## NOTA GENERAL (R)
// ============================================================

function generarHTMLNotaGeneral(index) {
    return `
        <div class="campo-repetible" data-campo="nota-general-${index}">
            <div class="campo-header">
                <span class="campo-label">Nota general #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('nota-general-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-2">
                <div class="col-md-12">
                    <label class="subcampo-label">$a Nota general</label>
                    <textarea name="nota_general_a_${index}" class="form-control" rows="2"
                        placeholder="Ej: Obra inédita conservada en el archivo del compositor."></textarea>
                </div>
            </div>
        </div>
    `;
}

window.agregarNotaGeneral = function () {
    if (!validarContenedor("nota-general-container")) return;
    const index = contadores.obtener("nota-general");
    insertarHTML("nota-general-container", generarHTMLNotaGeneral(index));
    contadores.incrementar("nota-general");
    console.log(`🟦 Nota general agregada (#${index + 1})`);
};

// ============================================================
// 505 00 CONTENIDO (R)
// ============================================================

function generarHTMLContenido(index) {
    return `
        <div class="campo-repetible" data-campo="contenido-${index}">
            <div class="campo-header">
                <span class="campo-label">Contenido #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('contenido-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-2">
                <div class="col-md-12">
                    <label class="subcampo-label">$a Contenido</label>
                    <textarea name="contenido_a_${index}" class="form-control" rows="2"
                        placeholder="Ej: 1. Allegro – 2. Andante – 3. Finale"></textarea>
                </div>
            </div>
        </div>
    `;
}

window.agregarContenido = function () {
    if (!validarContenedor("contenido-container")) return;
    const index = contadores.obtener("contenido");
    insertarHTML("contenido-container", generarHTMLContenido(index));
    contadores.incrementar("contenido");
    console.log(`🟩 Contenido agregado (#${index + 1})`);
};

// ============================================================
// 545 0# DATOS BIOGRÁFICOS DEL COMPOSITOR (R)
// ============================================================

function generarHTMLBiografia(index) {
    return `
        <div class="campo-repetible" data-campo="biografia-${index}">
            <div class="campo-header">
                <span class="campo-label">Biografía #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('biografia-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-2 mb-2">
                <div class="col-md-12">
                    <label class="subcampo-label">$a Datos biográficos del compositor</label>
                    <textarea name="biografia_a_${index}" class="form-control" rows="3"
                        placeholder="Ej: Compositor ecuatoriano del siglo XX, autor de obras sinfónicas y corales."></textarea>
                </div>
            </div>
            <div class="row g-2">
                <div class="col-md-12">
                    <label class="subcampo-label">$u URL relacionada</label>
                    <input type="url" name="biografia_u_${index}" class="form-control"
                        placeholder="https://sitio-web-del-compositor.com">
                </div>
            </div>
        </div>
    `;
}

window.agregarBiografia = function () {
    if (!validarContenedor("biografia-container")) return;
    const index = contadores.obtener("biografia");
    insertarHTML("biografia-container", generarHTMLBiografia(index));
    contadores.incrementar("biografia");
    console.log(`🟨 Biografía agregada (#${index + 1})`);
};

// ============================================================
// ♻️ FUNCIÓN GLOBAL PARA ELIMINAR CAMPOS
// ============================================================

window.eliminarCampo = function (idCampo) {
    const campo = document.querySelector(`[data-campo="${idCampo}"]`);
    if (campo) {
        campo.remove();
        console.log(`❌ Campo eliminado: ${idCampo}`);
    }
};
