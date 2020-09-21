from django.db import models

class cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=30, null=False)
    apellido=models.CharField(max_length=30, null=False)
    dni=models.IntegerField(null=False)
    genero=models.CharField(max_length=15)
    email=models.EmailField(max_length=256, null=False)
    monto=models.IntegerField(null=False)
    status=models.BooleanField(default=False)
    query_date = models.DateTimeField(auto_now_add=True)  # automaticamente guarda la hora en que se crea el registro

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    class Meta:
        ordering = ['apellido']