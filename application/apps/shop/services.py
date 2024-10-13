# data = products = {
#     [
#         "product_id": 2,
#         "amount": 12
#     ]
# }


from rest_framework.serializers import ValidationError
from apps.shop.models import *


class OrderCreator:
    def create_order(self, data: list):
        products = data
        all_product = Product.objects.filter(id__in=[p["product_id"] for p in products])
        products_info = {
            p.pk: {
                "product_id": p.pk,
                "name": p.name,
                "quantity": p.quantity,
                "model": p,
            }
            for p in all_product
        }
        for product in products:
            if product["product_id"] not in products_info:
                raise ValidationError(f"Данного товара несуществует")
            if product["amount"] > products_info[product["product_id"]]["quantity"]:
                raise ValidationError(
                    f"Недостаточно товара {products_info[product["product_id"]]['name']} на складе для заказа. Доступно {products_info[product["product_id"]]['quantity']}"
                )
        order = Order.objects.create(status=StatusChoices.IN_P)

        to_update_quantity = []
        to_create_orderitem = []

        for product in products:
            to_create_orderitem.append(
                OrderItem(
                    order=order,
                    product_id=product["product_id"],
                    quantity=product["amount"],
                )
            )
            p_model = products_info[product["product_id"]]["model"]
            p_model.quantity -= product["amount"]
            to_update_quantity.append(p_model)

        Product.objects.bulk_update(to_update_quantity, ["quantity"])
        OrderItem.objects.bulk_create(to_create_orderitem)

        dictsssssss = {
            "order_id": order.pk,
            "status": order.get_status_display(),
            "order_items": [
                {
                    "product_id": el["product_id"],
                    "name": el["name"],
                    "quantity": el["quantity"],
                }
                for el in products_info.values()
            ],
        }
        return dictsssssss
    
class GetOrder:
    def get_orders():
        all_order = Order.objects.all()
        return all_order
