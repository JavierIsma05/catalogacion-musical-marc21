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
}

// ============================================
// VALIDACIÓN DEL FORMULARIO Y LOGGING
// ============================================

function validarFormulario() {
    const form = document.getElementById("obraForm");

    if (!form) {
        console.warn("⚠️ Formulario no encontrado");
        return;
    }

    form.addEventListener("submit", function (e) {
        // Prevenir el envío temporal para ver los logs
        // e.preventDefault();

        logearDatosFormulario(form);
        // form.submit();
    });
}

/**
 * Función para loguear todos los datos del formulario de manera organizada
 * Agrupa los campos repetibles y subcampos
 */
function logearDatosFormulario(form) {
    const formData = new FormData(form);

    console.log("\n" + "=".repeat(80));
    console.log("📋 DATOS DEL FORMULARIO - OBRA GENERAL MARC21");
    console.log("=".repeat(80) + "\n");

    // Objeto para organizar los datos
    const datosOrganizados = {
        cabecera: {},
        bloque_0xx: {},
        bloque_1xx: {},
        bloque_2xx: {},
        bloque_3xx: {},
        bloque_4xx: {},
        bloque_5xx: {},
        bloque_6xx: {},
        bloque_7xx: {},
        bloque_8xx: {},
        otros: {},
    };

    // Procesar todos los campos
    for (let [key, value] of formData.entries()) {
        if (value) {
            // Solo mostrar campos con valor
            // Clasificar por bloque
            if (
                key.includes("tipo_registro") ||
                key.includes("nivel_bibliografico")
            ) {
                datosOrganizados.cabecera[key] = value;
            } else if (
                key.includes("020") ||
                key.includes("024") ||
                key.includes("028") ||
                key.includes("031") ||
                key.includes("041") ||
                key.includes("044") ||
                key.includes("isbn") ||
                key.includes("ismn") ||
                key.includes("numero_editor") ||
                key.includes("incipit") ||
                key.includes("idioma") ||
                key.includes("codigo_pais")
            ) {
                datosOrganizados.bloque_0xx[key] = value;
            } else if (
                key.includes("100") ||
                key.includes("110") ||
                key.includes("130") ||
                key.includes("240") ||
                key.includes("funcion_compositor") ||
                key.includes("atribucion") ||
                key.includes("forma_") ||
                key.includes("medio_interpretacion_") ||
                key.includes("numero_parte") ||
                key.includes("nombre_parte")
            ) {
                datosOrganizados.bloque_1xx[key] = value;
            } else if (
                key.includes("245") ||
                key.includes("246") ||
                key.includes("250") ||
                key.includes("264") ||
                key.includes("titulo") ||
                key.includes("subtitulo") ||
                key.includes("mencion_responsabilidad") ||
                key.includes("edicion") ||
                key.includes("produccion_publicacion")
            ) {
                datosOrganizados.bloque_2xx[key] = value;
            } else if (
                key.includes("300") ||
                key.includes("340") ||
                key.includes("348") ||
                key.includes("382") ||
                key.includes("383") ||
                key.includes("descripcion_fisica") ||
                key.includes("extension_300") ||
                key.includes("dimension_300") ||
                key.includes("medio_fisico") ||
                key.includes("tecnica_340") ||
                key.includes("caracteristica_musica") ||
                key.includes("formato_348") ||
                key.includes("medio_382") ||
                key.includes("solista_382") ||
                key.includes("numero_interpretes") ||
                key.includes("designacion_numerica") ||
                key.includes("numero_obra_383") ||
                key.includes("opus_383")
            ) {
                datosOrganizados.bloque_3xx[key] = value;
            } else if (
                key.includes("490") ||
                key.includes("mencion_serie") ||
                key.includes("titulo_serie_490") || 
                key.includes("volumen_serie_490")
            ) {
                datosOrganizados.bloque_4xx[key] = value;
            
            } else if(
                key.includes("500") ||
                key.includes("505") ||
                key.includes("nota_general") ||
                key.includes("nota_contenido")
            ) {
                datosOrganizados.bloque_5xx[key]=value;
            }
            else if (
                key.includes("600") ||
                key.includes("650") ||
                key.includes("materia")
            ) {
                datosOrganizados.bloque_6xx[key] = value;
            }
            else if (
                key.includes("700") ||
                key.includes("710") ||
                key.includes("720") ||
                key.includes("nombre_relacionado")
            ) {
                datosOrganizados.bloque_7xx[key] = value;
            }
            else if (
                key.includes("800") ||
                key.includes("810") ||
                key.includes("830") ||
                key.includes("ubicacion")
            ) {
                datosOrganizados.bloque_8xx[key] = value;
            }else {
                datosOrganizados.otros[key] = value;
            }
        }
    }

    // Mostrar datos por bloques
    mostrarBloque("CABECERA", datosOrganizados.cabecera);
    mostrarBloque(
        "BLOQUE 0XX - CAMPOS DE CONTROL",
        datosOrganizados.bloque_0xx
    );
    mostrarBloque(
        "BLOQUE 1XX - ENTRADAS PRINCIPALES",
        datosOrganizados.bloque_1xx
    );
    mostrarBloque(
        "BLOQUE 2XX - TÍTULOS Y PUBLICACIÓN",
        datosOrganizados.bloque_2xx
    );
    mostrarBloque(
        "BLOQUE 3XX - DESCRIPCIÓN FÍSICA",
        datosOrganizados.bloque_3xx
    );
    mostrarBloque("BLOQUE 4XX - SERIES", datosOrganizados.bloque_4xx);

    if (Object.keys(datosOrganizados.otros).length > 0) {
        mostrarBloque("OTROS CAMPOS", datosOrganizados.otros);
    }

    // Análisis de campos repetibles
    analizarCamposRepetibles(datosOrganizados);

    // Resumen
    mostrarResumen(formData);

    console.log("\n" + "=".repeat(80));
    console.log("✅ FIN DEL LOG DE DATOS DEL FORMULARIO");
    console.log("=".repeat(80) + "\n");
}

