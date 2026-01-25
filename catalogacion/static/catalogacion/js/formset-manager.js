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
        console.log('FormsetManager: Inicializando todos los formsets...');
        
        // Buscar todos los botones de agregar campo y conectarlos
        document
            .querySelectorAll(".campo-add-btn[data-formset-target]")
            .forEach((button) => {
                // Remover TODOS los listeners existentes clonando el botón
                const newButton = button.cloneNode(true);
                button.parentNode.replaceChild(newButton, button);
                
                const prefix = newButton.dataset.formsetTarget;
                console.log(`FormsetManager: Inicializando botón para prefix "${prefix}"`);
                
                const container = document.querySelector(
                    `[data-formset-prefix="${prefix}"]`
                );

                if (!container) {
                    console.warn(
                        `FormsetManager: No se encontró contenedor para prefix "${prefix}"`
                    );
                    return;
                }

                // Crear handler único
                const clickHandler = (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log(`FormsetManager: Click detectado para prefix "${prefix}"`);
                    addNewForm(prefix);
                };
                
                newButton.addEventListener("click", clickHandler);
                newButton.dataset.formsetManagerInitialized = "true";
                console.log(`FormsetManager: Botón inicializado para prefix "${prefix}"`);
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
        console.log(`FormsetManager: Agregando nuevo formulario para prefix "${prefix}"`);
        
        // Prevenir múltiples ejecuciones con un flag
        if (window._formsetAdding && window._formsetAdding[prefix]) {
            console.log(`FormsetManager: Ya se está agregando para ${prefix}, ignorando...`);
            return;
        }
        
        // Marcar que estamos agregando
        if (!window._formsetAdding) window._formsetAdding = {};
        window._formsetAdding[prefix] = true;
        
        const container = document.querySelector(
            `[data-formset-prefix="${prefix}"]`
        );
        if (!container) {
            window._formsetAdding[prefix] = false;
            return;
        }

        const totalFormsInput = container.querySelector(
            `#id_${prefix}-TOTAL_FORMS`
        );
        const formsContainer = container.querySelector(".formset-forms");
        const emptyFormTemplate = formsContainer?.querySelector(".empty-form");

        if (!totalFormsInput || !formsContainer || !emptyFormTemplate) {
            console.error(
                `FormsetManager: Faltan elementos para prefix "${prefix}"`
            );
            window._formsetAdding[prefix] = false;
            return;
        }

        const totalForms = parseInt(totalFormsInput.value, 10) || 0;
        console.log(`FormsetManager: Formularios actuales: ${totalForms}`);

        // Clonar el template vacío
        const newForm = emptyFormTemplate.cloneNode(true);
        console.log('FormsetManager: Template clonado');

        // Reemplazar __prefix__ con el nuevo índice
        newForm.innerHTML = newForm.innerHTML.replace(
            /__prefix__/g,
            totalForms
        );
        newForm.classList.remove("empty-form");
        newForm.style.display = "";

        // Insertar antes del template vacío
        formsContainer.insertBefore(newForm, emptyFormTemplate);

        // Incrementar contador
        totalFormsInput.value = totalForms + 1;
        console.log(`FormsetManager: Nuevo total de formularios: ${totalForms + 1}`);

        // Liberar el flag después de un pequeño delay
        setTimeout(() => {
            window._formsetAdding[prefix] = false;
        }, 100);

        // Emitir evento para que otras lógicas (plantillas específicas) puedan
        // reindexar o reinicializar elementos dentro del formset recién añadido.
        try {
            const ev = new CustomEvent('formset:added', { 
                detail: { 
                    prefix,
                    newForm: newForm,
                    totalForms: totalForms + 1
                } 
            });
            container.dispatchEvent(ev);
            console.log(`FormsetManager: Evento formset:added emitido para ${prefix}`, { prefix, newForm, totalForms: totalForms + 1 });
        } catch (err) {
            console.warn('FormsetManager: Error al emitir evento formset:added', err);
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
