# Generated by Django 3.2.12 on 2023-09-24 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Fridge', '0006_fridgeproduct_assign_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fridgeproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='User.user'),
        ),
    ]
