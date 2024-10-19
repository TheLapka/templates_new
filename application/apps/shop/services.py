from rest_framework.serializers import ValidationError
from apps.shop.models import *


class OrderCreator:

    def create_order(self, products: list[dict]):

        all_product = self._create_list_product(products)
        products_info = self._create_info_products(all_product)
        self._check_quantity_product(products, products_info)
        order = self._save_new_order_in_db()
        self._to_update_quantity_products(products, products_info)
        self._to_create_orderitem(products, order)
        return self._create_list_products_on_order(order, products_info)

    def _to_update_quantity_products(
        self, products: list[dict], products_info: dict
    ) -> None:
        to_update_quantity = []

        for product in products:
            p_model = products_info[product["product_id"]]["model"]
            p_model.quantity -= product["amount"]
            to_update_quantity.append(p_model)

        Product.objects.bulk_update(to_update_quantity, ["quantity"])

    def _to_create_orderitem(self, products, order) -> None:
        to_create_orderitem = []

        for product in products:
            to_create_orderitem.append(
                OrderItem(
                    order=order,
                    product_id=product["product_id"],
                    quantity=product["amount"],
                )
            )
        OrderItem.objects.bulk_create(to_create_orderitem)

    # тут неправильно нахуй блять собака ебанная

    def _create_list_products_on_order(self, order, products_info) -> dict:
        product_order = OrderItem.objects.filter(order=order).select_related("product")
        dictsssssss = {
            "order_id": order.pk,
            "status": order.get_status_display(),
            "order_items": [
                {
                    "product_id": el.product.pk,
                    "name": el.product.name,
                    "quantity": el.quantity,
                }
                for el in product_order
            ],
        }
        return dictsssssss

    def _save_new_order_in_db(self) -> Order:
        return Order.objects.create(status=StatusChoices.IN_P)

    def _create_list_product(self, pr):
        all_product = Product.objects.filter(id__in=[p["product_id"] for p in pr])
        return all_product

        ############

    def _create_info_products(self, a_p: list[dict]) -> dict[dict]:
        products_info = {
            p.pk: {
                "product_id": p.pk,
                "name": p.name,
                "quantity": p.quantity,
                "model": p,
            }
            for p in a_p
        }
        return products_info

    def _check_quantity_product(self, products: list[dict], products_info) -> None:
        for product in products:
            if product["product_id"] not in products_info:
                raise ValidationError(f"Данного товара несуществует")
            if product["amount"] > products_info[product["product_id"]]["quantity"]:
                raise ValidationError(
                    f"Недостаточно товара {products_info[product["product_id"]]['name']} на складе для заказа. Доступно {products_info[product["product_id"]]['quantity']}"
                )


class CreateGetOrder:
    def get_order(self, pk):
        order = Order.objects.filter(pk=pk).values().first()
        if not order:
            raise ValidationError(f"Такого ID заказа не сущестует")
        product_order = OrderItem.objects.filter(order=pk).select_related("product")
        my_order = {
            "id": order["id"],
            "creation_date": order["creation_date"],
            "status": order["status"],
            "order_items": [
                {
                    "product_id": el.product.pk,
                    "name": el.product.name,
                    "quantity": el.quantity,
                }
                for el in product_order
            ],
        }

        return my_order


class UpdateOrderStatusService:
    def update_order_status(self, data, id) -> dict:
        self._check_order(id)
        self._update_status(id, data["status"])
        return data

    # Разеберись с тайп хинтами например для перечисления, вот наподобии Optionla[Order]
    def _check_order(self, id: int) -> None:
        if not Order.objects.filter(pk=id).exists():
            raise ValidationError(f"Такого ID заказа не сущестует")

    def _update_status(self, id: int, status: str) -> None:
        Order.objects.filter(pk=id).update(status=status)
