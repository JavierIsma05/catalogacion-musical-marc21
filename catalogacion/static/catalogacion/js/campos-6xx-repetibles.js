/* =====================================================
   BLOQUE 6XX - MATERIAS (650) y GÉNERO/FORMA (655)
   ===================================================== */

// --- Contadores globales para numerar campos y subcampos ---
let contadorMateria650 = 1;
let contadorMateria655 = 1;

// ============================================================
// 650 ## Materia (Temas)
// ============================================================

function agregarMateria650() {
    const contenedor = document.getElementById("materia650-container");
    const nuevoId = `materia650-${contadorMateria650}`;
    const nuevoCampo = document.createElement("div");
    nuevoCampo.classList.add("campo-repetible");
    nuevoCampo.dataset.campo = nuevoId;

    nuevoCampo.innerHTML = `
        <div class="campo-header">
            <span class="campo-label">Materia #${contadorMateria650 + 1}</span>
            <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('${nuevoId}')">
                <i class="bi bi-trash"></i> Eliminar
            </button>
        </div>
        <div class="row g-2 mb-3">
            <div class="col-md-12">
                <label class="subcampo-label">$a Materia</label>
                <input type="text" name="materia650_a_${contadorMateria650}" class="form-control" placeholder="Ej: Música barroca, Composición musical, etc.">
            </div>
        </div>

        <div class="subcampo-group mt-2">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <label class="subcampo-label mb-0">$x Subdivisión de materia</label>
                <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarSubdivisionMateria650(${contadorMateria650})">
                    <i class="bi bi-plus"></i> Subdivisión
                </button>
            </div>
            <div id="materia650-${contadorMateria650}-subdivisiones">
                <div class="mb-2" data-subcampo="subdivision-650-${contadorMateria650}-0">
                    <div class="input-group input-group-sm">
                        <input type="text" name="materia650_x_${contadorMateria650}_0" class="form-control" placeholder="Ej: Historia y crítica, Análisis, etc.">
                        <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('subdivision-650-${contadorMateria650}-0')">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    contenedor.appendChild(nuevoCampo);
    contadorMateria650++;
}

function agregarSubdivisionMateria650(indiceMateria) {
    const contenedor = document.getElementById(`materia650-${indiceMateria}-subdivisiones`);
    const nuevoIndice = contenedor.children.length;
    const idSubcampo = `subdivision-650-${indiceMateria}-${nuevoIndice}`;
    const nuevoSubcampo = document.createElement("div");
    nuevoSubcampo.classList.add("mb-2");
    nuevoSubcampo.dataset.subcampo = idSubcampo;

    nuevoSubcampo.innerHTML = `
        <div class="input-group input-group-sm">
            <input type="text" name="materia650_x_${indiceMateria}_${nuevoIndice}" class="form-control" placeholder="Ej: Historia y crítica, Análisis, etc.">
            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('${idSubcampo}')">
                <i class="bi bi-x"></i>
            </button>
        </div>
    `;
    contenedor.appendChild(nuevoSubcampo);
}

// ============================================================
// 655 #4 Materia (Género/Forma)
// ============================================================

function agregarMateria655() {
    const contenedor = document.getElementById("materia655-container");
    const nuevoId = `materia655-${contadorMateria655}`;
    const nuevoCampo = document.createElement("div");
    nuevoCampo.classList.add("campo-repetible");
    nuevoCampo.dataset.campo = nuevoId;

    nuevoCampo.innerHTML = `
        <div class="campo-header">
            <span class="campo-label">Género/Forma #${contadorMateria655 + 1}</span>
            <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('${nuevoId}')">
                <i class="bi bi-trash"></i> Eliminar
            </button>
        </div>

        <div class="row g-2 mb-3">
            <div class="col-md-12">
                <label class="subcampo-label">$a Materia (Género/Forma)</label>
                <input type="text" name="materia655_a_${contadorMateria655}" class="form-control" placeholder="Ej: Sinfonías, Sonatas, Canciones, etc.">
            </div>
        </div>

        <div class="subcampo-group mt-2">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <label class="subcampo-label mb-0">$x Subdivisión general</label>
                <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarSubdivision655(${contadorMateria655})">
                    <i class="bi bi-plus"></i> Subdivisión
                </button>
            </div>
            <div id="materia655-${contadorMateria655}-subdivisiones">
                <div class="mb-2" data-subcampo="subdivision-655-${contadorMateria655}-0">
                    <div class="input-group input-group-sm">
                        <input type="text" name="materia655_x_${contadorMateria655}_0" class="form-control" placeholder="Ej: Crítica e interpretación, Historia, etc.">
                        <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('subdivision-655-${contadorMateria655}-0')">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    contenedor.appendChild(nuevoCampo);
    contadorMateria655++;
}

function agregarSubdivision655(indiceMateria) {
    const contenedor = document.getElementById(`materia655-${indiceMateria}-subdivisiones`);
    const nuevoIndice = contenedor.children.length;
    const idSubcampo = `subdivision-655-${indiceMateria}-${nuevoIndice}`;
    const nuevoSubcampo = document.createElement("div");
    nuevoSubcampo.classList.add("mb-2");
    nuevoSubcampo.dataset.subcampo = idSubcampo;

    nuevoSubcampo.innerHTML = `
        <div class="input-group input-group-sm">
            <input type="text" name="materia655_x_${indiceMateria}_${nuevoIndice}" class="form-control" placeholder="Ej: Crítica e interpretación, Historia, etc.">
            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('${idSubcampo}')">
                <i class="bi bi-x"></i>
            </button>
        </div>
    `;
    contenedor.appendChild(nuevoSubcampo);
}

// ============================================================
// 🔧 Funciones generales reutilizables
// ============================================================

function eliminarCampo(idCampo) {
    const campo = document.querySelector(`[data-campo="${idCampo}"]`);
    if (campo) campo.remove();
}

function eliminarSubcampo(idSubcampo) {
    const subcampo = document.querySelector(`[data-subcampo="${idSubcampo}"]`);
    if (subcampo) subcampo.remove();
}
