from rest_framework.response import Response
from inmuebleslist_app.models import Inmueble, Empresa, Comentario
from inmuebleslist_app.api import serializer as SR
from rest_framework.validators import ValidationError

# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from inmuebleslist_app.api.permissions import (
    IsAdminOrReadOnly,
    IsComentarioUserOrReadOnly,
)
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class ComentariosCreate(generics.CreateAPIView):
    serializer_class = SR.ComentarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comentario.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        inmueble = Inmueble.objects.get(pk=pk)
        user = self.request.user

        comentario_queryset = Comentario.objects.filter(
            inmueble=inmueble, comentario_user=user
        )

        if comentario_queryset.exists():
            raise ValidationError(
                "El usuario ya escribio un comentario para este inmueble"
            )

        if inmueble.number_calificacion == 0:
            inmueble.avg_calificacion = serializer.validated_data["calificacion"]
        else:
            inmueble.avg_calificacion = (
                serializer.validated_data["calificacion"] + inmueble.avg_calificacion
            ) / 2

        inmueble.number_calificacion += 1
        inmueble.save()

        serializer.save(inmueble_id=inmueble.id, comentario_user=user)


class ComentariosList(generics.ListCreateAPIView):
    serializer_class = SR.ComentarioSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Comentario.objects.filter(inmueble=pk)


class ComentariosDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = SR.ComentarioSerializer
    permission_classes = [IsComentarioUserOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


"""class ComentariosList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Comentario.objects.all()
    serializer_class = SR.ComentarioSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class CometariosDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Comentario.objects.all()
    serializer_class = SR.ComentarioSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)"""


class EmpresaVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Empresa.objects.all()
    serializer_class = SR.EmpresaSerializer


"""class EmpresaVS(viewsets.ViewSet):

    def list(self, request):
        empresa = Empresa.objects.all()
        serializer = SR.EmpresaSerializer(empresa, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Empresa.objects.all()
        inmuebles = get_object_or_404(queryset, pk=pk)
        serializer = SR.EmpresaSerializer(inmuebles)
        return Response(serializer.data)

    def create(self, request):
        serializer = SR.EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SR.EmpresaSerializer(empresa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

        empresa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


class EmpresaAV(APIView):
    def get(self, request):
        empresa = Empresa.objects.all()
        serializer = SR.EmpresaSerializer(
            empresa, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = SR.EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmpresaDetalleAV(APIView):

    def get(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)

        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SR.EmpresaSerializer(empresa, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SR.EmpresaSerializer(
            empresa, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        empresa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InmueblesListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        inmuebles = Inmueble.objects.all()
        serializer = SR.InmuebleSerializer(inmuebles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SR.InmuebleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InmuebleDetallesAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            inmueble = Inmueble.objects.get(pk=pk)
        except Inmueble.DoesNotExist:
            return Response(
                {"Error": "Inmueble no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SR.InmuebleSerializer(inmueble)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            inmueble = Inmueble.objects.get(pk=pk)
        except Inmueble.DoesNotExist:
            return Response(
                {"Error": "Inmueble no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SR.InmuebleSerializer(inmueble, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            inmueble = Inmueble.objects.get(pk=pk)
        except Inmueble.DoesNotExist:
            return Response(
                {"Error": "Inmueble no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        inmueble.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
@api_view(['GET', 'POST'])
def inmueble_list(request):
    if request.method == 'GET':
        inmuebles = Inmueble.objects.all()
        serializer = SR.InmuebleSerializer(inmuebles, many=True)    
        return Response(serializer.data)
    if request.method == 'POST':
        de_serializer = SR.InmuebleSerializer(data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response(de_serializer.data)
        else:
            return Response(de_serializer.errors)
        
            
@api_view(['GET', 'PUT', 'DELETE'])
def inmueble_detalles(request, pk):    
    try:
        if request.method == 'GET':
            inmueble = Inmueble.objects.get(pk=pk)
            serializer = SR.InmuebleSerializer(inmueble)
            return Response(serializer.data) 
    except Inmueble.DoesNotExist:
        return Response({'Error': 'El inmueble no existe'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'PUT':
        inmueble = Inmueble.objects.get(pk=pk)
        de_serializer = SR.InmuebleSerializer(inmueble, data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response(de_serializer.data)
        else:
            return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
    if request.method == 'DELETE':
        try:
            inmueble = Inmueble.objects.get(pk=pk)
            inmueble.delete()
        except Inmueble.DoesNotExist:
            return Response({'error': 'El inmueble no existe'},status=status.HTTP_404_NOT_FOUND)    
        
        return Response(status=status.HTTP_204_NO_CONTENT)"""
