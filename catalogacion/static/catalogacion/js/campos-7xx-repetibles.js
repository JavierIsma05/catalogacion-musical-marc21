/* ============================================================
 * BLOQUE 7XX – Relaciones y Enlaces (700, 710, 773, 774, 787)
 * Requiere helpers globales:
 *   - contadores (registrar, obtener, incrementar, inicializarSubcontador,
 *                 obtenerSubcontador, incrementarSubcontador)
 *   - insertarHTML(id, html)
 *   - validarContenedor(id)
 *   - eliminarCampo(idDataAttr)
 *   - eliminarSubcampo(idDataAttr)
 * ============================================================ */

// Registrar contadores raíz (uno por campo)
contadores.registrar("nombreRelacionado700", 1);
contadores.registrar("entidad710", 1);
contadores.registrar("coleccion773", 1);
contadores.registrar("obra774", 1);
contadores.registrar("otras787", 1);

/* ------------------------------------------------------------
 * Utilidades internas (7xx)
 * ----------------------------------------------------------*/
function _inputGroup(textName, dataId, placeholder) {
  return `
    <div class="input-group input-group-sm mb-2" data-subcampo="${dataId}">
      <input type="text" name="${textName}" class="form-control" placeholder="${placeholder || ""}">
      <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('${dataId}')">X</button>
    </div>
  `;
}

/* ============================================================
 * 700 1# – Nombre relacionado (R)
 *   $a (NR)  $c (R)  $d (NR)  $e (R)  $i (R)  $j (R)  $t (NR)
 * Contenedores del template:
 *   #nombre-relacionado-container
 *   cada tarjeta: data-campo="nombre-relacionado-{i}"
 * Subcontadores por tarjeta:
 *   700_funcion[i], 700_relacion[i], 700_autoria[i]
 * ============================================================ */

function generarHTMLNombreRelacionado700(index) {
  return `
    <div class="campo-repetible mb-3 p-3 border bg-white shadow-sm" data-campo="nombre-relacionado-${index}">
      <div class="campo-header d-flex justify-content-between align-items-center mb-3">
        <span class="campo-label fw-bold">Nombre Relacionado #${index + 1}</span>
        <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('nombre-relacionado-${index}')">Eliminar</button>
      </div>

      <div class="row g-2 mb-2">
        <div class="col-md-6">
          <label class="subcampo-label">$a Apellidos, Nombres</label>
          <input type="text" class="form-control" name="nombre700_a_${index}" placeholder="Ej: Bach, Johann Sebastian">
        </div>
        <div class="col-md-6">
          <label class="subcampo-label">$d Coordenadas biográficas</label>
          <input type="text" class="form-control" name="nombre700_d_${index}" placeholder="Ej: 1685-1750">
        </div>
      </div>

      <div class="row g-2 mb-2">
        <div class="col-md-6">
          <label class="subcampo-label">$c Término asociado al nombre</label>
          <input type="text" class="form-control" name="nombre700_c_${index}" placeholder="Ej: compositor, intérprete, editor, etc.">
        </div>
        <div class="col-md-6">
          <label class="subcampo-label">$t Título de obra</label>
          <input type="text" class="form-control" name="nombre700_t_${index}" placeholder="Ej: El arte de la fuga">
        </div>
      </div>

      <!-- $e Función (R) -->
      <div class="subcampo-group mt-3">
        <label class="subcampo-label">$e Función (R)</label>
        <div id="funciones700-${index}" class="mb-2">
          ${_inputGroup(`nombre700_e_${index}_0`, `funcion700-${index}-0`, "Ej: compositor, arreglista")}
        </div>
        <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarFuncion700(${index})">+ Agregar función</button>
      </div>

      <!-- $i Relación (R) -->
      <div class="subcampo-group mt-3">
        <label class="subcampo-label">$i Relación (R)</label>
        <div id="relaciones700-${index}" class="mb-2">
          ${_inputGroup(`nombre700_i_${index}_0`, `relacion700-${index}-0`, "Ej: Maestro de..., Estudiante de...")}
        </div>
        <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarRelacion700(${index})">+ Agregar relación</button>
      </div>

      <!-- $j Autoría (R) -->
      <div class="subcampo-group mt-3">
        <label class="subcampo-label">$j Autoría (R)</label>
        <div id="autorias700-${index}" class="mb-2">
          ${_inputGroup(`nombre700_j_${index}_0`, `autoria700-${index}-0`, "Ej: certificada, atribuida, copista")}
        </div>
        <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarAutoria700(${index})">+ Agregar autoría</button>
      </div>
    </div>
  `;
}

