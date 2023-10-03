# Generated by Django 3.2.12 on 2023-10-03 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fridge', '0007_alter_fridgeproduct_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fridgeproduct',
            name='units',
            field=models.CharField(choices=[('gramm', 'Gr'), ('kilogram', 'KG'), ('milliter', 'ML'), ('liter', 'L'), ('Units', 'Units')], db_index=True, max_length=16),
        ),
    ]
