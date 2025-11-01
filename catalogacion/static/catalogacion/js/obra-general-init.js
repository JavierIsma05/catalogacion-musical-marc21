/**
 * ============================================
 * OBRA-GENERAL-INIT.JS
 * ============================================
 * Inicialización y funciones generales del formulario
 * Este archivo se carga AL FINAL, después de todos los demás
 */

// ============================================
// SCROLL-SPY PARA SIDEBAR
// ============================================

function inicializarScrollSpy() {
    const sections = document.querySelectorAll("[id]");
    const navLinks = document.querySelectorAll(".sidebar-nav .nav-link");

    if (sections.length === 0 || navLinks.length === 0) {
        console.warn(
            "⚠️ No se encontraron secciones o links de navegación para scroll-spy"
        );
        return;
    }

    function changeActiveLink() {
        let index = sections.length;
        while (--index && window.scrollY + 100 < sections[index].offsetTop) {}

        navLinks.forEach((link) => link.classList.remove("active"));
        if (navLinks[index]) {
            navLinks[index].classList.add("active");
        }
    }

    // Ejecutar al cargar
    changeActiveLink();

    // Ejecutar al hacer scroll
    window.addEventListener("scroll", changeActiveLink);

    // Smooth scroll al hacer clic en los links
    navLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetId = this.getAttribute("href");
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                });
            }
        });
    });

    console.log("✅ Scroll-spy inicializado");
}

// ============================================
// VALIDACIÓN DEL FORMULARIO
// ============================================

function validarFormulario() {
    const form = document.getElementById("obraForm");

    if (!form) {
        console.warn("⚠️ Formulario no encontrado");
        return;
    }

    form.addEventListener("submit", function (e) {
        // Validaciones personalizadas antes de enviar
        console.log("📝 Enviando formulario...");

        // Aquí puedes agregar validaciones adicionales si las necesitas
        // Por ejemplo:
        /*
        const tipoRegistro = form.querySelector('[name="tipo_registro"]').value;
        if (!tipoRegistro) {
            e.preventDefault();
            alert('Por favor selecciona un tipo de registro');
            return false;
        }
        */
    });

    console.log("✅ Validación de formulario configurada");
}

// ============================================
// ATAJOS DE TECLADO (OPCIONAL)
// ============================================

