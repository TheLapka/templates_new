from django.db.models import TextChoices

class StatusChoices(TextChoices):
    SENT = ('SENT', 'Отправлено')
    DELIVERED = ('DELIVERED', 'Доставлено')
    IN_P = ('IN_P', 'В процессе')
