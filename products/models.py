from django.db import models
from users.models import User

class Product(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'vendor'})
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price'])
        ]
    
    def __str__(self):
        return self.name