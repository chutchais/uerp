# Generated by Django 2.1.5 on 2019-04-26 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20190426_1011'),
        ('recipe', '0002_auto_20190426_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='prod_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipes', to='product.ProductGroup'),
        ),
    ]
