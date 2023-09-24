from factory import fuzzy, SubFactory, DjangoModelFactory
from core.User.factories import UserFactory
from core.Fridge.models import FridgeProduct
from core.Fridge.factories import FridgeProductFactory, FridgeFactory
from core.Utils.Tests.fuzzy_fields import FuzzyParagraph
from .models import ShoppingList, ShoppingListProduct


class ShoppingListFactory(DjangoModelFactory):
    name = FuzzyParagraph(length=64)
    user = SubFactory(UserFactory)

    class Meta:
        model = ShoppingList


class ShoppingListProductFactory(DjangoModelFactory):
    shopping_list = SubFactory(ShoppingListFactory)
    product = SubFactory(FridgeProductFactory)
    fridge = SubFactory(FridgeFactory)
    name = FuzzyParagraph(length=64)
    amount = fuzzy.FuzzyInteger(1, 100)
    units = fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys())

    class Meta:
        model = ShoppingListProduct
