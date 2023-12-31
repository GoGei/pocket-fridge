# Generated by Django 3.2.12 on 2023-10-23 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Finances', '0002_stripe_model_changes'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('created_stamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_stamp', models.DateTimeField(auto_now=True)),
                ('archived_stamp', models.DateTimeField(null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, unique=True)),
                ('expire_date', models.DateField(db_index=True)),
                ('last_digits_of_card', models.CharField(max_length=4)),
                ('card_type', models.CharField(choices=[('amex', 'American Express'), ('diners', 'Diners Club'), ('discover', 'Discover'), ('jcb', 'JCB'), ('mastercard', 'MasterCard'), ('unionpay', 'UnionPay'), ('visa', 'Visa'), ('unknown', 'Unknown')], max_length=20)),
                ('is_default', models.BooleanField(default=False)),
                ('archived_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'clinic_card',
            },
        ),
    ]
