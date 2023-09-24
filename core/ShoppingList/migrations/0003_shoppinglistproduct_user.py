# Generated by Django 3.2.12 on 2023-09-24 20:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ShoppingList', '0002_alter_shoppinglistproduct_units'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglistproduct',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]