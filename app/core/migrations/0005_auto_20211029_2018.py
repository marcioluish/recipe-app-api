# Generated by Django 2.1.15 on 2021-10-29 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingrediets',
            new_name='ingredients',
        ),
    ]
