# Generated by Django 4.0.3 on 2022-03-30 11:20

import CookingHeaven.common.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_recipe_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodtype',
            name='name',
            field=models.CharField(max_length=50, unique=True, validators=[CookingHeaven.common.validators.is_alpha]),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(2), CookingHeaven.common.validators.is_alpha]),
        ),
    ]
