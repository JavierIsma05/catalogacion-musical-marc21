/**
 * Validación Pre-Envío de Formulario de Obra
 * Verifica campos requeridos ANTES de intentar enviar
 * Muestra mensajes claros al usuario sobre qué falta
 */

console.log("✅ [FORM-VALIDATOR] Script cargado");

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('obra-form');

    if (!form) {
        console.log("⚠️  [FORM-VALIDATOR] No se encontró #obra-form");
        return;
    }
    
    // Campos obligatorios del formulario principal
    const CAMPOS_OBLIGATORIOS = {
        'tipo_registro': 'Tipo de Registro',
        'nivel_bibliografico': 'Nivel Bibliográfico',
        'centro_catalogador': 'Centro Catalogador',
        'titulo_principal': 'Título Principal',
        'ms_imp': 'Técnica / Soporte',
    };
    
    // Campos de punto de acceso (al menos uno debe estar lleno)
    const CAMPOS_PUNTO_ACCESO = {
        'compositor': 'Compositor',
        'compositor_texto': 'Compositor (texto)',
        'titulo_uniforme': 'Título Uniforme',
        'titulo_uniforme_texto': 'Título Uniforme (texto)',
    };
    
    /**
     * Obtener valor limpio de un campo
     */
    function getFieldValue(fieldName) {
        const field = form.querySelector(`[name="${fieldName}"]`);
        if (!field) return null;
        
        if (field.type === 'checkbox') return field.checked;
        return (field.value || '').trim();
    }
    
    /**
     * Validar campos obligatorios individuales
     */
    function validarCamposObligatorios() {
        const errores = [];
        
        for (const [fieldName, fieldLabel] of Object.entries(CAMPOS_OBLIGATORIOS)) {
            const value = getFieldValue(fieldName);
            
            if (!value) {
                errores.push(`❌ ${fieldLabel} es obligatorio`);
            }
        }
        
        return errores;
    }
    
    /**
     * Validar que existe al menos un punto de acceso
     */
    function validarPuntoAcceso() {
        let tieneCompositor = false;
        let tieneTituloUniforme = false;
        
        // Verificar compositor
        if (getFieldValue('compositor') || getFieldValue('compositor_texto')) {
            tieneCompositor = true;
        }
        
        // Verificar título uniforme
        if (getFieldValue('titulo_uniforme') || getFieldValue('titulo_uniforme_texto')) {
            tieneTituloUniforme = true;
        }
        
        if (!tieneCompositor && !tieneTituloUniforme) {
            return ["❌ Debe especificar AL MENOS UNO de:\n   • Compositor (100)\n   • Título Uniforme (130)"];
        }
        
        return [];
    }
    
    /**
     * Validar ManagementForms de formsets
     */
    function validarFormsets() {
        const errores = [];
        const prefijos = [
            'incipits', 'lenguas', 'paises', 'funciones', 'medios_382',
            'titulos_alt', 'ediciones', 'produccion', 'menciones_490',
            'notas_500', 'contenidos_505', 'sumarios_520', 'biograficos_545',
            'materias_650', 'generos_655', 'nombres_700', 'entidades_710',
            'enlaces_773', 'enlaces_774', 'relaciones_787', 'ubicaciones_852',
            'disponibles_856'
        ];
        
        for (const prefix of prefijos) {
            const totalField = form.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
            const initialField = form.querySelector(`input[name="${prefix}-INITIAL_FORMS"]`);
            
            if (!totalField || !initialField) {
                console.warn(`⚠️  [FORM-VALIDATOR] Formset ${prefix} sin ManagementForm`);
                // No consideramos esto un error fatal, algunos formsets pueden no estar en la página
            }
        }
        
        return errores;
    }
    
    /**
     * Mostrar modal de error al usuario
     */
    function mostrarErrores(errores) {
        // Crear contenedor de error si no existe
        let errorContainer = document.getElementById('form-validation-errors');
        
        if (!errorContainer) {
            errorContainer = document.createElement('div');
            errorContainer.id = 'form-validation-errors';
            errorContainer.style.cssText = `
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: #f8d7da;
                border: 2px solid #f5c6cb;
                border-radius: 8px;
                padding: 20px;
                max-width: 600px;
                z-index: 9999;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            `;
            document.body.appendChild(errorContainer);
        }
        
        // Generar HTML de errores
        const errorList = errores
            .map(e => `<li style="margin: 8px 0; font-size: 14px; white-space: pre-wrap;">${e}</li>`)
            .join('');
        
        errorContainer.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: #721c24;">⚠️ Errores en el formulario</h4>
                    <ul style="margin: 0; padding-left: 20px; color: #721c24;">
                        ${errorList}
                    </ul>
                </div>
                <button onclick="this.parentElement.parentElement.style.display='none'" 
                        style="background: none; border: none; font-size: 20px; cursor: pointer; padding: 0;">×</button>
            </div>
        `;
        
        // Mostrar durante 8 segundos (o hasta que cierren)
        setTimeout(() => {
            if (errorContainer.style.display !== 'none') {
                errorContainer.style.display = 'none';
            }
        }, 8000);
        
        // Scroll al error
        errorContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    /**
     * Manejador del submit del formulario
     */
    form.addEventListener('submit', function(e) {
        console.log("📤 [FORM-VALIDATOR] Evento submit detectado");
        
        // Recolectar todos los errores
        let todosLosErrores = [];
        
        todosLosErrores.push(...validarCamposObligatorios());
        todosLosErrores.push(...validarPuntoAcceso());
        todosLosErrores.push(...validarFormsets());
        
        // Si hay errores, mostrar y prevenir submit
        if (todosLosErrores.length > 0) {
            console.error("❌ [FORM-VALIDATOR] Errores encontrados:", todosLosErrores);
            
            e.preventDefault();
            mostrarErrores(todosLosErrores);
            
            return false;
        }
        
        console.log("✅ [FORM-VALIDATOR] Validación OK - permitiendo submit");
    }, false);
    
    console.log("✅ [FORM-VALIDATOR] Listener de submit agregado");
});
