# Generated by Django 5.2.2 on 2025-06-28 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trabajadores', '0002_populate_trabajadores'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajador',
            name='tipo_trabajador',
            field=models.CharField(default='Empleado', help_text='Tipo o cargo del trabajador', max_length=50, verbose_name='Tipo de Trabajador'),
        ),
    ]
