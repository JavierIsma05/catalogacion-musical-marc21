contadores.registrar("medioInterpretacion382", 1);
contadores.registrar("medio382a", 1);
contadores.registrar("numeroInterpretes382", 1);

// ============================================
// 382 - MEDIO DE INTERPRETACIÓN (Repetible)
// ============================================

function generarHTMLMedioInterpretacion382(index) {
    return `
        <div class="campo-repetible" data-campo="medio-interpretacion-382-${index}">
            <div class="campo-header">
                <span class="campo-label">Medio de Interpretación #${
                    index + 1
                }</span>
                <button type="button" class="btn btn-outline-danger btn-remove" onclick="eliminarCampo('medio-interpretacion-382-${index}')">
                    <i class="bi bi-trash"></i> Eliminar
                </button>
            </div>
            
            <!-- Subcampo $a - Medio (Repetible) -->
            <div class="subcampo-group mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$a Medio de Interpretación</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarMedio382a(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="medios-382a-${index}">
                    <div class="mb-2" data-subcampo="medio-382a-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$a</span>
                            <select name="medio_382_a_${index}_0" class="form-select form-select-sm">
                                <option value="piano" selected>Piano</option>
                                <option value="dos pianos">Dos pianos</option>
                                <option value="piano a cuatro manos">Piano a cuatro manos</option>
                                <option value="piano con acompañamiento">Piano con acompañamiento</option>
                            </select>
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('medio-382a-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Subcampo $b - Solista (Repetible) -->
            <div class="subcampo-group mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$b Solista</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarSolista382(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="solistas-382-${index}">
                    <div class="mb-2" data-subcampo="solista-382-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$b</span>
                            <select name="solista_382_b_${index}_0" class="form-select form-select-sm">
                                <option value="piano" selected>Piano</option>
                            </select>
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('solista-382-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Subcampo $n - Número de Intérpretes (Repetible) -->
            <div class="subcampo-group">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="subcampo-label mb-0">$n Número de Intérpretes</label>
                    <button type="button" class="btn btn-outline-primary btn-sm" onclick="agregarNumeroInterpretes382(${index})">
                        <i class="bi bi-plus"></i>
                    </button>
                </div>
                <div id="numeros-interpretes-382-${index}">
                    <div class="mb-2" data-subcampo="numero-interpretes-382-${index}-0">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text">$n</span>
                            <input type="number" min="1" name="numero_interpretes_382_n_${index}_0" class="form-control" placeholder="Ej: 2, 4, 8">
                            <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('numero-interpretes-382-${index}-0')">
                                <i class="bi bi-x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

window.agregarMedioInterpretacion382 = function () {
    if (!validarContenedor("medios-interpretacion-382-container")) return;

    const index = contadores.obtener("medioInterpretacion382");
    insertarHTML(
        "medios-interpretacion-382-container",
        generarHTMLMedioInterpretacion382(index)
    );
    contadores.incrementar("medioInterpretacion382");
};

window.agregarMedio382a = function (parentIndex) {
    const contenedor = document.getElementById(`medios-382a-${parentIndex}`);
    if (!contenedor) return;

    const index = contadores.obtener("medio382a");
    const html = `
        <div class="mb-2" data-subcampo="medio-382a-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$a</span>
                <select name="medio_382_a_${parentIndex}_${index}" class="form-select form-select-sm">
                    <option value="piano" selected>Piano</option>
                    <option value="dos pianos">Dos pianos</option>
                    <option value="piano a cuatro manos">Piano a cuatro manos</option>
                    <option value="piano con acompañamiento">Piano con acompañamiento</option>
                </select>
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('medio-382a-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("medio382a");
};

window.agregarNumeroInterpretes382 = function (parentIndex) {
    const contenedor = document.getElementById(
        `numeros-interpretes-382-${parentIndex}`
    );
    if (!contenedor) return;

    const index = contadores.obtener("numeroInterpretes382");
    const html = `
        <div class="mb-2" data-subcampo="numero-interpretes-382-${parentIndex}-${index}">
            <div class="input-group input-group-sm">
                <span class="input-group-text">$n</span>
                <input type="number" min="1" name="numero_interpretes_382_n_${parentIndex}_${index}" class="form-control" placeholder="Ej: 2, 4, 8">
                <button type="button" class="btn btn-outline-danger" onclick="eliminarSubcampo('numero-interpretes-382-${parentIndex}-${index}')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        </div>
    `;
    contenedor.insertAdjacentHTML("beforeend", html);
    contadores.incrementar("numeroInterpretes382");
};
