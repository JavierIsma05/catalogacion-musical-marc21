/* ==========================================================
   FUNCIONES DINÁMICAS PARA BLOQUE 8XX - UBICACIÓN Y DISPONIBILIDAD
   ========================================================== */

// === 852 $c – Estantería (Repetible) ===
let contadorEstanteria852 = 1;
function agregarEstanteria852() {
  const contenedor = document.getElementById("estanterias-852");
  const id = `estanteria-852-${contadorEstanteria852}`;

  const nuevoCampo = document.createElement("div");
  nuevoCampo.classList.add("mb-2");
  nuevoCampo.dataset.subcampo = id;
  nuevoCampo.innerHTML = `
    <div class="input-group input-group-sm">
      <span class="input-group-text">$c</span>
      <input type="text" name="estanteria_852c_${contadorEstanteria852}"
             class="form-control"
             placeholder="Ej: Archivo Central, Estante C-4">
      <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('${id}')">
        <i class="bi bi-x"></i>
      </button>
    </div>`;
  
  contenedor.appendChild(nuevoCampo);
  contadorEstanteria852++;
}

// === 856 $u – URL del recurso (Repetible) ===
function agregarURL856(index) {
  const contenedor = document.getElementById(`urls-856-${index}`);
  const count = contenedor.querySelectorAll("[data-subcampo]").length;
  const id = `url-856-${index}-${count}`;

  const nuevoCampo = document.createElement("div");
  nuevoCampo.classList.add("mb-2");
  nuevoCampo.dataset.subcampo = id;
  nuevoCampo.innerHTML = `
    <div class="input-group input-group-sm">
      <span class="input-group-text">$u</span>
      <input type="url"
             name="url_856u_${index}_${count}"
             class="form-control"
             placeholder="https://repositorio.unl.edu.ec/handle/123456789/xxxx">
      <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('${id}')">
        <i class="bi bi-x"></i>
      </button>
    </div>`;
  contenedor.appendChild(nuevoCampo);
}

// === 856 $y – Texto del enlace (Repetible) ===
function agregarTextoEnlace856(index) {
  const contenedor = document.getElementById(`textos-enlace-856-${index}`);
  const count = contenedor.querySelectorAll("[data-subcampo]").length;
  const id = `texto-enlace-856-${index}-${count}`;

  const nuevoCampo = document.createElement("div");
  nuevoCampo.classList.add("mb-2");
  nuevoCampo.dataset.subcampo = id;
  nuevoCampo.innerHTML = `
    <div class="input-group input-group-sm">
      <span class="input-group-text">$y</span>
      <input type="text"
             name="texto_enlace_856y_${index}_${count}"
             class="form-control"
             placeholder="Ver partitura digital">
      <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('${id}')">
        <i class="bi bi-x"></i>
      </button>
    </div>`;
  contenedor.appendChild(nuevoCampo);
}

// === 856 – Campo completo repetible ===
let contadorDisponible856 = 1;
function agregarDisponible856() {
  const container = document.getElementById("disponibles-container");
  const index = contadorDisponible856;

  const nuevoCampo = document.createElement("div");
  nuevoCampo.classList.add("campo-repetible", "mb-3");
  nuevoCampo.dataset.campo = `disponible-856-${index}`;
  nuevoCampo.innerHTML = `
    <div class="campo-header d-flex justify-content-between align-items-center mb-2">
      <span class="fw-bold">856 #${index + 1} – Recurso Electrónico</span>
      <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarCampo('disponible-856-${index}')">
        <i class="bi bi-trash"></i> Eliminar
      </button>
    </div>

    <!-- Subcampos $u -->
    <div class="subcampo-group mb-3">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <label class="subcampo-label mb-0">$u URL del recurso (R)</label>
        <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarURL856(${index})">
          <i class="bi bi-plus"></i>
        </button>
      </div>
      <div id="urls-856-${index}">
        <div class="mb-2" data-subcampo="url-856-${index}-0">
          <div class="input-group input-group-sm">
            <span class="input-group-text">$u</span>
            <input type="url" name="url_856u_${index}_0" class="form-control"
                   placeholder="https://repositorio.unl.edu.ec/handle/123456789/xxxx">
            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('url-856-${index}-0')">
              <i class="bi bi-x"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Subcampos $y -->
    <div class="subcampo-group mb-3">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <label class="subcampo-label mb-0">$y Texto del enlace (R)</label>
        <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarTextoEnlace856(${index})">
          <i class="bi bi-plus"></i>
        </button>
      </div>
      <div id="textos-enlace-856-${index}">
        <div class="mb-2" data-subcampo="texto-enlace-856-${index}-0">
          <div class="input-group input-group-sm">
            <span class="input-group-text">$y</span>
            <input type="text" name="texto_enlace_856y_${index}_0" class="form-control"
                   placeholder="Ver partitura digital">
            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('texto-enlace-856-${index}-0')">
              <i class="bi bi-x"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <small class="text-muted">
      <strong>Ejemplo:</strong> 856 4# $uhttps://repositorio.unl.edu.ec/... $yVer partitura digital
    </small>
  `;

  container.appendChild(nuevoCampo);
  contadorDisponible856++;
}

// === Función genérica para eliminar ===
function eliminarSubcampo(id) {
  const elemento = document.querySelector(`[data-subcampo="${id}"]`);
  if (elemento) elemento.remove();
}

function eliminarCampo(id) {
  const campo = document.querySelector(`[data-campo="${id}"]`);
  if (campo) campo.remove();
}

document.addEventListener("DOMContentLoaded", function () {
  configurarAutocompletado(
    "ubicacion_institucion",      // ID del input
    "ubicacion-autocomplete",     // ID del contenedor de sugerencias
    "entidad",                    // Tipo de modelo en Django (puede ser 'institucion' o el que uses)
    function (id, text) {
      document.getElementById("ubicacion_institucion").value = text;
    }
  );
});
