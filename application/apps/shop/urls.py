from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("product", views.ProductView)

urlpatterns = router.urls + [
    path("orders/", view=views.OrdersView.as_view()),
    path("getorders/", view=views.GetOrdersAll.as_view())
]