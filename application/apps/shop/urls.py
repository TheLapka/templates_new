from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register("product", views.ProductView)

urlpatterns = router.urls + [
    path("orders/", view=views.OrdersView.as_view()),
    path("getorders/", view=views.GetAllOrdersView.as_view()),
    path("getorders/<int:pk>", view=views.GetOrderView.as_view()),
    path("updateorder/<int:id>/status", view=views.UpdateOrderStatus.as_view()),
]
