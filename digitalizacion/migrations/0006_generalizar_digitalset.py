from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalizacion', '0005_update_estado_values'),
    ]

    operations = [
        # 1. Renombrar coleccion -> obra
        migrations.RenameField(
            model_name='digitalset',
            old_name='coleccion',
            new_name='obra',
        ),
        # 2. Agregar campo tipo (default COLECCION para datos existentes)
        migrations.AddField(
            model_name='digitalset',
            name='tipo',
            field=models.CharField(
                choices=[('COLECCION', 'Colección'), ('OBRA_SUELTA', 'Obra suelta')],
                default='COLECCION',
                max_length=20,
            ),
        ),
    ]
