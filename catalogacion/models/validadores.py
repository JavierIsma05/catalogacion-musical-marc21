"""
Validadores especializados por tipo de obra MARC21
Separa la lógica de validación del modelo principal
"""
from django.core.exceptions import ValidationError


class ValidadorBase:
    """Clase base para validadores de obras"""
    
    def __init__(self, obra):
        self.obra = obra
        self.errores = {}
    
    def validar(self):
        """Método principal de validación"""
        self.validar_campos_obligatorios()
        self.validar_punto_acceso_principal()
        self.validar_reglas_especificas()
        
        if self.errores:
            raise ValidationError(self.errores)
    
    def validar_campos_obligatorios(self):
        """Valida campos obligatorios básicos"""
        if not self.obra.titulo_principal or not self.obra.titulo_principal.strip():
            self.errores['titulo_principal'] = "El título principal (245 $a) es obligatorio."
    
    def validar_punto_acceso_principal(self):
        """Valida el punto de acceso principal (100 vs 130)"""
        if self.obra.compositor and self.obra.titulo_uniforme:
            self.errores['compositor'] = (
                "Si hay compositor (campo 100), use campo 240 para el título uniforme."
            )
            self.errores['titulo_uniforme'] = (
                "No puede usar campo 130 cuando hay compositor."
            )
        
        if not self.obra.compositor and self.obra.titulo_240:
            self.errores['titulo_240'] = (
                "El campo 240 solo se usa cuando hay compositor (campo 100)."
            )
        
        if not self.obra.compositor and not self.obra.titulo_uniforme:
            self.errores['compositor'] = (
                "Debe existir un punto de acceso principal: complete 100 o 130."
            )
            self.errores['titulo_uniforme'] = (
                "Debe existir un punto de acceso principal: complete 130 o 100."
            )
    
    def validar_reglas_especificas(self):
        """Método para sobrescribir en subclases"""
        pass


class ValidadorColeccion(ValidadorBase):
    """Validador para colecciones (nivel_bibliografico = 'c')"""
    
    def validar_reglas_especificas(self):
        """Validaciones específicas para colecciones"""
        # Una colección debe tener obras componentes (774)
        if self.obra.pk is None:
            unidades = self.obra.enlaces_unidades_774.count()
            if unidades == 0:
                self.errores['__all__'] = (
                    "Una colección debe tener al menos una obra componente (campo 774)."
                )
        
        # Validar que no sea parte de otra colección
        if self.obra.pk and self.obra.enlaces_documento_fuente_773.exists():
            self.errores['__all__'] = (
                "Una colección no puede ser parte de otra colección (campo 773)."
            )


class ValidadorObraEnColeccion(ValidadorBase):
    """Validador para obras que forman parte de una colección (nivel_bibliografico = 'a')"""
    
    def validar_reglas_especificas(self):
        """Validaciones específicas para obras en colección"""
        # Debe tener referencia a la colección contenedora (773)
        if self.obra.pk:
            if not self.obra.enlaces_documento_fuente_773.exists():
                self.errores['__all__'] = (
                    "Una obra componente debe tener referencia a su colección "
                    "contenedora (campo 773)."
                )
        
        # No debe tener unidades constituyentes (774)
        if self.obra.pk and self.obra.enlaces_unidades_774.exists():
            self.errores['__all__'] = (
                "Una obra componente no puede tener unidades constituyentes (campo 774)."
            )


class ValidadorObraIndependiente(ValidadorBase):
    """Validador para obras independientes (nivel_bibliografico = 'm')"""
    
    def validar_reglas_especificas(self):
        """Validaciones específicas para obras independientes"""
        # Una obra independiente no debe tener 773 ni 774
        if self.obra.pk:
            if self.obra.enlaces_documento_fuente_773.exists():
                self.errores['__all__'] = (
                    "Una obra independiente no debe tener referencia a colección "
                    "contenedora (campo 773)."
                )
            
            if self.obra.enlaces_unidades_774.exists():
                self.errores['__all__'] = (
                    "Una obra independiente no debe tener unidades constituyentes "
                    "(campo 774). Cambie el nivel bibliográfico a 'c' (Colección)."
                )


class ValidadorObraImpresa(ValidadorBase):
    """Validador adicional para obras impresas (tipo_registro = 'c')"""
    
    def validar_reglas_especificas(self):
        """Validaciones específicas para obras impresas"""
        super().validar_reglas_especificas()
        
        # Advertir si no tiene ISBN o ISMN (no es error, solo advertencia)
        if not self.obra.isbn and not self.obra.ismn:
            # No es un error crítico, solo una nota
            pass


class ValidadorObraManuscrita(ValidadorBase):
    """Validador adicional para obras manuscritas (tipo_registro = 'd')"""
    
    def validar_reglas_especificas(self):
        """Validaciones específicas para obras manuscritas"""
        super().validar_reglas_especificas()
        
        # Los manuscritos no deben tener ISBN/ISMN
        if self.obra.isbn or self.obra.ismn:
            self.errores['isbn'] = (
                "Los manuscritos no deben tener ISBN o ISMN. "
                "Estos campos son solo para obras impresas."
            )


def obtener_validador(obra):
    """
    Factory function que retorna el validador apropiado según el tipo de obra
    """
    # Primero determinar el validador base según nivel bibliográfico
    validadores_base = {
        'c': ValidadorColeccion,
        'a': ValidadorObraEnColeccion,
        'm': ValidadorObraIndependiente,
    }
    
    ValidadorClase = validadores_base.get(obra.nivel_bibliografico, ValidadorBase)
    
    # Si es impresa o manuscrita, podríamos agregar validaciones adicionales
    # Por ahora, usamos solo el validador base
    return ValidadorClase(obra)


