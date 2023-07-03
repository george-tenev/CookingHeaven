# Generated by Django 4.0.3 on 2022-04-10 14:58

import CookingHeaven.common.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0016_remove_recipe_types_recipe_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="unit",
            name="name",
            field=models.CharField(
                max_length=60,
                unique=True,
                validators=[CookingHeaven.common.validators.is_alpha],
            ),
        ),
    ]
