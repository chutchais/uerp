# Generated by Django 2.1.5 on 2019-04-26 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.Product'),
        ),
    ]
