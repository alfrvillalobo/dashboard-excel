from django.db import models

from django.contrib.auth.models import User

class ArchivoExcel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='excels/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.archivo.name} - {self.usuario.username}"