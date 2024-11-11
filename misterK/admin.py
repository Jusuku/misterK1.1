from django.contrib import admin
from misterK.models import Productos,Categorias,Agregados

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','descripcion','categoria','oferta','porcentajeOferta']
admin.site.register(Productos,ProductoAdmin)

class CategoriasAdmin(admin.ModelAdmin):
    list_display = ['nombre_categoria']
admin.site.register(Categorias,CategoriasAdmin)

class AgregadosAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio']
admin.site.register(Agregados,AgregadosAdmin)