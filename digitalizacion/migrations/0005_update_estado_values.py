# Generated migration to update estado field values from English to Spanish

from django.db import migrations, models


def update_estado_forward(apps, schema_editor):
    """Update estado values from English to Spanish"""
    DigitalSet = apps.get_model('digitalizacion', 'DigitalSet')

    DigitalSet.objects.filter(estado='NEW').update(estado='NUEVO')
    DigitalSet.objects.filter(estado='IMPORTED').update(estado='IMPORTADO')
    DigitalSet.objects.filter(estado='SEGMENTED').update(estado='SEGMENTADO')


def update_estado_backward(apps, schema_editor):
    """Reverse: update estado values from Spanish back to English"""
    DigitalSet = apps.get_model('digitalizacion', 'DigitalSet')

    DigitalSet.objects.filter(estado='NUEVO').update(estado='NEW')
    DigitalSet.objects.filter(estado='IMPORTADO').update(estado='IMPORTED')
    DigitalSet.objects.filter(estado='SEGMENTADO').update(estado='SEGMENTED')


class Migration(migrations.Migration):

    dependencies = [
        ('digitalizacion', '0004_digitalset_pdf_total_pages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='digitalset',
            name='estado',
            field=models.CharField(
                choices=[('NUEVO', 'Nuevo'), ('IMPORTADO', 'Importado'), ('SEGMENTADO', 'Segmentado')],
                default='NUEVO',
                max_length=20
            ),
        ),
        migrations.RunPython(update_estado_forward, update_estado_backward),
    ]
