# Generated by Django 4.0.3 on 2022-04-11 13:12

import CookingHeaven.main.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_recipe_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='photo',
            field=CookingHeaven.main.models.RecipeCloudinaryField(max_length=255),
        ),
    ]