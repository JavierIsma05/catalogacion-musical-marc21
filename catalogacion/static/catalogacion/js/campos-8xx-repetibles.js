/* ============================================================
   📦 BLOQUE 8XX – Ubicación y Recursos Disponibles
   ============================================================ */

console.log("🟢 Script bloque_8xx.js cargado correctamente");

// Contadores globales
const contadores8xx = {
  ubicacion852: 1,
  recurso856: 0,
  subC852: {},  // subcampos de $c
  subU856: {},  // subcampos $u
  subY856: {}   // subcampos $y
};

/* ============================================================
   🏛️ 852 – UBICACIÓN (INSTITUCIÓN, SIGNATURA, ESTANTERÍA)
   ============================================================ */

// Agregar una nueva ubicación completa (bloque 852)
// Agregar un nuevo subcampo $c (Estantería)
window.agregarC852 = function () {
  // Tomar el índice correcto del último bloque de ubicación
  const ubicaciones = document.querySelectorAll("[data-campo^='ubicacion852-']");
  const index = ubicaciones.length - 1; // siempre el último bloque visible
  if (index < 0) return;

  if (!contadores8xx.subC852[index]) contadores8xx.subC852[index] = 1;
  const subIndex = contadores8xx.subC852[index]++;

  const contenedor = document.getElementById(`ubicacion852-${index}-campos`);
  if (!contenedor) return;

  // Clon visual exacto del campo original (mantiene $c y estilos)
  const div = document.createElement("div");
  div.classList.add("mb-2");
  div.setAttribute("data-subcampo", `c852-${index}-${subIndex}`);
  div.innerHTML = `
      <div class="input-group input-group-sm">
        <span class="input-group-text">$c</span>
        <input type="text" name="ubicacion852_c_${index}_${subIndex}" 
               class="form-control" 
               placeholder="Ej: Sala Música Antigua, Estante 4B">
        <button type="button" class="btn btn-outline-danger"
                onclick="eliminarSubcampo('c852-${index}-${subIndex}')">
          X
        </button>
      </div>
  `;
  
  contenedor.appendChild(div);
  console.log(`📚 Subcampo $c agregado correctamente a ubicación (852) #${index}`);
};


// Eliminar una ubicación completa
window.eliminarUbicacion852 = function (boton) {
  const campo = boton.closest(".campo-repetible");
  if (campo) campo.remove();
  console.log("🗑️ Ubicación (852) eliminada");
};

// Agregar un nuevo subcampo $c (Estantería)
window.agregarC852 = function () {
  const index = contadores8xx.ubicacion852 - 1;
  if (index < 0) return;

  if (!contadores8xx.subC852[index]) contadores8xx.subC852[index] = 1;
  const subIndex = contadores8xx.subC852[index]++;

  const contenedor = document.getElementById(`ubicacion852-${index}-campos`);
  if (!contenedor) return;

  const div = document.createElement("div");
  div.classList.add("mb-2");
  div.setAttribute("data-subcampo", `c852-${index}-${subIndex}`);
  div.innerHTML = `
      <div class="input-group input-group-sm">
        <span class="input-group-text">$c</span>
        <input type="text" name="ubicacion852_c_${index}_${subIndex}" class="form-control"
               placeholder="Ej: Sala Música Antigua, Estante 4B">
        <button type="button" class="btn btn-outline-danger"
                onclick="eliminarSubcampo('c852-${index}-${subIndex}')">X</button>
      </div>
  `;
  contenedor.appendChild(div);

  console.log(`📚 Subcampo $c agregado en ubicación (852) #${index}`);
};

/* ============================================================
   🌐 856 – RECURSOS DISPONIBLES
   ============================================================ */

// Agregar un recurso (856)
window.agregarRecurso856 = function () {
  const container = document.getElementById("recurso856-container");
  const template = document.getElementById("tpl-recurso856");

  const index = contadores8xx.recurso856++;
  const nuevoCampo = template.content.cloneNode(true);

  // Actualizar índices
  nuevoCampo.querySelectorAll("[name]").forEach(input => {
    input.name = input.name.replace("_0", `_${index}`);
  });

  nuevoCampo.querySelectorAll("[id]").forEach(el => {
    el.id = el.id.replace("-0", `-${index}`);
  });

  // Actualizar etiquetas
  nuevoCampo.querySelectorAll("h5").forEach(h => {
    h.textContent = `Recurso disponible (856) #${index + 1}`;
  });

  container.appendChild(nuevoCampo);

  contadores8xx.subU856[index] = 1;
  contadores8xx.subY856[index] = 1;

  console.log(`🌐 Recurso (856) agregado #${index}`);
};

// Eliminar recurso completo
window.eliminarRecurso856 = function (boton) {
  const bloque = boton.closest(".campo-repetible");
  if (bloque) bloque.remove();
  console.log("🗑️ Recurso (856) eliminado");
};

// Agregar subcampo $u (URL)
window.agregarU856 = function () {
  const index = contadores8xx.recurso856 - 1;
  if (index < 0) return;

  if (!contadores8xx.subU856[index]) contadores8xx.subU856[index] = 1;
  const subIndex = contadores8xx.subU856[index]++;

  const contenedor = document.getElementById(`recurso856-${index}-urls`);
  if (!contenedor) return;

  const div = document.createElement("div");
  div.classList.add("mb-2");
  div.setAttribute("data-subcampo", `u856-${index}-${subIndex}`);
  div.innerHTML = `
    <div class="input-group input-group-sm">
      <span class="input-group-text">$u</span>
      <input type="url" name="recurso856_u_${index}_${subIndex}" class="form-control" placeholder="https://...">
      <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('u856-${index}-${subIndex}')">X</button>
    </div>
  `;
  contenedor.appendChild(div);

  console.log(`🔗 Subcampo $u agregado al recurso (856) #${index}`);
};

// Agregar subcampo $y (Texto del enlace)
window.agregarY856 = function () {
  const index = contadores8xx.recurso856 - 1;
  if (index < 0) return;

  if (!contadores8xx.subY856[index]) contadores8xx.subY856[index] = 1;
  const subIndex = contadores8xx.subY856[index]++;

  const contenedor = document.getElementById(`recurso856-${index}-textos`);
  if (!contenedor) return;

  const div = document.createElement("div");
  div.classList.add("mb-2");
  div.setAttribute("data-subcampo", `y856-${index}-${subIndex}`);
  div.innerHTML = `
    <div class="input-group input-group-sm">
      <span class="input-group-text">$y</span>
      <input type="text" name="recurso856_y_${index}_${subIndex}" class="form-control"
             placeholder="Ej: Ver partitura, Escuchar audio, etc.">
      <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('y856-${index}-${subIndex}')">X</button>
    </div>
  `;
  contenedor.appendChild(div);

  console.log(`📝 Subcampo $y agregado al recurso (856) #${index}`);
};

/* ============================================================
   🧹 Función genérica para eliminar subcampos
   ============================================================ */
window.eliminarSubcampo = function (id) {
  const subcampo = document.querySelector(`[data-subcampo="${id}"]`);
  if (subcampo) subcampo.remove();
  console.log(`❌ Subcampo eliminado: ${id}`);
};
