# Generated by Django 3.2.12 on 2023-09-17 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fridge', '0002_alter_fridgeproduct_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='fridgetype',
            name='create_on_user_creation',
            field=models.BooleanField(default=False),
        ),
    ]
