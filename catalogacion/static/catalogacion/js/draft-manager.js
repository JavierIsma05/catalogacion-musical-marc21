/**
 * =============================================================================
 * DRAFT MANAGER - Sistema de Borradores v2.0
 * =============================================================================
 *
 * FILOSOFÍA:
 * Este sistema NO intenta interpretar la estructura del formulario.
 * En cambio, trabaja con SNAPSHOTS del estado visual del DOM.
 *
 * SERIALIZACIÓN:
 * - Captura la estructura actual del formulario (cuántas filas, qué valores)
 * - Guarda cada formset con sus filas en orden posicional
 * - Los subcampos se guardan como listas de valores por contenedor
 *
 * RESTAURACIÓN:
 * - Primero reconstruye la estructura (crear filas necesarias)
 * - Luego llena los valores en orden
 * - Usa los botones existentes para agregar filas (click programático)
 *
 * VENTAJAS:
 * - No depende de patterns de nombres complejos
 * - Funciona aunque cambien los timestamps de los inputs
 * - Es predecible: lo que guardas es lo que recuperas
 *
 * =============================================================================
 */

(function () {
    "use strict";

    // =========================================================================
    // CONFIGURACIÓN
    // =========================================================================

    const CONFIG = {
        AUTOSAVE_INTERVAL: 60000, // Autoguardado cada 60s
        CHANGE_DEBOUNCE: 3000, // Esperar 3s después del último cambio
        ROW_ANIMATION_DELAY: 80, // Delay entre crear filas
        DEBUG: false, // Logs de depuración
    };

    const URLS = {
        save: "/catalogacion/api/borradores/guardar/",
        autoSave: "/catalogacion/api/borradores/autoguardar/",
        get: (id) => `/catalogacion/api/borradores/${id}/`,
        getByObra: (obraId) =>
            `/catalogacion/api/borradores/obra/${obraId}/ultimo/`,
        delete: (id) => `/catalogacion/api/borradores/${id}/eliminar/`,
        clearSession: "/catalogacion/api/borradores/limpiar-sesion/",
        searchObras: "/catalogacion/api/buscar-obras/",
    };

    // =========================================================================
    // UTILIDADES
    // =========================================================================

    const Utils = {
        getCsrf() {
            return (
                document.querySelector('[name="csrfmiddlewaretoken"]')?.value ||
                ""
            );
        },

        wait(ms) {
            return new Promise((resolve) => setTimeout(resolve, ms));
        },

        log(...args) {
            if (CONFIG.DEBUG) console.log("[DraftManager]", ...args);
        },

        /**
         * Obtiene el tipo de obra basado en tipo_registro y nivel_bibliografico
         */
        getTipoObra() {
            const tipoReg = document.getElementById("id_tipo_registro")?.value;
            const nivelBib = document.getElementById(
                "id_nivel_bibliografico"
            )?.value;

            if (!tipoReg || !nivelBib) return null;

            const tipos = {
                d_c: "coleccion_manuscrita",
                d_a: "obra_en_coleccion_manuscrita",
                d_m: "obra_manuscrita_individual",
                c_c: "coleccion_impresa",
                c_a: "obra_en_coleccion_impresa",
                c_m: "obra_impresa_individual",
            };

            return tipos[`${tipoReg}_${nivelBib}`] || null;
        },

        /**
         * ID de obra en modo edición (desde URL)
         */
        getObraId() {
            const match = location.pathname.match(/\/obras\/(\d+)\/editar\/?$/);
            return match ? parseInt(match[1], 10) : null;
        },
    };

    // =========================================================================
    // SERIALIZER - Captura el estado del formulario
    // =========================================================================

    const Serializer = {
        /**
         * Serializa TODO el formulario a un objeto JSON
         * Estructura resultante:
         * {
         *   version: 2,
         *   campos: { "name": "value" | ["val1", "val2"] },
         *   formsets: {
         *     "prefix": [
         *       { campos: {field: value}, subcampos: {tipo: [val1, val2]} },
         *       ...
         *     ]
         *   },
         *   meta: { timestamp, tipoObra, pestana }
         * }
         */
        serialize(form) {
            const data = {
                version: 2,
                campos: {},
                formsets: {},
                subcamposGlobales: {}, // Subcampos fuera de formsets (ej: 100 $e)
                meta: {
                    timestamp: Date.now(),
                    tipoObra: Utils.getTipoObra(),
                    pestana:
                        typeof currentTabIndex !== "undefined"
                            ? currentTabIndex
                            : 0,
                },
            };

            // 1. Serializar campos simples (no pertenecen a formsets)
            this._serializeCamposSimples(form, data);

            // 2. Serializar cada formset
            form.querySelectorAll(
                ".formset-container[data-formset-prefix]"
            ).forEach((container) => {
                const prefix = container.dataset.formsetPrefix;
                data.formsets[prefix] = this._serializeFormset(
                    container,
                    prefix
                );
            });

            // 3. Serializar subcampos globales (fuera de formsets)
            this._serializeSubcamposGlobales(form, data);

            Utils.log("Serializado:", data);
            return data;
        },

        /**
         * Serializa subcampos repetibles que están FUERA de formset-rows
         * Incluye subcampos globales como 100 $e que tienen su propio formset-container
         * pero usan estructura de subcampo-row
         */
        _serializeSubcamposGlobales(form, data) {
            // Buscar contenedores de subcampos que NO están dentro de un formset-row
            form.querySelectorAll("[data-borrador-container]").forEach(
                (container) => {
                    // Verificar que NO esté dentro de un formset-row
                    const formsetRow = container.closest(".formset-row");
                    if (formsetRow) return; // Ignorar, ya se procesa en _serializeFormset como subcampo

                    const tipo = container.dataset.borradorContainer;
                    const values = [];

                    container
                        .querySelectorAll(
                            ".subcampo-row:not(.d-none):not([class*='template'])"
                        )
                        .forEach((subRow) => {
                            // Ignorar filas ocultas
                            if (subRow.style.display === "none") return;

                            const input = subRow.querySelector(
                                "input, select, textarea"
                            );
                            if (input) {
                                const val = input.value?.trim();
                                if (val) values.push(val);
                            }
                        });

                    if (values.length > 0) {
                        data.subcamposGlobales[tipo] = values;
                    }
                }
            );
        },

        /**
         * Serializa campos que NO pertenecen a formsets
         */
        _serializeCamposSimples(form, data) {
            const formData = new FormData(form);
            const formsetPrefixes = new Set();

            // Identificar prefijos de formsets
            form.querySelectorAll(
                ".formset-container[data-formset-prefix]"
            ).forEach((c) => {
                formsetPrefixes.add(c.dataset.formsetPrefix);
            });

            for (const [name, value] of formData.entries()) {
                // Ignorar campos de management forms y formsets
                if (
                    name.includes("-TOTAL_FORMS") ||
                    name.includes("-INITIAL_FORMS")
                )
                    continue;
                if (
                    name.includes("-MIN_NUM_FORMS") ||
                    name.includes("-MAX_NUM_FORMS")
                )
                    continue;

                // Ignorar si es parte de un formset (pattern: prefix-N-campo)
                const isFormsetField = Array.from(formsetPrefixes).some((p) =>
                    new RegExp(`^${p}-\\d+-`).test(name)
                );
                if (isFormsetField) continue;

                // Ignorar subcampos dinámicos (tienen formato tipo_subtipo_index_timestamp)
                if (/^\w+_\w+_\d+_\d+$/.test(name)) continue;
                if (/^\w+_\w+_\w+_\d+_\d+$/.test(name)) continue;

                // Guardar campo simple
                if (data.campos.hasOwnProperty(name)) {
                    if (!Array.isArray(data.campos[name])) {
                        data.campos[name] = [data.campos[name]];
                    }
                    data.campos[name].push(value);
                } else {
                    data.campos[name] = value;
                }
            }

            // Checkboxes no marcados
            form.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
                if (!cb.checked && !data.campos.hasOwnProperty(cb.name)) {
                    // Verificar que no sea de formset
                    const isFormsetField = Array.from(formsetPrefixes).some(
                        (p) => new RegExp(`^${p}-\\d+-`).test(cb.name)
                    );
                    if (!isFormsetField) {
                        data.campos[cb.name] = "";
                    }
                }
            });
        },

        /**
         * Serializa un formset completo con sus filas y subcampos
         */
        _serializeFormset(container, prefix) {
            const rows = [];

            // Buscar filas del formset (.formset-row)
            let formsetRows = container.querySelectorAll(
                ".formset-row:not(.empty-form)"
            );

            // Si no hay .formset-row, buscar en contenedor de subcampos (ej: 100e)
            if (formsetRows.length === 0) {
                const subcampoContainer = container.querySelector(
                    "[data-borrador-container]"
                );
                if (subcampoContainer) {
                    formsetRows = subcampoContainer.querySelectorAll(
                        ".subcampo-row:not(.d-none):not([class*='template'])"
                    );
                }
            }

            formsetRows.forEach((row) => {
                // Ignorar filas ocultas (marcadas para eliminar)
                if (row.style.display === "none") return;

                // Ignorar filas marcadas para eliminar
                const deleteCheckbox = row.querySelector(
                    'input[name*="-DELETE"]'
                );
                if (deleteCheckbox?.checked) return;

                const rowData = {
                    campos: {},
                    subcampos: {},
                };

                // Campos del formset (pattern: prefix-index-field)
                row.querySelectorAll("input, select, textarea").forEach(
                    (input) => {
                        const match = input.name?.match(
                            new RegExp(`^${prefix}-(\\d+)-(.+)$`)
                        );
                        if (match) {
                            const field = match[2];
                            if (field !== "DELETE" && field !== "id") {
                                rowData.campos[field] =
                                    this._getInputValue(input);
                            }
                        }
                    }
                );

                // Subcampos repetibles dentro de esta fila
                row.querySelectorAll("[data-borrador-container]").forEach(
                    (subContainer) => {
                        const tipo = subContainer.dataset.borradorContainer;
                        const values = [];

                        subContainer
                            .querySelectorAll(".subcampo-row:not(.d-none)")
                            .forEach((subRow) => {
                                const input = subRow.querySelector(
                                    "input, select, textarea"
                                );
                                if (input) {
                                    const val = input.value?.trim();
                                    if (val) values.push(val);
                                }
                            });

                        if (values.length > 0) {
                            rowData.subcampos[tipo] = values;
                        }
                    }
                );

                // Solo guardar si tiene datos significativos
                // Ignorar filas que solo tienen selects con valor por defecto o campos vacíos
                const hasRealData = this._rowHasRealData(row, rowData);

                if (hasRealData) {
                    rows.push(rowData);
                }
            });

            return rows;
        },

        /**
         * Verifica si una fila tiene datos reales (no solo valores por defecto)
         */
        _rowHasRealData(row, rowData) {
            // Verificar subcampos primero
            if (Object.keys(rowData.subcampos).length > 0) {
                return true;
            }

            // Verificar campos - ignorar selects con valor por defecto
            for (const [field, value] of Object.entries(rowData.campos)) {
                if (!value || !String(value).trim()) continue;

                // Buscar el input correspondiente
                const input = row.querySelector(`[name$="-${field}"]`);

                if (input?.tagName === "SELECT") {
                    // Para selects, verificar si es el valor por defecto
                    const options = input.querySelectorAll("option");
                    const firstOption = options[0];

                    let defaultValue = "";
                    if (firstOption) {
                        if (!firstOption.value || firstOption.value === "") {
                            defaultValue = "";
                        } else {
                            const selectedDefault =
                                input.querySelector("option[selected]");
                            defaultValue = selectedDefault
                                ? selectedDefault.value
                                : firstOption.value;
                        }
                    }

                    if (value === defaultValue) {
                        continue; // Es valor por defecto, ignorar
                    }
                }

                // Si llegamos aquí, hay un valor real
                return true;
            }

            return false;
        },

        _getInputValue(input) {
            if (input.type === "checkbox") {
                return input.checked ? "on" : "";
            }
            if (input.type === "radio") {
                return input.checked ? input.value : "";
            }
            return input.value || "";
        },
    };

    // =========================================================================
    // RESTORER - Reconstruye el formulario desde los datos guardados
    // =========================================================================

    const Restorer = {
        /**
         * Restaura el formulario desde los datos del borrador
         */
        async restore(form, data) {
            if (!data) return;

            Utils.log("Restaurando datos:", data);

            // Normalizar datos de versiones anteriores
            const normalized = this._normalize(data);

            // 1. Restaurar campos simples
            this._restoreCamposSimples(form, normalized.campos);

            // 2. Restaurar formsets (crear filas + llenar)
            await this._restoreFormsets(form, normalized.formsets);

            // 3. Restaurar subcampos globales (fuera de formsets)
            await this._restoreSubcamposGlobales(
                form,
                normalized.subcamposGlobales || {}
            );

            // 4. Rehidratar campos especiales (enlaces a obras)
            await this._rehydrateObraLinks(form);

            Utils.log("Restauración completada");
        },

        /**
         * Convierte formato v1 a v2 si es necesario
         */
        _normalize(data) {
            // Ya es v2
            if (data.version === 2 && data.campos && data.formsets) {
                return {
                    ...data,
                    subcamposGlobales: data.subcamposGlobales || {},
                };
            }

            // Convertir desde v1 (formato antiguo)
            const result = {
                version: 2,
                campos: {},
                formsets: {},
                subcamposGlobales: {},
                meta: data.meta || {},
            };

            // Campos simples antiguos
            const oldCampos = data._campos_simples || data.campos || {};
            for (const [name, value] of Object.entries(oldCampos)) {
                // Filtrar campos de formset
                if (!/^[a-z_]+-\d+-/.test(name)) {
                    result.campos[name] = value;
                }
            }

            // Formsets antiguos: { prefix: { "0": {campo: val}, "1": {...} } }
            const oldFormsets = data._formsets || {};
            const oldSubcampos =
                data._subcampos_dinamicos || data.subcampos || {};

            for (const [prefix, indexedData] of Object.entries(oldFormsets)) {
                result.formsets[prefix] = [];

                const indices = Object.keys(indexedData)
                    .filter((k) => k !== "_total" && !isNaN(parseInt(k)))
                    .map((k) => parseInt(k))
                    .sort((a, b) => a - b);

                indices.forEach((idx, newIdx) => {
                    const oldRow = indexedData[String(idx)] || {};
                    const rowData = { campos: {}, subcampos: {} };

                    // Copiar campos
                    for (const [field, val] of Object.entries(oldRow)) {
                        if (field !== "id" && field !== "DELETE") {
                            rowData.campos[field] = val;
                        }
                    }

                    // Buscar subcampos que pertenezcan a este índice
                    for (const [key, items] of Object.entries(oldSubcampos)) {
                        if (!items?.length) continue;

                        // Extraer parentIndex del key
                        const first = items[0];
                        if (first.parentIndex === idx) {
                            const tipo = `${first.tipo}_${first.subtipo}`;
                            rowData.subcampos[tipo] = items
                                .filter((it) => it.value?.trim())
                                .map((it) => it.value);
                        }
                    }

                    result.formsets[prefix].push(rowData);
                });
            }

            return result;
        },

        /**
         * Restaura campos simples
         */
        _restoreCamposSimples(form, campos) {
            for (const [name, value] of Object.entries(campos)) {
                const inputs = form.querySelectorAll(`[name="${name}"]`);
                if (!inputs.length) continue;

                if (Array.isArray(value)) {
                    inputs.forEach((input, i) => {
                        if (i < value.length) {
                            this._setInputValue(input, value[i]);
                        }
                    });
                } else {
                    inputs.forEach((input) =>
                        this._setInputValue(input, value)
                    );
                }
            }
        },

        /**
         * Restaura todos los formsets
         */
        async _restoreFormsets(form, formsets) {
            for (const [prefix, rows] of Object.entries(formsets)) {
                if (!rows.length) continue;

                const container = form.querySelector(
                    `[data-formset-prefix="${prefix}"]`
                );
                if (!container) {
                    Utils.log(`Formset no encontrado: ${prefix}`);
                    continue;
                }

                // Detectar si es formset tipo subcampo (100e)
                const subcampoContainer = container.querySelector(
                    "[data-borrador-container]"
                );
                const isSubcampoFormset =
                    subcampoContainer &&
                    !container.querySelector(".formset-row:not(.empty-form)");

                // Contar filas existentes (no ocultas)
                let existingRows;
                if (isSubcampoFormset) {
                    existingRows = subcampoContainer.querySelectorAll(
                        ".subcampo-row:not(.d-none):not([class*='template'])"
                    );
                } else {
                    existingRows = container.querySelectorAll(
                        ".formset-row:not(.empty-form)"
                    );
                }
                let currentCount = Array.from(existingRows).filter(
                    (r) =>
                        r.style.display !== "none" &&
                        !r.classList.contains("d-none")
                ).length;

                // Crear filas adicionales si es necesario
                while (currentCount < rows.length) {
                    const added = await this._addFormsetRow(prefix, container, {
                        isSubcampoFormset,
                        subcampoContainer,
                    });
                    if (!added) break;
                    currentCount++;
                    await Utils.wait(CONFIG.ROW_ANIMATION_DELAY);
                }

                // Obtener todas las filas visibles
                let allRows;
                if (isSubcampoFormset) {
                    allRows = Array.from(
                        subcampoContainer.querySelectorAll(
                            ".subcampo-row:not(.d-none):not([class*='template'])"
                        )
                    ).filter((r) => r.style.display !== "none");
                } else {
                    allRows = Array.from(
                        container.querySelectorAll(
                            ".formset-row:not(.empty-form)"
                        )
                    ).filter((r) => r.style.display !== "none");
                }

                // Llenar cada fila
                for (let i = 0; i < rows.length && i < allRows.length; i++) {
                    await this._restoreFormsetRow(
                        allRows[i],
                        prefix,
                        i,
                        rows[i]
                    );
                }
            }
        },

        /**
         * Agrega una fila al formset
         */
        async _addFormsetRow(prefix, container, options = {}) {
            const isSubcampoFormset = !!options.isSubcampoFormset;
            const subcampoContainer = options.subcampoContainer || null;

            const countRows = () => {
                if (isSubcampoFormset) {
                    const target = subcampoContainer || container;
                    return Array.from(
                        target.querySelectorAll(
                            ".subcampo-row:not(.d-none):not([class*='template'])"
                        )
                    ).filter((r) => r.style.display !== "none").length;
                }

                return Array.from(
                    container.querySelectorAll(".formset-row:not(.empty-form)")
                ).filter((r) => r.style.display !== "none").length;
            };

            const clickAndVerify = async (btnOrFn) => {
                const before = countRows();
                if (typeof btnOrFn === "function") {
                    btnOrFn();
                } else if (btnOrFn?.click) {
                    btnOrFn.click();
                } else {
                    return false;
                }

                await Utils.wait(80);
                return countRows() > before;
            };

            // Método 1: Botón local específico del contenedor (ej: 100e)
            // Importante: NO usar .subcampo-add-btn para formsets normales (ej: 700),
            // porque esos botones agregan subfilas internas y no una fila del formset principal.
            const localSelector = isSubcampoFormset
                ? ".add-funcion-100e-btn, .add-form-row, .add-funcion-btn, .subcampo-add-btn"
                : ".add-funcion-100e-btn, .add-form-row, .add-funcion-btn";

            const localBtn = container.querySelector(localSelector);
            if (localBtn && (await clickAndVerify(localBtn))) {
                return true;
            }

            // Método 2: FormsetManager global
            if (window.FormsetManager?.addNewForm) {
                const added = await clickAndVerify(() => {
                    window.FormsetManager.addNewForm(prefix);
                });
                if (added) return true;
            }

            // Método 3: Botón en header
            const headerBtn = document.querySelector(
                `.campo-add-btn[data-formset-target="${prefix}"]`
            );
            if (headerBtn && (await clickAndVerify(headerBtn))) {
                return true;
            }

            Utils.log(`No se pudo agregar fila para: ${prefix}`);
            return false;
        },

        /**
         * Restaura una fila de formset con sus campos y subcampos
         */
        async _restoreFormsetRow(row, prefix, index, rowData) {
            // 1. Restaurar campos normales del formset
            for (const [field, value] of Object.entries(rowData.campos)) {
                // Buscar input con nombre exacto o aproximado
                let input = row.querySelector(
                    `[name="${prefix}-${index}-${field}"]`
                );

                // Si no se encuentra, buscar cualquier input que coincida con el campo
                if (!input) {
                    const regex = new RegExp(`^${prefix}-\\d+-${field}$`);
                    const inputs = row.querySelectorAll(
                        "input, select, textarea"
                    );
                    for (const inp of inputs) {
                        if (inp.name && regex.test(inp.name)) {
                            input = inp;
                            break;
                        }
                    }
                }

                if (input) {
                    this._setInputValue(input, value);
                }
            }

            // 2. Restaurar subcampos repetibles (ej: 264 tiene lugares, entidades, fechas)
            for (const [tipo, values] of Object.entries(
                rowData.subcampos || {}
            )) {
                await this._restoreSubcampos(row, tipo, index, values);
            }
        },

        /**
         * Restaura subcampos repetibles de una fila
         */
        async _restoreSubcampos(row, tipo, parentIndex, values) {
            if (!values?.length) return;

            // Buscar contenedor de subcampos
            const container = row.querySelector(
                `[data-borrador-container="${tipo}"]`
            );
            if (!container) {
                Utils.log(`Contenedor de subcampos no encontrado: ${tipo}`);
                return;
            }

            // Buscar botón de agregar
            const addButton = row.querySelector(
                `[data-borrador-add="${tipo}"]`
            );

            // Obtener filas de subcampos existentes
            let subRows = container.querySelectorAll(
                ".subcampo-row:not(.d-none)"
            );

            // Llenar valores
            for (let i = 0; i < values.length; i++) {
                if (i < subRows.length) {
                    // Usar fila existente
                    const input = subRows[i].querySelector(
                        "input, select, textarea"
                    );
                    if (input) {
                        this._setInputValue(input, values[i]);
                    }
                } else if (addButton) {
                    // Crear nueva fila
                    addButton.click();
                    await Utils.wait(30);

                    // Re-obtener filas
                    subRows = container.querySelectorAll(
                        ".subcampo-row:not(.d-none)"
                    );
                    const newRow = subRows[subRows.length - 1];
                    if (newRow) {
                        const input = newRow.querySelector(
                            "input, select, textarea"
                        );
                        if (input) {
                            this._setInputValue(input, values[i]);
                        }
                    }
                }
            }
        },

        /**
         * Restaura subcampos globales (fuera de formsets, ej: 382 $a, etc.)
         */
        async _restoreSubcamposGlobales(form, subcamposGlobales) {
            for (const [tipo, values] of Object.entries(subcamposGlobales)) {
                if (!values?.length) continue;

                // Buscar contenedor que NO esté dentro de un formset-row
                const containers = form.querySelectorAll(
                    `[data-borrador-container="${tipo}"]`
                );

                let container = null;
                for (const c of containers) {
                    if (!c.closest(".formset-row")) {
                        container = c;
                        break;
                    }
                }

                if (!container) {
                    Utils.log(`Contenedor global no encontrado: ${tipo}`);
                    continue;
                }

                // Buscar botón de agregar
                let addButton = container.querySelector(
                    `[data-borrador-add="${tipo}"]`
                );
                if (!addButton) {
                    addButton = container.querySelector(
                        ".subcampo-add-btn, .add-funcion-btn"
                    );
                }
                if (!addButton) {
                    const parent = container.closest(
                        ".col-full, .campo-grid, .subcampo-wrapper, .formset-container"
                    );
                    if (parent) {
                        addButton = parent.querySelector(
                            `[data-borrador-add="${tipo}"]`
                        );
                    }
                }

                // Obtener filas existentes (visibles)
                let subRows = Array.from(
                    container.querySelectorAll(
                        ".subcampo-row:not(.d-none):not([class*='template'])"
                    )
                ).filter((r) => r.style.display !== "none");

                // Llenar valores
                for (let i = 0; i < values.length; i++) {
                    if (i < subRows.length) {
                        const input = subRows[i].querySelector(
                            "input, select, textarea"
                        );
                        if (input) {
                            this._setInputValue(input, values[i]);
                        }
                    } else if (addButton) {
                        addButton.click();
                        await Utils.wait(100);

                        subRows = Array.from(
                            container.querySelectorAll(
                                ".subcampo-row:not(.d-none):not([class*='template'])"
                            )
                        ).filter((r) => r.style.display !== "none");

                        const newRow = subRows[subRows.length - 1];
                        if (newRow) {
                            const input = newRow.querySelector(
                                "input, select, textarea"
                            );
                            if (input) {
                                this._setInputValue(input, values[i]);
                            }
                        }
                    } else {
                        Utils.log(`No se pudo agregar subcampo para: ${tipo}`);
                    }
                }
            }
        },

        /**
         * Establece el valor de un input
         */
        _setInputValue(input, value) {
            if (input.type === "checkbox") {
                input.checked =
                    value === "on" || value === true || value === "true";
            } else if (input.type === "radio") {
                input.checked = input.value === value;
            } else if (input.tagName === "SELECT") {
                input.value = value || "";
                // Select2
                if (window.$ && $(input).data("select2")) {
                    $(input).val(value).trigger("change");
                }
            } else {
                input.value = value || "";
            }

            // Disparar eventos
            input.dispatchEvent(new Event("input", { bubbles: true }));
            input.dispatchEvent(new Event("change", { bubbles: true }));
        },

        /**
         * Rehidrata campos de enlaces a obras (773, 774, 787)
         * El hidden tiene el ID, el visible debe mostrar num_control
         */
        async _rehydrateObraLinks(form) {
            const hiddenInputs = form.querySelectorAll(
                'input.obra-relacionada-id-input[name^="w_"]'
            );
            if (!hiddenInputs.length) return;

            const cache = new Map();

            for (const hidden of hiddenInputs) {
                const obraId = hidden.value?.trim();
                if (!obraId) continue;

                const group = hidden.closest(".input-group");
                const visible = group?.querySelector(".numero-w-input");
                if (!visible) continue;

                // Buscar num_control
                if (!cache.has(obraId)) {
                    try {
                        const resp = await fetch(
                            `${URLS.searchObras}?id=${obraId}`
                        );
                        const data = await resp.json();
                        cache.set(
                            obraId,
                            data?.results?.[0]?.num_control || null
                        );
                    } catch {
                        cache.set(obraId, null);
                    }
                }

                const numControl = cache.get(obraId);
                if (numControl) {
                    visible.value = numControl;
                    visible.dispatchEvent(
                        new Event("input", { bubbles: true })
                    );
                }
            }
        },
    };

    // =========================================================================
    // UI - Notificaciones e indicadores
    // =========================================================================

    const UI = {
        notify(message, type = "info", duration = 3000) {
            const colors = {
                success: "#27AE60",
                error: "#E74C3C",
                info: "#3498DB",
                warning: "#F39C12",
            };

            const el = document.createElement("div");
            el.textContent = message;
            el.style.cssText = `
                position: fixed; top: 20px; right: 20px;
                padding: 12px 20px; border-radius: 6px;
                color: white; font-size: 14px; font-weight: 500;
                z-index: 10000; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                background: ${colors[type] || colors.info};
                animation: slideIn 0.3s ease;
            `;

            document.body.appendChild(el);
            setTimeout(() => {
                el.style.animation = "slideOut 0.3s ease";
                setTimeout(() => el.remove(), 300);
            }, duration);
        },

        updateSaveIndicator(state) {
            let indicator = document.getElementById("draft-indicator");

            if (!indicator) {
                indicator = document.createElement("div");
                indicator.id = "draft-indicator";
                indicator.style.cssText = `
                    position: fixed; bottom: 20px; left: 20px;
                    padding: 8px 16px; border-radius: 20px;
                    font-size: 12px; font-weight: 500; z-index: 9999;
                    display: flex; align-items: center; gap: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    transition: all 0.3s ease;
                `;
                document.body.appendChild(indicator);
            }

            if (state.hasChanges) {
                indicator.style.background = "#F39C12";
                indicator.style.color = "white";
                indicator.innerHTML = "<span>●</span> Cambios sin guardar";
            } else if (state.draftId) {
                indicator.style.background = "#27AE60";
                indicator.style.color = "white";
                indicator.innerHTML = "<span>✓</span> Borrador guardado";
            } else {
                indicator.style.display = "none";
            }
        },
    };

    // =========================================================================
    // API - Comunicación con el servidor
    // =========================================================================

    const API = {
        async save(data, isAuto = false) {
            try {
                const payload = {
                    tipo_obra: Utils.getTipoObra(),
                    datos_formulario: data,
                    pestana_actual: data.meta?.pestana || 0,
                };

                const obraId = Utils.getObraId();
                if (obraId) payload.obra_objetivo_id = obraId;
                if (DraftManager.state.draftId)
                    payload.borrador_id = DraftManager.state.draftId;

                const response = await fetch(
                    isAuto ? URLS.autoSave : URLS.save,
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": Utils.getCsrf(),
                        },
                        body: JSON.stringify(payload),
                    }
                );

                const result = await response.json();

                if (result.success) {
                    DraftManager.state.draftId = result.borrador_id;
                    DraftManager.state.hasChanges = false;
                    return result;
                } else {
                    throw new Error(result.error);
                }
            } catch (error) {
                Utils.log("Error guardando:", error);
                throw error;
            }
        },

        async load(id) {
            const response = await fetch(URLS.get(id));
            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error);
            }

            return result.borrador;
        },

        async loadByObra(obraId) {
            const response = await fetch(URLS.getByObra(obraId));
            const result = await response.json();

            if (result.success && result.tiene_borrador) {
                return result.borrador;
            }
            return null;
        },

        async delete(id) {
            const response = await fetch(URLS.delete(id), {
                method: "POST",
                headers: { "X-CSRFToken": Utils.getCsrf() },
            });
            return response.json();
        },
    };

    // =========================================================================
    // DRAFT MANAGER - Controlador principal
    // =========================================================================

    const DraftManager = {
        state: {
            draftId: null,
            hasChanges: false,
            autoSaveTimer: null,
            changeTimer: null,
            allowUnload: false,
        },

        form: null,

        /**
         * Inicializa el sistema
         */
        init() {
            this.form = document.getElementById("obra-form");
            if (!this.form) return;

            Utils.log("Inicializando DraftManager...");

            // Esperar a que el formulario esté listo
            this._waitForReady().then(() => {
                this._setupEventListeners();
                this._startAutoSave();
                this._checkForExistingDraft();
                this._installExitAlerts();
            });
        },

        /**
         * Espera a que tipo_registro y nivel_bibliografico estén definidos
         */
        _waitForReady() {
            return new Promise((resolve) => {
                const check = () => {
                    const obraId = Utils.getObraId();

                    // En edición, no necesitamos esperar
                    if (obraId) {
                        resolve();
                        return;
                    }

                    // En creación, esperar tipo de obra
                    const tipoObra = Utils.getTipoObra();
                    if (tipoObra) {
                        resolve();
                    } else {
                        setTimeout(check, 100);
                    }
                };
                check();
            });
        },

        /**
         * Configura listeners de cambios
         */
        _setupEventListeners() {
            const onChange = () => {
                this.state.hasChanges = true;
                UI.updateSaveIndicator(this.state);

                // Debounce para autoguardado
                if (this.state.changeTimer) {
                    clearTimeout(this.state.changeTimer);
                }
                this.state.changeTimer = setTimeout(() => {
                    this.save(true);
                }, CONFIG.CHANGE_DEBOUNCE);
            };

            this.form.addEventListener("input", onChange);
            this.form.addEventListener("change", onChange);

            // Eliminar borrador al publicar
            this.form.addEventListener("submit", (e) => {
                if (e.submitter?.value === "publish" && this.state.draftId) {
                    API.delete(this.state.draftId);
                }
            });
        },

        /**
         * Inicia autoguardado periódico
         */
        _startAutoSave() {
            this.state.autoSaveTimer = setInterval(() => {
                if (this.state.draftId && this.state.hasChanges) {
                    this.save(true);
                }
            }, CONFIG.AUTOSAVE_INTERVAL);
        },

        /**
         * Verifica si hay borrador existente para cargar
         */
        async _checkForExistingDraft() {
            // Desde variable de sesión (lista de borradores)
            if (
                typeof BORRADOR_A_RECUPERAR !== "undefined" &&
                BORRADOR_A_RECUPERAR
            ) {
                setTimeout(() => this.load(BORRADOR_A_RECUPERAR), 300);
                return;
            }

            // En edición: cargar borrador de la obra
            const obraId = Utils.getObraId();
            if (obraId) {
                const params = new URLSearchParams(location.search);
                const draftId = params.get("borrador");

                if (draftId && !isNaN(parseInt(draftId))) {
                    setTimeout(() => this.load(parseInt(draftId)), 300);
                } else {
                    const draft = await API.loadByObra(obraId);
                    if (draft?.id) {
                        setTimeout(() => this.load(draft.id), 300);
                    }
                }
            }
        },

        /**
         * Guarda el borrador
         */
        async save(isAuto = false) {
            try {
                const data = Serializer.serialize(this.form);
                const result = await API.save(data, isAuto);

                UI.updateSaveIndicator(this.state);
                UI.notify(
                    isAuto ? "Autoguardado" : "Borrador guardado",
                    "success",
                    isAuto ? 2000 : 3000
                );

                return result;
            } catch (error) {
                if (!isAuto) {
                    UI.notify("Error al guardar", "error");
                }
                throw error;
            }
        },

        /**
         * Carga un borrador
         */
        async load(id) {
            try {
                UI.notify("Cargando borrador...", "info", 2000);

                const draft = await API.load(id);
                const obraId = Utils.getObraId();
                const tipoObra = Utils.getTipoObra();

                // Validar tipo de obra en creación
                if (!obraId && draft.tipo_obra !== tipoObra) {
                    UI.notify(
                        "Este borrador es de otro tipo de obra",
                        "error",
                        5000
                    );
                    return;
                }

                this.state.draftId = draft.id;

                await Restorer.restore(this.form, draft.datos_formulario);

                // Navegar a pestaña guardada
                if (typeof switchTab === "function" && draft.pestana_actual) {
                    setTimeout(() => switchTab(draft.pestana_actual), 500);
                }

                UI.updateSaveIndicator(this.state);
                UI.notify("Borrador recuperado", "success");

                // Limpiar sesión
                fetch(URLS.clearSession, {
                    method: "POST",
                    headers: { "X-CSRFToken": Utils.getCsrf() },
                }).catch(() => {});
            } catch (error) {
                Utils.log("Error cargando:", error);
                UI.notify("Error al cargar borrador", "error");
            }
        },

        /**
         * Elimina un borrador
         */
        async delete(id) {
            try {
                await API.delete(id);
                if (id === this.state.draftId) {
                    this.state.draftId = null;
                }
            } catch (error) {
                Utils.log("Error eliminando:", error);
            }
        },

        /**
         * Instala alertas de salida
         */
        _installExitAlerts() {
            // Prevenir pérdida de datos
            window.addEventListener("beforeunload", (e) => {
                if (this.state.allowUnload) return;

                if (this.state.hasChanges || this.state.draftId) {
                    e.preventDefault();
                    e.returnValue = "";
                }
            });

            // Interceptar navegación
            const showExitAlert = async (action, onContinue) => {
                if (typeof Swal === "undefined") {
                    if (
                        confirm(
                            "Tu avance está guardado como borrador.\n\n¿Salir de todos modos?"
                        )
                    ) {
                        onContinue();
                    }
                    return;
                }

                const result = await Swal.fire({
                    icon: "info",
                    title: "Borrador guardado",
                    html: `
                        <div class="text-start">
                            <p>Tu avance ya está guardado como <strong>borrador</strong>.</p>
                            <ul>
                                <li>Para continuar luego, ve a <strong>Borradores</strong>.</li>
                                <li>Si ${action}, el formulario se reiniciará.</li>
                            </ul>
                        </div>
                    `,
                    showCancelButton: true,
                    showDenyButton: true,
                    confirmButtonText: "Ir a Borradores",
                    denyButtonText: "Continuar",
                    cancelButtonText: "Cancelar",
                    focusCancel: true,
                });

                if (result.isConfirmed) {
                    location.href = "/catalogacion/borradores/";
                } else if (result.isDenied) {
                    onContinue();
                }
            };

            // F5 / Ctrl+R
            window.addEventListener(
                "keydown",
                async (e) => {
                    const isReload =
                        e.key === "F5" ||
                        ((e.ctrlKey || e.metaKey) &&
                            e.key.toLowerCase() === "r");

                    if (!isReload || !this.state.draftId) return;

                    e.preventDefault();
                    e.stopPropagation();

                    await showExitAlert("recargas la página", () => {
                        this.state.allowUnload = true;
                        location.reload();
                    });
                },
                true
            );

            // Links internos
            document.addEventListener(
                "click",
                async (e) => {
                    const link = e.target.closest("a[href]");
                    if (!link) return;

                    const href = link.getAttribute("href");
                    if (
                        !href ||
                        href.startsWith("#") ||
                        href.startsWith("javascript:")
                    )
                        return;
                    if (
                        link.getAttribute("target") &&
                        link.getAttribute("target") !== "_self"
                    )
                        return;
                    if (link.hasAttribute("download")) return;
                    if (!this.state.draftId) return;

                    try {
                        const dest = new URL(href, location.href);
                        if (
                            dest.href.split("#")[0] ===
                            location.href.split("#")[0]
                        )
                            return;
                    } catch {
                        return;
                    }

                    e.preventDefault();
                    e.stopPropagation();

                    await showExitAlert("sales de la página", () => {
                        this.state.allowUnload = true;
                        location.href = href;
                    });
                },
                true
            );
        },
    };

    // =========================================================================
    // INICIALIZACIÓN
    // =========================================================================

    // Agregar estilos de animación
    const style = document.createElement("style");
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);

    // Iniciar cuando el DOM esté listo
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () =>
            DraftManager.init()
        );
    } else {
        DraftManager.init();
    }

    // Exponer API pública
    window.DraftManager = {
        save: () => DraftManager.save(false),
        load: (id) => DraftManager.load(id),
        delete: (id) => DraftManager.delete(id),
        getState: () => ({ ...DraftManager.state }),
    };
})();
