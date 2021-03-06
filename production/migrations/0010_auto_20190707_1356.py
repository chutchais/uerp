# Generated by Django 2.1.5 on 2019-07-07 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0009_auto_20190701_2226'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='downtimehour',
            options={'verbose_name': 'Hour - Downtime', 'verbose_name_plural': 'Productions Hour - Downtimes'},
        ),
        migrations.AlterModelOptions(
            name='productionhour',
            options={'verbose_name': 'Hour - Output', 'verbose_name_plural': 'Productions Hour - Outputs'},
        ),
        migrations.AlterModelOptions(
            name='rawmaterialusage',
            options={'verbose_name': 'Material Usage', 'verbose_name_plural': 'Productions - Material Usage'},
        ),
        migrations.AlterModelOptions(
            name='scraphour',
            options={'verbose_name': 'Hour - Scrap', 'verbose_name_plural': 'Productions Hour - Scraps'},
        ),
        migrations.AlterModelOptions(
            name='wastehour',
            options={'verbose_name': 'Hour - Waste', 'verbose_name_plural': 'Productions Hour - Wastes'},
        ),
        migrations.AddField(
            model_name='production',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
