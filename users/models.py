from django.db import models
from django.contrib.auth.models import AbstractUser 

USER_TYPES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    ]

class User(AbstractUser):
    
    user_type = models.CharField(max_length = 10, choices=USER_TYPES, default = 'customer')
    email = models.EmailField(unique=True, db_index=True)

    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return f'(self.username) ({self.user_type})'