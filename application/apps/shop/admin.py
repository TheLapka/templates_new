from django.contrib import admin
from apps.shop.models import *

# 	Product (Товар): id, название, описание, цена,
#   количество на складе.
#
# 	Order (Заказ): id, дата создания, статус (напр.
#   "в процессе", "отправлен", "доставлен").
#
# 	OrderItem (Элемент заказа в корзине): id, id заказа,
#   id товара, количество товара в заказе.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "price")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk" ,"status")

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order" ,"product", "quantity")

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)