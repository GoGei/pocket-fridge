from django.utils import timezone
from factory import fuzzy, SubFactory, DjangoModelFactory, LazyAttribute
from factory.faker import Faker
from core.User.factories import UserFactory
from core.Utils.Tests.fuzzy_fields import FuzzyParagraph, FuzzyImage
from .models import FridgeType, Fridge, FridgeProduct


class FridgeTypeFactory(DjangoModelFactory):
    name = FuzzyParagraph(length=64)
    slug = Faker('slug')
    create_on_user_creation = True

    class Meta:
        model = FridgeType
        django_get_or_create = ('slug',)


class FridgeFactory(DjangoModelFactory):
    name = FuzzyParagraph(length=64)
    user = SubFactory(UserFactory)
    fridge_type = SubFactory(FridgeTypeFactory)

    class Meta:
        model = Fridge


class FridgeProductFactory(DjangoModelFactory):
    name = FuzzyParagraph(length=64)
    fridge = SubFactory(FridgeFactory)
    user = LazyAttribute(lambda e: e.fridge.user)
    amount = fuzzy.FuzzyInteger(1, 100)
    units = fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys())
    manufacture_date = fuzzy.FuzzyDate(start_date=timezone.now().date())
    shelf_life_date = fuzzy.FuzzyDate(start_date=timezone.now().date())
    notes = FuzzyParagraph(length=2048)
    image = FuzzyImage()
    barcode = None

    class Meta:
        model = FridgeProduct
