# Generated by Django 4.0.3 on 2023-08-13 09:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0026_delete_like"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="amount",
            field=models.FloatField(
                validators=[django.core.validators.MinValueValidator(0.0)]
            ),
        ),
    ]