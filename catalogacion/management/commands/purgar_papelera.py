"""
Comando para purgar obras eliminadas de la papelera.
Elimina permanentemente obras que llevan mas de X dias eliminadas.

Uso:
    python manage.py purgar_papelera
    python manage.py purgar_papelera --dias=60
    python manage.py purgar_papelera --dry-run
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from catalogacion.models import (
    NumeroControl773,
    NumeroControl774,
    NumeroControl787,
    ObraGeneral,
)


class Command(BaseCommand):
    help = "Purga obras eliminadas que llevan mas de X dias en la papelera"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dias",
            type=int,
            default=30,
            help="Dias minimos en papelera antes de purgar (default: 30)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simular sin eliminar realmente",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Purgar incluso obras con relaciones (elimina las relaciones primero)",
        )

    def handle(self, *args, **options):
        dias = options["dias"]
        dry_run = options["dry_run"]
        force = options["force"]

        self.stdout.write(f"Buscando obras eliminadas hace mas de {dias} dias...")

        limite = timezone.now() - timedelta(days=dias)
        obras_a_purgar = ObraGeneral.objects.filter(
            activo=False,
            fecha_eliminacion__lt=limite,
        )

        total = obras_a_purgar.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No hay obras para purgar."))
            return

        self.stdout.write(f"Encontradas {total} obra(s) candidatas a purgar.")

        purgadas = 0
        protegidas = 0
        errores = 0

        for obra in obras_a_purgar:
            titulo = obra.titulo_principal or "Sin titulo"
            num_control = obra.num_control or "?"

            # Verificar relaciones PROTECT
            tiene_773 = NumeroControl773.objects.filter(obra_relacionada=obra).exists()
            tiene_774 = NumeroControl774.objects.filter(obra_relacionada=obra).exists()
            tiene_787 = NumeroControl787.objects.filter(obra_relacionada=obra).exists()

            tiene_relaciones = tiene_773 or tiene_774 or tiene_787

            if tiene_relaciones and not force:
                self.stdout.write(
                    self.style.WARNING(
                        f"  OMITIDA: {titulo} ({num_control}) - tiene relaciones activas"
                    )
                )
                protegidas += 1
                continue

            if dry_run:
                self.stdout.write(
                    f"  [DRY-RUN] Se eliminaria: {titulo} ({num_control})"
                )
                purgadas += 1
            else:
                try:
                    if force and tiene_relaciones:
                        # Eliminar relaciones primero
                        NumeroControl773.objects.filter(obra_relacionada=obra).delete()
                        NumeroControl774.objects.filter(obra_relacionada=obra).delete()
                        NumeroControl787.objects.filter(obra_relacionada=obra).delete()
                        self.stdout.write(
                            f"  Relaciones eliminadas para: {titulo}"
                        )

                    obra.delete()
                    self.stdout.write(
                        self.style.SUCCESS(f"  PURGADA: {titulo} ({num_control})")
                    )
                    purgadas += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"  ERROR: {titulo} - {str(e)}")
                    )
                    errores += 1

        # Resumen
        self.stdout.write("")
        self.stdout.write("=" * 50)
        self.stdout.write(f"RESUMEN:")
        self.stdout.write(f"  - Total candidatas: {total}")
        self.stdout.write(f"  - Purgadas: {purgadas}")
        self.stdout.write(f"  - Protegidas (con relaciones): {protegidas}")
        self.stdout.write(f"  - Errores: {errores}")

        if dry_run:
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "MODO DRY-RUN: No se elimino nada. "
                    "Ejecute sin --dry-run para purgar realmente."
                )
            )
