"""
Comando de gestión para limpiar borradores antiguos.

Este comando marca como 'descartado' todos los borradores activos que tengan
más de un determinado número de días sin modificarse.

Uso:
    python manage.py limpiar_borradores [--dias=30] [--dry-run]

Opciones:
    --dias: Número de días de antigüedad (default: 30)
    --dry-run: Simular la operación sin modificar la base de datos
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from catalogacion.models.borradores import BorradorObra


class Command(BaseCommand):
    help = 'Marca como descartados los borradores activos antiguos que no han sido modificados en un tiempo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dias',
            type=int,
            default=30,
            help='Número de días de antigüedad para considerar un borrador como antiguo (default: 30)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular la operación sin modificar la base de datos'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Mostrar información detallada de los borradores procesados'
        )

    def handle(self, *args, **options):
        dias = options['dias']
        dry_run = options['dry_run']
        verbose = options['verbose']

        # Calcular fecha límite
        fecha_limite = timezone.now() - timedelta(days=dias)

        # Buscar borradores activos antiguos
        borradores_antiguos = BorradorObra.objects.filter(
            estado='activo',
            fecha_modificacion__lt=fecha_limite
        ).select_related('usuario')

        total = borradores_antiguos.count()

        if total == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ No se encontraron borradores activos con más de {dias} días de antigüedad.'
                )
            )
            return

        # Modo dry-run
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'SIMULACIÓN: Se descartarían {total} borrador(es):'
                )
            )
            if verbose:
                for borrador in borradores_antiguos:
                    dias_antiguedad = (timezone.now() - borrador.fecha_modificacion).days
                    self.stdout.write(
                        f'  • ID {borrador.id}: "{borrador.titulo_temporal or "Sin título"}" '
                        f'(Usuario: {borrador.usuario.username if borrador.usuario else "N/A"}, '
                        f'Antigüedad: {dias_antiguedad} días)'
                    )
            self.stdout.write(
                self.style.WARNING(
                    '\nEjecuta el comando sin --dry-run para aplicar los cambios.'
                )
            )
            return

        # Procesar borradores
        if verbose:
            self.stdout.write(f'Procesando {total} borrador(es)...\n')
            for borrador in borradores_antiguos:
                dias_antiguedad = (timezone.now() - borrador.fecha_modificacion).days
                self.stdout.write(
                    f'  • Descartando ID {borrador.id}: "{borrador.titulo_temporal or "Sin título"}" '
                    f'(Antigüedad: {dias_antiguedad} días)'
                )

        # Actualizar estado en lote
        borradores_actualizados = borradores_antiguos.update(estado='descartado')

        # Mensaje de éxito
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Se descartaron {borradores_actualizados} borrador(es) '
                f'con más de {dias} días de antigüedad.'
            )
        )

        # Sugerencia
        if borradores_actualizados > 0:
            self.stdout.write(
                self.style.NOTICE(
                    '\nTip: Puedes programar este comando en cron o Task Scheduler '
                    'para mantener la base de datos limpia automáticamente.'
                )
            )
