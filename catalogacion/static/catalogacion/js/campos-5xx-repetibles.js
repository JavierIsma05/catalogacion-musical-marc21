
/* ==========================================================
   BLOQUE 5XX – Notas y descripciones (MARC21)
   ========================================================== */

// =========================
// 500 - NOTA GENERAL (R)
// =========================
let contadorNotaGeneral = 1;

function agregarNotaGeneral() {
  const container = document.getElementById("nota-general-container");
  const id = `nota-general-${contadorNotaGeneral}`;

  const nuevoCampo = document.createElement("div");
  nuevoCampo.classList.add("campo-repetible", "mb-3");
  nuevoCampo.dataset.campo = id;

  nuevoCampo.innerHTML = `
    <div class="campo-header d-flex justify-content-between align-items-center mb-2">
      <span class="fw-bold">Nota general #${contadorNotaGeneral + 1}</span>
      <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('${id}')">
        <i class="bi bi-trash"></i> Eliminar
      </button>
    </div>

    <div id="subcampo-nota-${contadorNotaGeneral}">
      <div class="input-group mb-2">
        <span class="input-group-text">$a</span>
        <textarea name="nota_general_a_${contadorNotaGeneral}_0" 
                  class="form-control" rows="2"
                  placeholder="Ej: Obra inédita conservada..."></textarea>
        <button type="button" class="btn btn-outline-primary" 
                onclick="agregarSubcampoNota(${contadorNotaGeneral})">
          <i class="bi bi-plus"></i>
        </button>
      </div>
    </div>
  `;
  container.appendChild(nuevoCampo);
  contadorNotaGeneral++;
}

function agregarSubcampoNota(index) {
  const subcontainer = document.getElementById(`subcampo-nota-${index}`);
  const nuevo = document.createElement("div");
  nuevo.classList.add("input-group", "mb-2");
  nuevo.innerHTML = `
    <span class="input-group-text">$a</span>
    <textarea name="nota_general_a_${index}_${subcontainer.children.length}" 
              class="form-control" rows="2"
              placeholder="Otra nota general..."></textarea>
    <button type="button" class="btn btn-outline-danger" onclick="this.parentElement.remove()">
      <i class="bi bi-x"></i>
    </button>
  `;
  subcontainer.appendChild(nuevo);
}

// =========================
// 505 - CONTENIDO (R)
// =========================
let contadorContenido = 1;

function agregarContenido() {
  const container = document.getElementById("contenido-container");
  const id = `contenido-${contadorContenido}`;

  const nuevoCampo = document.createElement("div");
  nuevoCampo.classList.add("campo-repetible", "mb-3");
  nuevoCampo.dataset.campo = id;

  nuevoCampo.innerHTML = `
    <div class="campo-header d-flex justify-content-between align-items-center mb-2">
      <span class="fw-bold">Contenido #${contadorContenido + 1}</span>
      <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('${id}')">
        <i class="bi bi-trash"></i> Eliminar
      </button>
    </div>

    <div id="subcampo-contenido-${contadorContenido}">
      <div class="input-group mb-2">
        <span class="input-group-text">$a</span>
        <textarea name="contenido_a_${contadorContenido}_0" class="form-control" rows="2"
                  placeholder="Ej: 1. Allegro – 2. Andante – 3. Finale"></textarea>
        <button type="button" class="btn btn-outline-primary" 
                onclick="agregarSubcampoContenido(${contadorContenido})">
          <i class="bi bi-plus"></i>
        </button>
      </div>
    </div>
  `;
  container.appendChild(nuevoCampo);
  contadorContenido++;
}

function agregarSubcampoContenido(index) {
  const subcontainer = document.getElementById(`subcampo-contenido-${index}`);
  const nuevo = document.createElement("div");
  nuevo.classList.add("input-group", "mb-2");
  nuevo.innerHTML = `
    <span class="input-group-text">$a</span>
    <textarea name="contenido_a_${index}_${subcontainer.children.length}" 
              class="form-control" rows="2" placeholder="Otro contenido..."></textarea>
    <button type="button" class="btn btn-outline-danger" onclick="this.parentElement.remove()">
      <i class="bi bi-x"></i>
    </button>
  `;
  subcontainer.appendChild(nuevo);
}

