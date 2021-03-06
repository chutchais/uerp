# Generated by Django 2.1.5 on 2019-06-29 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0001_initial'),
        ('production', '0005_auto_20190624_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapHour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Scrap Qty')),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('productionhour', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scraps', to='production.ProductionHour')),
                ('scrap', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scraps', to='scrap.Scrap')),
            ],
        ),
    ]
