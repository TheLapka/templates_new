from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from apps.shop.services import OrderCreator
from apps.shop.serializer import ProductSerializer, OrderSerializer
from apps.shop.models import Product, Order

class ProductView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class OrdersView(GenericAPIView):
    serializer_class = OrderSerializer
    
    def post(self, request):
        sz = OrderSerializer(data=request.data)
        sz.is_valid(raise_exception=True)

        creator = OrderCreator()
        result = creator.create_order(sz.data)
        return Response(data=result,status=status.HTTP_200_OK)
    
class GetOrdersAll(ListAPIView):
    queryset = Order.objects.all()
    
    def get(self):
        return f':jgf ,j,hf b z t` dst,fk'
    
    