/**
 * formset-manager.js
 * Gestor centralizado para todos los formsets de Django
 * Maneja agregar/eliminar formularios de manera unificada
 */

(function () {
    "use strict";

    /**
     * Inicializa todos los formsets en la página
     */
    function initAllFormsets() {
        // Buscar todos los botones de agregar campo y conectarlos
        document
            .querySelectorAll(".campo-add-btn[data-formset-target]")
            .forEach((button) => {
                if (button.dataset.formsetManagerInitialized) return;

                const prefix = button.dataset.formsetTarget;
                const container = document.querySelector(
                    `[data-formset-prefix="${prefix}"]`
                );

                if (!container) {
                    console.warn(
                        `FormsetManager: No se encontró contenedor para prefix "${prefix}"`
                    );
                    return;
                }

                button.addEventListener("click", () => addNewForm(prefix));
                button.dataset.formsetManagerInitialized = "true";
            });

        // Delegar eventos de eliminación en el documento
        if (!document.body.dataset.formsetDeleteInitialized) {
            document.body.addEventListener("click", handleDeleteClick);
            document.body.dataset.formsetDeleteInitialized = "true";
        }
    }

    /**
     * Agrega un nuevo formulario al formset
     */
    function addNewForm(prefix) {
        const container = document.querySelector(
            `[data-formset-prefix="${prefix}"]`
        );
        if (!container) return;

        const totalFormsInput = container.querySelector(
            `#id_${prefix}-TOTAL_FORMS`
        );
        const formsContainer = container.querySelector(".formset-forms");
        const emptyFormTemplate = formsContainer?.querySelector(".empty-form");

        if (!totalFormsInput || !formsContainer || !emptyFormTemplate) {
            console.error(
                `FormsetManager: Faltan elementos para prefix "${prefix}"`
            );
            return;
        }

        const totalForms = parseInt(totalFormsInput.value, 10) || 0;

        // Clonar el template vacío
        const newForm = emptyFormTemplate.cloneNode(true);

        // Reemplazar __prefix__ con el nuevo índice
        newForm.innerHTML = newForm.innerHTML.replace(
            /__prefix__/g,
            totalForms
        );
        newForm.classList.remove("empty-form");
        newForm.style.display = "";

        // Limpiar cualquier artefacto de Select2 que haya sido inicializado
        // sobre el template vacío (para evitar inputs "No results found"/IDs duplicados)
        newForm
            .querySelectorAll(".select2-container")
            .forEach((el) => el.remove());
        newForm.querySelectorAll("select").forEach((select) => {
            select.classList.remove("select2-hidden-accessible");
            select.removeAttribute("data-select2-id");
            select.removeAttribute("tabindex");

            // Si el select está marcado como no-select2, remover también la clase select2
            // (esto evita que cualquier inicialización posterior lo convierta a Select2).
            if (
                select.classList.contains("no-select2") ||
                select.getAttribute("data-no-select2") === "1"
            ) {
                select.classList.remove("select2");
            }

            const next = select.nextElementSibling;
            if (next && next.classList && next.classList.contains("select2")) {
                next.remove();
            }
        });

        // Insertar antes del template vacío
        formsContainer.insertBefore(newForm, emptyFormTemplate);

        // Incrementar contador
        totalFormsInput.value = totalForms + 1;

        // Reinicializar Select2 SOLO en campos marcados con .select2
        // y que NO estén marcados como no-select2.
        if (
            typeof $ !== "undefined" &&
            $.fn &&
            typeof $.fn.select2 === "function"
        ) {
            newForm.querySelectorAll("select.select2").forEach((select) => {
                if (
                    select.classList.contains("no-select2") ||
                    select.getAttribute("data-no-select2") === "1"
                ) {
                    return;
                }
                // Siempre reinicializar limpio
                try {
                    if ($(select).hasClass("select2-hidden-accessible")) {
                        $(select).select2("destroy");
                    }
                } catch (e) {
                    // ignore
                }

                $(select).select2({
                    theme: "bootstrap-5",
                    width: "100%",
                    placeholder: function () {
                        return $(this).data("placeholder");
                    },
                    allowClear: true,
                });
            });

            // Kill switch: algunos selects NO deben ser Select2 aunque se cuele por clones o scripts.
            // Caso crítico: 264 (prefix "produccion") indicador/función debe ser dropdown nativo.
            const forceNativeSelect = (select) => {
                try {
                    if ($(select).data("select2")) {
                        $(select).select2("destroy");
                    }
                } catch (e) {
                    // ignore
                }

                select.classList.remove("select2-hidden-accessible");
                select.classList.remove("select2");
                select.removeAttribute("data-select2-id");
                select.removeAttribute("tabindex");
                select.removeAttribute("aria-hidden");

                // Remover cualquier contenedor select2 adyacente o dentro del mismo wrapper
                const next = select.nextElementSibling;
                if (
                    next &&
                    next.classList &&
                    next.classList.contains("select2")
                ) {
                    next.remove();
                }
                const parent = select.parentElement;
                if (parent) {
                    parent
                        .querySelectorAll(".select2-container")
                        .forEach((el) => el.remove());
                }
            };

            if (prefix === "produccion") {
                newForm
                    .querySelectorAll('select[name$="-funcion"]')
                    .forEach(forceNativeSelect);
            }
        }

        // Emitir evento para que otras lógicas (plantillas específicas) puedan
        // reindexar o reinicializar elementos dentro del formset recién añadido.
        try {
            const ev = new CustomEvent('formset:added', { detail: { prefix } });
            container.dispatchEvent(ev);
        } catch (err) {
            // Silenciar si CustomEvent no está soportado
        }

        // Inicializar visibilidad de botones de eliminar en subcampos
        newForm
            .querySelectorAll(".subcampo-repetible-container")
            .forEach(updateSubcampoDeleteVisibility);

        // Notificar a scripts específicos (por ejemplo, autocompletes de 773/774)
        // que se añadió una nueva fila al formset.
        try {
            document.dispatchEvent(
                new CustomEvent("formset:added", {
                    detail: {
                        prefix,
                        container,
                        newForm,
                    },
                })
            );
        } catch (e) {
            // ignore
        }
    }

    /**
     * Maneja clicks en botones de eliminar
     */
    function handleDeleteClick(e) {
        const deleteBtn = e.target.closest(".delete-row-btn");
        if (!deleteBtn) return;

        const row = deleteBtn.closest(".formset-row");
        if (!row || row.classList.contains("empty-form")) return;

        const container = row.closest(".formset-container");
        if (!container) return;

        const prefix = container.dataset.formsetPrefix;
        const totalFormsInput = container.querySelector(
            `#id_${prefix}-TOTAL_FORMS`
        );
        const deleteCheckbox = row.querySelector('input[name*="DELETE"]');

        if (row.classList.contains("existing-form")) {
            // Formulario existente: marcar/desmarcar para eliminación
            if (deleteCheckbox && deleteCheckbox.checked) {
                deleteCheckbox.checked = false;
                row.style.opacity = "1";
                deleteBtn.classList.remove("btn-warning");
                deleteBtn.innerHTML = '<i class="bi bi-x-lg"></i>';
                deleteBtn.title = "Eliminar";
            } else if (deleteCheckbox) {
                deleteCheckbox.checked = true;
                row.style.opacity = "0.5";
                deleteBtn.classList.add("btn-warning");
                deleteBtn.innerHTML =
                    '<i class="bi bi-arrow-counterclockwise"></i>';
                deleteBtn.title = "Cancelar eliminación";
            }
        } else {
            // Formulario nuevo: eliminar completamente
            row.remove();
            if (totalFormsInput) {
                totalFormsInput.value = parseInt(totalFormsInput.value, 10) - 1;
            }
        }
    }

    /**
     * Actualiza la visibilidad de botones de eliminar en subcampos
     */
    function updateSubcampoDeleteVisibility(container) {
        const rows = container.querySelectorAll(".subcampo-row");
        rows.forEach((row, index) => {
            const deleteBtn = row.querySelector(".subcampo-delete-btn");
            if (deleteBtn) {
                // El primer subcampo (con el botón +) no se puede eliminar
                // Los demás solo se pueden eliminar si hay más de uno
                const hasAddButton = row.querySelector(".subcampo-add-btn");
                if (hasAddButton) {
                    // Primera fila: nunca mostrar botón eliminar
                    deleteBtn.style.visibility = "hidden";
                } else {
                    // Filas adicionales: mostrar siempre
                    deleteBtn.style.visibility = "visible";
                }
            }
        });
    }

    /**
     * Exponer función para actualizar visibilidad de subcampos
     */
    window.FormsetManager = {
        init: initAllFormsets,
        addNewForm: addNewForm,
        updateSubcampoDeleteVisibility: updateSubcampoDeleteVisibility,
    };

    // Inicializar cuando el DOM esté listo
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initAllFormsets);
    } else {
        initAllFormsets();
    }

    // Re-inicializar cuando se actualice el DOM (para HTMX u otras librerías)
    document.addEventListener("htmx:afterSwap", initAllFormsets);
})();
