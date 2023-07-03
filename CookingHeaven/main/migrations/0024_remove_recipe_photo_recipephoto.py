# Generated by Django 4.0.3 on 2023-06-28 15:14

import CookingHeaven.main.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0023_alter_recipe_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="photo",
        ),
        migrations.CreateModel(
            name="RecipePhoto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "photo",
                    CookingHeaven.main.models.RecipeCloudinaryField(max_length=255),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="main.recipe",
                    ),
                ),
            ],
        ),
    ]