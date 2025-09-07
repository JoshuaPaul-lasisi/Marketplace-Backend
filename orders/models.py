from django.db import models
from users.models import User
from products.models import Product

ORDER_STATUS = (
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled')
)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'customer'}, db_index=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='pending', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.quantity} f {self.product.name}"
    