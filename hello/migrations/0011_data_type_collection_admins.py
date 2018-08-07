# Generated by Django 2.1 on 2018-08-06 18:50

from django.conf import settings
from django.db import migrations, models
import hello.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hello', '0010_auto_20180806_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_type_collection',
            name='admins',
            field=models.ManyToManyField(default=hello.models.get_admin, related_name='db_admins', to=settings.AUTH_USER_MODEL),
        ),
    ]