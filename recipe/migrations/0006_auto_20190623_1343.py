# Generated by Django 2.1.5 on 2019-06-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_auto_20190517_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeitem',
            name='ratio',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8),
        ),
    ]
