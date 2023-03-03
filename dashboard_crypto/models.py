from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(blank=False, null=False, default='Portfolio')
    crypto = models.TextField(blank=True, null=True)
    totalBalance = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

