# Generated by Django 4.0.3 on 2022-03-19 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeproduct',
            old_name='Product',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='product',
            name='recipe',
            field=models.ManyToManyField(blank=True, null=True, through='main.RecipeProduct', to='main.recipe'),
        ),
    ]
