from django.db import models

from django.contrib.auth.models import User

class ArchivoExcel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='excels/')
    nombre = models.CharField(max_length=200, blank=True)  # nuevo campo
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.nombre:
            self.nombre = self.archivo.name.split("/")[-1]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"