window.agregarNombreRelacionado700 = function () {
  if (!validarContenedor("nombre-relacionado-container")) return;

  const index = contadores.obtener("nombreRelacionado700");
  insertarHTML("nombre-relacionado-container", generarHTMLNombreRelacionado700(index));

  // Subcontadores por tarjeta 700
  contadores.inicializarSubcontador("700_funcion", index, 1);
  contadores.inicializarSubcontador("700_relacion", index, 1);
  contadores.inicializarSubcontador("700_autoria", index, 1);

  contadores.incrementar("nombreRelacionado700");
  console.log(`👤 700 agregado (total: ${index + 1})`);
};

window.agregarFuncion700 = function (cardIndex) {
  const sub = contadores.obtenerSubcontador("700_funcion", cardIndex);
  insertarHTML(`funciones700-${cardIndex}`, _inputGroup(`nombre700_e_${cardIndex}_${sub}`, `funcion700-${cardIndex}-${sub}`, "Ej: compositor, arreglista"));
  contadores.incrementarSubcontador("700_funcion", cardIndex);
};

window.agregarRelacion700 = function (cardIndex) {
  const sub = contadores.obtenerSubcontador("700_relacion", cardIndex);
  insertarHTML(`relaciones700-${cardIndex}`, _inputGroup(`nombre700_i_${cardIndex}_${sub}`, `relacion700-${cardIndex}-${sub}`, "Ej: Maestro de..., Estudiante de..."));
  contadores.incrementarSubcontador("700_relacion", cardIndex);
};

window.agregarAutoria700 = function (cardIndex) {
  const sub = contadores.obtenerSubcontador("700_autoria", cardIndex);
  insertarHTML(`autorias700-${cardIndex}`, _inputGroup(`nombre700_j_${cardIndex}_${sub}`, `autoria700-${cardIndex}-${sub}`, "Ej: certificada, atribuida, copista"));
  contadores.incrementarSubcontador("700_autoria", cardIndex);
};

/* ============================================================
 * 710 2# – Entidad Relacionada (R)
 *   $a (NR)  $e (R)
 * Contenedor: #entidad710-container
 * Subcontador por tarjeta: 710_funcion[i]
 * ============================================================ */

function generarHTMLEntidad710(index) {
  return `
    <div class="campo-repetible mb-3 p-3 border bg-white shadow-sm" data-campo="entidad710-${index}">
      <div class="campo-header d-flex justify-content-between align-items-center mb-3">
        <span class="campo-label fw-bold">Entidad Relacionada #${index + 1}</span>
        <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('entidad710-${index}')">Eliminar</button>
      </div>

      <div class="row g-2 mb-3">
        <div class="col-md-12">
          <label class="subcampo-label">$a Entidad relacionada</label>
          <input type="text" class="form-control" name="entidad710_a_${index}" placeholder="Ej: Universidad Nacional de Loja, Ministerio de Cultura">
        </div>
      </div>

      <div class="subcampo-group mt-2">
        <label class="subcampo-label">$e Función (R)</label>
        <div id="funciones710-${index}" class="mb-2">
          ${_inputGroup(`entidad710_e_${index}_0`, `funcion710-${index}-0`, "Ej: coeditor, patrocinante, lugar de ejecución")}
        </div>
        <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarFuncion710(${index})">+ Agregar función</button>
      </div>
    </div>
  `;
}

window.agregarEntidad710 = function () {
  if (!validarContenedor("entidad710-container")) return;

  const index = contadores.obtener("entidad710");
  insertarHTML("entidad710-container", generarHTMLEntidad710(index));
  contadores.inicializarSubcontador("710_funcion", index, 1);
  contadores.incrementar("entidad710");
  console.log(`🏛️ 710 agregado (total: ${index + 1})`);
};

window.agregarFuncion710 = function (cardIndex) {
  const sub = contadores.obtenerSubcontador("710_funcion", cardIndex);
  insertarHTML(`funciones710-${cardIndex}`, _inputGroup(`entidad710_e_${cardIndex}_${sub}`, `funcion710-${cardIndex}-${sub}`, "Ej: coeditor, patrocinante, lugar de ejecución"));
  contadores.incrementarSubcontador("710_funcion", cardIndex);
};

/* ============================================================
 * 773 1# – Colección (R)
 *   $a (NR)  $t (NR)  $w (R)
 * Contenedor: #coleccion773-container
 * ============================================================ */

