# Generated by Django 2.1.5 on 2019-06-23 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0011_rawmaterialusage_lot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawmaterialusage',
            name='job',
        ),
        migrations.RemoveField(
            model_name='rawmaterialusage',
            name='recipeitem',
        ),
        migrations.RemoveField(
            model_name='job',
            name='machine',
        ),
        migrations.DeleteModel(
            name='RawMaterialUsage',
        ),
    ]
