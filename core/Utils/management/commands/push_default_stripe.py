from django.db import transaction
from django.core.management.base import BaseCommand
from core.Finances.stripe.handlers import ProductHandler, PriceHandler
from core.Finances.models import Product, Price


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        product = Product.objects.filter(is_default=True).active().first()
        prices = Price.objects.filter(product=product).active()

        # Payment.objects.all().delete(); Invoice.objects.all().delete(); Subscription.objects.all().delete(); Price.objects.all().delete(); Product.objects.all().delete()

        try:
            ProductHandler().get_or_create(product)
            for price in prices:
                PriceHandler().get_or_create(price)
            self.stdout.write('[+] Default product created with prices in stripe', style_func=self.style.SUCCESS)
        except Exception as e:
            self.stdout.write(str(e), style_func=self.style.ERROR)
