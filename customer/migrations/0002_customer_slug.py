# Generated by Django 2.1.5 on 2019-04-26 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