// =========================
// 520 - SUMARIO (NR subcampo)
// =========================
let contadorSumario = 1;

function agregarSumario() {
  const container = document.getElementById("sumario-container");
  const id = `sumario-${contadorSumario}`;

  const nuevoCampo = document.createElement("div");
  nuevoCampo.classList.add("campo-repetible", "mb-3");
  nuevoCampo.dataset.campo = id;

  nuevoCampo.innerHTML = `
    <div class="campo-header d-flex justify-content-between align-items-center mb-2">
      <span class="fw-bold">Sumario #${contadorSumario + 1}</span>
      <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('${id}')">
        <i class="bi bi-trash"></i> Eliminar
      </button>
    </div>

    <div class="mb-2">
      <label class="subcampo-label">$a Sumario</label>
      <textarea name="sumario_a_${contadorSumario}" 
                class="form-control" rows="2"
                placeholder="Breve descripción del contenido de la obra."></textarea>
    </div>
  `;
  container.appendChild(nuevoCampo);
  contadorSumario++;
}

// =========================
// 545 - BIOGRAFÍA (R con subcampos repetibles)
// =========================
let contadorBiografia = 1;

function agregarBiografia() {
  const container = document.getElementById("biografia-container");
  const id = `biografia-${contadorBiografia}`;

  const nuevoCampo = document.createElement("div");
  nuevoCampo.classList.add("campo-repetible", "mb-3");
  nuevoCampo.dataset.campo = id;

  nuevoCampo.innerHTML = `
    <div class="campo-header d-flex justify-content-between align-items-center mb-2">
      <span class="fw-bold">Biografía #${contadorBiografia + 1}</span>
      <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('${id}')">
        <i class="bi bi-trash"></i> Eliminar
      </button>
    </div>

    <div id="subcampo-bio-${contadorBiografia}">
      <div class="input-group mb-2">
        <span class="input-group-text">$a</span>
        <textarea name="biografia_a_${contadorBiografia}_0" class="form-control" rows="3"
                  placeholder="Ej: Compositor ecuatoriano del siglo XX..."></textarea>
        <button type="button" class="btn btn-outline-primary" 
                onclick="agregarSubcampoBio(${contadorBiografia}, 'a')">
          <i class="bi bi-plus"></i>
        </button>
      </div>

      <div class="input-group mb-2">
        <span class="input-group-text">$u</span>
        <input type="url" name="biografia_u_${contadorBiografia}_0" class="form-control"
               placeholder="https://sitio-web-del-compositor.com">
        <button type="button" class="btn btn-outline-primary"
                onclick="agregarSubcampoBio(${contadorBiografia}, 'u')">
          <i class="bi bi-plus"></i>
        </button>
      </div>
    </div>
  `;
  container.appendChild(nuevoCampo);
  contadorBiografia++;
}

function agregarSubcampoBio(index, tipo) {
  const subcontainer = document.getElementById(`subcampo-bio-${index}`);
  const nuevo = document.createElement("div");
  nuevo.classList.add("input-group", "mb-2");

  if (tipo === 'a') {
    nuevo.innerHTML = `
      <span class="input-group-text">$a</span>
      <textarea name="biografia_a_${index}_${subcontainer.children.length}" 
                class="form-control" rows="3"
                placeholder="Otro párrafo biográfico..."></textarea>
      <button type="button" class="btn btn-outline-danger" onclick="this.parentElement.remove()">
        <i class="bi bi-x"></i>
      </button>`;
  } else {
    nuevo.innerHTML = `
      <span class="input-group-text">$u</span>
      <input type="url" name="biografia_u_${index}_${subcontainer.children.length}" 
             class="form-control" placeholder="Otra URL relacionada">
      <button type="button" class="btn btn-outline-danger" onclick="this.parentElement.remove()">
        <i class="bi bi-x"></i>
      </button>`;
  }

  subcontainer.appendChild(nuevo);
}

// Función genérica para eliminar campos completos
function eliminarCampo(id) {
  const campo = document.querySelector(`[data-campo="${id}"]`);
  if (campo) campo.remove();
}
