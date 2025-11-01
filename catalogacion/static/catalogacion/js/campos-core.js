class ContadoresCampos {
    constructor() {
        // Contadores principales para campos repetibles
        this.contadores = {};

        // Subcontadores para campos anidados (ej: URLs dentro de Incipit)
        this.subcontadores = {};
    }

    /**
     * Registra un nuevo contador para un tipo de campo
     * @param {string} tipo - Nombre del tipo de campo (ej: 'isbn', 'autor')
     * @param {number} valorInicial - Valor inicial del contador (default: 1)
     */
    registrar(tipo, valorInicial = 1) {
        if (!this.contadores[tipo]) {
            this.contadores[tipo] = valorInicial;
            console.log(`📊 Contador registrado: ${tipo} = ${valorInicial}`);
        }
    }

    /**
     * Obtiene el valor actual de un contador
     */
    obtener(tipo) {
        if (this.contadores[tipo] === undefined) {
            console.warn(`⚠️ Contador no registrado: ${tipo}`);
            return 0;
        }
        return this.contadores[tipo];
    }

    /**
     * Incrementa un contador y devuelve el nuevo valor
     */
    incrementar(tipo) {
        if (this.contadores[tipo] !== undefined) {
            this.contadores[tipo]++;
        }
        return this.contadores[tipo];
    }

    /**
     * Obtiene el valor de un subcontador (para campos anidados)
     * @param {string} tipo - Tipo de subcontador (ej: 'incipitURLs')
     * @param {number} indice - Índice del campo padre
     */
    obtenerSubcontador(tipo, indice) {
        if (!this.subcontadores[tipo]) {
            this.subcontadores[tipo] = {};
        }
        return this.subcontadores[tipo][indice] || 0;
    }

    /**
     * Incrementa un subcontador específico
     */
    incrementarSubcontador(tipo, indice) {
        if (!this.subcontadores[tipo]) {
            this.subcontadores[tipo] = {};
        }
        if (this.subcontadores[tipo][indice] === undefined) {
            this.subcontadores[tipo][indice] = 0;
        }
        this.subcontadores[tipo][indice]++;
        return this.subcontadores[tipo][indice];
    }

    /**
     * Inicializa un subcontador con un valor específico
     */
    inicializarSubcontador(tipo, indice, valor = 1) {
        if (!this.subcontadores[tipo]) {
            this.subcontadores[tipo] = {};
        }
        this.subcontadores[tipo][indice] = valor;
    }

    /**
     * Muestra todos los contadores actuales (útil para debugging)
     */
    mostrarEstado() {
        console.log("📊 Estado de contadores:", this.contadores);
        console.log("📊 Estado de subcontadores:", this.subcontadores);
    }
}

window.contadores = new ContadoresCampos();

// ============================================
// FUNCIONES GENÉRICAS PARA TODOS LOS CAMPOS
// ============================================

/**
 * Elimina un campo repetible del DOM
 * @param {string} campoId - ID único del campo a eliminar
 */
window.eliminarCampo = function (campoId) {
    const campo = document.querySelector(`[data-campo="${campoId}"]`);
    if (campo) {
        // Animación suave antes de eliminar
        campo.style.transition = "opacity 0.3s";
        campo.style.opacity = "0";
        setTimeout(() => campo.remove(), 300);
        console.log(`🗑️ Campo eliminado: ${campoId}`);
    } else {
        console.warn(`⚠️ Campo no encontrado: ${campoId}`);
    }
};

/**
 * Elimina un subcampo del DOM
 * @param {string} subcampoId - ID único del subcampo a eliminar
 */
window.eliminarSubcampo = function (subcampoId) {
    const subcampo = document.querySelector(`[data-subcampo="${subcampoId}"]`);
    if (subcampo) {
        subcampo.style.transition = "opacity 0.3s";
        subcampo.style.opacity = "0";
        setTimeout(() => subcampo.remove(), 300);
        console.log(`🗑️ Subcampo eliminado: ${subcampoId}`);
    } else {
        console.warn(`⚠️ Subcampo no encontrado: ${subcampoId}`);
    }
};

/**
 * Inserta HTML en un contenedor específico
 * @param {string} containerId - ID del contenedor donde insertar
 * @param {string} html - HTML a insertar
 */
window.insertarHTML = function (containerId, html) {
    const container = document.getElementById(containerId);
    if (container) {
        container.insertAdjacentHTML("beforeend", html);

        // Animación de entrada
        const nuevoElemento = container.lastElementChild;
        if (nuevoElemento) {
            nuevoElemento.style.opacity = "0";
            nuevoElemento.style.transition = "opacity 0.3s";
            setTimeout(() => (nuevoElemento.style.opacity = "1"), 10);
        }

        console.log(`✅ HTML insertado en: ${containerId}`);
    } else {
        console.error(`❌ Contenedor no encontrado: ${containerId}`);
    }
};

/**
 * Función de utilidad para crear selectores de opciones
 * @param {Array} opciones - Array de objetos con {value, text, selected}
 * @returns {string} HTML de las opciones
 */
window.generarOpciones = function (opciones) {
    return opciones
        .map((opcion) => {
            const selected = opcion.selected ? "selected" : "";
            return `<option value="${opcion.value}" ${selected}>${opcion.text}</option>`;
        })
        .join("");
};

/**
 * Función para validar que un contenedor existe antes de agregar campos
 * @param {string} containerId - ID del contenedor
 * @returns {boolean}
 */
window.validarContenedor = function (containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(
            `❌ ERROR: Contenedor "${containerId}" no existe en el HTML.`
        );
        alert(
            `Error: No se encontró el contenedor para este campo. Verifica el HTML.`
        );
        return false;
    }
    return true;
};

// ============================================
// UTILIDADES ADICIONALES
// ============================================

/**
 * Genera un ID único para campos
 */
window.generarIdUnico = function (prefijo) {
    return `${prefijo}-${Date.now()}-${Math.random()
        .toString(36)
        .substr(2, 9)}`;
};

/**
 * Scroll suave a un elemento
 */
window.scrollSuaveA = function (elementoId) {
    const elemento = document.getElementById(elementoId);
    if (elemento) {
        elemento.scrollIntoView({ behavior: "smooth", block: "start" });
    }
};

// ============================================
// INICIALIZACIÓN
// ============================================

console.log("✅ campos-core.js cargado correctamente");
console.log("📦 Funciones disponibles:");
console.log("   - window.contadores (gestor de contadores)");
console.log("   - window.eliminarCampo(campoId)");
console.log("   - window.eliminarSubcampo(subcampoId)");
console.log("   - window.insertarHTML(containerId, html)");
console.log("   - window.generarOpciones(opciones)");
console.log("   - window.validarContenedor(containerId)");
