/**
 * Sistema de validación y seguimiento de campos obligatorios MARC21
 */

(function () {
    "use strict";

    // Configuración de campos obligatorios por tipo de obra
    const REQUIRED_FIELDS = {
        // Campos obligatorios para TODOS los tipos de obra
        all: [
            {
                id: "id_centro_catalogador",
                label: "040 - Centro Catalogador",
                tab: 0,
            },
            {
                id: "id_titulo_principal",
                label: "245 - Título Principal",
                tab: 2,
            },
            { id: "id_ms_imp", label: "340 - Medio Físico", tab: 3 },
        ],
        // Campos obligatorios según punto de acceso principal
        conditional: {
            // Si tiene 100 (compositor)
            compositor: [
                { id: "id_compositor", label: "100 - Compositor", tab: 1 },
            ],
            // Si tiene 130 (título uniforme)
            titulo_uniforme: [
                {
                    id: "id_titulo_uniforme_texto",
                    label: "130 - Título Uniforme",
                    tab: 1,
                },
            ],
        },
    };

    let progressData = {
        total: 0,
        completed: 0,
        fields: [],
    };

    /**
     * Inicializa el sistema de campos obligatorios
     */
    function init() {
        // Desactivar validación HTML5 nativa del navegador
        const form = document.getElementById("obra-form");
        if (form) {
            form.setAttribute("novalidate", "novalidate");
        }

        identifyRequiredFields();
        createProgressPanel();
        markRequiredFields();
        setupValidation();
        updateProgress();

        // Actualizar progreso cuando cambian los campos
        document.addEventListener("input", debounce(updateProgress, 500));
        document.addEventListener("change", updateProgress);

        // NO usar MutationObserver para evitar bucles infinitos
        // En su lugar, el sistema de borradores llamará manualmente updateProgress
    }

    /**
     * Identifica qué campos son obligatorios según el formulario actual
     */
    function identifyRequiredFields() {
        progressData.fields = [];

        // Agregar campos obligatorios comunes
        REQUIRED_FIELDS.all.forEach((field) => {
            const element = document.getElementById(field.id);
            if (element) {
                progressData.fields.push({
                    ...field,
                    element: element,
                    completed: false,
                });
            }
        });

        // Verificar si tiene compositor (100) o título uniforme (130)
        const hasCompositor = document.getElementById("id_compositor");
        const hasTituloUniforme = document.getElementById(
            "id_titulo_uniforme_texto"
        );

        if (hasCompositor) {
            progressData.fields.push({
                id: "id_compositor",
                label: "100 - Compositor",
                tab: 1,
                element: hasCompositor,
                completed: false,
                conditional: true,
            });
        }

        if (hasTituloUniforme) {
            progressData.fields.push({
                id: "id_titulo_uniforme_texto",
                label: "130 - Título Uniforme",
                tab: 1,
                element: hasTituloUniforme,
                completed: false,
                conditional: true,
            });
        }

        // Campo 382 - Medio de Interpretación (verificar si hay al menos uno)
        // Agregar SIEMPRE, pero la validación determinará si está completo
        progressData.fields.push({
            id: "medio_interpretacion_check",
            label: "382 - Medio de Interpretación",
            tab: 3,
            element: null, // Se valida de forma especial
            completed: false,
            isFormset: true,
        });

        progressData.total = progressData.fields.length;
    }

    /**
     * Crea el panel de progreso en la parte superior
     */
    function createProgressPanel() {
        const form = document.getElementById("obra-form");
        if (!form) return;

        const panel = document.createElement("div");
        panel.className = "progress-panel";
        panel.id = "progress-panel";
        panel.innerHTML = `
            <h6><i class="bi bi-check-circle"></i> Progreso de Campos Obligatorios</h6>
            <div class="progress-stats">
                <div class="progress-circle">
                    <svg width="80" height="80">
                        <circle class="bg-circle" cx="40" cy="40" r="36"></circle>
                        <circle class="progress-circle-bar" cx="40" cy="40" r="36"
                                stroke-dasharray="226" stroke-dashoffset="226"></circle>
                    </svg>
                    <div class="progress-text">0%</div>
                </div>
                <div class="progress-details">
                    <p><strong><span id="completed-count">0</span> de <span id="total-count">0</span></strong> campos completados</p>
                    <p class="mb-0" style="font-size: 0.85rem; opacity: 0.9;">
                        Los campos obligatorios están marcados con 
                        <span class="required-badge" style="font-size: 0.65rem; margin: 0 0.25rem;">OBLIGATORIO</span>
                    </p>
                    <div class="field-list" id="field-status-list"></div>
                </div>
            </div>
        `;

        form.parentElement.insertBefore(panel, form);
    }

    /**
     * Marca visualmente los campos obligatorios
     */
    function markRequiredFields() {
        progressData.fields.forEach((field) => {
            if (!field.element) return;

            const formGroup = field.element.closest(".form-group, .mb-3");
            if (!formGroup) return;

            // Agregar clase de campo obligatorio
            formGroup.classList.add("required-field");

            // Agregar badge al label
            const label = formGroup.querySelector("label");
            if (label && !label.querySelector(".required-badge")) {
                const badge = document.createElement("span");
                badge.className = "required-badge";
                badge.textContent = "Obligatorio";
                label.appendChild(badge);
            }

            // Marcar input visualmente (NO usar required de HTML5)
            if (
                field.element.tagName === "INPUT" ||
                field.element.tagName === "SELECT" ||
                field.element.tagName === "TEXTAREA"
            ) {
                field.element.classList.add("required-input");
                // NO establecer required=true para evitar validación HTML5
                // field.element.required = true;
            }
        });

        // Marcar pestañas que tienen campos obligatorios
        markRequiredTabs();
    }

    /**
     * Marca las pestañas que contienen campos obligatorios
     */
    function markRequiredTabs() {
        const tabsWithRequired = new Set();

        progressData.fields.forEach((field) => {
            tabsWithRequired.add(field.tab);
        });

        tabsWithRequired.forEach((tabIndex) => {
            const tabButton = document.querySelector(
                `[data-tab-index="${tabIndex}"]`
            );
            if (tabButton && !tabButton.querySelector(".required-indicator")) {
                const indicator = document.createElement("span");
                indicator.className = "required-indicator";
                indicator.title = "Contiene campos obligatorios";
                tabButton.appendChild(indicator);
            }
        });
    }

    /**
     * Configura validación en tiempo real
     */
    function setupValidation() {
        progressData.fields.forEach((field) => {
            if (!field.element) return;

            field.element.addEventListener("input", function () {
                validateField(field);
            });

            field.element.addEventListener("change", function () {
                validateField(field);
            });
        });
    }

    /**
     * Valida un campo específico
     */
    function validateField(field) {
        if (field.isFormset) {
            // Validación especial para formsets (ej: 382)
            const validationResult = validateFormset382();

            if (validationResult === null) {
                // El formset no existe en este tipo de obra - eliminarlo de campos obligatorios
                const index = progressData.fields.findIndex(
                    (f) => f.id === field.id
                );
                if (index !== -1) {
                    progressData.fields.splice(index, 1);
                    progressData.total = progressData.fields.length;
                    updateProgress(); // Actualizar UI
                }
                return;
            }

            // true = tiene datos (completo), false = existe pero vacío (incompleto)
            field.completed = validationResult;
        } else if (field.element) {
            // Validación normal
            const value = field.element.value.trim();
            field.completed = value.length > 0;

            // Actualizar clases visuales
            const formGroup = field.element.closest(".form-group, .mb-3");
            if (formGroup) {
                if (field.completed) {
                    formGroup.classList.add("field-complete");
                    const badge = formGroup.querySelector(".required-badge");
                    if (badge) badge.classList.add("complete");
                } else {
                    formGroup.classList.remove("field-complete");
                    const badge = formGroup.querySelector(".required-badge");
                    if (badge) badge.classList.remove("complete");
                }
            }
        }

        return field.completed;
    }

    /**
     * Valida que exista al menos un medio de interpretación (382)
     * Retorna: true si tiene datos, false si está vacío, null si no existe en este tipo
     */
    function validateFormset382() {
        // Intentar varios selectores posibles
        let container =
            document.querySelector(
                '[data-formset-prefix="mediointerpretacion382_set"]'
            ) ||
            document.querySelector(
                '[data-formset-prefix="medio_interpretacion_382"]'
            ) ||
            document.querySelector('[data-formset-prefix*="medio"]');

        if (!container) {
            // Buscar por contenido - cualquier formset que tenga "382" en el título
            const allContainers =
                document.querySelectorAll(".formset-container");
            for (let cont of allContainers) {
                const addButton = cont.querySelector(".add-form-row");
                if (addButton && addButton.textContent.includes("382")) {
                    container = cont;
                    break;
                }
            }
        }

        if (!container) {
            // Si no lo encuentra, el formset no existe en este tipo de obra
            // Retornar null para indicar "no aplicable"
            return null;
        }

        const rows = container.querySelectorAll(
            ".formset-row:not(.empty-form)"
        );
        let hasValue = false;

        rows.forEach((row) => {
            // Buscar inputs/selects que contengan "medio" en el name
            const inputs = row.querySelectorAll(
                'input[name*="medio"], select[name*="medio"]'
            );

            inputs.forEach((input) => {
                const value = input.value.trim();
                if (value && value.length > 0) {
                    hasValue = true;
                }
            });
        });

        return hasValue;
    }

    /**
     * Valida campos condicionales (100 o 130)
     */
    function validateConditionalFields() {
        const compositor = progressData.fields.find(
            (f) => f.id === "id_compositor"
        );
        const tituloUniforme = progressData.fields.find(
            (f) => f.id === "id_titulo_uniforme_texto"
        );

        if (compositor && tituloUniforme) {
            // Debe tener al menos uno de los dos
            const compositorComplete = compositor.completed;
            const tituloComplete = tituloUniforme.completed;

            if (compositorComplete || tituloComplete) {
                // Si uno está completo, ambos cuentan como satisfechos
                compositor.satisfied = true;
                tituloUniforme.satisfied = true;
                return 2; // Ambos cuentan
            } else {
                compositor.satisfied = false;
                tituloUniforme.satisfied = false;
                return 0;
            }
        }

        return 0;
    }

    /**
     * Actualiza el progreso general
     */
    function updateProgress() {
        // Validar todos los campos
        progressData.fields.forEach((field) => validateField(field));

        // Manejar campos condicionales
        const conditionalSatisfied = validateConditionalFields();

        // Calcular progreso
        let completed = 0;
        progressData.fields.forEach((field) => {
            if (field.conditional) {
                if (field.satisfied) completed++;
            } else {
                if (field.completed) completed++;
            }
        });

        progressData.completed = completed;

        // Actualizar UI
        updateProgressUI();
        updateTabIndicators();
    }

    /**
     * Actualiza la UI del panel de progreso
     */
    function updateProgressUI() {
        const percentage = Math.round(
            (progressData.completed / progressData.total) * 100
        );

        // Actualizar círculo de progreso
        const progressBar = document.querySelector(".progress-circle-bar");
        const progressText = document.querySelector(".progress-text");
        const completedCount = document.getElementById("completed-count");
        const totalCount = document.getElementById("total-count");

        if (progressBar) {
            const circumference = 2 * Math.PI * 36;
            const offset = circumference - (percentage / 100) * circumference;
            progressBar.style.strokeDashoffset = offset;
        }

        if (progressText) {
            progressText.textContent = `${percentage}%`;
        }

        if (completedCount) {
            completedCount.textContent = progressData.completed;
        }

        if (totalCount) {
            totalCount.textContent = progressData.total;
        }

        // Actualizar lista de campos
        updateFieldStatusList();

        // Cambiar color del panel según progreso
        const panel = document.getElementById("progress-panel");
        if (panel) {
            if (percentage === 100) {
                panel.style.background =
                    "linear-gradient(135deg, #10b981 0%, #059669 100%)";
            } else {
                panel.style.background =
                    "linear-gradient(135deg, #667eea 0%, #764ba2 100%)";
            }
        }
    }

    /**
     * Actualiza la lista de estados de campos
     */
    function updateFieldStatusList() {
        const list = document.getElementById("field-status-list");
        if (!list) return;

        list.innerHTML = "";

        progressData.fields.forEach((field) => {
            const isComplete = field.conditional
                ? field.satisfied
                : field.completed;
            const badge = document.createElement("span");
            badge.className = `field-badge ${
                isComplete ? "complete" : "incomplete"
            }`;
            badge.textContent = field.label;
            badge.title = isComplete ? "Completado" : "Pendiente";
            list.appendChild(badge);
        });
    }

    /**
     * Actualiza indicadores en pestañas
     */
    function updateTabIndicators() {
        const tabsByIndex = {};

        // Agrupar campos por pestaña
        progressData.fields.forEach((field) => {
            if (!tabsByIndex[field.tab]) {
                tabsByIndex[field.tab] = { total: 0, completed: 0 };
            }
            tabsByIndex[field.tab].total++;

            const isComplete = field.conditional
                ? field.satisfied
                : field.completed;
            if (isComplete) {
                tabsByIndex[field.tab].completed++;
            }
        });

        // Actualizar indicadores visuales
        Object.keys(tabsByIndex).forEach((tabIndex) => {
            const stats = tabsByIndex[tabIndex];
            const tabButton = document.querySelector(
                `[data-tab-index="${tabIndex}"]`
            );

            if (tabButton) {
                const indicator = tabButton.querySelector(
                    ".required-indicator"
                );
                if (indicator) {
                    if (stats.completed === stats.total) {
                        tabButton.classList.add("has-required-complete");
                    } else {
                        tabButton.classList.remove("has-required-complete");
                    }
                }
            }
        });
    }

    /**
     * Utilidad: debounce
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

    // Inicializar cuando el DOM esté listo
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }

    // Exportar para uso externo
    window.RequiredFieldsTracker = {
        updateProgress: updateProgress,
        getProgress: () => progressData,
    };
})();
