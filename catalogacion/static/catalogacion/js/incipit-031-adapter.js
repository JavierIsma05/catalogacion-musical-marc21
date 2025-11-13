// Adapter mínimo entre el formulario Django (031) y el motor incipitManager.js
// Usa el objeto global CanvasIncipit que crea incipitManager.js.

(function () {
  // Verificamos que el legacy se haya cargado
  if (typeof window.CanvasIncipit === "undefined") {
    console.warn("incipit-031-adapter: CanvasIncipit no está disponible");
    return;
  }

  // 1) Envolvemos el método TransformIncipitToPAEC del objeto CanvasIncipit
  var originalTransform = CanvasIncipit.TransformIncipitToPAEC
    ? CanvasIncipit.TransformIncipitToPAEC.bind(CanvasIncipit)
    : null;

  if (!originalTransform) {
    console.warn(
      "incipit-031-adapter: CanvasIncipit.TransformIncipitToPAEC no está definido"
    );
  } else {
    CanvasIncipit.TransformIncipitToPAEC = function (context) {
      // Ejecutar lógica original del legacy
      originalTransform(context);

      // Leer el PAE que el legacy escribe en #incipitPaec
      var paecInput = document.getElementById("incipitPaec");
      var paeCode = paecInput ? paecInput.value : "";


      // Copiar al textarea oficial del 031 $p (primer incipit)
      var textareaP = document.getElementById("incipit_p_0");
      if (textareaP && typeof paeCode === "string") {
        textareaP.value = paeCode;
      }
    };
  }

  // 2) Inicializar el canvas del primer incipit una vez cargado el DOM
  document.addEventListener("DOMContentLoaded", function () {
    var canvasEl = document.getElementById("incipit_canvas_0");
    if (!canvasEl) {
      console.warn("incipit-031-adapter: no se encontró #incipit_canvas_0");
      return;
    }

    // Asegurarnos de que existen los hidden con los ids que espera el legacy
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

    // Inicializar el canvas del legacy: 'add' = nuevo incipit editable
    // Tercer parámetro = PAE inicial (vacío al crear)
    CanvasIncipit.initializeCanvas("incipit_canvas_0", "add", "");
  });
})();