function generarHTMLColeccion773(index) {
  return `
    <div class="campo-repetible mb-3 p-3 border bg-white shadow-sm" data-campo="coleccion773-${index}">
      <div class="campo-header d-flex justify-content-between align-items-center mb-3">
        <span class="campo-label fw-bold">Colección #${index + 1}</span>
        <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('coleccion773-${index}')">Eliminar</button>
      </div>

      <div class="row g-2 mb-3">
        <div class="col-md-4">
          <label class="subcampo-label">$a Compositor</label>
          <input type="text" class="form-control" name="coleccion773_a_${index}" placeholder="Ej: Mozart, W. A.">
        </div>
        <div class="col-md-4">
          <label class="subcampo-label">$t Título de colección</label>
          <input type="text" class="form-control" name="coleccion773_t_${index}" placeholder="Ej: Obras completas para piano">
        </div>
        <div class="col-md-4">
          <label class="subcampo-label">$w Número de documento fuente</label>
          <input type="text" class="form-control" name="coleccion773_w_${index}" placeholder="Ej: DOC-1234">
        </div>
      </div>
    </div>
  `;
}

window.agregarColeccion773 = function () {
  if (!validarContenedor("coleccion773-container")) return;

  const index = contadores.obtener("coleccion773");
  insertarHTML("coleccion773-container", generarHTMLColeccion773(index));
  contadores.incrementar("coleccion773");
  console.log(`📘 773 agregado (total: ${index + 1})`);
};

/* ============================================================
 * 774 1# – Obra en esta colección (R)
 *   $a (NR)  $t (NR)  $w (R)
 * Contenedor: #obra774-container
 * ============================================================ */

function generarHTMLObra774(index) {
  return `
    <div class="campo-repetible mb-3 p-3 border bg-white shadow-sm" data-campo="obra774-${index}">
      <div class="campo-header d-flex justify-content-between align-items-center mb-3">
        <span class="campo-label fw-bold">Obra #${index + 1}</span>
        <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('obra774-${index}')">Eliminar</button>
      </div>

      <div class="row g-2 mb-3">
        <div class="col-md-4">
          <label class="subcampo-label">$a Compositor</label>
          <input type="text" class="form-control" name="obra774_a_${index}" placeholder="Ej: Beethoven, Ludwig van">
        </div>
        <div class="col-md-4">
          <label class="subcampo-label">$t Título</label>
          <input type="text" class="form-control" name="obra774_t_${index}" placeholder="Ej: Sonata n.º 5">
        </div>
        <div class="col-md-4">
          <label class="subcampo-label">$w Número de esta obra en la colección</label>
          <input type="text" class="form-control" name="obra774_w_${index}" placeholder="Ej: N-4567">
        </div>
      </div>
    </div>
  `;
}

window.agregarObra774 = function () {
  if (!validarContenedor("obra774-container")) return;

  const index = contadores.obtener("obra774");
  insertarHTML("obra774-container", generarHTMLObra774(index));
  contadores.incrementar("obra774");
  console.log(`📗 774 agregado (total: ${index + 1})`);
};

/* ============================================================
 * 787 1# – Otras relaciones (R)
 *   $a (NR)  $t (NR)  $w (R)
 * Contenedor: #otras787-container
 * ============================================================ */

function generarHTMLOtras787(index) {
  return `
    <div class="campo-repetible mb-3 p-3 border bg-white shadow-sm" data-campo="otras787-${index}">
      <div class="campo-header d-flex justify-content-between align-items-center mb-3">
        <span class="campo-label fw-bold">Obra Relacionada #${index + 1}</span>
        <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('otras787-${index}')">Eliminar</button>
      </div>

      <div class="row g-2 mb-3">
        <div class="col-md-4">
          <label class="subcampo-label">$a Compositor</label>
          <input type="text" class="form-control" name="otras787_a_${index}" placeholder="Ej: Haydn, Joseph">
        </div>
        <div class="col-md-4">
          <label class="subcampo-label">$t Título</label>
          <input type="text" class="form-control" name="otras787_t_${index}" placeholder="Ej: Sinfonía n.º 94">
        </div>
        <div class="col-md-4">
          <label class="subcampo-label">$w Número de obra relacionada</label>
          <input type="text" class="form-control" name="otras787_w_${index}" placeholder="Ej: REL-9087">
        </div>
      </div>
    </div>
  `;
}

window.agregarOtras787 = function () {
  if (!validarContenedor("otras787-container")) return;

  const index = contadores.obtener("otras787");
  insertarHTML("otras787-container", generarHTMLOtras787(index));
  contadores.incrementar("otras787");
  console.log(`🔗 787 agregado (total: ${index + 1})`);
};

/* ============================================================
 * FIN BLOQUE 7XX
 * ============================================================ */
