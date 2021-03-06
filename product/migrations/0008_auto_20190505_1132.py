# Generated by Django 2.1.5 on 2019-05-05 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20190430_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prod_type',
            field=models.CharField(choices=[('CON', 'Consumable'), ('FG', 'Finish Goods'), ('SEMI', 'Semi part'), ('SET', 'Sets'), ('RAW', 'Raw Material'), ('OT', 'Other')], default='RAW', max_length=5),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_per_pack',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=7, verbose_name='Unit per pack'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Unit weight'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_runner',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Runner weight'),
        ),
    ]
