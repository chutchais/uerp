# Generated by Django 2.1.5 on 2019-09-14 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0004_auto_20190914_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='created_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
