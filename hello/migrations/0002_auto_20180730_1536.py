# Generated by Django 2.0.7 on 2018-07-30 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_type_collection',
            name='admins',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_contributors', to=settings.AUTH_USER_MODEL),
        ),
    ]
