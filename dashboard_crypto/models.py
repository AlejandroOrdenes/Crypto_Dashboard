from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Crypto(models.Model):
    name = models.CharField(max_length=255, unique=True)
    symbol = models.CharField(max_length=10, unique=True)
    cryptoAmount = models.DecimalField(max_digits=20, decimal_places=10)

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
