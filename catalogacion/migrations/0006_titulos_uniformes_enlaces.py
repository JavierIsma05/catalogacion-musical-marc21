import django.db.models.deletion
from django.db import migrations, models


def populate_titulos_uniformes(apps, schema_editor):
    AutoridadTituloUniforme = apps.get_model(
        'catalogacion', 'AutoridadTituloUniforme'
    )
    EnlaceDocumentoFuente773 = apps.get_model(
        'catalogacion', 'EnlaceDocumentoFuente773'
    )
    EnlaceUnidadConstituyente774 = apps.get_model(
        'catalogacion', 'EnlaceUnidadConstituyente774'
    )

    def resolver_titulo(valor):
        texto = (valor or '').strip()
        if not texto:
            return None
        existente = AutoridadTituloUniforme.objects.filter(
            titulo__iexact=texto
        ).first()
        if existente:
            return existente
        return AutoridadTituloUniforme.objects.create(titulo=texto)

    for enlace in EnlaceDocumentoFuente773.objects.all():
        autoridad = resolver_titulo(enlace.titulo)
        if autoridad:
            enlace.titulo_autoridad = autoridad
            enlace.save(update_fields=['titulo_autoridad'])

    for enlace in EnlaceUnidadConstituyente774.objects.all():
        autoridad = resolver_titulo(enlace.titulo)
        if autoridad:
            enlace.titulo_autoridad = autoridad
            enlace.save(update_fields=['titulo_autoridad'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalogacion', '0005_add_missing_columns_datos_545'),
    ]

    operations = [
        migrations.AddField(
            model_name='enlacedocumentofuente773',
            name='titulo_autoridad',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='+',
                to='catalogacion.autoridadtitulouniforme',
                help_text='773 $t – Título (NR)'
            ),
        ),
        migrations.AddField(
            model_name='enlaceunidadconstituyente774',
            name='titulo_autoridad',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='+',
                to='catalogacion.autoridadtitulouniforme',
                help_text='774 $t – Título (NR)'
            ),
        ),
        migrations.RunPython(populate_titulos_uniformes, noop),
        migrations.RemoveField(
            model_name='enlacedocumentofuente773',
            name='titulo',
        ),
        migrations.RemoveField(
            model_name='enlaceunidadconstituyente774',
            name='titulo',
        ),
        migrations.RenameField(
            model_name='enlacedocumentofuente773',
            old_name='titulo_autoridad',
            new_name='titulo',
        ),
        migrations.RenameField(
            model_name='enlaceunidadconstituyente774',
            old_name='titulo_autoridad',
            new_name='titulo',
        ),
        migrations.AlterField(
            model_name='enlacedocumentofuente773',
            name='titulo',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='catalogacion.autoridadtitulouniforme',
                help_text='773 $t – Título (NR)'
            ),
        ),
        migrations.AlterField(
            model_name='enlaceunidadconstituyente774',
            name='titulo',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='catalogacion.autoridadtitulouniforme',
                help_text='774 $t – Título (NR)'
            ),
        ),
    ]
