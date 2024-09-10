from decimal import Decimal
from rest_framework import serializers

from .models import Product, Collection, Reviews


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context.get('product_id')
        return Reviews.objects.create(product_id=product_id, **validated_data)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    # serializers.Serializer
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    # first way to add collection
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )

    # second way to add collection
    # collection = serializers.StringRelatedField()

    # third way to add collection
    # collection = CollectionSerializer()

    # forth way to add collection
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.promotions = 'gol'
    #     product.save()
    #     return product
    #
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance

    # custom validator
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match!')
    #     else:
    #         return data
