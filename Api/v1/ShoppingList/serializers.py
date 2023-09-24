from rest_framework import serializers
from Api.fields import UserPrimaryKeyRelatedField
from core.Fridge.models import FridgeProduct, Fridge
from core.ShoppingList.models import ShoppingList, ShoppingListProduct


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = (
            'id',
            'name',
        )

    def save(self, **kwargs):
        user = self.context.get('user')
        kwargs.update({'user': user})
        return super().save(**kwargs)


class ShoppingListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListProduct
        fields = (
            'id',
            'name',
            'amount',
            'units',
        )

    def save(self, **kwargs):
        context = self.context
        shopping_list = context.get('shopping_list')
        user = context.get('user')
        kwargs.update({'shopping_list': shopping_list,
                       'user': user})
        return super().save(**kwargs)


class ShoppingListProductViewSerializer(serializers.ModelSerializer):
    class ShoppingListProductFridgeProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = FridgeProduct
            fields = read_only_fields = (
                'id',
                'name',
                'amount',
                'units',
                'manufacture_date',
                'shelf_life_date',
                'notes',
            )

    class ShoppingListProductFridgeSerializer(serializers.ModelSerializer):
        fridge_type_name = serializers.CharField(max_length=64, source='fridge_type.name')
        fridge_type_slug = serializers.CharField(max_length=255, source='fridge_type.slug')

        class Meta:
            model = Fridge
            fields = read_only_fields = (
                'id',
                'name',
                'fridge_type_name',
                'fridge_type_slug',
            )

    product = ShoppingListProductFridgeProductSerializer()
    fridge = ShoppingListProductFridgeSerializer()

    class Meta:
        model = ShoppingListProduct
        fields = read_only_fields = (
            'id',
            'name',
            'amount',
            'units',
            'product',
            'fridge',
        )


class ShoppingListProductCreateFromProductSerializer(serializers.ModelSerializer):
    product = UserPrimaryKeyRelatedField(queryset=FridgeProduct.objects.select_related('user', 'fridge').all())

    class Meta:
        model = ShoppingListProduct
        fields = (
            'id',
            'product',
        )

    def validate(self, data):
        data = super().validate(data)
        product = data.get('product')
        data.update({
            'fridge': product.fridge,
            'name': product.name,
            'amount': product.amount,
            'units': product.units,
        })
        return data

    def save(self, **kwargs):
        context = self.context
        shopping_list = context.get('shopping_list')
        user = context.get('user')
        kwargs.update({'shopping_list': shopping_list,
                       'user': user})
        return super().save(**kwargs)
