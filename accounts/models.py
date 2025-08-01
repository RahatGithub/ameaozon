from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    CUSTOMER = 'customer'
    ADMIN = 'admin'
    
    USER_TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (ADMIN, 'Admin'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=CUSTOMER)
    profile_picture = models.ImageField(upload_to='users/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def is_admin(self):
        return self.user_type == self.ADMIN
    
    def is_customer(self):
        return self.user_type == self.CUSTOMER