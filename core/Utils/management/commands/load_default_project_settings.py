from django.db import transaction
from django.core.management.base import BaseCommand
from core.Fridge.models import FridgeType
from core.Licence.models import LicenceVersion


class Command(BaseCommand):
    def load_fridge_types(self):
        if FridgeType.objects.exists():
            self.stdout.write('Fridge types already exists', style_func=self.style.WARNING)
            return

        fixture = [
            {
                "name": "Fridge",
                "slug": "fridge",
                "create_on_user_creation": True,
            },
            {
                "name": "Freezer",
                "slug": "freezer",
                "create_on_user_creation": True,
            },
            {
                "name": "Pantry",
                "slug": "pantry",
                "create_on_user_creation": True,
            },
            {
                "name": "Default",
                "slug": "default",
            },
            {
                "name": "Not slugified yet",
            }
        ]
        for data in fixture:
            FridgeType.objects.create(**data)
        self.stdout.write('Fridge types created', style_func=self.style.SUCCESS)

    def load_licences(self):
        if LicenceVersion.objects.exists():
            self.stdout.write('Licences already exists', style_func=self.style.WARNING)
            return

        fixture = [
            {
                "name": "Licence",
                "slug": "licence",
                "is_default": True,
            },
            {
                "name": "Beta",
                "slug": "beta",
            },
            {
                "name": "Licence v2",
                "slug": "licence-v2",
            }
        ]
        for data in fixture:
            LicenceVersion.objects.create(**data)
        self.stdout.write('Licences created', style_func=self.style.SUCCESS)

    @transaction.atomic
    def handle(self, *args, **options):
        self.load_fridge_types()
        self.load_licences()
