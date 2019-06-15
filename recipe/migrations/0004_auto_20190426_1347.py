# Generated by Django 2.1.5 on 2019-04-26 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_recipe_prod_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeitem',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='recipe.Recipe'),
        ),
    ]