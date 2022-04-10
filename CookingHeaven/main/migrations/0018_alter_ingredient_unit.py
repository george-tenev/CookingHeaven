# Generated by Django 4.0.3 on 2022-04-10 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_unit_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.unit'),
        ),
    ]