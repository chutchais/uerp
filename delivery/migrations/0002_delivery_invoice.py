# Generated by Django 2.1.5 on 2019-06-10 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='invoice',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
