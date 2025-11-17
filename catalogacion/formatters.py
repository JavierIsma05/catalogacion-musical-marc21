"""
Clase separada para formatear registros MARC21
Separa responsabilidades: modelo de datos vs presentación
"""


class MARCFormatter:
    """
    Formateador de registros MARC21.
    Genera la salida en formato legible o para exportación.
    """
    
    def __init__(self, obra):
        """
        Inicializa el formateador con una obra.
        
        Args:
            obra: Instancia de ObraGeneral
        """
        self.obra = obra
    
    def format_leader(self):
        """Formatea el Leader (líder del registro)"""
        return (
            f"Leader: "
            f"estado={self.obra.estado_registro} "
            f"tipo={self.obra.tipo_registro} "
            f"nivel={self.obra.nivel_bibliografico}"
        )
    
    def format_001(self):
        """Formatea campo 001 - Número de control"""
        return f"001 {self.obra.num_control}"
    
    def format_005(self):
        """Formatea campo 005 - Fecha/hora última transacción"""
        return f"005 {self.obra.fecha_hora_ultima_transaccion}"
    
    def format_008(self):
        """Formatea campo 008 - Información codificada"""
        return f"008 {self.obra.codigo_informacion}"
    
    def format_020(self):
        """Formatea campo 020 - ISBN"""
        if not self.obra.isbn:
            return None
        return f"020 ## $a{self.obra.isbn}"
    
    def format_024(self):
        """Formatea campo 024 - ISMN"""
        if not self.obra.ismn:
            return None
        return f"024 ## $a{self.obra.ismn}"
    
    def format_028(self):
        """Formatea campo 028 - Número de editor"""
        if not self.obra.numero_editor:
            return None
        
        ind1 = self.obra.tipo_numero_028 or '2'
        ind2 = self.obra.control_nota_028 or '0'
        
        marc = f"028 {ind1}{ind2} $a{self.obra.numero_editor}"
        
        return marc
    
    def format_040(self):
        """Formatea campo 040 - Centro catalogador"""
        return f"040 ## $a{self.obra.centro_catalogador}"
    
    def format_092(self):
        """Formatea campo 092 - Clasificación local"""
        return self.obra.campo_092_marc
    
    def format_100(self):
        """Formatea campo 100 - Compositor principal"""
        if not self.obra.compositor:
            return None
        
        marc = f"100 1# $a{self.obra.compositor.apellidos_nombres}"
        
        if self.obra.termino_asociado:
            marc += f" $c{self.obra.termino_asociado}"
        
        if self.obra.compositor.coordenadas_biograficas:
            marc += f" $d{self.obra.compositor.coordenadas_biograficas}"
        
        if self.obra.autoria and self.obra.autoria != 'certificada':
            marc += f" $j{self.obra.autoria}"
        
        return marc
    
    def format_130(self):
        """Formatea campo 130 - Título uniforme principal"""
        if not self.obra.titulo_uniforme:
            return None
        
        marc = f"130 0# $a{self.obra.titulo_uniforme.titulo}"
        
        if self.obra.forma_130:
            marc += f" $k{self.obra.forma_130.forma}"
        
        if self.obra.medio_interpretacion_130:
            marc += f" $m{self.obra.medio_interpretacion_130}"
        
        if self.obra.numero_parte_130:
            marc += f" $n{self.obra.numero_parte_130}"
        
        if self.obra.arreglo_130:
            marc += f" $o{self.obra.arreglo_130}"
        
        if self.obra.nombre_parte_130:
            marc += f" $p{self.obra.nombre_parte_130}"
        
        if self.obra.tonalidad_130:
            marc += f" $r{self.obra.tonalidad_130}"
        
        return marc
    
    def format_240(self):
        """Formatea campo 240 - Título uniforme secundario"""
        if not self.obra.titulo_240:
            return None
        
        marc = f"240 10 $a{self.obra.titulo_240.titulo}"
        
        if self.obra.forma_240:
            marc += f" $k{self.obra.forma_240.forma}"
        
        if self.obra.medio_interpretacion_240:
            marc += f" $m{self.obra.medio_interpretacion_240}"
        
        if self.obra.numero_parte_240:
            marc += f" $n{self.obra.numero_parte_240}"
        
        if self.obra.arreglo_240:
            marc += f" $o{self.obra.arreglo_240}"
        
        if self.obra.nombre_parte_240:
            marc += f" $p{self.obra.nombre_parte_240}"
        
        if self.obra.tonalidad_240:
            marc += f" $r{self.obra.tonalidad_240}"
        
        return marc
    
    def format_245(self):
        """Formatea campo 245 - Título principal"""
        marc = f"245 10 $a{self.obra.titulo_principal}"
        
        if self.obra.subtitulo:
            marc += f" $b{self.obra.subtitulo}"
        
        if self.obra.mencion_responsabilidad:
            marc += f" $c{self.obra.mencion_responsabilidad}"
        
        return marc
    
    def format_300(self):
        """Formatea campo 300 - Descripción física"""
        if not any([self.obra.extension, self.obra.otras_caracteristicas, 
                    self.obra.dimension, self.obra.material_acompanante]):
            return None
        
        marc = "300 ##"
        
        if self.obra.extension:
            marc += f" $a{self.obra.extension}"
        
        if self.obra.otras_caracteristicas:
            marc += f" $b{self.obra.otras_caracteristicas}"
        
        if self.obra.dimension:
            marc += f" $c{self.obra.dimension}"
        
        if self.obra.material_acompanante:
            marc += f" $e{self.obra.material_acompanante}"
        
        return marc
    
    def format_340(self):
        """Formatea campo 340 - Técnica"""
        if not self.obra.ms_imp:
            return None
        return f"340 ## $d{self.obra.ms_imp}"
    
    def format_348(self):
        """Formatea campo 348 - Formato"""
        if not self.obra.formato:
            return None
        return f"348 ## $a{self.obra.formato}"
    
    def format_382(self):
        """Formatea campo 382 - Medio de interpretación"""
        if not self.obra.solista:
            return None
        return f"382 ## $b{self.obra.solista}"
    
    def format_383(self):
        """Formatea campo 383 - Designación numérica"""
        if not any([self.obra.numero_obra, self.obra.opus]):
            return None
        
        marc = "383 ##"
        
        if self.obra.numero_obra:
            marc += f" $a{self.obra.numero_obra}"
        
        if self.obra.opus:
            marc += f" $b{self.obra.opus}"
        
        return marc
    
    def format_384(self):
        """Formatea campo 384 - Tonalidad"""
        if not self.obra.tonalidad_384:
            return None
        return f"384 ## $a{self.obra.tonalidad_384}"
    
    def format_520(self):
        """Formatea campo 520 - Sumario"""
        if not self.obra.sumario_520:
            return None
        return f"520 ## $a{self.obra.sumario_520}"
    
    def format_650(self):
        """Formatea campo 650 - Materia"""
        if not self.obra.materia_principal_650:
            return None
        return f"650 #0 $a{self.obra.materia_principal_650}"
    
    def format_655(self):
        """Formatea campo 655 - Género/Forma"""
        if not self.obra.materia_genero_655:
            return None
        return f"655 #7 $a{self.obra.materia_genero_655}"
    
    def format_full_record(self):
        """
        Genera el registro completo en formato MARC legible.
        
        Returns:
            str: Registro MARC completo con saltos de línea
        """
        campos = [
            self.format_leader(),
            self.format_001(),
            self.format_005(),
            self.format_008(),
            self.format_020(),
            self.format_024(),
            self.format_028(),
            self.format_040(),
            self.format_092(),
            self.format_100(),
            self.format_130(),
            self.format_240(),
            self.format_245(),
            self.format_300(),
            self.format_340(),
            self.format_348(),
            self.format_382(),
            self.format_383(),
            self.format_384(),
            self.format_520(),
            self.format_650(),
            self.format_655(),
        ]
        
        # Filtrar campos None y unir con saltos de línea
        campos_validos = [c for c in campos if c is not None]
        return "\n".join(campos_validos)
    
    def to_dict(self):
        """
        Genera un diccionario con todos los campos MARC.
        Útil para exportación JSON o procesamiento adicional.
        
        Returns:
            dict: Diccionario con estructura MARC
        """
        return {
            'leader': {
                'estado': self.obra.estado_registro,
                'tipo': self.obra.tipo_registro,
                'nivel': self.obra.nivel_bibliografico,
            },
            '001': self.obra.num_control,
            '005': self.obra.fecha_hora_ultima_transaccion,
            '008': self.obra.codigo_informacion,
            '020': {'a': self.obra.isbn} if self.obra.isbn else None,
            '024': {'a': self.obra.ismn} if self.obra.ismn else None,
            '028': {
                'ind1': self.obra.tipo_numero_028,
                'ind2': self.obra.control_nota_028,
                'a': self.obra.numero_editor,
            } if self.obra.numero_editor else None,
            '040': {'a': self.obra.centro_catalogador},
            '100': {
                'a': str(self.obra.compositor),
                'c': self.obra.termino_asociado,
                'd': self.obra.compositor.coordenadas_biograficas if self.obra.compositor else None,
                'j': self.obra.autoria,
            } if self.obra.compositor else None,
            '130': {
                'a': str(self.obra.titulo_uniforme),
                'k': str(self.obra.forma_130) if self.obra.forma_130 else None,
                'm': self.obra.medio_interpretacion_130,
                'n': self.obra.numero_parte_130,
                'o': self.obra.arreglo_130,
                'p': self.obra.nombre_parte_130,
                'r': self.obra.tonalidad_130,
            } if self.obra.titulo_uniforme else None,
            '240': {
                'a': str(self.obra.titulo_240),
                'k': str(self.obra.forma_240) if self.obra.forma_240 else None,
                'm': self.obra.medio_interpretacion_240,
                'n': self.obra.numero_parte_240,
                'o': self.obra.arreglo_240,
                'p': self.obra.nombre_parte_240,
                'r': self.obra.tonalidad_240,
            } if self.obra.titulo_240 else None,
            '245': {
                'a': self.obra.titulo_principal,
                'b': self.obra.subtitulo,
                'c': self.obra.mencion_responsabilidad,
            },
            '300': {
                'a': self.obra.extension,
                'b': self.obra.otras_caracteristicas,
                'c': self.obra.dimension,
                'e': self.obra.material_acompanante,
            } if any([self.obra.extension, self.obra.otras_caracteristicas]) else None,
            # ... más campos según necesidad
        }
    
    def __str__(self):
        """Representación en string del registro completo"""
        return self.format_full_record()