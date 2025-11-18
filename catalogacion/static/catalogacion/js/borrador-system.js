/**
 * Sistema de Borradores para Obras MARC21
 * Maneja guardado automático y recuperación de borradores
 */

(function () {
    "use strict";

    // Configuración
    const AUTOSAVE_INTERVAL = 60000; // Autoguardar cada 60 segundos
    const MIN_CHANGE_DELAY = 3000; // Esperar 3 segundos después del último cambio

    let borradorId = null;
    let autoSaveTimer = null;
    let changeTimer = null;
    let hasUnsavedChanges = false;
    let lastSavedData = null;

    // Elementos del DOM
    const form = document.getElementById("obra-form");
    const tipoObraElement = document.querySelector(
        'input[name="tipo_registro"], input[name="nivel_bibliografico"]'
    );

    // Obtener URLs desde el data attribute del formulario
    const API_URLS = {
        guardar: "/api/borradores/guardar/",
        autoguardar: "/api/borradores/autoguardar/",
        verificar: "/api/borradores/verificar/",
        obtener: (id) => `/api/borradores/${id}/`,
        eliminar: (id) => `/api/borradores/${id}/eliminar/`,
        listar: "/api/borradores/listar/",
    };

    /**
     * Obtiene el CSRF token para requests AJAX
     */
    function getCsrfToken() {
        const token = document.querySelector('[name="csrfmiddlewaretoken"]');
        return token ? token.value : "";
    }

    /**
     * Serializa todos los datos del formulario a JSON
     */
    function serializeFormData() {
        const formData = new FormData(form);
        const data = {};

        // Campos simples
        for (let [key, value] of formData.entries()) {
            if (
                key.includes("-TOTAL_FORMS") ||
                key.includes("-INITIAL_FORMS")
            ) {
                // Metadata de formsets
                data[key] = value;
            } else if (key.includes("-")) {
                // Campos de formsets
                if (!data[key]) {
                    data[key] = [];
                }
                data[key].push(value);
            } else {
                // Campos normales
                data[key] = value;
            }
        }

        return data;
    }

    /**
     * Obtiene el tipo de obra actual
     */
    function getTipoObra() {
        const tipoRegistro = document.getElementById("id_tipo_registro")?.value;
        const nivelBibliografico = document.getElementById(
            "id_nivel_bibliografico"
        )?.value;

        // Determinar tipo de obra basándose en tipo_registro y nivel_bibliografico
        if (tipoRegistro === "d") {
            // Manuscrito
            if (nivelBibliografico === "c") return "manuscrito_coleccion";
            return "manuscrito_independiente";
        } else if (tipoRegistro === "c") {
            // Impreso
            if (nivelBibliografico === "c") return "impreso_coleccion";
            return "impreso_independiente";
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
            const pestanaActual = currentTabIndex; // Variable global del sistema de pestañas

            console.log("📝 Guardando borrador:", {
                esAutoguardado,
                tipoObra,
                borradorId,
                pestanaActual,
                datosCantidad: Object.keys(datos).length,
            });

            const payload = {
                tipo_obra: tipoObra,
                datos_formulario: datos,
                pestana_actual: pestanaActual,
            };

            if (borradorId) {
                payload.borrador_id = borradorId;
            }

            const url = esAutoguardado
                ? API_URLS.autoguardar
                : API_URLS.guardar;

            console.log("🌐 Enviando a:", url);

            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCsrfToken(),
                },
                body: JSON.stringify(payload),
            });

            console.log("📡 Respuesta status:", response.status);
            const result = await response.json();
            console.log("📦 Respuesta data:", result);

            if (result.success) {
                borradorId = result.borrador_id;
                lastSavedData = JSON.stringify(datos);
                hasUnsavedChanges = false;

                mostrarNotificacion(
                    esAutoguardado ? "Autoguardado" : result.message,
                    "success",
                    esAutoguardado ? 2000 : 3000
                );

                actualizarIndicadorGuardado();
            } else {
                console.error("Error guardando borrador:", result.error);
                mostrarNotificacion("Error al guardar borrador", "error");
            }
        } catch (error) {
            console.error("Error en guardarBorrador:", error);
            if (!esAutoguardado) {
                mostrarNotificacion("Error de conexión", "error");
            }
        }
    }

    /**
     * Verifica si existe un borrador al cargar la página
     */
    async function verificarBorradorExistente() {
        try {
            const tipoObra = getTipoObra();
            const response = await fetch(
                `${API_URLS.verificar}?tipo_obra=${encodeURIComponent(
                    tipoObra
                )}`
            );
            const result = await response.json();

            if (result.success && result.tiene_borrador) {
                mostrarDialogoRecuperarBorrador(result.borrador);
            }
        } catch (error) {
            console.error("Error verificando borrador:", error);
        }
    }

    /**
     * Muestra diálogo elegante para recuperar borrador existente
     */
    function mostrarDialogoRecuperarBorrador(borrador) {
        const dias = borrador.dias_antiguedad;
        let tiempoGuardado;

        if (dias === 0) {
            tiempoGuardado = "Guardado hoy";
        } else if (dias === 1) {
            tiempoGuardado = "Guardado ayer";
        } else {
            tiempoGuardado = `Guardado hace ${dias} días`;
        }

        // Crear modal
        const modalHtml = `
            <div class="modal fade" id="modalRecuperarBorrador" tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false">
                <div class="modal-dialog modal-dialog-centered modal-sm">
                    <div class="modal-content">
                        <div class="modal-header bg-info text-white">
                            <h6 class="modal-title mb-0">
                                <i class="bi bi-cloud-arrow-down"></i> Borrador Encontrado
                            </h6>
                        </div>
                        <div class="modal-body text-center py-4">
                            <i class="bi bi-cloud-check text-info" style="font-size: 3rem;"></i>
                            <p class="mt-3 mb-2">Tienes un borrador guardado</p>
                            <small class="text-muted">${tiempoGuardado}</small>
                            <p class="mt-3 mb-0"><small class="text-muted">¿Deseas recuperarlo y continuar?</small></p>
                        </div>
                        <div class="modal-footer justify-content-center">
                            <button type="button" class="btn btn-outline-danger btn-sm" id="btnEmpezarNuevo">
                                <i class="bi bi-x-circle"></i> Empezar de Nuevo
                            </button>
                            <button type="button" class="btn btn-info btn-sm" id="btnRecuperar">
                                <i class="bi bi-check-circle"></i> Recuperar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Agregar modal al DOM
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modalElement = document.getElementById('modalRecuperarBorrador');
        const modal = new bootstrap.Modal(modalElement);

        // Eventos de botones
        document.getElementById('btnRecuperar').addEventListener('click', () => {
            modal.hide();
            cargarBorrador(borrador.id);
            setTimeout(() => modalElement.remove(), 300);
        });

        document.getElementById('btnEmpezarNuevo').addEventListener('click', () => {
            modal.hide();
            limpiarFormularioCompleto();
            eliminarBorrador(borrador.id);
            setTimeout(() => modalElement.remove(), 300);
        });

        // Mostrar modal
        modal.show();
    }

    /**
     * Carga un borrador específico
     */
    async function cargarBorrador(id) {
        try {
            const response = await fetch(API_URLS.obtener(id));
            const result = await response.json();

            if (result.success) {
                const borrador = result.borrador;
                borradorId = borrador.id;

                // Cargar datos en el formulario
                cargarDatosEnFormulario(borrador.datos_formulario);

                // Navegar a la pestaña donde se quedó
                if (
                    typeof switchTab === "function" &&
                    borrador.pestana_actual
                ) {
                    switchTab(borrador.pestana_actual);
                }

                mostrarNotificacion(
                    "Borrador recuperado exitosamente",
                    "success"
                );
                actualizarIndicadorGuardado();
            } else {
                mostrarNotificacion("Error al cargar borrador", "error");
            }
        } catch (error) {
            console.error("Error cargando borrador:", error);
            mostrarNotificacion("Error al cargar borrador", "error");
        }
    }

    /**
     * Carga datos del borrador en el formulario
     */
    function cargarDatosEnFormulario(datos) {
        for (let [key, value] of Object.entries(datos)) {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                if (input.type === "checkbox") {
                    input.checked = value === "on" || value === true;
                } else if (input.type === "radio") {
                    if (input.value === value) {
                        input.checked = true;
                    }
                } else {
                    input.value = value;
                }

                // Trigger change event para actualizar UI
                input.dispatchEvent(new Event("change", { bubbles: true }));
            }
        }
    }

    /**
     * Limpia completamente el formulario
     */
    function limpiarFormularioCompleto() {
        // Resetear todos los inputs de texto, textarea, select
        form.querySelectorAll('input[type="text"], input[type="number"], input[type="date"], input[type="email"], input[type="url"], textarea, select').forEach(input => {
            input.value = '';
            // Limpiar Select2 si existe
            if ($(input).data('select2')) {
                $(input).val(null).trigger('change');
            }
        });

        // Desmarcar checkboxes
        form.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });

        // Desmarcar radios
        form.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.checked = false;
        });

        // Limpiar archivos
        form.querySelectorAll('input[type="file"]').forEach(fileInput => {
            fileInput.value = '';
        });

        // Resetear hidden inputs (excepto CSRF y campos de tipo)
        form.querySelectorAll('input[type="hidden"]').forEach(hidden => {
            if (hidden.name !== 'csrfmiddlewaretoken' && 
                hidden.name !== 'tipo_registro' && 
                hidden.name !== 'nivel_bibliografico') {
                hidden.value = '';
            }
        });

        // Volver a la primera pestaña
        if (typeof switchTab === 'function') {
            switchTab(0);
        }

        // Resetear variables del sistema de borradores
        borradorId = null;
        hasUnsavedChanges = false;
        lastSavedData = null;
        actualizarIndicadorGuardado();

        mostrarNotificacion('Formulario limpiado - Empezando de nuevo', 'info', 3000);
        console.log('✓ Formulario limpiado completamente');
    }

    /**
     * Elimina un borrador
     */
    async function eliminarBorrador(id) {
        try {
            const response = await fetch(API_URLS.eliminar(id), {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                },
            });

            const result = await response.json();

            if (result.success) {
                if (id === borradorId) {
                    borradorId = null;
                }
                mostrarNotificacion("Borrador eliminado", "info", 2000);
            }
        } catch (error) {
            console.error("Error eliminando borrador:", error);
        }
    }

    /**
     * Muestra notificación toast
     */
    function mostrarNotificacion(mensaje, tipo = "info", duracion = 3000) {
        // Crear elemento de notificación
        const notif = document.createElement("div");
        notif.className = `toast-notification toast-${tipo}`;
        notif.textContent = mensaje;

        // Estilos inline para la notificación
        notif.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 4px;
            color: white;
            font-size: 14px;
            font-weight: 500;
            z-index: 10000;
            animation: slideIn 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;

        // Colores según tipo
        const colores = {
            success: "#27AE60",
            error: "#E74C3C",
            info: "#3498DB",
            warning: "#F39C12",
        };
        notif.style.backgroundColor = colores[tipo] || colores.info;

        document.body.appendChild(notif);

        setTimeout(() => {
            notif.style.animation = "slideOut 0.3s ease";
            setTimeout(() => notif.remove(), 300);
        }, duracion);
    }

    /**
     * Actualiza indicador visual de guardado
     */
    function actualizarIndicadorGuardado() {
        let indicador = document.getElementById("save-indicator");

        if (!indicador) {
            indicador = document.createElement("div");
            indicador.id = "save-indicator";
            indicador.style.cssText = `
                position: fixed;
                bottom: 20px;
                left: 20px;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
                z-index: 9999;
                display: flex;
                align-items: center;
                gap: 8px;
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

            // Ocultar después de 3 segundos
            setTimeout(() => {
                indicador.style.opacity = "0";
                setTimeout(() => {
                    indicador.style.opacity = "1";
                }, 3000);
            }, 3000);
        } else {
            indicador.style.display = "none";
        }
    }

    /**
     * Detecta cambios en el formulario
     */
    function onFormChange() {
        hasUnsavedChanges = true;
        actualizarIndicadorGuardado();

        // Resetear timer de cambio
        if (changeTimer) {
            clearTimeout(changeTimer);
        }

        // Autoguardar después de inactividad (siempre, incluso si no hay borrador)
        changeTimer = setTimeout(() => {
            guardarBorrador(true);
        }, MIN_CHANGE_DELAY);
    }

    /**
     * Inicia el sistema de autoguardado
     */
    function iniciarAutoguardado() {
        // Limpiar timer existente
        if (autoSaveTimer) {
            clearInterval(autoSaveTimer);
        }

        // Autoguardar periódicamente si hay borrador
        autoSaveTimer = setInterval(() => {
            if (borradorId && hasUnsavedChanges) {
                guardarBorrador(true);
            }
        }, AUTOSAVE_INTERVAL);
    }

    /**
     * Manejo del botón "Guardar Borrador"
     */
    function configurarBotonGuardarBorrador() {
        // Buscar o crear botón de guardar borrador
        const botonesAccion = document.querySelector(".tab-navigation-buttons");

        if (botonesAccion && !document.getElementById("btn-guardar-borrador")) {
            const btnGuardar = document.createElement("button");
            btnGuardar.id = "btn-guardar-borrador";
            btnGuardar.type = "button";
            btnGuardar.className = "btn btn-outline-info btn-sm";
            btnGuardar.innerHTML =
                '<i class="bi bi-cloud-arrow-up"></i> Guardar Borrador';
            btnGuardar.onclick = () => guardarBorrador(false);

            // Insertar en la primera pestaña
            const primeraSeccion = document.querySelector(
                "#tab-0xx .tab-navigation-buttons"
            );
            if (primeraSeccion) {
                const contenedor =
                    primeraSeccion.querySelector("div:first-child");
                if (contenedor) {
                    contenedor.appendChild(btnGuardar);
                }
            }
        }
    }

    /**
     * Prevenir pérdida de datos al salir
     */
    function configurarPrevencionPerdida() {
        window.addEventListener("beforeunload", (e) => {
            if (hasUnsavedChanges) {
                e.preventDefault();
                e.returnValue = "Tienes cambios sin guardar. ¿Deseas salir?";
                return e.returnValue;
            }
        });
    }

    /**
     * Eliminar borrador al publicar obra
     */
    function configurarEliminacionAlPublicar() {
        form.addEventListener("submit", (e) => {
            const action = e.submitter?.value;

            // Si es "publish", eliminar borrador
            if (action === "publish" && borradorId) {
                eliminarBorrador(borradorId);
            }
        });
    }

    /**
     * Agregar estilos CSS para las animaciones
     */
    function agregarEstilos() {
        const style = document.createElement("style");
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Inicialización
     */
    function init() {
        if (!form) {
            console.warn("Formulario no encontrado");
            return;
        }

        console.log("🚀 Iniciando sistema de borradores...");
        console.log("📋 Formulario:", form.id);
        console.log("🔗 API URLs:", API_URLS);

        agregarEstilos();
        verificarBorradorExistente();
        configurarBotonGuardarBorrador();
        iniciarAutoguardado();
        configurarPrevencionPerdida();
        configurarEliminacionAlPublicar();

        // Detectar cambios en inputs
        form.addEventListener("input", onFormChange);
        form.addEventListener("change", onFormChange);

        console.log("✓ Sistema de borradores inicializado");
    }

    // Inicializar cuando el DOM esté listo
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }

    // Exponer funciones globales
    window.BorradorSystem = {
        guardar: () => guardarBorrador(false),
        cargar: cargarBorrador,
        eliminar: eliminarBorrador,
        verificar: verificarBorradorExistente,
    };
})();