/**
 * Muestra un bloque de datos organizado
 */
function mostrarBloque(titulo, datos) {
    const cantidad = Object.keys(datos).length;

    if (cantidad === 0) {
        console.log(`\n📦 ${titulo}: Sin datos`);
        return;
    }

    console.log(
        `\n📦 ${titulo} (${cantidad} campo${cantidad !== 1 ? "s" : ""})`
    );
    console.log("─".repeat(80));

    for (let [key, value] of Object.entries(datos)) {
        // Detectar si es campo repetible
        const esRepetible = /_\d+(_\d+)?$/.test(key);
        const icono = esRepetible ? "🔁" : "📝";

        console.log(`${icono} ${key}: "${value}"`);
    }
}

/**
 * Analiza y agrupa los campos repetibles
 */
function analizarCamposRepetibles(datosOrganizados) {
    console.log("\n\n🔄 ANÁLISIS DE CAMPOS REPETIBLES");
    console.log("=".repeat(80));

    const camposRepetibles = {
        // Bloque 0XX
        "ISMN (024)": [],
        "Número Editor (028)": [],
        "Incipit Musical (031)": [],
        "Incipit URL": [],
        "Idioma Obra (041)": [],
        "Código País (044)": [],

        // Bloque 1XX
        "Función Compositor (100)": [],
        "Atribución Compositor": [],
        "Forma 130": [],
        "Medio Interpretación 130": [],
        "Número Parte/Sección 130": [],
        "Nombre Parte/Sección 130": [],
        "Forma 240": [],
        "Medio Interpretación 240": [],
        "Número Parte/Sección 240": [],
        "Nombre Parte/Sección 240": [],

        // Bloque 2XX
        "Título Alternativo (246)": [],
        "Edición (250)": [],
        "Producción/Publicación (264)": [],

        // Bloque 3XX
        "Descripción Física (300)": [],
        "Extensión (300 $a)": [],
        "Dimensión (300 $c)": [],
        "Medio Físico (340)": [],
        "Técnica (340 $d)": [],
        "Característica Música Notada (348)": [],
        "Formato (348)": [],
        "Medio Interpretación (382)": [],
        "Medio Interpretación 382 $a": [],
        "Solista (382)": [],
        "Número Intérpretes (382)": [],
        "Designación Numérica Obra (383)": [],
        "Número Obra (383)": [],
        "Opus (383)": [],

        // Bloque 4XX
        "Mención de Serie (490)": [],
        "Título Serie (490 $a)": [],
        "Volumen Serie (490 $v)": [],
    };

    // Agrupar todos los datos
    const todosDatos = {
        ...datosOrganizados.bloque_0xx,
        ...datosOrganizados.bloque_1xx,
        ...datosOrganizados.bloque_2xx,
        ...datosOrganizados.bloque_3xx,
        ...datosOrganizados.bloque_4xx,
    };

    // Clasificar campos repetibles
    for (let [key, value] of Object.entries(todosDatos)) {
        // ISMN
        if (key.includes("ismn_") || key.match(/024.*_\d+/)) {
            const match = key.match(/_(\d+)$/);
            if (match) {
                camposRepetibles["ISMN (024)"].push({
                    indice: match[1],
                    valor: value,
                });
            }
        }

        // Incipit
        if (key.includes("incipit_") && !key.includes("url")) {
            const match = key.match(/_(\d+)/);
            if (match) {
                camposRepetibles["Incipit Musical (031)"].push({
                    campo: key,
                    valor: value,
                });
            }
        }

        // Incipit URL
        if (key.includes("incipit_url")) {
            camposRepetibles["Incipit URL"].push({ campo: key, valor: value });
        }

        // Idioma Obra
        if (key.includes("idioma_obra")) {
            camposRepetibles["Idioma Obra (041)"].push({
                campo: key,
                valor: value,
            });
        }

        // Código País
        if (key.includes("codigo_pais")) {
            camposRepetibles["Código País (044)"].push({
                campo: key,
                valor: value,
            });
        }

        // Título Alternativo
        if (key.includes("titulo_alternativo")) {
            const match = key.match(/_(\d+)$/);
            if (match) {
                camposRepetibles["Título Alternativo (246)"].push({
                    indice: match[1],
                    campo: key,
                    valor: value,
                });
            }
        }

        // Extensión 300
        if (key.includes("extension_300")) {
            camposRepetibles["Extensión (300 $a)"].push({
                campo: key,
                valor: value,
            });
        }

        // Dimensión 300
        if (key.includes("dimension_300")) {
            camposRepetibles["Dimensión (300 $c)"].push({
                campo: key,
                valor: value,
            });
        }

        // Técnica 340
        if (key.includes("tecnica_340")) {
            camposRepetibles["Técnica (340 $d)"].push({
                campo: key,
                valor: value,
            });
        }

        // Mención de Serie 490
        if (key.includes("mencion_serie_relacion")) {
            const match = key.match(/_(\d+)$/);
            if (match) {
                camposRepetibles["Mención de Serie (490)"].push({
                    indice: match[1],
                    valor: value,
                });
            }
        }

        // Título Serie 490
        if (key.includes("titulo_serie_490")) {
            camposRepetibles["Título Serie (490 $a)"].push({
                campo: key,
                valor: value,
            });
        }

        // Volumen Serie 490
        if (key.includes("volumen_serie_490")) {
            camposRepetibles["Volumen Serie (490 $v)"].push({
                campo: key,
                valor: value,
            });
        }
    }

    // Mostrar solo los que tienen datos
    for (let [nombre, datos] of Object.entries(camposRepetibles)) {
        if (datos.length > 0) {
            console.log(
                `\n📌 ${nombre}: ${datos.length} instancia${
                    datos.length !== 1 ? "s" : ""
                }`
            );
            datos.forEach((item, idx) => {
                if (item.indice !== undefined) {
                    console.log(
                        `   [${parseInt(item.indice) + 1}] ${
                            item.campo || ""
                        }: "${item.valor}"`
                    );
                } else {
                    console.log(
                        `   [${idx + 1}] ${item.campo}: "${item.valor}"`
                    );
                }
            });
        }
    }
}

