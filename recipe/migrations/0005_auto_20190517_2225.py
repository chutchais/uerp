# Generated by Django 2.1.5 on 2019-05-17 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20190505_1132'),
        ('recipe', '0004_auto_20190426_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeitem',
            name='name',
        ),
        migrations.AddField(
            model_name='recipeitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipeintems', to='product.Product'),
        ),
    ]
