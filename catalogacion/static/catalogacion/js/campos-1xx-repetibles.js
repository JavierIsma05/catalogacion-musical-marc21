/**
 * ============================================
 * CAMPOS-1XX-REPETIBLES.JS
 * ============================================
 * Contiene todos los campos REPETIBLES del bloque 1XX
 * (Entradas Principales: Autores Personales, Corporativos, etc.)
 *
 * NOTA: Este es un archivo de PLANTILLA con ejemplos.
 * Adapta según los campos que necesites en tu sistema.
 */

// ============================================
// REGISTRO DE CONTADORES
// ============================================

contadores.registrar("autorPersonal", 1);
contadores.registrar("autorCorporativo", 1);
contadores.registrar("entradaUniforme", 1);

// ============================================
// 100 - Autor Personal (Entrada Principal)
// ============================================

function generarHTMLAutorPersonal(index) {
    return `
        <div class="campo-repetible" data-campo="autor-personal-${index}">
            <div class="campo-header">
                <span class="campo-label">Autor Personal #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('autor-personal-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-2 mb-2">
                <div class="col-md-12">
                    <label class="subcampo-label">$a Nombre Personal</label>
                    <input type="text" name="autor_personal_a_${index}" class="form-control" 
                           placeholder="Apellido, Nombre" required>
                    <small class="text-muted">Formato: Apellido, Nombre</small>
                </div>
            </div>
            <div class="row g-2 mb-2">
                <div class="col-md-6">
                    <label class="subcampo-label">$d Fechas asociadas al nombre</label>
                    <input type="text" name="autor_personal_d_${index}" class="form-control" 
                           placeholder="Ej: 1920-1990">
                </div>
                <div class="col-md-6">
                    <label class="subcampo-label">$e Término de la relación</label>
                    <input type="text" name="autor_personal_e_${index}" class="form-control" 
                           placeholder="Ej: compositor, arreglista">
                </div>
            </div>
            <div class="row g-2">
                <div class="col-md-6">
                    <label class="subcampo-label">Indicador 1 - Tipo de entrada</label>
                    <select name="autor_personal_ind1_${index}" class="form-select">
                        <option value="0">0 - Nombre en orden directo</option>
                        <option value="1" selected>1 - Apellido en primer lugar</option>
                        <option value="3">3 - Nombre de familia</option>
                    </select>
                </div>
            </div>
        </div>
    `;
}

window.agregarAutorPersonal = function () {
    if (!validarContenedor("autor-personal-container")) return;

    const index = contadores.obtener("autorPersonal");
    insertarHTML("autor-personal-container", generarHTMLAutorPersonal(index));
    contadores.incrementar("autorPersonal");
    console.log(`👤 Autor Personal agregado (total: ${index + 1})`);
};

// ============================================
// 110 - Autor Corporativo (Entrada Principal)
// ============================================

function generarHTMLAutorCorporativo(index) {
    return `
        <div class="campo-repetible" data-campo="autor-corporativo-${index}">
            <div class="campo-header">
                <span class="campo-label">Autor Corporativo #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('autor-corporativo-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-2 mb-2">
                <div class="col-md-12">
                    <label class="subcampo-label">$a Nombre de la entidad corporativa</label>
                    <input type="text" name="autor_corporativo_a_${index}" class="form-control" 
                           placeholder="Ej: Orquesta Sinfónica Nacional" required>
                </div>
            </div>
            <div class="row g-2 mb-2">
                <div class="col-md-6">
                    <label class="subcampo-label">$b Unidad subordinada</label>
                    <input type="text" name="autor_corporativo_b_${index}" class="form-control" 
                           placeholder="Ej: Departamento de Música">
                </div>
                <div class="col-md-6">
                    <label class="subcampo-label">$e Término de la relación</label>
                    <input type="text" name="autor_corporativo_e_${index}" class="form-control" 
                           placeholder="Ej: intérprete">
                </div>
            </div>
            <div class="row g-2">
                <div class="col-md-6">
                    <label class="subcampo-label">Indicador 1 - Tipo de nombre corporativo</label>
                    <select name="autor_corporativo_ind1_${index}" class="form-select">
                        <option value="0">0 - Nombre en orden inverso</option>
                        <option value="1">1 - Nombre de jurisdicción</option>
                        <option value="2" selected>2 - Nombre en orden directo</option>
                    </select>
                </div>
            </div>
        </div>
    `;
}

window.agregarAutorCorporativo = function () {
    if (!validarContenedor("autor-corporativo-container")) return;

    const index = contadores.obtener("autorCorporativo");
    insertarHTML(
        "autor-corporativo-container",
        generarHTMLAutorCorporativo(index)
    );
    contadores.incrementar("autorCorporativo");
    console.log(`🏢 Autor Corporativo agregado (total: ${index + 1})`);
};

// ============================================
// 130 - Título Uniforme (Entrada Principal)
// ============================================

function generarHTMLEntradaUniforme(index) {
    return `
        <div class="campo-repetible" data-campo="entrada-uniforme-${index}">
            <div class="campo-header">
                <span class="campo-label">Título Uniforme #${index + 1}</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('entrada-uniforme-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            <div class="row g-2 mb-2">
                <div class="col-md-12">
                    <label class="subcampo-label">$a Título uniforme</label>
                    <input type="text" name="entrada_uniforme_a_${index}" class="form-control" 
                           placeholder="Ej: Sinfonías" required>
                </div>
            </div>
            <div class="row g-2 mb-2">
                <div class="col-md-4">
                    <label class="subcampo-label">$n Número de la obra</label>
                    <input type="text" name="entrada_uniforme_n_${index}" class="form-control" 
                           placeholder="Ej: No. 5">
                </div>
                <div class="col-md-4">
                    <label class="subcampo-label">$r Clave musical</label>
                    <input type="text" name="entrada_uniforme_r_${index}" class="form-control" 
                           placeholder="Ej: Do menor">
                </div>
                <div class="col-md-4">
                    <label class="subcampo-label">$m Medio de ejecución</label>
                    <input type="text" name="entrada_uniforme_m_${index}" class="form-control" 
                           placeholder="Ej: orquesta">
                </div>
            </div>
            <div class="row g-2">
                <div class="col-md-6">
                    <label class="subcampo-label">Indicador 1 - Número de caracteres a ignorar</label>
                    <input type="number" name="entrada_uniforme_ind1_${index}" 
                           class="form-control" min="0" max="9" value="0">
                </div>
            </div>
        </div>
    `;
}

window.agregarEntradaUniforme = function () {
    if (!validarContenedor("entrada-uniforme-container")) return;

    const index = contadores.obtener("entradaUniforme");
    insertarHTML(
        "entrada-uniforme-container",
        generarHTMLEntradaUniforme(index)
    );
    contadores.incrementar("entradaUniforme");
    console.log(`📖 Título Uniforme agregado (total: ${index + 1})`);
};

// ============================================
// CONFIRMACIÓN DE CARGA
// ============================================

console.log("✅ campos-1xx-repetibles.js cargado correctamente");
console.log("📋 Campos disponibles:");
console.log("   - 100 Autor Personal");
console.log("   - 110 Autor Corporativo");
console.log("   - 130 Título Uniforme");
console.log("");
console.log("💡 NOTA: Estos son campos de EJEMPLO.");
console.log("   Adapta según los campos que necesites para tu sistema.");
