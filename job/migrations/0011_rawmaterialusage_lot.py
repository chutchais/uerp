# Generated by Django 2.1.5 on 2019-06-23 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0010_rawmaterialusage'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawmaterialusage',
            name='lot',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
