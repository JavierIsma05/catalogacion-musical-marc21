from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalogacion", "0003_alter_entidadrelacionada710_entidad_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="borradorobra",
            name="obra_objetivo",
            field=models.ForeignKey(
                blank=True,
                help_text=(
                    "Si se está editando una obra existente, referencia la obra objetivo. "
                    "Si es un borrador de creación, queda vacío."
                ),
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="borradores_edicion",
                to="catalogacion.obrageneral",
            ),
        ),
        migrations.AddIndex(
            model_name="borradorobra",
            index=models.Index(fields=["obra_objetivo"], name="catalogacio_obra_ob_3f5c4f_idx"),
        ),
    ]
