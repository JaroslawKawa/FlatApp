from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ShoppingItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=10, choices=[
        ('szt', 'szt'),
        ('kg', 'kg'),
        ('g', 'g'),
        ('l', 'l'),
        ('ml', 'ml'),
        ('opak', 'opakowanie')
    ], default='szt')
    bought = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    in_cart = models.BooleanField(default=False)
    bought_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def mark_as_bought(self):
        self.bought = True
        self.bought_at = timezone.now()
        self.save()