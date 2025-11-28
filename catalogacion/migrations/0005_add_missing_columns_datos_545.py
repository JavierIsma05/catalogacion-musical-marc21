from django.db import migrations


def ensure_datos_545_columns(apps, schema_editor):
    """Garantiza que existan las columnas texto_biografico y uri."""
    table_name = 'catalogacion_datosbiograficos545'
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info({table_name})")
        existing_columns = {row[1] for row in cursor.fetchall()}

    if 'texto_biografico' not in existing_columns:
        schema_editor.execute(
            f"ALTER TABLE {table_name} ADD COLUMN texto_biografico TEXT"
        )

    if 'uri' not in existing_columns:
        schema_editor.execute(
            f"ALTER TABLE {table_name} ADD COLUMN uri VARCHAR(200)"
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('catalogacion', '0004_remove_incipitmusical_nota_general_and_more'),
    ]

    operations = [
        migrations.RunPython(ensure_datos_545_columns, noop),
    ]
