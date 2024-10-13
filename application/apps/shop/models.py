from django.db import models

from apps.shop.choices import StatusChoices

# 	Product (Товар): id, название, описание, цена,
#   количество на складе.
#
# 	Order (Заказ): id, дата создания, статус (напр.
#   "в процессе", "отправлен", "доставлен").
#
# 	OrderItem (Элемент заказа в корзине): id, id заказа,
#   id товара, количество товара в заказе.


class Product(models.Model):
    name = models.CharField(max_length=30, verbose_name="Наименование товара")
    description = models.TextField(max_length=500, verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(verbose_name="Колличество")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    creation_date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=StatusChoices, default=StatusChoices.IN_P)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="id заказа")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Наименование товара"
    )
    quantity = models.PositiveIntegerField(verbose_name="Колличество")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"{self.product}"
