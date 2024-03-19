from rest_framework import serializers

from inmuebleslist_app.models import Inmueble, Empresa, Comentario


class ComentarioSerializer(serializers.ModelSerializer):
    comentario_user = serializers.StringRelatedField(read_only=True)
    inmueble_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comentario
        # fields = "__all__"
        exclude = ["inmueble"]


class InmuebleSerializer(serializers.ModelSerializer):
    # long_direccion = serializers.SerializerMethodField()

    comentarios = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = Inmueble
        fields = "__all__"
        # fields = ['id', 'active', 'pais', 'imagen']
        # exclude = ['id']


class EmpresaSerializer(serializers.ModelSerializer):
    inmuebles = InmuebleSerializer(many=True, read_only=True)
    # inmuebles= serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    """ inmuebles= serializers.HyperlinkedRelatedField(many=True, 
                                                   read_only=True,
                                                   view_name='inmueble-detalles')"""

    class Meta:
        model = Empresa
        fields = "__all__"

    """def get_long_direccion(self, object):
        cantidad = len(object.direccion)
        return cantidad    
    
    def validate(self, data):
        if data['direccion'] == data['pais']:
            raise serializers.ValidationError('El pais y la direccion deben ser diferentes')
        else: 
            return data
        
    def validate_imagen(self, data):
        if len(data) < 5:
            raise serializers.ValidationError("La url de la imagen es muy corta")
        else:
            return data """


"""
def column_longitud(value):
    if len(value) < 3:
        raise serializers.ValidationError("La valor es muy corto")

class InmuebleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    direccion = serializers.CharField(validators = [column_longitud])
    pais = serializers.CharField(validators = [column_longitud])
    descripcion = serializers.CharField()
    imagen = serializers.CharField()
    active = serializers.BooleanField()
    
    def create(self, validated_data):
        return Inmueble.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.pais = validated_data.get('pais', instance.pais)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.imagen = validated_data.get('imagen', instance.imagen)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    def validate(self, data):
        if data['direccion'] == data['pais']:
            raise serializers.ValidationError('El pais y la direccion deben ser diferentes')
        else: 
            return data
        
    def validate_imagen(self, data):
        if len(data) < 5:
            raise serializers.ValidationError("La url de la imagen es muy corta")
        else:
            return data
        """
