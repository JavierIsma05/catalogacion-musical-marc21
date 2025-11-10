// Adapter mínimo entre el formulario Django (031) y el motor incipitManager.js
// Requiere que incipitManager.js ya haya cargado y definido CanvasIncipit y TransformIncipitToPAEC.

(function () {
  // Si por lo que sea el legacy no está cargado, salimos
  if (
    typeof CanvasIncipit === "undefined" ||
    typeof TransformIncipitToPAEC === "undefined"
  ) {
    console.warn(
      "incipit-031-adapter: CanvasIncipit o TransformIncipitToPAEC no están disponibles"
    );
    return;
  }

  // 1) Envolvemos la función global TransformIncipitToPAEC para copiar el PAE al textarea Django
  var originalTransform = window.TransformIncipitToPAEC;

  window.TransformIncipitToPAEC = function (context) {
    // Ejecutar la lógica original (calcula paec, var031p, etc. y escribe en #incipitPaec)
    originalTransform(context);

    // Leer el PAE que el legacy escribió en #incipitPaec
    var paecInput = document.getElementById("incipitPaec");
    var paeCode = paecInput ? paecInput.value : "";

    // Copiar al textarea oficial del 031 $p (primer incipit)
    var textareaP = document.getElementById("incipit_p_0");
    if (textareaP && paeCode !== undefined) {
      textareaP.value = paeCode;
    }
  };

  // 2) Inicializar el canvas del primer incipit al cargar la página
  document.addEventListener("DOMContentLoaded", function () {
    var canvasEl = document.getElementById("incipit_canvas_0");
    if (!canvasEl) {
      console.warn("incipit-031-adapter: no se encontró #incipit_canvas_0");
      return;
    }

    // Asegurarnos de que existen los hidden con los ids que el legacy espera
    var hiddenPaec = document.getElementById("incipitPaec");
    if (!hiddenPaec) {
      hiddenPaec = document.createElement("input");
      hiddenPaec.type = "hidden";
      hiddenPaec.id = "incipitPaec";
      hiddenPaec.name = "incipit_paec_0";
      canvasEl.parentNode.appendChild(hiddenPaec);
    }

    var hiddenTransp = document.getElementById("incipitTransposition");
    if (!hiddenTransp) {
      hiddenTransp = document.createElement("input");
      hiddenTransp.type = "hidden";
      hiddenTransp.id = "incipitTransposition";
      hiddenTransp.name = "incipit_transp_0";
      canvasEl.parentNode.appendChild(hiddenTransp);
    }

    // Inicializar el canvas con la operación "add" (nuevo incipit editable)
    // Tercer parámetro = PAE inicial (cadena vacía al crear)
    CanvasIncipit.initializeCanvas("incipit_canvas_0", "add", "");
  });
})();
