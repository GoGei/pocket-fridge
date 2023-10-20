from django.db import transaction
from django.core.management.base import BaseCommand
from core.Finances.stripe.handlers import ProductHandler, PriceHandler
from core.Finances.models import Product, Price


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        product_id = 'product_id_from_stripe'
        prices = [
            # array of prices related to product
        ]
        try:
            ProductHandler().sync_from_stripe(external_id=product_id)
            for price in prices:
                PriceHandler().sync_from_stripe(external_id=price)
            self.stdout.write('[+] Default product with prices synced from stripe', style_func=self.style.SUCCESS)
        except Exception as e:
            self.stdout.write(str(e), style_func=self.style.ERROR)
