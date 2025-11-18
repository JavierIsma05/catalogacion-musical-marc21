from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogacion", "0017_borradorobra"),
    ]

    operations = [
        migrations.AddField(
            model_name="tituloalternativo",
            name="texto_visualizacion",
            field=models.CharField(
                blank=True,
                help_text="246 $i – Texto de visualización",
                max_length=500,
                null=True,
            ),
        ),
    ]
