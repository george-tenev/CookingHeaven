# Generated by Django 4.0.3 on 2022-03-21 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_recipe_likes_alter_recipe_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='photo',
            field=models.ImageField(default=1, upload_to='recipe'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='RecipePhoto',
        ),
    ]
