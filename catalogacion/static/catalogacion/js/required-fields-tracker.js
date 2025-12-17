/**
 * Sistema de seguimiento de campos obligatorios MARC21
 * Actualiza el sidebar de progreso en tiempo real
 */

(function () {
    "use strict";

    // Configuración de campos obligatorios por tipo de obra
    // Solo se incluyen campos editables por el usuario (040, 092, 100/130, 245, 340, 382)
    // Los campos 001, 005 y 008 son automáticos y no se rastrean
    const REQUIRED_FIELDS_CONFIG = {
        coleccion_manuscrita: [
            { id: "id_centro_catalogador", label: "040", tab: 6 },
            { id: "id_titulo_uniforme_texto", label: "130", tab: 0, hidden: true },
            { id: "id_titulo_principal", label: "245", tab: 0 },
            { id: "id_ms_imp", label: "340", tab: 1 },
            {
            id: "id_medios_382-0-solista", // ← FORMSET, no input
            label: "382",
            tab: 2,
            hidden: true,
            },
        ],
        obra_en_coleccion_manuscrita: [
            { id: "id_centro_catalogador", label: "040", tab: 6 },
            { id: "id_compositor", label: "100", tab: 0 },
            { id: "id_titulo_principal", label: "245", tab: 0 },
            { id: "id_ms_imp", label: "340", tab: 1 },
            {
                id: "id_medios_382-0-solista", // ← FORMSET, no input
                label: "382",
                tab: 2,
                hidden: true,
            },
        ],
        obra_manuscrita_individual: [
            { id: "id_centro_catalogador", label: "040", tab: 6 },
            { id: "id_compositor", label: "100", tab: 0 },
            { id: "id_titulo_principal", label: "245", tab: 0 },
            { id: "id_ms_imp", label: "340", tab: 1 },
            {
                id: "id_medios_382-0-solista", // ← FORMSET, no input
                label: "382",
                tab: 2,
                hidden: true,
            },
        ],

        coleccion_impresa: [
            { id: "id_centro_catalogador", label: "040", tab: 6 },
            { id: "id_compositor", label: "100", tab: 0 },
            { id: "id_titulo_principal", label: "245", tab: 0 },
            { id: "id_ms_imp", label: "340", tab: 1 },
            {
            id: "id_medios_382-0-solista", // ← FORMSET, no input
            label: "382",
            tab: 2,
            hidden: true,
        },
        ],
        obra_en_coleccion_impresa: [
            { id: "id_centro_catalogador", label: "040", tab: 6 },
            { id: "id_compositor", label: "100 - Compositor", tab: 0 },
            { id: "id_titulo_principal", label: "245", tab: 0 },
            { id: "id_ms_imp", label: "340", tab: 1 },
            {
                id: "id_medios_382-0-solista", // ← FORMSET, no input
                label: "382",
                tab: 2,
                hidden: true,
            },
        ],
        obra_impresa_individual: [
            { id: "id_centro_catalogador", label: "040", tab: 6 },
            { id: "id_compositor", label: "100 - Compositor", tab: 0 },
            { id: "id_titulo_principal", label: "245", tab: 0 },
            { id: "id_ms_imp", label: "340", tab: 1 },
            {
                id: "id_medios_382-0-solista", // ← FORMSET, no input
                label: "382",
                tab: 2,
                hidden: true,
            },
        ],
    };


    // Estado del tracker
    let tipoObra = null;
    let requiredFields = [];
    let fieldStates = {};

    /**
     * Inicializar el tracker
     */
    function init() {
        // Obtener tipo de obra de la sesión o del formulario
        tipoObra = getTipoObra();

        if (!tipoObra) {
            console.warn("No se pudo determinar el tipo de obra");
            return;
        }

        // Obtener configuración de campos obligatorios
        requiredFields = REQUIRED_FIELDS_CONFIG[tipoObra] || [];

        if (requiredFields.length === 0) {
            console.warn(
                "No hay campos obligatorios configurados para:",
                tipoObra
            );
            return;
        }

        // Inicializar estados
        initFieldStates();

        // Renderizar UI del sidebar
        renderProgressSidebar();

        // Configurar listeners
        setupFieldListeners();

        // Primera actualización
        updateProgress();
    }

    /**
     * Obtener tipo de obra actual
     */
    function getTipoObra() {
        // Intentar obtener del data attribute del body o del template
        const bodyTipo = document.body.getAttribute("data-tipo-obra");
        if (bodyTipo) return bodyTipo;

        // Intentar obtener de la URL
        const urlParams = new URLSearchParams(window.location.search);
        const urlTipo = urlParams.get("tipo");
        if (urlTipo) return urlTipo;

        // Intentar obtener del path
        const pathMatch = window.location.pathname.match(
            /\/crear-obra\/([^\/]+)/
        );
        if (pathMatch) return pathMatch[1];

        // Fallback: buscar en el contexto del template
        const tipoFromContext = window.TIPO_OBRA_ACTUAL;
        if (tipoFromContext) return tipoFromContext;

        return null;
    }

    /**
     * Inicializar estados de campos
     */
    function initFieldStates() {
        requiredFields.forEach((field) => {
            fieldStates[field.id] = {
                complete: false,
                field: field,
            };
        });
    }

    /**
     * Renderizar sidebar de progreso
     */
    function renderProgressSidebar() {
        const listContainer = document.getElementById("required-fields-list");
        if (!listContainer) return;

        listContainer.innerHTML = "";

        requiredFields.forEach((field) => {
            const li = document.createElement("li");
            li.className = "required-field-item incomplete";
            li.setAttribute("data-field-id", field.id);
            li.setAttribute("data-tab-index", field.tab);

            // Extraer solo el número antes del guión → ej: "040"
            const fieldCode = field.label.split(" - ")[0];

            // Tooltip con el label completo
            li.title = field.label;

            // Nuevo HTML reducido en pantalla
            li.innerHTML = `
                <div class="required-field-indicator"></div>
                <span class="required-field-code">${fieldCode}</span>
            `;


            // Click para navegar a la pestaña del campo
            li.addEventListener("click", () => {
                const tabIndex = field.tab;

                if (typeof switchTab === "function") {
                    switchTab(tabIndex);

                    // Le damos un tiempo para que la transición visual termine
                    setTimeout(() => {
                        const fieldElement = document.getElementById(field.id);

                        if (fieldElement) {
                            fieldElement.scrollIntoView({
                                behavior: "smooth",
                                block: "center",
                            });
                            fieldElement.focus({ preventScroll: true });
                        } else {
                            console.warn("⚠ No se encontró el input de campo:", field.id);
                        }
                    }, 350);
                }
            });


            listContainer.appendChild(li);
        });
    }

    /**
     * Configurar listeners en campos obligatorios
     */
    function setupFieldListeners() {
        requiredFields.forEach((field) => {
            if (field.special) {
                // Campos especiales como 382 que son formsets
                setupSpecialFieldListener(field);
            } else {
                // Campos normales
                const element = document.getElementById(field.id);
                if (element) {
                    // Input normal
                    element.addEventListener("input", () =>
                        checkField(field.id)
                    );
                    element.addEventListener("change", () =>
                        checkField(field.id)
                    );
                    element.addEventListener("blur", () =>
                        checkField(field.id)
                    );
                } else {
                    // Buscar en select2
                    const select2Element = document.querySelector(
                        `[name="${field.id.replace("id_", "")}"]`
                    );
                    if (select2Element) {
                        $(select2Element).on("change", () =>
                            checkField(field.id)
                        );
                    }
                }
            }
        });

        // Listener global para detectar cambios dinámicos
        document.addEventListener("input", debounce(updateProgress, 300));
        document.addEventListener("change", debounce(updateProgress, 300));
    }

    /**
     * Configurar listener para campos especiales (formsets)
     */
    function setupSpecialFieldListener(field) {
        if (field.id === "id_medio_interpretacion_382") {
            // Observar cambios en el formset de medios de interpretación
            const formsetContainer =
                document.querySelector('[id*="medios_382"]');
            if (formsetContainer) {
                // Usar MutationObserver para detectar cambios dinámicos
                const observer = new MutationObserver(() => {
                    checkField(field.id);
                });

                observer.observe(formsetContainer, {
                    childList: true,
                    subtree: true,
                });

                // También escuchar eventos de input en el contenedor
                formsetContainer.addEventListener("input", () =>
                    checkField(field.id)
                );
                formsetContainer.addEventListener("change", () =>
                    checkField(field.id)
                );
            }
        }
    }

    /**
     * Verificar si un campo está completo
     */
    function checkField(fieldId) {
        const field = requiredFields.find((f) => f.id === fieldId);
        if (!field) return false;

        let isComplete = false;

        if (field.special) {
            isComplete = checkSpecialField(field);
        } else {
            const element = document.getElementById(fieldId);
            if (element) {
                isComplete = element.value && element.value.trim() !== "";
            } else {
                // Buscar por name en caso de select2
                const elementByName = document.querySelector(
                    `[name="${fieldId.replace("id_", "")}"]`
                );
                if (elementByName) {
                    isComplete =
                        elementByName.value &&
                        elementByName.value.trim() !== "";
                }
            }
        }

        // Actualizar estado
        fieldStates[fieldId].complete = isComplete;

        // Actualizar UI del campo en la lista
        updateFieldItemUI(fieldId, isComplete);

        // NO llamar a updateProgress() aquí para evitar bucle infinito
        // updateProgress() se llama desde los event listeners de cambio

        return isComplete;
    }

    /**
     * Verificar campos especiales (como formsets)
     */
    function checkSpecialField(field) {
        if (field.id === "id_medio_interpretacion_382") {
            // Verificar si hay al menos un medio de interpretación con subcampo $a

            // Buscar inputs dinámicos de subcampos $a
            const medioInputs = document.querySelectorAll(
                '[id^="medio_interpretacion_382_"]'
            );

            // Verificar si alguno tiene valor
            for (let input of medioInputs) {
                if (input.value && input.value.trim() !== "") {
                    return true;
                }
            }

            // También verificar en el formset estándar
            const formsetForms = document.querySelectorAll(
                '[id*="medios_382"] .formset-row:not(.empty-form)'
            );
            for (let form of formsetForms) {
                // Verificar si no está marcado para eliminar
                const deleteCheckbox = form.querySelector('[name*="DELETE"]');
                if (deleteCheckbox && deleteCheckbox.checked) {
                    continue;
                }

                // Buscar inputs de medios dentro de este form
                const medioInputsInForm = form.querySelectorAll(
                    '[id^="medio_interpretacion_382_"]'
                );
                for (let input of medioInputsInForm) {
                    if (input.value && input.value.trim() !== "") {
                        return true;
                    }
                }
            }

            return false;
        }

        return false;
    }

    /**
     * Actualizar UI de un campo en la lista del sidebar
     */
    function updateFieldItemUI(fieldId, isComplete) {
        const fieldItem = document.querySelector(
            `[data-field-id="${fieldId}"]`
        );
        if (!fieldItem) return;

        if (isComplete) {
            fieldItem.classList.remove("incomplete");
            fieldItem.classList.add("complete");
        } else {
            fieldItem.classList.remove("complete");
            fieldItem.classList.add("incomplete");
        }
    }

    /**
     * Actualizar progreso general
     */
    function updateProgress() {
        // Verificar todos los campos
        requiredFields.forEach((field) => {
            checkField(field.id);
        });

        // Calcular estadísticas
        const completedCount = Object.values(fieldStates).filter(
            (state) => state.complete
        ).length;
        const totalCount = requiredFields.length;
        const pendingCount = totalCount - completedCount;
        const percentage =
            totalCount > 0
                ? Math.round((completedCount / totalCount) * 100)
                : 0;

        // Actualizar UI
        updateProgressUI(completedCount, pendingCount, totalCount, percentage);
    }

    /**
     * Actualizar UI del progreso
     */
    function updateProgressUI(completed, pending, total, percentage) {
        // Actualizar porcentaje circular
        const progressPercent = document.getElementById("progress-percent");
        if (progressPercent) {
            progressPercent.textContent = `${percentage}%`;
        }

        // Actualizar círculo de progreso (SVG)
        const progressCircle = document.getElementById("progress-circle");
        if (progressCircle) {
            const circumference = 226.19; // 2 * PI * radius (36)
            const offset = circumference - (percentage / 100) * circumference;
            progressCircle.style.strokeDashoffset = offset;
        }

        // Actualizar estadísticas
        const camposCompletados = document.getElementById("campos-completados");
        const camposPendientes = document.getElementById("campos-pendientes");
        const camposTotales = document.getElementById("campos-totales");

        if (camposCompletados) camposCompletados.textContent = completed;
        if (camposPendientes) camposPendientes.textContent = pending;
        if (camposTotales) camposTotales.textContent = total;
    }

    /**
     * Debounce helper
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * API pública
     */
    window.RequiredFieldsTracker = {
        init: init,
        updateProgress: updateProgress,
        checkField: checkField,
        getProgress: function () {
            const completedCount = Object.values(fieldStates).filter(
                (state) => state.complete
            ).length;
            const totalCount = requiredFields.length;
            return {
                completed: completedCount,
                total: totalCount,
                percentage:
                    totalCount > 0
                        ? Math.round((completedCount / totalCount) * 100)
                        : 0,
            };
        },
    };

    // Auto-inicializar cuando el DOM esté listo
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
