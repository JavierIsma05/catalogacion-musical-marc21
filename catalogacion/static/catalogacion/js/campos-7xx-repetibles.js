/* ===== Helpers ===== */
function eliminarCampo(id) {
  const nodo = document.querySelector(`[data-campo="${id}"]`);
  if (nodo) nodo.remove();
}
function delSub(id) {
  const nodo = document.querySelector(`[data-sub="${id}"]`);
  if (nodo) nodo.remove();
}
function createSubInput(prefix, nameBase, idxCampo, idxSub) {
  return `
    <div class="mb-1" data-sub="${prefix}_${nameBase}_${idxSub}">
      <div class="input-group input-group-sm">
        <span class="input-group-text">$${nameBase.slice(-1)}</span>
        <input name="${nameBase}_${idxCampo}_${idxSub}" class="form-control">
        <button class="btn btn-outline-danger" type="button"
                onclick="delSub('${prefix}_${nameBase}_${idxSub}')"><i class="bi bi-x"></i></button>
      </div>
    </div>`;
}

/* ===== 700 ===== */
let idx700 = 1;

function agregar700() {
  const cont = document.getElementById('c700-container');
  const base = cont.children[0];
  const nuevo = base.cloneNode(true);
  const id = `c700-${idx700}`;

  nuevo.dataset.campo = id;
  nuevo.querySelector('span.fw-bold').textContent = `700 #${idx700 + 1}`;

  // 🔹 limpiar todos los inputs
  nuevo.querySelectorAll('input').forEach(i => i.value = '');

  // 🔹 actualizar IDs de los inputs principales ($a y $d)
  const inputApellidos = nuevo.querySelector('[name^="700a_"]');
  const inputFechas = nuevo.querySelector('[name^="700d_"]');
  const dropdown = nuevo.querySelector('.autocomplete-dropdown');

  if (inputApellidos) {
    inputApellidos.id = `nombre_relacionado_apellidos_${idx700}`;
    inputApellidos.name = `700a_${idx700}`;
  }

  if (inputFechas) {
    inputFechas.id = `nombre_relacionado_fechas_${idx700}`;
    inputFechas.name = `700d_${idx700}`;
  }

  if (dropdown) {
    dropdown.id = `nombre-relacionado-autocomplete-${idx700}`;
    dropdown.innerHTML = '';
  }

  // 🔹 reset contenedores de subcampos R ($c, $e, $i, $j)
  ['700c','700e','700i','700j'].forEach(code => {
    const box = nuevo.querySelector(`#${base.dataset.campo || 'c700-0'}_${code}`);
    const nuevoBoxId = `${id}_${code}`;
    if (box) {
      box.id = nuevoBoxId;
      box.innerHTML = '';
    }
  });

  // 🔹 agregar nuevo bloque al DOM
  cont.appendChild(nuevo);

  // 🔹 inicializar autocompletado para este nuevo campo
  inicializarAutocompletado700(idx700);

  idx700++;
}

function addSub(prefixId, code) {
  // agrega una fila a un contenedor de subcampo repetible
  const box = document.getElementById(`${prefixId}_${code}`);
  if (!box) return;
  const childs = box.querySelectorAll('[data-sub]').length;
  box.insertAdjacentHTML('beforeend', createSubInput(prefixId, code, prefixId.split('-').pop(), childs));
}

/* ===== 710 ===== */
let idx710 = 1;
function agregar710() {
  const cont = document.getElementById('c710-container');
  const base = cont.children[0];
  const nuevo = base.cloneNode(true);
  const id = `c710-${idx710}`;
  nuevo.dataset.campo = id;
  nuevo.querySelector('span.fw-bold').textContent = `710 #${idx710 + 1}`;
  nuevo.querySelectorAll('input').forEach(i => i.value = '');
  const eBox = nuevo.querySelector(`#${base.dataset.campo || 'c710-0'}_710e`);
  if (eBox) { eBox.id = `${id}_710e`; eBox.innerHTML = ''; }
  cont.appendChild(nuevo);
  idx710++;
}

/* ===== 773 ===== */
let idx773 = 1;
function agregar773() {
  const cont = document.getElementById('c773-container');
  const base = cont.children[0];
  const nuevo = base.cloneNode(true);
  const id = `c773-${idx773}`;
  nuevo.dataset.campo = id;
  nuevo.querySelector('span.fw-bold').textContent = `773 #${idx773 + 1}`;
  nuevo.querySelectorAll('input').forEach(i => i.value = '');
  const wBox = nuevo.querySelector(`#${base.dataset.campo || 'c773-0'}_773w`);
  if (wBox) { wBox.id = `${id}_773w`; wBox.innerHTML = ''; }
  cont.appendChild(nuevo);
  idx773++;
}

/* ===== 774 ===== */
let idx774 = 1;
function agregar774() {
  const cont = document.getElementById('c774-container');
  const base = cont.children[0];
  const nuevo = base.cloneNode(true);
  const id = `c774-${idx774}`;
  nuevo.dataset.campo = id;
  nuevo.querySelector('span.fw-bold').textContent = `774 #${idx774 + 1}`;
  nuevo.querySelectorAll('input').forEach(i => i.value = '');
  const wBox = nuevo.querySelector(`#${base.dataset.campo || 'c774-0'}_774w`);
  if (wBox) { wBox.id = `${id}_774w`; wBox.innerHTML = ''; }
  cont.appendChild(nuevo);
  idx774++;
}

/* ===== 787 ===== */
let idx787 = 1;
function agregar787() {
  const cont = document.getElementById('c787-container');
  const base = cont.children[0];
  const nuevo = base.cloneNode(true);
  const id = `c787-${idx787}`;
  nuevo.dataset.campo = id;
  nuevo.querySelector('span.fw-bold').textContent = `787 #${idx787 + 1}`;
  nuevo.querySelectorAll('input').forEach(i => i.value = '');
  const wBox = nuevo.querySelector(`#${base.dataset.campo || 'c787-0'}_787w`);
  if (wBox) { wBox.id = `${id}_787w`; wBox.innerHTML = ''; }
  cont.appendChild(nuevo);
  idx787++;
}

function inicializarAutocompletado700(indice) {
  configurarAutocompletado(
    `nombre_relacionado_apellidos_${indice}`,
    `nombre-relacionado-autocomplete-${indice}`,
    "compositor", // ⚠️ usa el mismo modelo que el campo 100
    function (id, text, fechas) {
      const apellidosNombres = id;
      document.getElementById(`nombre_relacionado_apellidos_${indice}`).value = apellidosNombres;

      if (fechas) {
        document.getElementById(`nombre_relacionado_fechas_${indice}`).value = fechas;
      }
    }
  );
}

// Inicializa el primero al cargar la página
document.addEventListener('DOMContentLoaded', function () {
  inicializarAutocompletado700(0);
});
