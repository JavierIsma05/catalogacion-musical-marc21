/**
 * subcampo-validators.js
 * Validaciones en tiempo real para subcampos repetibles
 * Evita duplicados dentro del mismo campo y muestra errores visibles
 */

(function () {
    "use strict";

    /**
     * Clase para manejar validaciones de subcampos
     */
    class SubcampoValidator {
        constructor() {
            this.errorClass = "subcampo-error";
            this.errorMessageClass = "subcampo-error-message";
            this.init();
        }

        init() {
            // Escuchar cambios en todos los selects de subcampos
            document.addEventListener("change", (e) => {
                const select = e.target.closest("select");
                if (!select) return;

                // Validar según el tipo de subcampo
                if (select.classList.contains("idioma-select")) {
                    this.validateIdiomasInContainer(select);
                } else if (select.classList.contains("medio-select")) {
                    this.validateMediosInContainer(select);
                } else if (
                    select.classList.contains("lugar-input") ||
                    select.classList.contains("entidad-input") ||
                    select.classList.contains("fecha-input")
                ) {
                    // Para inputs de texto (264)
                    this.validateTextInputsInContainer(select);
                }
            });

            // También validar inputs de texto
            document.addEventListener("input", (e) => {
                const input = e.target;
                if (!input.matches('input[type="text"]')) return;

                if (
                    input.classList.contains("lugar-input") ||
                    input.classList.contains("entidad-input") ||
                    input.classList.contains("fecha-input") ||
                    input.classList.contains("titulo-input") ||
                    input.classList.contains("volumen-input")
                ) {
                    this.validateTextInputsInContainer(input);
                }
            });

            // Validar al agregar nuevos elementos
            document.addEventListener("click", (e) => {
                // Esperar un poco para que el DOM se actualice
                setTimeout(() => {
                    const container = e.target.closest(
                        ".subcampo-repetible-container"
                    );
                    if (container) {
                        this.validateContainer(container);
                    }
                }, 100);
            });
        }

        /**
         * Valida idiomas dentro de un contenedor de campo 041
         */
        validateIdiomasInContainer(changedSelect) {
            const container = changedSelect.closest(
                ".subcampo-repetible-container"
            );
            if (!container) return;

            const selects = container.querySelectorAll(".idioma-select");
            const values = [];
            const duplicates = new Set();

            // Encontrar duplicados
            selects.forEach((select) => {
                const value = select.value;
                if (value && value !== "") {
                    if (values.includes(value)) {
                        duplicates.add(value);
                    }
                    values.push(value);
                }
            });

            // Marcar/desmarcar errores
            selects.forEach((select) => {
                const value = select.value;
                const row = select.closest(".subcampo-row");

                if (value && duplicates.has(value)) {
                    this.showError(
                        select,
                        row,
                        "Este idioma ya está seleccionado en este campo 041"
                    );
                } else {
                    this.clearError(select, row);
                }
            });

            return duplicates.size === 0;
        }

        /**
         * Valida medios de interpretación dentro de un contenedor de campo 382
         */
        validateMediosInContainer(changedSelect) {
            const container = changedSelect.closest(
                ".subcampo-repetible-container"
            );
            if (!container) return;

            const selects = container.querySelectorAll(".medio-select");
            const values = [];
            const duplicates = new Set();

            selects.forEach((select) => {
                const value = select.value;
                if (value && value !== "") {
                    if (values.includes(value)) {
                        duplicates.add(value);
                    }
                    values.push(value);
                }
            });

            selects.forEach((select) => {
                const value = select.value;
                const row = select.closest(".subcampo-row");

                if (value && duplicates.has(value)) {
                    this.showError(
                        select,
                        row,
                        "Este medio ya está seleccionado en este campo 382"
                    );
                } else {
                    this.clearError(select, row);
                }
            });

            return duplicates.size === 0;
        }

        /**
         * Valida inputs de texto dentro de un contenedor (264, 490)
         */
        validateTextInputsInContainer(changedInput) {
            const container = changedInput.closest(
                ".subcampo-repetible-container"
            );
            if (!container) return;

            // Determinar qué clase de input buscar
            let inputClass = "";
            let fieldName = "";

            if (changedInput.classList.contains("lugar-input")) {
                inputClass = ".lugar-input";
                fieldName = "lugar";
            } else if (changedInput.classList.contains("entidad-input")) {
                inputClass = ".entidad-input";
                fieldName = "entidad";
            } else if (changedInput.classList.contains("fecha-input")) {
                inputClass = ".fecha-input";
                fieldName = "fecha";
            } else if (changedInput.classList.contains("titulo-input")) {
                inputClass = ".titulo-input";
                fieldName = "título de serie";
            } else if (changedInput.classList.contains("volumen-input")) {
                inputClass = ".volumen-input";
                fieldName = "volumen";
            } else {
                return;
            }

            const inputs = container.querySelectorAll(inputClass);
            const values = [];
            const duplicates = new Set();

            inputs.forEach((input) => {
                const value = input.value.trim().toLowerCase();
                if (value && value !== "") {
                    if (values.includes(value)) {
                        duplicates.add(value);
                    }
                    values.push(value);
                }
            });

            inputs.forEach((input) => {
                const value = input.value.trim().toLowerCase();
                const row = input.closest(".subcampo-row");

                if (value && duplicates.has(value)) {
                    this.showError(
                        input,
                        row,
                        `Este ${fieldName} ya está ingresado en este campo`
                    );
                } else {
                    this.clearError(input, row);
                }
            });

            return duplicates.size === 0;
        }

        /**
         * Valida todos los elementos de un contenedor
         */
        validateContainer(container) {
            // Validar selects de idioma
            const idiomaSelect = container.querySelector(".idioma-select");
            if (idiomaSelect) {
                this.validateIdiomasInContainer(idiomaSelect);
            }

            // Validar selects de medio
            const medioSelect = container.querySelector(".medio-select");
            if (medioSelect) {
                this.validateMediosInContainer(medioSelect);
            }

            // Validar inputs de texto
            const textInputs = container.querySelectorAll(
                ".lugar-input, .entidad-input, .fecha-input, .titulo-input, .volumen-input"
            );
            if (textInputs.length > 0) {
                this.validateTextInputsInContainer(textInputs[0]);
            }
        }

        /**
         * Muestra un mensaje de error en el elemento
         */
        showError(element, row, message) {
            // Marcar el elemento con error
            element.classList.add(this.errorClass);
            element.classList.add("is-invalid");

            // Marcar la fila
            if (row) {
                row.classList.add("has-error");
            }

            // Buscar o crear el mensaje de error
            let errorMsg = row
                ? row.querySelector("." + this.errorMessageClass)
                : null;

            if (!errorMsg && row) {
                errorMsg = document.createElement("div");
                errorMsg.className =
                    this.errorMessageClass + " invalid-feedback d-block";
                row.appendChild(errorMsg);
            }

            if (errorMsg) {
                errorMsg.textContent = message;
                errorMsg.style.display = "block";
            }

            // Agregar un indicador visual más notorio
            if (row && !row.querySelector(".error-icon")) {
                const icon = document.createElement("span");
                icon.className = "error-icon text-danger ms-2";
                icon.innerHTML =
                    '<i class="bi bi-exclamation-triangle-fill"></i>';
                icon.title = message;

                const selectOrInput = row.querySelector(
                    'select, input[type="text"]'
                );
                if (selectOrInput && selectOrInput.parentNode) {
                    selectOrInput.parentNode.style.position = "relative";
                }
            }
        }

        /**
         * Limpia el error de un elemento
         */
        clearError(element, row) {
            element.classList.remove(this.errorClass);
            element.classList.remove("is-invalid");

            if (row) {
                row.classList.remove("has-error");

                // Remover mensaje de error
                const errorMsg = row.querySelector(
                    "." + this.errorMessageClass
                );
                if (errorMsg) {
                    errorMsg.style.display = "none";
                }

                // Remover icono de error
                const errorIcon = row.querySelector(".error-icon");
                if (errorIcon) {
                    errorIcon.remove();
                }
            }
        }

        /**
         * Valida todos los subcampos antes de enviar el formulario
         * Retorna true si todo está válido, false si hay errores
         */
        validateAll() {
            let isValid = true;
            const errors = [];

            // Validar todos los contenedores de idiomas
            document
                .querySelectorAll("[data-idiomas-container]")
                .forEach((container) => {
                    const select = container.querySelector(".idioma-select");
                    if (select && !this.validateIdiomasInContainer(select)) {
                        isValid = false;
                        errors.push("Hay idiomas duplicados en el campo 041");
                    }
                });

            // Validar todos los contenedores de medios
            document
                .querySelectorAll("[data-medios-container]")
                .forEach((container) => {
                    const select = container.querySelector(".medio-select");
                    if (select && !this.validateMediosInContainer(select)) {
                        isValid = false;
                        errors.push("Hay medios duplicados en el campo 382");
                    }
                });

            // Validar lugares, entidades, fechas (264)
            document
                .querySelectorAll("[data-lugares-container]")
                .forEach((container) => {
                    const input = container.querySelector(".lugar-input");
                    if (input && !this.validateTextInputsInContainer(input)) {
                        isValid = false;
                        errors.push("Hay lugares duplicados en el campo 264");
                    }
                });

            document
                .querySelectorAll("[data-entidades-container]")
                .forEach((container) => {
                    const input = container.querySelector(".entidad-input");
                    if (input && !this.validateTextInputsInContainer(input)) {
                        isValid = false;
                        errors.push("Hay entidades duplicadas en el campo 264");
                    }
                });

            document
                .querySelectorAll("[data-fechas-container]")
                .forEach((container) => {
                    const input = container.querySelector(".fecha-input");
                    if (input && !this.validateTextInputsInContainer(input)) {
                        isValid = false;
                        errors.push("Hay fechas duplicadas en el campo 264");
                    }
                });

            // Validar títulos y volúmenes (490)
            document
                .querySelectorAll("[data-titulos-container]")
                .forEach((container) => {
                    const input = container.querySelector(".titulo-input");
                    if (input && !this.validateTextInputsInContainer(input)) {
                        isValid = false;
                        errors.push("Hay títulos duplicados en el campo 490");
                    }
                });

            document
                .querySelectorAll("[data-volumenes-container]")
                .forEach((container) => {
                    const input = container.querySelector(".volumen-input");
                    if (input && !this.validateTextInputsInContainer(input)) {
                        isValid = false;
                        errors.push("Hay volúmenes duplicados en el campo 490");
                    }
                });

            return { isValid, errors };
        }

        /**
         * Muestra un resumen de errores al usuario
         */
        showErrorSummary(errors) {
            if (errors.length === 0) return;

            // Buscar el primer elemento con error y hacer scroll hacia él
            const firstError = document.querySelector(
                ".subcampo-error, .has-error"
            );
            if (firstError) {
                firstError.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                });

                // Resaltar temporalmente
                firstError.style.animation = "pulse-error 0.5s ease-in-out 3";
                setTimeout(() => {
                    firstError.style.animation = "";
                }, 1500);
            }

            // Mostrar alerta con los errores
            const uniqueErrors = [...new Set(errors)];
            const message =
                "Por favor corrija los siguientes errores antes de guardar:\n\n• " +
                uniqueErrors.join("\n• ");

            // Si existe SweetAlert2, usarlo
            if (typeof Swal !== "undefined") {
                Swal.fire({
                    icon: "warning",
                    title: "Errores de validación",
                    html:
                        '<ul class="text-start">' +
                        uniqueErrors.map((e) => `<li>${e}</li>`).join("") +
                        "</ul>",
                    confirmButtonText: "Entendido",
                });
            } else {
                alert(message);
            }
        }
    }

    // Crear instancia global
    window.SubcampoValidator = new SubcampoValidator();

    // Interceptar envío del formulario para validar duplicados
    document.addEventListener("DOMContentLoaded", function () {
        const form = document.getElementById("obra-form");
        if (form) {
            // Interceptar antes del submit
            form.addEventListener(
                "submit",
                function (e) {
                    const validation = window.SubcampoValidator.validateAll();

                    if (!validation.isValid) {
                        e.preventDefault();
                        e.stopPropagation();
                        window.SubcampoValidator.showErrorSummary(
                            validation.errors
                        );
                        return false;
                    }
                },
                true
            ); // Captura temprana
        }
    });

    // Agregar estilos CSS para los errores
    const style = document.createElement("style");
    style.textContent = `
        .subcampo-error {
            border-color: #dc3545 !important;
            box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25) !important;
        }
        
        .subcampo-row.has-error {
            background-color: rgba(220, 53, 69, 0.05);
            border-radius: 4px;
            padding: 4px;
            margin: -4px;
        }
        
        .subcampo-error-message {
            font-size: 0.8rem;
            color: #dc3545;
            margin-top: 4px;
            padding-left: 40px;
        }
        
        .error-icon {
            position: absolute;
            right: 45px;
            top: 50%;
            transform: translateY(-50%);
            z-index: 10;
        }
        
        @keyframes pulse-error {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); box-shadow: 0 0 10px rgba(220, 53, 69, 0.5); }
        }
    `;
    document.head.appendChild(style);
})();
