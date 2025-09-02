from django.db import models
from users.models import user
from products.models import Product

ORDER_STATUS = (
    ('pending', 'Pending'),
    ('paid', 'Pending'),
    ('skipped', 'Pending'),
    ('completed', 'Pending'),
    ('pending', 'Pending'),
)

class Order(models.Model):
    customer = models.ForeignKey(user, on-delete=models.CASCADE)