from rest_framework import serializers
from Api.fields import UserPrimaryKeyRelatedField
from core.Fridge.models import FridgeType, Fridge, FridgeProduct


class FridgeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeType
        fields = (
            'id',
            'name',
            'slug',
        )


class FridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fridge
        fields = (
            'id',
            'name',
            'fridge_type',
            'label',
        )
        read_only_fields = ('id', 'label')

    def save(self, **kwargs):
        user = self.context.get('user')
        kwargs.update({'user': user})
        return super().save(**kwargs)


class FridgeViewSerializer(FridgeSerializer):
    fridge_type = FridgeTypeSerializer()

    class Meta(FridgeSerializer.Meta):
        fields = read_only_fields = FridgeSerializer.Meta.fields


class FridgeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeProduct
        fields = (
            'id',
            'name',
            'amount',
            'units',
            'manufacture_date',
            'shelf_life_date',
            'notes',
            'label',
        )
        read_only_fields = ('id', 'label')

    def save(self, **kwargs):
        context = self.context
        fridge = context.get('fridge')
        user = context.get('user')
        kwargs.update({'fridge': fridge,
                       'user': user})
        return super().save(**kwargs)


class FridgeProductViewSerializer(FridgeProductSerializer):
    class Meta(FridgeProductSerializer.Meta):
        fields = read_only_fields = FridgeProductSerializer.Meta.fields


class ProductSerializer(FridgeProductSerializer):
    fridge = UserPrimaryKeyRelatedField(queryset=Fridge.objects.select_related('user').all())

    class Meta:
        model = FridgeProduct
        fields = (
            'id',
            'fridge',
            'name',
            'amount',
            'units',
            'manufacture_date',
            'shelf_life_date',
            'notes',
            'label',
        )
        read_only_fields = ('id', 'label')

    def save(self, **kwargs):
        context = self.context
        user = context.get('user')
        kwargs.update({'user': user})
        return super().save(**kwargs)


class ProductViewSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = read_only_fields = ProductSerializer.Meta.fields
