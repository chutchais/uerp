# Generated by Django 2.1.5 on 2019-07-01 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0011_auto_20190614_2005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Downtime',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('productgroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='downtimes', to='product.ProductGroup')),
            ],
        ),
    ]
