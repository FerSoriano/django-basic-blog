from django.db import models


class Post(models.Model):
    user = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    modificado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
