# Generated by Django 3.2.12 on 2023-09-24 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShoppingList', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglistproduct',
            name='units',
            field=models.CharField(choices=[('gramm', 'Gr'), ('kilogram', 'KG'), ('milliter', 'ML'), ('liter', 'L'), ('items', 'Items')], db_index=True, max_length=16),
        ),
    ]