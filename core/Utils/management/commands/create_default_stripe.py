from decimal import Decimal

from django.db import transaction
from django.core.management.base import BaseCommand
from core.Currency.models import Currency
from core.Finances.models import Product, Price


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        currency = Currency.objects.get_default()

        product = Product(name='Premium', description='Premium')
        product.save()
        product.set_as_default()

        price1 = Price(
            product=product,
            price=Decimal(10),
            currency=currency,
            interval=Price.PriceIntervalChoices.MONTH,
            interval_count=1,
            is_default=False,
        )
        price2 = Price(
            product=product,
            price=Decimal(15),
            currency=currency,
            interval=Price.PriceIntervalChoices.MONTH,
            interval_count=1,
            is_default=False,
        )
        price3 = Price(
            product=product,
            price=Decimal(100),
            currency=currency,
            interval=Price.PriceIntervalChoices.YEAR,
            interval_count=1,
            is_default=False,
        )
        price1.save()
        price2.save()
        price3.save()
        price1.set_as_default()

        self.stdout.write('[+] Default product created with prices', style_func=self.style.SUCCESS)