function inicializarAtajosTeclado() {
    document.addEventListener("keydown", function (e) {
        // Ctrl + S para guardar (previene guardar del navegador)
        if (e.ctrlKey && e.key === "s") {
            e.preventDefault();
            const form = document.getElementById("obraForm");
            if (form) {
                console.log("💾 Guardando con Ctrl+S...");
                form.submit();
            }
        }

        // Ctrl + B para ir al inicio
        if (e.ctrlKey && e.key === "b") {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    });

    console.log("⌨️ Atajos de teclado activados:");
    console.log("   - Ctrl+S: Guardar formulario");
    console.log("   - Ctrl+B: Ir al inicio");
}

// ============================================
// CONTADOR DE CAMPOS (ESTADÍSTICAS)
// ============================================

function mostrarEstadisticas() {
    // Solo para debugging/desarrollo
    console.log("📊 ESTADÍSTICAS DEL FORMULARIO");
    console.log("═".repeat(50));

    const stats = {
        campos0xx: [
            { nombre: "ISBN", count: contadores.obtener("isbn") - 1 },
            { nombre: "ISMN", count: contadores.obtener("ismn") - 1 },
            {
                nombre: "Número Editor",
                count: contadores.obtener("numeroEditor") - 1,
            },
            { nombre: "Incipit", count: contadores.obtener("incipit") - 1 },
            {
                nombre: "Código Lengua",
                count: contadores.obtener("codigoLengua") - 1,
            },
            {
                nombre: "Código País",
                count: contadores.obtener("codigoPais") - 1,
            },
        ],
        campos1xx: [
            {
                nombre: "Autor Personal",
                count: contadores.obtener("autorPersonal") - 1,
            },
            {
                nombre: "Autor Corporativo",
                count: contadores.obtener("autorCorporativo") - 1,
            },
        ],
    };

    console.log("📦 CAMPOS 0XX:");
    stats.campos0xx.forEach((campo) => {
        if (campo.count >= 0) {
            console.log(
                `   ${campo.nombre}: ${campo.count} campo(s) agregado(s)`
            );
        }
    });

    console.log("");
    console.log("👥 CAMPOS 1XX:");
    stats.campos1xx.forEach((campo) => {
        if (campo.count >= 0) {
            console.log(
                `   ${campo.nombre}: ${campo.count} campo(s) agregado(s)`
            );
        }
    });

    console.log("═".repeat(50));
}

// ============================================
// AUTO-GUARDADO (OPCIONAL - localStorage)
// ============================================

function inicializarAutoGuardado() {
    const form = document.getElementById("obraForm");
    if (!form) return;

    // Guardar cada 30 segundos
    setInterval(() => {
        const formData = new FormData(form);
        const data = {};

        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        // Guardar en localStorage
        localStorage.setItem("obra_general_draft", JSON.stringify(data));
        console.log("💾 Borrador guardado automáticamente");
    }, 30000);

    // Restaurar al cargar
    const draft = localStorage.getItem("obra_general_draft");
    if (draft) {
        console.log("📄 Se encontró un borrador guardado");
        // Aquí puedes implementar la restauración si lo deseas
    }
}

// ============================================
// BOTÓN "VOLVER ARRIBA"
// ============================================

function crearBotonVolverArriba() {
    // Crear botón
    const button = document.createElement("button");
    button.innerHTML = '<i class="bi bi-arrow-up"></i>';
    button.className = "btn btn-primary position-fixed";
    button.style.cssText = `
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: none;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;

    button.onclick = () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    document.body.appendChild(button);

    // Mostrar/ocultar según scroll
    window.addEventListener("scroll", () => {
        if (window.scrollY > 300) {
            button.style.display = "block";
        } else {
            button.style.display = "none";
        }
    });

    console.log('⬆️ Botón "Volver arriba" creado');
}

// ============================================
// PREVENIR PÉRDIDA DE DATOS
// ============================================

function prevenirPerdidaDatos() {
    const form = document.getElementById("obraForm");
    if (!form) return;

    let formModificado = false;

    // Detectar cambios en el formulario
    form.addEventListener("input", () => {
        formModificado = true;
    });

    // Advertir antes de salir si hay cambios sin guardar
    window.addEventListener("beforeunload", (e) => {
        if (formModificado) {
            e.preventDefault();
            e.returnValue = "";
            return "¿Seguro que quieres salir? Hay cambios sin guardar.";
        }
    });

    // Marcar como guardado al enviar
    form.addEventListener("submit", () => {
        formModificado = false;
    });

    console.log("🛡️ Protección contra pérdida de datos activada");
}

// ============================================
// INICIALIZACIÓN PRINCIPAL
// ============================================

document.addEventListener("DOMContentLoaded", function () {
    console.log("");
    console.log("INICIALIZANDO FORMULARIO OBRA GENERAL");
    console.log("═".repeat(50));

    // Funciones principales
    inicializarScrollSpy();
    validarFormulario();

    // Funciones opcionales (puedes comentar las que no necesites)
    inicializarAtajosTeclado();
    crearBotonVolverArriba();
    prevenirPerdidaDatos();
    // inicializarAutoGuardado(); // Descomenta si quieres auto-guardado

    // Mostrar estadísticas (solo para desarrollo)
    // mostrarEstadisticas(); // Descomenta para ver estadísticas

    console.log("═".repeat(50));
    console.log("✅ Formulario inicializado correctamente");
    console.log("");
    console.log("💡 TIP: Abre la consola para ver los logs detallados");
    console.log("");
});

// ============================================
// FUNCIONES DE UTILIDAD GLOBAL
// ============================================

/**
 * Función para debugging - Ver estado completo del formulario
 */
window.verEstadoFormulario = function () {
    mostrarEstadisticas();
    contadores.mostrarEstado();
};

/**
 * Función para limpiar localStorage
 */
window.limpiarBorrador = function () {
    localStorage.removeItem("obra_general_draft");
    console.log("🗑️ Borrador eliminado");
};

// Exponer función de estadísticas
window.mostrarEstadisticas = mostrarEstadisticas;

console.log("✅ obra-general-init.js cargado correctamente");
