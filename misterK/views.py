from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from misterK.models import Productos, Categorias , Agregados
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def index(request):
    
    productos_en_oferta = Productos.objects.filter(oferta=True)[:6]  
    data = {
        'productos_en_oferta': productos_en_oferta,
    }
    
    return render(request, 'index.html',data)

def agregados(request):
    
    return render(request, 'agregados.html')

def menu(request):
    productos = Productos.objects.all()
    categorias = Categorias.objects.all()
    agregados = Agregados.objects.all()
    
    data = {
        'productos' : productos,
        'categorias' : categorias,
        'agregados' : agregados
    }
    
    return render(request, 'menu.html',data)

def ubicacion(request):
    
    return render(request, 'ubicacion.html')

def login(request):
    
    return render(request, 'login.html')

def detalle_producto(request, id):
    producto = get_object_or_404(Productos, id=id)
    categorias = Categorias.objects.all()
    productos_relacionados = Productos.objects.filter(categoria=producto.categoria).exclude(id=producto.id)[:3]
    data = {
        'producto': producto,
        'categorias' : categorias,
        'productos_relacionados' : productos_relacionados 
    }
    return render(request, 'detalle_producto.html',data)

def categoria(request,id) :
    categoria = get_object_or_404(Categorias, id=id)
    categorias = Categorias.objects.all()
    productos_en_categoria = Productos.objects.filter(categoria=categoria)
    data = {
        'categoria':categoria,
        'categorias' : categorias,
        'productos_en_categoria': productos_en_categoria
        
    }
    return render(request,'categorias.html', data)

def carrito(request):
    carrito = request.session.get('carrito', {})

    # Calcular el total del carrito
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': total,
    })

def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id)
    
    # Obtener el carrito de la sesión (si existe)
    carrito = request.session.get('carrito', {})
    
    # Calcular el precio con descuento
    precio_producto = producto.precio_con_descuento()  # Usar el método para obtener el precio con descuento

    # Verifica si el producto ya está en el carrito y si es así, aumenta la cantidad
    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        carrito[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': precio_producto,  # Guardamos el precio con descuento
            'cantidad': 1,
            'id': producto.id
        }

    # Guardar el carrito actualizado en la sesión
    request.session['carrito'] = carrito

    return JsonResponse({'mensaje': f'Agregaste {producto.nombre} al carrito', 'carrito': carrito})

def eliminar_producto(request, producto_id):
    carrito = request.session.get('carrito', {})

    # Verificar si el producto está en el carrito
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]  # Eliminar el producto del carrito
        request.session['carrito'] = carrito  # Guardar los cambios en la sesión
        messages.success(request, "Producto eliminado del carrito.")
    else:
        messages.error(request, "El producto no está en el carrito.")

    # Redirigir al carrito después de eliminar el producto
    return redirect('carrito')

def procesar_compra(request):
    # Verificar si hay productos en el carrito
    carrito = request.session.get('carrito', {})

    if carrito:
        # Vaciar el carrito (simulando que se ha comprado)
        request.session['carrito'] = {}

        # Mostrar un mensaje de éxito
        messages.success(request, "¡Compra realizada con éxito! Gracias por tu compra.")

    else:
        # Mostrar un mensaje de error si el carrito está vacío
        messages.error(request, "Tu carrito está vacío. No puedes realizar la compra.")

    # Redirigir al usuario a la página del carrito después de simular la compra
    return redirect('carrito')

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:  # Verifica si es staff (permiso de admin)
            auth_login(request, user)  # Usa auth_login en lugar de login
            return redirect('administracion')  # Redirige a la URL de administracion.html
        else:
            messages.error(request, 'Error en el nombre de usuario o la contraseña')

    return render(request, 'login.html')

def administracion(request):
    productos = Productos.objects.all()      # Carga todos los productos
    categorias = Categorias.objects.all()    # Carga todas las categorías
    usuarios = User.objects.all()           # Carga todos los usuarios

    if request.method == 'POST':
        # Agregar nuevo producto
        if 'add_producto' in request.POST:
            nombre = request.POST['nombre']
            precio = request.POST['precio']
            Productos.objects.create(nombre=nombre, precio=precio)
            messages.success(request, 'Producto agregado exitosamente')
            return redirect('administracion')

        # Actualizar producto
        if 'update_producto' in request.POST:
            producto_id = request.POST['producto_id']
            producto = Productos.objects.get(id=producto_id)
            producto.nombre = request.POST['nombre']
            producto.precio = request.POST['precio']
            producto.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('administracion')

        # Eliminar producto
        if 'delete_producto' in request.POST:
            producto_id = request.POST['producto_id']
            producto = Productos.objects.get(id=producto_id)
            producto.delete()
            messages.success(request, 'Producto eliminado exitosamente')
            return redirect('administracion')

        # Similarmente para Categorías y Usuarios
        # (Agregar, actualizar, eliminar categorías y usuarios de forma similar)

    data = {
        'productos': productos,
        'categorias': categorias,
        'usuarios': usuarios,
    }

    return render(request, 'administracion.html', data)