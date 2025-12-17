/**
 * Sistema de Borradores para Obras MARC21
 * VERSION CORREGIDA - Maneja subcampos dinámicos anidados
 */

(function () {
    "use strict";

    // Configuración
    const AUTOSAVE_INTERVAL = 60000; // 60 segundos
    const MIN_CHANGE_DELAY = 3000; // 3 segundos después del último cambio

    let borradorId = null;
    let autoSaveTimer = null;
    let changeTimer = null;
    let hasUnsavedChanges = false;

    const form = document.getElementById("obra-form");

    // Si no hay formulario, no inicializar nada (evita errores en otras páginas)
    if (!form) {
        return;
    }

    const API_URLS = {
        guardar: "/catalogacion/api/borradores/guardar/",
        autoguardar: "/catalogacion/api/borradores/autoguardar/",
        obtener: (id) => `/catalogacion/api/borradores/${id}/`,
        obtenerUltimoPorObra: (obraId) =>
            `/catalogacion/api/borradores/obra/${obraId}/ultimo/`,
        eliminar: (id) => `/catalogacion/api/borradores/${id}/eliminar/`,
    };

    function getObraObjetivoId() {
        // Detectar modo edición por URL: /catalogacion/obras/<pk>/editar/
        const match = window.location.pathname.match(
            /\/obras\/(\d+)\/editar\/?$/
        );
        return match ? parseInt(match[1], 10) : null;
    }

    /**
     * Obtiene el CSRF token
     */
    function getCsrfToken() {
        const token = document.querySelector('[name="csrfmiddlewaretoken"]');
        return token ? token.value : "";
    }

    /**
     * NUEVO: Serializa TODOS los datos incluyendo subcampos dinámicos
     */
    function serializeFormData() {
        const formData = new FormData(form);
        const data = {
            _campos_simples: {},
            _formsets: {},
            _subcampos_dinamicos: {}, // NUEVO: Para idiomas, títulos, volúmenes, etc.
        };

        // 1. Procesar campos simples y formsets normales
        for (let [key, value] of formData.entries()) {
            if (shouldExcludeField(key)) continue;

            // Subcampos dinámicos - Dos patrones:
            // 1. tipo_subtipo_parentIndex_timestamp (4 partes):
            //    - idioma_lengua_0_1234567890 (campo 041)
            //    - lugar_produccion_264_0_1234567890 (campo 264 $a)
            //    - entidad_produccion_264_0_1234567890 (campo 264 $b)
            //    - fecha_produccion_264_0_1234567890 (campo 264 $c)
            //    - medio_interpretacion_382_0_1234567890 (campo 382 $a)
            //    - termino_asociado_700_0_1234567890 (campo 700 $c)
            //    - funcion_700_0_1234567890 (campo 700 $e)
            // 2. tipo_subtipo_campo_parentIndex_timestamp (5 partes):
            //    - numero_enlace_773_0_1234567890 (campo 773)

            // Primero intentar patrón de 5 partes
            let subcampoMatch = key.match(/^(\w+)_(\w+)_(\d+)_(\d+)_(\d+)$/);
            if (subcampoMatch) {
                const [, tipo, subtipo, campo, parentIndex, timestamp] =
                    subcampoMatch;
                const subcampoKey = `${tipo}_${subtipo}_${campo}_${parentIndex}`;

                if (!data._subcampos_dinamicos[subcampoKey]) {
                    data._subcampos_dinamicos[subcampoKey] = [];
                }

                data._subcampos_dinamicos[subcampoKey].push({
                    value: value,
                    tipo: tipo,
                    subtipo: subtipo,
                    campo: campo, // Número de campo MARC (773, 774, 787, 852)
                    parentIndex: parentIndex,
                });

                continue;
            }

            // Luego intentar patrón de 4 partes (incluye 264 y 382)
            subcampoMatch = key.match(/^(\w+)_(\w+)_(\d+)_(\d+)$/);
            if (subcampoMatch) {
                const [, tipo, subtipo, parentIndex, timestamp] = subcampoMatch;
                const subcampoKey = `${tipo}_${subtipo}_${parentIndex}`;

                if (!data._subcampos_dinamicos[subcampoKey]) {
                    data._subcampos_dinamicos[subcampoKey] = [];
                }

                data._subcampos_dinamicos[subcampoKey].push({
                    value: value,
                    tipo: tipo,
                    subtipo: subtipo,
                    parentIndex: parentIndex,
                });

                continue;
            }

            // Campos normales
            if (data._campos_simples.hasOwnProperty(key)) {
                if (!Array.isArray(data._campos_simples[key])) {
                    data._campos_simples[key] = [data._campos_simples[key]];
                }
                data._campos_simples[key].push(value);
            } else {
                data._campos_simples[key] = value;
            }
        }

        // 2. Agrupar por formsets
        for (let key in data._campos_simples) {
            const formsetMatch = key.match(/^([a-z_]+)-(\d+)-(.+)$/);
            if (formsetMatch) {
                const [, prefix, index, field] = formsetMatch;

                if (!data._formsets[prefix]) {
                    data._formsets[prefix] = {};
                }
                if (!data._formsets[prefix][index]) {
                    data._formsets[prefix][index] = {};
                }

                data._formsets[prefix][index][field] =
                    data._campos_simples[key];
            }
        }

        // 3. Incluir checkboxes no marcados
        form.querySelectorAll('input[type="checkbox"]').forEach((checkbox) => {
            if (
                !checkbox.checked &&
                !data._campos_simples.hasOwnProperty(checkbox.name)
            ) {
                data._campos_simples[checkbox.name] = "";
            }
        });

        return data;
    }

    /**
     * Determina si un campo debe excluirse
     */
    function shouldExcludeField(fieldName) {
        if (!fieldName || fieldName === "") return true;

        // NO excluir subcampos dinámicos (cambio principal)
        // Solo excluir campos realmente inválidos
        if (fieldName.includes("NaN") || fieldName === "undefined") {
            return true;
        }

        return false;
    }

    /**
     * Obtiene el tipo de obra actual
     */
    function getTipoObra() {
        const tipoRegistro = document.getElementById("id_tipo_registro")?.value;
        const nivelBibliografico = document.getElementById(
            "id_nivel_bibliografico"
        )?.value;

        // Si los campos no están disponibles aún, retornar null
        if (!tipoRegistro || !nivelBibliografico) {
            return null;
        }

        // Mapeo correcto según TIPO_OBRA_CONFIG en obra_config.py
        if (tipoRegistro === "d" && nivelBibliografico === "c") {
            return "coleccion_manuscrita";
        } else if (tipoRegistro === "d" && nivelBibliografico === "a") {
            return "obra_en_coleccion_manuscrita";
        } else if (tipoRegistro === "d" && nivelBibliografico === "m") {
            return "obra_manuscrita_individual";
        } else if (tipoRegistro === "c" && nivelBibliografico === "c") {
            return "coleccion_impresa";
        } else if (tipoRegistro === "c" && nivelBibliografico === "a") {
            return "obra_en_coleccion_impresa";
        } else if (tipoRegistro === "c" && nivelBibliografico === "m") {
            return "obra_impresa_individual";
        }
        return "desconocido";
    }

    /**
     * Guarda o actualiza el borrador
     */
    async function guardarBorrador(esAutoguardado = false) {
        try {
            const datos = serializeFormData();
            const tipoObra = getTipoObra();
            const obraObjetivoId = getObraObjetivoId();

            // En edición permitimos guardar aunque el tipo de obra aún no esté listo.
            if (!obraObjetivoId && (!tipoObra || tipoObra === "desconocido")) {
                if (!esAutoguardado) {
                    console.warn(
                        "No se puede guardar: tipo de obra no determinado"
                    );
                }
                return;
            }

            const pestanaActual =
                typeof currentTabIndex !== "undefined" ? currentTabIndex : 0;

            const payload = {
                tipo_obra: tipoObra,
                datos_formulario: datos,
                pestana_actual: pestanaActual,
            };

            if (obraObjetivoId) {
                payload.obra_objetivo_id = obraObjetivoId;
            }

            if (borradorId) {
                payload.borrador_id = borradorId;
            }

            const url = esAutoguardado
                ? API_URLS.autoguardar
                : API_URLS.guardar;

            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCsrfToken(),
                },
                body: JSON.stringify(payload),
            });

            const result = await response.json();

            if (result.success) {
                borradorId = result.borrador_id;
                hasUnsavedChanges = false;

                mostrarNotificacion(
                    esAutoguardado ? "Autoguardado" : result.message,
                    "success",
                    esAutoguardado ? 2000 : 3000
                );

                actualizarIndicadorGuardado();
            } else {
                console.error("Error guardando:", result.error);
                if (!esAutoguardado) {
                    mostrarNotificacion("Error al guardar", "error");
                }
            }
        } catch (error) {
            console.error("Error en guardarBorrador:", error);
            if (!esAutoguardado) {
                mostrarNotificacion("Error de conexión", "error");
            }
        }
    }

    /**
     * NUEVO: Carga un borrador con subcampos dinámicos
     */
    async function cargarBorrador(id) {
        try {
            mostrarNotificacion("Cargando borrador...", "info", 2000);

            const response = await fetch(API_URLS.obtener(id));
            const result = await response.json();

            if (result.success) {
                const borrador = result.borrador;

                const obraObjetivoId = getObraObjetivoId();

                // VALIDACIÓN: Verificar que el tipo de obra coincida (solo en creación)
                const tipoObraActual = getTipoObra();

                // Si aún no se ha determinado el tipo de obra, esperar (solo creación)
                if (
                    !obraObjetivoId &&
                    (!tipoObraActual || tipoObraActual === "desconocido")
                ) {
                    console.warn(
                        "Tipo de obra aún no determinado, reintentando..."
                    );
                    // Reintentar después de un momento
                    setTimeout(() => cargarBorrador(id), 500);
                    return;
                }

                if (!obraObjetivoId && borrador.tipo_obra !== tipoObraActual) {
                    console.error(
                        `ERROR: Tipo de obra no coincide. Borrador: ${borrador.tipo_obra}, Actual: ${tipoObraActual}`
                    );
                    mostrarNotificacion(
                        "Error: Este borrador es de otro tipo de obra.",
                        "error",
                        5000
                    );
                    return;
                }

                borradorId = borrador.id;
                const datos = borrador.datos_formulario;

                // 1. Preparar formsets principales
                await prepararFormsetsPrincipales(datos);

                // 2. Cargar campos simples y formsets
                await cargarCamposYFormsets(datos);

                // 3. NUEVO: Restaurar subcampos dinámicos
                await restaurarSubcamposDinamicos(datos);

                // 4. Navegar a pestaña guardada
                if (
                    typeof switchTab === "function" &&
                    borrador.pestana_actual
                ) {
                    setTimeout(() => switchTab(borrador.pestana_actual), 500);
                }

                mostrarNotificacion(
                    "Borrador recuperado exitosamente",
                    "success"
                );
                actualizarIndicadorGuardado();

                // Limpiar la variable de sesión para evitar recargas automáticas
                if (typeof BORRADOR_A_RECUPERAR !== "undefined") {
                    // Hacer una petición para limpiar la sesión
                    fetch("/catalogacion/api/borradores/limpiar-sesion/", {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": getCsrfToken(),
                        },
                    }).catch((err) =>
                        console.error("Error limpiando sesión:", err)
                    );
                }
            } else {
                mostrarNotificacion("Error al cargar borrador", "error");
            }
        } catch (error) {
            console.error("Error cargando borrador:", error);
            mostrarNotificacion("Error al cargar borrador", "error");
        }
    }

    /**
     * Prepara formsets principales (crea filas necesarias)
     */
    async function prepararFormsetsPrincipales(datos) {
        const formsets = datos._formsets || {};

        for (let prefix in formsets) {
            const indices = Object.keys(formsets[prefix]).filter(
                (k) => k !== "_total"
            );
            const totalNeeded =
                Math.max(...indices.map((i) => parseInt(i))) + 1;

            const container = document.querySelector(
                `[data-formset-prefix="${prefix}"]`
            );
            if (!container) continue;

            const currentRows = container.querySelectorAll(
                ".formset-row:not(.empty-form)"
            ).length;
            const rowsToAdd = totalNeeded - currentRows;

            if (rowsToAdd > 0) {
                const addButton = container.querySelector(".add-form-row");

                if (addButton) {
                    for (let i = 0; i < rowsToAdd; i++) {
                        addButton.click();
                        await new Promise((resolve) =>
                            setTimeout(resolve, 100)
                        );
                    }
                }
            }
        }
    }

    /**
     * Carga campos simples y formsets
     */
    async function cargarCamposYFormsets(datos) {
        const camposSimples = datos._campos_simples || {};

        for (let [key, value] of Object.entries(camposSimples)) {
            if (
                key.includes("-TOTAL_FORMS") ||
                key.includes("-INITIAL_FORMS")
            ) {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) input.value = value;
                continue;
            }

            if (Array.isArray(value)) {
                const inputs = form.querySelectorAll(`[name="${key}"]`);
                inputs.forEach((input, index) => {
                    if (index < value.length) {
                        establecerValorInput(input, value[index]);
                    }
                });
            } else {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) {
                    establecerValorInput(input, value);
                }
            }
        }
    }

    /**
     * NUEVO: Restaura subcampos dinámicos (idiomas, títulos, volúmenes, etc.)
     */
    async function restaurarSubcamposDinamicos(datos) {
        const subcampos = datos._subcampos_dinamicos || {};

        for (let key in subcampos) {
            const items = subcampos[key];
            if (!items || items.length === 0) continue;

            const firstItem = items[0];
            const { tipo, subtipo, parentIndex, campo } = firstItem;

            // Buscar el contenedor correcto según el tipo
            let container, addButton, template;

            if (tipo === "idioma" && subtipo === "lengua") {
                // Campo 041 - Idiomas
                container = document.querySelector(
                    `[data-idiomas-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-idioma-btn[data-lengua-index="${parentIndex}"]`
                );
                template = document.querySelector(".idioma-template");
            } else if (tipo === "titulo" && subtipo === "mencion") {
                // Campo 490 - Títulos de serie
                container = document.querySelector(
                    `[data-titulos-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-titulo-btn[data-mencion-index="${parentIndex}"]`
                );
                template = document.querySelector(".titulo-template-490");
            } else if (tipo === "volumen" && subtipo === "mencion") {
                // Campo 490 - Volúmenes
                container = document.querySelector(
                    `[data-volumenes-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-volumen-btn[data-mencion-index="${parentIndex}"]`
                );
                template = document.querySelector(".volumen-template-490");
            } else if (tipo === "texto" && subtipo === "biografico") {
                // Campo 545 - Textos biográficos
                container = document.querySelector(
                    `[data-textos-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-texto-btn[data-dato-index="${parentIndex}"]`
                );
                template = document.querySelector(".texto-template-545");
            } else if (tipo === "uri") {
                // Campo 545 - URIs
                container = document.querySelector(
                    `[data-uris-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-uri-btn[data-dato-index="${parentIndex}"]`
                );
                template = document.querySelector(".uri-template-545");
            } else if (tipo === "url" && subtipo === "disponible") {
                // Campo 856 - URLs
                container = document.querySelector(
                    `[data-urls-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-url-btn[data-disponible-index="${parentIndex}"]`
                );
                template = document.querySelector(".url-template-856");
            } else if (tipo === "texto" && subtipo === "disponible") {
                // Campo 856 - Textos de enlace
                container = document.querySelector(
                    `[data-textos-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-texto-btn[data-disponible-index="${parentIndex}"]`
                );
                template = document.querySelector(".texto-template-856");
            } else if (tipo === "numero" && subtipo === "enlace") {
                // Campos 773/774/787 - Números de obra (diferenciar por campo)
                // IMPORTANTE: Todos los campos están en la misma pestaña y comparten
                // los mismos valores de data-numeros-container, así que debemos buscar
                // dentro del .campo-marc específico que contiene el badge correcto

                // Buscar el contenedor .campo-marc que tenga el badge con el número de campo
                const campoMarc = Array.from(
                    document.querySelectorAll(".campo-marc")
                ).find((div) => {
                    const badge = div.querySelector(".badge-marc");
                    return badge && badge.textContent.trim() === campo;
                });

                if (campoMarc) {
                    container = campoMarc.querySelector(
                        `[data-numeros-container="${parentIndex}"]`
                    );
                    addButton = campoMarc.querySelector(
                        `.add-numero-btn[data-enlace-index="${parentIndex}"]`
                    );
                } else {
                    console.warn(
                        `⚠️ No se encontró .campo-marc con badge ${campo}`
                    );
                    container = null;
                    addButton = null;
                }

                // Seleccionar template correcto según el número de campo MARC
                if (campo === "773") {
                    template = document.querySelector(".numero-template");
                } else if (campo === "774") {
                    template = document.querySelector(".numero-template-774");
                } else if (campo === "787") {
                    template = document.querySelector(".numero-template-787");
                }
            } else if (tipo === "estanteria" && subtipo === "ubicacion") {
                // Campo 852 - Estanterías
                container = document.querySelector(
                    `[data-estanterias-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-estanteria-btn[data-ubicacion-index="${parentIndex}"]`
                );
                template = document.querySelector(".estanteria-template-852");
            } else if (tipo === "lugar" && subtipo === "produccion") {
                // Campo 264 - Lugares de producción ($a)
                container = document.querySelector(
                    `[data-lugares-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-lugar-btn[data-produccion-index="${parentIndex}"]`
                );
            } else if (tipo === "entidad" && subtipo === "produccion") {
                // Campo 264 - Entidades productoras ($b)
                container = document.querySelector(
                    `[data-entidades-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-entidad-btn[data-produccion-index="${parentIndex}"]`
                );
            } else if (tipo === "fecha" && subtipo === "produccion") {
                // Campo 264 - Fechas de producción ($c)
                container = document.querySelector(
                    `[data-fechas-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-fecha-btn[data-produccion-index="${parentIndex}"]`
                );
            } else if (tipo === "medio" && subtipo === "interpretacion") {
                // Campo 382 - Medios de interpretación ($a)
                container = document.querySelector(
                    `[data-medios-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-medio-btn[data-medio-index="${parentIndex}"]`
                );
            } else if (tipo === "termino" && subtipo === "asociado") {
                // Campo 700 - Términos asociados ($c)
                container = document.querySelector(
                    `[data-terminos-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-termino-btn[data-nombre-index="${parentIndex}"]`
                );
            } else if (tipo === "funcion" && subtipo === "700") {
                // Campo 700 - Funciones ($e)
                container = document.querySelector(
                    `[data-funciones-container="${parentIndex}"]`
                );
                addButton = document.querySelector(
                    `.add-funcion-btn[data-nombre-index="${parentIndex}"]`
                );
            }

            if (!container || !addButton) {
                console.warn(`⚠️ No se encontró contenedor para ${key}`);
                continue;
            }

            // Crear y llenar los subcampos
            for (let item of items) {
                addButton.click();
                await new Promise((resolve) => setTimeout(resolve, 50));

                // Buscar el último input/select/textarea creado
                const lastRow = container.querySelector(
                    ":scope > div:last-child, :scope > .idioma-form-row:last-child, :scope > .titulo-form-row:last-child, :scope > .volumen-form-row:last-child, :scope > .texto-form-row:last-child, :scope > .uri-form-row:last-child, :scope > .url-form-row:last-child, :scope > .numero-form-row:last-child, :scope > .estanteria-form-row:last-child, :scope > .lugar-form-row:last-child, :scope > .entidad-form-row:last-child, :scope > .fecha-form-row:last-child, :scope > .medio-form-row:last-child, :scope > .termino-form-row:last-child, :scope > .funcion-form-row:last-child"
                );

                if (lastRow) {
                    const input = lastRow.querySelector(
                        "input, select, textarea"
                    );
                    if (input) {
                        if (input.tagName === "SELECT") {
                            input.value = item.value;
                            if ($(input).data("select2")) {
                                $(input).val(item.value).trigger("change");
                            }
                        } else {
                            input.value = item.value;
                        }
                    }
                }
            }
        }
    }

    /**
     * Establece el valor de un input
     */
    function establecerValorInput(input, value) {
        if (input.type === "checkbox") {
            input.checked =
                value === "on" || value === true || value === "true";
        } else if (input.type === "radio") {
            if (input.value === value) input.checked = true;
        } else {
            input.value = value || "";
            if ($(input).data("select2")) {
                $(input).val(value).trigger("change");
            }
        }
        input.dispatchEvent(new Event("change", { bubbles: true }));
    }

    /**
     * Limpia completamente el formulario
     */
    function limpiarFormularioCompleto() {
        const camposExcluidos = [
            "csrfmiddlewaretoken",
            "tipo_registro",
            "nivel_bibliografico",
        ];

        // Limpiar inputs normales
        form.querySelectorAll(
            'input[type="text"], input[type="number"], textarea, select'
        ).forEach((input) => {
            if (!camposExcluidos.includes(input.name)) {
                input.value = "";
                if ($(input).data("select2")) {
                    $(input).val(null).trigger("change");
                }
            }
        });

        // Limpiar checkboxes y radios
        form.querySelectorAll(
            'input[type="checkbox"], input[type="radio"]'
        ).forEach((input) => {
            input.checked = false;
        });

        // Resetear formsets a 1 fila vacía
        form.querySelectorAll('input[name$="-TOTAL_FORMS"]').forEach(
            (totalInput) => {
                totalInput.value = "1";

                const container = totalInput.closest(".formset-container");
                if (container) {
                    const rows = container.querySelectorAll(
                        ".formset-row:not(.empty-form)"
                    );
                    rows.forEach((row, index) => {
                        if (index > 0) {
                            row.remove();
                        } else {
                            // Limpiar primera fila completamente
                            row.querySelectorAll(
                                "input, select, textarea"
                            ).forEach((field) => {
                                if (
                                    field.type === "checkbox" ||
                                    field.type === "radio"
                                ) {
                                    field.checked = false;
                                } else {
                                    field.value = "";
                                }
                            });

                            // Limpiar subcampos dentro de la fila
                            row.querySelectorAll(
                                "[data-idiomas-container], [data-titulos-container], [data-volumenes-container], [data-textos-container], [data-uris-container], [data-urls-container], [data-numeros-container], [data-estanterias-container], [data-lugares-container], [data-entidades-container], [data-fechas-container], [data-medios-container], [data-terminos-container], [data-funciones-container]"
                            ).forEach((subContainer) => {
                                subContainer.innerHTML = "";
                            });
                        }
                    });
                }
            }
        );

        if (typeof switchTab === "function") {
            switchTab(0);
        }

        borradorId = null;
        hasUnsavedChanges = false;
        actualizarIndicadorGuardado();

        mostrarNotificacion("Formulario limpiado completamente", "info");
    }

    /**
     * Elimina un borrador
     */
    async function eliminarBorrador(id) {
        try {
            const response = await fetch(API_URLS.eliminar(id), {
                method: "POST",
                headers: { "X-CSRFToken": getCsrfToken() },
            });

            const result = await response.json();
            if (result.success && id === borradorId) {
                borradorId = null;
            }
        } catch (error) {
            console.error("Error eliminando:", error);
        }
    }

    /**
     * Notificación toast
     */
    function mostrarNotificacion(mensaje, tipo = "info", duracion = 3000) {
        const notif = document.createElement("div");
        notif.textContent = mensaje;
        notif.style.cssText = `
            position: fixed; top: 20px; right: 20px;
            padding: 12px 20px; border-radius: 4px;
            color: white; font-size: 14px; font-weight: 500;
            z-index: 10000; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;

        const colores = {
            success: "#27AE60",
            error: "#E74C3C",
            info: "#3498DB",
        };
        notif.style.backgroundColor = colores[tipo] || colores.info;

        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), duracion);
    }

    /**
     * Indicador de guardado
     */
    function actualizarIndicadorGuardado() {
        let indicador = document.getElementById("save-indicator");

        if (!indicador) {
            indicador = document.createElement("div");
            indicador.id = "save-indicator";
            indicador.style.cssText = `
                position: fixed; bottom: 20px; left: 20px;
                padding: 8px 16px; border-radius: 20px;
                font-size: 12px; font-weight: 500; z-index: 9999;
                display: flex; align-items: center; gap: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            `;
            document.body.appendChild(indicador);
        }

        if (hasUnsavedChanges) {
            indicador.style.backgroundColor = "#F39C12";
            indicador.style.color = "white";
            indicador.innerHTML = "<span>●</span> Cambios sin guardar";
        } else if (borradorId) {
            indicador.style.backgroundColor = "#27AE60";
            indicador.style.color = "white";
            indicador.innerHTML = "<span>✓</span> Guardado";
        }
    }

    /**
     * Detecta cambios
     */
    function onFormChange() {
        hasUnsavedChanges = true;
        actualizarIndicadorGuardado();

        if (changeTimer) clearTimeout(changeTimer);
        changeTimer = setTimeout(() => guardarBorrador(true), MIN_CHANGE_DELAY);
    }

    /**
     * Autoguardado periódico
     */
    function iniciarAutoguardado() {
        if (autoSaveTimer) clearInterval(autoSaveTimer);

        autoSaveTimer = setInterval(() => {
            if (borradorId && hasUnsavedChanges) {
                guardarBorrador(true);
            }
        }, AUTOSAVE_INTERVAL);
    }

    /**
     * Prevenir pérdida de datos
     */
    window.addEventListener("beforeunload", (e) => {
        if (hasUnsavedChanges) {
            e.preventDefault();
            e.returnValue = "";
        }
    });

    /**
     * Eliminar borrador al publicar
     */
    form.addEventListener("submit", (e) => {
        console.log("🗑️ [BORRADOR-SYSTEM] Listener de submit activado");
        console.log("   Submitter:", e.submitter);
        console.log("   Submitter value:", e.submitter?.value);
        console.log("   BorradorId actual:", borradorId);

        if (e.submitter?.value === "publish" && borradorId) {
            console.log("   ✅ Eliminando borrador:", borradorId);
            eliminarBorrador(borradorId);
        } else {
            console.log(
                "   ℹ️ No se elimina borrador (no es publish o no hay borradorId)"
            );
        }
    });

    /**
     * Inicialización
     */
    function init() {
        // Esperar a que los campos tipo_registro y nivel_bibliografico estén disponibles
        const esperarFormularioListo = () => {
            const tipoRegistro = document.getElementById("id_tipo_registro");
            const nivelBibliografico = document.getElementById(
                "id_nivel_bibliografico"
            );

            const obraObjetivoId = getObraObjetivoId();

            // En creación, esperamos a tipo_registro/nivel_bibliografico para poder identificar tipo_obra.
            // En edición, podemos continuar aunque aún no estén listos.
            if (!obraObjetivoId && (!tipoRegistro || !nivelBibliografico)) {
                setTimeout(esperarFormularioListo, 100);
                return;
            }

            // Formulario listo, proceder con la inicialización
            // Si hay un borrador específico a recuperar (desde lista de borradores con botón "Continuar")
            if (
                typeof BORRADOR_A_RECUPERAR !== "undefined" &&
                BORRADOR_A_RECUPERAR !== null
            ) {
                // Esperar un poco más para asegurar que todo está cargado
                setTimeout(() => cargarBorrador(BORRADOR_A_RECUPERAR), 300);
            }

            // En edición: si existe un borrador activo ligado a esta obra, cargarlo automáticamente
            if (obraObjetivoId) {
                fetch(API_URLS.obtenerUltimoPorObra(obraObjetivoId))
                    .then((r) => r.json())
                    .then((res) => {
                        if (
                            res &&
                            res.success &&
                            res.tiene_borrador &&
                            res.borrador &&
                            res.borrador.id
                        ) {
                            setTimeout(
                                () => cargarBorrador(res.borrador.id),
                                300
                            );
                        }
                    })
                    .catch((err) =>
                        console.error(
                            "Error consultando borrador de edición:",
                            err
                        )
                    );
            }

            iniciarAutoguardado();

            form.addEventListener("input", onFormChange);
            form.addEventListener("change", onFormChange);
        };

        esperarFormularioListo();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }

    window.BorradorSystem = {
        guardar: () => guardarBorrador(false),
        cargar: cargarBorrador,
        eliminar: eliminarBorrador,
    };
})();
