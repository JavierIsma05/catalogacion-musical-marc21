
// Estado simple: solo 1 ubicación a la vez
let ubicacionCreada = true;   // ya arrancamos con 1 en el HTML
let contadorC852 = 1;

function agregarUbicacion852() {
    if (ubicacionCreada) return;
    const tpl = document.getElementById('tpl-ubicacion852');
    const contenedor = document.getElementById('ubicacion852-container');
    contenedor.appendChild(tpl.content.cloneNode(true));
    ubicacionCreada = true;
    document.getElementById('btnAgregarUbicacion852').style.display = 'none';
    contadorC852 = 1;
}

function eliminarUbicacion852() {
    const contenedor = document.getElementById('ubicacion852-container');
    contenedor.innerHTML = '';
    ubicacionCreada = false;
    document.getElementById('btnAgregarUbicacion852').style.display = 'inline-block';
}

function agregarC852() {
    const contenedor = document.getElementById('ubicacion852-0-campos');
    if (!contenedor) return;
    const id = `c852-${contadorC852}`;
    const wrap = document.createElement('div');
    wrap.className = 'mb-2';
    wrap.dataset.subcampo = id;
    wrap.innerHTML = `
      <div class="input-group input-group-sm">
        <input type="text" name="ubicacion852_c_0_${contadorC852}" class="form-control"
               placeholder="Ej: Sala Música Antigua, Estante 4B">
        <button type="button" class="btn btn-outline-danger"
                onclick="eliminarSubcampo('${id}')">X</button>
      </div>`;
    contenedor.appendChild(wrap);
    contadorC852++;
}

function eliminarSubcampo(id) {
    const nodo = document.querySelector('[data-subcampo="' + id + '"]');
    if (nodo) nodo.remove();
}

// =====================================================
// BLOQUE 856 – RECURSOS DISPONIBLES
// =====================================================

let recursoCreado856 = false;
let contadorU856 = 1;
let contadorY856 = 1;

function agregarRecurso856() {
    if (recursoCreado856) return;

    const tpl = document.getElementById('tpl-recurso856');
    const contenedor = document.getElementById('recurso856-container');

    if (tpl && contenedor) {
        contenedor.appendChild(tpl.content.cloneNode(true));
        recursoCreado856 = true;
        document.getElementById('btnAgregarRecurso856').style.display = 'none';
    }
}

function eliminarRecurso856() {
    const contenedor = document.getElementById('recurso856-container');
    if (contenedor) {
        contenedor.innerHTML = '';
        recursoCreado856 = false;
        document.getElementById('btnAgregarRecurso856').style.display = 'inline-block';
        contadorU856 = 1;
        contadorY856 = 1;
    }
}

function agregarU856() {
    const contenedor = document.getElementById('recurso856-0-urls');
    if (!contenedor) return;

    const id = `u856-${contadorU856}`;
    const div = document.createElement('div');
    div.className = 'mb-2';
    div.dataset.subcampo = id;

    div.innerHTML = `
      <div class="input-group input-group-sm">
        <input type="url" name="recurso856_u_0_${contadorU856}" class="form-control" placeholder="https://...">
        <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('${id}')">X</button>
      </div>
    `;
    contenedor.appendChild(div);
    contadorU856++;
}

function agregarY856() {
    const contenedor = document.getElementById('recurso856-0-textos');
    if (!contenedor) return;

    const id = `y856-${contadorY856}`;
    const div = document.createElement('div');
    div.className = 'mb-2';
    div.dataset.subcampo = id;

    div.innerHTML = `
      <div class="input-group input-group-sm">
        <input type="text" name="recurso856_y_0_${contadorY856}" class="form-control"
               placeholder="Ej: Ver partitura, Escuchar audio, etc.">
        <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('${id}')">X</button>
      </div>
    `;
    contenedor.appendChild(div);
    contadorY856++;
}
