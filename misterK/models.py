from django.db import models

# Create your models here.
class Categorias(models.Model):
    nombre_categoria = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_categoria

class Productos(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    oferta = models.BooleanField(default=False) 
    porcentajeOferta = models.IntegerField()  
    imagen = models.ImageField(upload_to='productos/',null=True,blank=True)
    # agregadosRelacionados = models.CharField(max_length=50) debe ser una lista
    
    def precio_con_descuento(self):
        if self.oferta:
            return round(self.precio * (1 - self.porcentajeOferta / 100), 2)
        return self.precio

    def __str__(self):
        return self.nombre


class Agregados(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    # productosRelacionado = models.CharField(max_length=50) debe ser una lista
    

    def __str__(self):
        return self.nombre
    


