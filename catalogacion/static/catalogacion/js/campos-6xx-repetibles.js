
/* ==========================================================
   BLOQUE 6XX – Materias y Géneros/Forma
   ========================================================== */

// === 650 $a / $x ===
let contadorMateria650 = 1;

function agregarMateria650() {
  const container = document.getElementById("materia-650-container");
  const id = `materia-650-${contadorMateria650}`;

  const nuevoCampo = document.createElement("div");
  nuevoCampo.classList.add("campo-repetible", "mb-3");
  nuevoCampo.dataset.campo = id;

  nuevoCampo.innerHTML = `
    <div class="campo-header d-flex justify-content-between align-items-center mb-2">
      <span class="fw-bold">Materia #${contadorMateria650 + 1}</span>
      <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('${id}')">
        <i class="bi bi-trash"></i> Eliminar
      </button>
    </div>

    <div class="row g-2 mb-2">
      <div class="col-md-12">
        <label class="subcampo-label">$a Materia (NR)</label>
        <input type="text" name="materia_650a_${contadorMateria650}" class="form-control form-control-sm" 
               placeholder="Ej: Música coral religiosa">
      </div>
    </div>

    <div id="submateria-650-${contadorMateria650}">
      <div class="input-group mb-2">
        <span class="input-group-text">$x</span>
        <input type="text" name="materia_650x_${contadorMateria650}_0" class="form-control form-control-sm"
               placeholder="Ej: Siglo XIX">
        <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarSubMateria650(${contadorMateria650})">
          <i class="bi bi-plus"></i>
        </button>
      </div>
    </div>
  `;
  container.appendChild(nuevoCampo);
  contadorMateria650++;
}

function agregarSubMateria650(index) {
  const subcontainer = document.getElementById(`submateria-650-${index}`);
  const nuevo = document.createElement("div");
  nuevo.classList.add("input-group", "mb-2");
  nuevo.innerHTML = `
    <span class="input-group-text">$x</span>
    <input type="text" name="materia_650x_${index}_${subcontainer.children.length}" 
           class="form-control form-control-sm" placeholder="Otra subdivisión de materia">
    <button type="button" class="btn btn-outline-danger btn-sm" onclick="this.parentElement.remove()">
      <i class="bi bi-x"></i>
    </button>
  `;
  subcontainer.appendChild(nuevo);
}

// === 655 $a / $x ===
let contadorMateria655 = 1;

function agregarMateria655() {
  const container = document.getElementById("materia-655-container");
  const id = `materia-655-${contadorMateria655}`;

  const nuevoCampo = document.createElement("div");
  nuevoCampo.classList.add("campo-repetible", "mb-3");
  nuevoCampo.dataset.campo = id;

  nuevoCampo.innerHTML = `
    <div class="campo-header d-flex justify-content-between align-items-center mb-2">
      <span class="fw-bold">Género/Forma #${contadorMateria655 + 1}</span>
      <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('${id}')">
        <i class="bi bi-trash"></i> Eliminar
      </button>
    </div>

    <div class="row g-2 mb-2">
      <div class="col-md-12">
        <label class="subcampo-label">$a Materia (Género/Forma) (NR)</label>
        <input type="text" name="materia_655a_${contadorMateria655}" class="form-control form-control-sm"
               placeholder="Ej: Motetes">
      </div>
    </div>

    <div id="submateria-655-${contadorMateria655}">
      <div class="input-group mb-2">
        <span class="input-group-text">$x</span>
        <input type="text" name="materia_655x_${contadorMateria655}_0" class="form-control form-control-sm"
               placeholder="Ej: Corales">
        <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarSubMateria655(${contadorMateria655})">
          <i class="bi bi-plus"></i>
        </button>
      </div>
    </div>
  `;
  container.appendChild(nuevoCampo);
  contadorMateria655++;
}

function agregarSubMateria655(index) {
  const subcontainer = document.getElementById(`submateria-655-${index}`);
  const nuevo = document.createElement("div");
  nuevo.classList.add("input-group", "mb-2");
  nuevo.innerHTML = `
    <span class="input-group-text">$x</span>
    <input type="text" name="materia_655x_${index}_${subcontainer.children.length}" 
           class="form-control form-control-sm" placeholder="Otra subdivisión general">
    <button type="button" class="btn btn-outline-danger btn-sm" onclick="this.parentElement.remove()">
      <i class="bi bi-x"></i>
    </button>
  `;
  subcontainer.appendChild(nuevo);
}

// === Función genérica para eliminar ===
function eliminarCampo(id) {
  const campo = document.querySelector(`[data-campo="${id}"]`);
  if (campo) campo.remove();
}
