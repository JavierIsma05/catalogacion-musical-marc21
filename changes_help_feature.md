# Cambios aplicados para la función de ayuda contextual (650)

Archivos modificados / creados:

- `catalogacion/static/catalogacion/js/field_help_texts.json`
  - Se añadió la entrada para el campo `650` con el texto de ayuda proporcionado. El texto fue colocado en `subfields.a` para que se muestre específicamente cuando se solicite ayuda para el subcampo `$a`.

- `catalogacion/static/catalogacion/js/field_help.js`
  - Se extendió el script para que, además de crear tooltips, gestione clicks en `.campo-help-btn` y abra el modal `#helpModal` rellenando su contenido dinámicamente con los textos del JSON.
  - Implementada la función `openHelpModal(fieldCode, subfield)` que inyecta título y cuerpo en el modal y lo muestra usando Bootstrap.

- `catalogacion/templates/catalogacion/includes/help_modal.html`
  - El `modal-body` fue reemplazado por un contenedor (`#helpModalContent`) cuya `innerHTML` será inyectada por `field_help.js`. Se mantiene el `id="helpModalLabel"` para el título.

- `catalogacion/templates/catalogacion/includes/formset_650_template.html`
  - Se añadieron botones de ayuda `span.campo-help-btn` con `data-field-code="650"` y `data-subfield="a"` junto al input principal de 650 $a.
  - Se añadieron botones `data-subfield="x"` en las filas de subdivisiones para permitir ayuda contextual por $x.

- `catalogacion/templates/catalogacion/secciones/materias_serie.html`
  - El botón de ayuda en la cabecera del campo 650 ahora incluye `data-help-mode="form"`. Al pulsarlo se abre el modal `#helpModal` con un formulario vacío (textarea) en vez de mostrar subcampos.

Nota: Los botones de ayuda por subcampo añadidos inicialmente en `formset_650_template.html` fueron revertidos y ya no están presentes.


Nota: El include `help_modal.html` se agregó en `crear_obra.html` para garantizar que el modal exista en la página donde se cargan `field_help.js`.

Adición: El textarea del modal en modo formulario ahora usa como `placeholder` el texto de ayuda disponible para el campo (si existe) —por ejemplo, la entrada de `650` en `field_help_texts.json`— truncada si es demasiado larga.

Adición: El textarea del modal en modo formulario ahora viene **prellenado** con el texto completo de ayuda para `650` (subcampo `$a`) cuando está disponible, tal como solicitaste.

Notas de uso / prueba rápida:

1. Abrir la página de edición/creación de obra donde aparece el formset 650.
2. Hacer clic en el icono de ayuda en la cabecera del campo 650 para ver la ayuda general del campo.
3. Hacer clic en el icono de ayuda junto al input de 650 $a (o en la ayuda del subcampo $x) para ver el texto específico inyectado en el modal.

Si quieres, puedo seguir y añadir entradas para otros campos/subcampos, o mover los textos a una vista que devuelva JSON para permitir edición desde el servidor.