/**
 * Muestra un resumen general
 */
function mostrarResumen(formData) {
    console.log("\n\n📊 RESUMEN GENERAL");
    console.log("=".repeat(80));

    const totalCampos = Array.from(formData.entries()).filter(
        ([_, value]) => value
    ).length;
    const camposVacios = Array.from(formData.entries()).filter(
        ([_, value]) => !value
    ).length;

    console.log(`📝 Total de campos con datos: ${totalCampos}`);
    console.log(`⚪ Total de campos vacíos: ${camposVacios}`);
    console.log(
        `📦 Total de campos en formulario: ${totalCampos + camposVacios}`
    );

    // Estadísticas de contadores
    console.log("\n🔢 CONTADORES DE CAMPOS REPETIBLES:");
    console.log("─".repeat(40));

    const contadoresActuales = [
        { nombre: "ISMN", key: "ismn" },
        { nombre: "Título Alternativo", key: "tituloAlternativo" },
        { nombre: "Descripción Física", key: "descripcionFisica" },
        { nombre: "Extensión 300", key: "extension300" },
        { nombre: "Dimensión 300", key: "dimension300" },
        { nombre: "Medio Físico", key: "medioFisico" },
        { nombre: "Técnica 340", key: "tecnica340" },
        { nombre: "Mención de Serie", key: "mencionSerie" },
        { nombre: "Título Serie 490", key: "tituloSerie490" },
        { nombre: "Volumen Serie 490", key: "volumenSerie490" },
    ];

    contadoresActuales.forEach(({ nombre, key }) => {
        const count = contadores.obtener(key);
        if (count > 0) {
            console.log(`   ${nombre}: ${count} (contador actual)`);
        }
    });
}

