from django.shortcuts import render
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from apps.shop.services import CreateGetOrder, OrderCreator, UpdateOrderStatusService
from apps.shop.serializer import (
    GetOrderSerializer,
    ProductSerializer,
    OrderSerializer,
    UpdateOrderStatusSerializer,
)
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
        return Response(data=result, status=status.HTTP_200_OK)


class GetOrderView(RetrieveAPIView):
    queryset = Order.objects.all()

    def get(self, request, pk):
        creator = CreateGetOrder()
        result = creator.get_order(pk)
        return Response(data=result, status=status.HTTP_200_OK)


class GetAllOrdersView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = GetOrderSerializer
    pagination_class = LimitOffsetPagination


class UpdateOrderStatus(UpdateAPIView):
    serializer_class = UpdateOrderStatusSerializer

    # Тут исправиь тайп хинты, посмотри видосик оленевод
    def patch(self, request: Request, id: int):
        sz = UpdateOrderStatusSerializer(data=request.data)
        sz.is_valid(raise_exception=True)

        updater = UpdateOrderStatusService()
        result = updater.update_order_status(sz.data, id)
        return Response(data=result, status=status.HTTP_200_OK)
