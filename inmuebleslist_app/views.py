"""from django.shortcuts import get_object_or_404, render
from inmuebleslist_app.models import Inmueble
from django.http import JsonResponse

# Create your views here.

def inmueble_list(request):
    inmueble = Inmueble.objects.all()
    data = {
        'inmuebles': list(inmueble.values())
    }
    return JsonResponse(data) 

def inmueble_detalles(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)
    data = {
        'direccion': inmueble.direccion,
        'pais': inmueble.pais,
        'descripcion': inmueble.descripcion,
        'imagen': inmueble.imagen,
        'active': inmueble.active,
    }
    
    return JsonResponse(data)
"""