// Hacer la función disponible globalmente
window.logearDatosFormulario = logearDatosFormulario;

/**
 * Función para obtener los datos del formulario como objeto JSON
 * Útil para debugging y testing
 */
window.obtenerDatosJSON = function () {
    const form = document.getElementById("obraForm");
    if (!form) {
        console.error("❌ Formulario no encontrado");
        return null;
    }

    const formData = new FormData(form);
    const datos = {};

    for (let [key, value] of formData.entries()) {
        if (value) {
            datos[key] = value;
        }
    }

    console.log("📋 Datos del formulario en formato JSON:");
    console.log(JSON.stringify(datos, null, 2));

    return datos;
};

/**
 * Función para copiar los datos JSON al portapapeles
 */
window.copiarDatosJSON = function () {
    const datos = obtenerDatosJSON();
    if (datos) {
        const json = JSON.stringify(datos, null, 2);
        navigator.clipboard
            .writeText(json)
            .then(() => {
                console.log("✅ Datos copiados al portapapeles");
                alert("✅ Datos copiados al portapapeles en formato JSON");
            })
            .catch((err) => {
                console.error("❌ Error al copiar:", err);
            });
    }
};

/**
 * Función para descargar los datos como archivo JSON
 */
window.descargarDatosJSON = function () {
    const datos = obtenerDatosJSON();
    if (datos) {
        const json = JSON.stringify(datos, null, 2);
        const blob = new Blob([json], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `obra-marc21-${new Date().getTime()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        console.log("✅ Archivo JSON descargado");
    }
};

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
                form.submit();
            }
        }

        // Ctrl + B para ir al inicio
        if (e.ctrlKey && e.key === "b") {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    });
}

// ============================================
// CONTADOR DE CAMPOS (ESTADÍSTICAS)
// ============================================

function mostrarEstadisticas() {
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
}

// ============================================
// INICIALIZACIÓN PRINCIPAL
// ============================================

document.addEventListener("DOMContentLoaded", function () {
    // Funciones principales
    inicializarScrollSpy();
    validarFormulario();

    // Funciones opcionales
    inicializarAtajosTeclado();
    crearBotonVolverArriba();
    prevenirPerdidaDatos();
    // inicializarAutoGuardado(); // Descomentar para autoguardado
});

window.verEstadoFormulario = function () {
    mostrarEstadisticas();
    contadores.mostrarEstado();
};

/**
 * Función para limpiar localStorage
 */
window.limpiarBorrador = function () {
    localStorage.removeItem("obra_general_draft");
};

// Exponer función de estadísticas
window.mostrarEstadisticas = mostrarEstadisticas;

// ============================================
// VERIFICACIÓN DE FUNCIONES DEL BLOQUE 1XX
// ============================================

window.addEventListener("DOMContentLoaded", function () {
    const funciones1xx = [
        "agregarFuncionCompositor",
        "agregarAtribucionCompositor",
        "agregarForma130",
        "agregarMedioInterpretacion130",
        "agregarNumeroParteSeccion130",
        "agregarNombreParteSeccion130",
        "agregarForma240",
        "agregarMedioInterpretacion240",
        "agregarNumeroParteSeccion240",
        "agregarNombreParteSeccion240",
    ];

    let faltantes = [];
    funciones1xx.forEach((fn) => {
        if (typeof window[fn] === "function") {
            // console.log(`   ✅ ${fn}`);
        } else {
            console.error(`   ❌ ${fn} NO ENCONTRADA`);
            faltantes.push(fn);
        }
    });

    if (faltantes.length === 0) {
        // console.log(
        //     "✅ Todas las funciones del bloque 1XX están disponibles\n"
        // );
    } else {
        console.error(
            `❌ Faltan ${faltantes.length} funciones del bloque 1XX:`,
            faltantes
        );
        console.error(
            "⚠️ Verifica que el archivo campos-1xx-repetibles.js se esté cargando correctamente"
        );
    }
});
