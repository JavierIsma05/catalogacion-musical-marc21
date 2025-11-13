document.addEventListener('DOMContentLoaded', function () {
    console.log('✅ Script auto_fecha_persona.js cargado correctamente');

    // Detectar todos los select2 de persona dentro de inlines 700
    document.querySelectorAll('select[name$="-persona"]').forEach(function (select) {

        // Escuchar evento de cambio nativo
        select.addEventListener('change', function () {
            // Obtener texto del option seleccionado
            const option = this.options[this.selectedIndex];
            const texto = option ? option.text : '';
            console.log('🧩 Texto seleccionado:', texto);

            // Buscar fechas con regex tipo "1756–1791" o "1546-1610"
            const match = texto.match(/\d{4}[–-]\d{4}/);
            const fecha = match ? match[0] : '';
            console.log('📅 Fecha detectada:', fecha);

            // Buscar el input de fechas dentro del mismo inline
            const inputFecha = this.closest('.inline-related')
                .querySelector('input[name$="-fechas"]');

            if (inputFecha) {
                inputFecha.value = fecha;
                console.log('✅ Campo fechas actualizado:', fecha);
            } else {
                console.warn('⚠️ No se encontró el campo fechas');
            }
        });
    });
});
