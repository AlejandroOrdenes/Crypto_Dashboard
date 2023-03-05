from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

# Create your models here.

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(blank=False, null=False, default='Portfolio')
    cryptoIds = models.JSONField(blank=True, null=True, default=list)
    totalBalance = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def deleteCoin(self, name):
        # Obtener el valor actual del campo JSON
        datos_json = self.cryptoIds

        # Eliminar el elemento con la clave dada
        del datos_json[name]

        # Actualizar el campo JSON
        self.mi_campo_json = datos_json
        self.save()