# Generated by Django 4.0.3 on 2022-03-22 04:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0008_unit_remove_ingredient_quantity_ingredient_amount_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="likes",
            field=models.ManyToManyField(
                related_name="recipe_likes_set", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="types",
            field=models.ManyToManyField(to="main.foodtype"),
        ),
    ]
