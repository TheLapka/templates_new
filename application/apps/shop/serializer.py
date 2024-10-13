from rest_framework import serializers
from apps.shop.models import Product
from rest_framework.serializers import ValidationError
# 	Product (Товар): id, название, описание, цена, количество на складе

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Product
        fields = "__all__"

class ProductToOrderSrializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    
    def validate_amount(self, value: int):
        if value <= 0:
            raise serializers.ValidationError("Колличество товаров не может быть меньше или равно 0")
        return value
    
class OrderSerializer(serializers.ListSerializer):
    child = ProductToOrderSrializer()