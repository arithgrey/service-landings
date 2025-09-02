from rest_framework import serializers
from .models import LandingTemplate, ProductLanding


class LandingTemplateSerializer(serializers.ModelSerializer):
    """Serializer para las plantillas de landing"""
    
    full_url_example = serializers.SerializerMethodField()
    
    class Meta:
        model = LandingTemplate
        fields = [
            'id', 'name', 'base_url', 'template_type', 'config', 
            'is_active', 'full_url_example', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_url_example(self, obj):
        """Retorna un ejemplo de URL completa"""
        return obj.get_full_url()


class ProductLandingSerializer(serializers.ModelSerializer):
    """Serializer para la relación Producto-Plantilla"""
    
    template = LandingTemplateSerializer(read_only=True)
    template_id = serializers.IntegerField(write_only=True)
    full_url_example = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductLanding
        fields = [
            'id', 'product_id', 'template', 'template_id',
            'is_primary', 'is_active', 'full_url_example', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_template_id(self, value):
        """Valida que el template_id existe y está activo"""
        try:
            template = LandingTemplate.objects.get(id=value, is_active=True)
        except LandingTemplate.DoesNotExist:
            raise serializers.ValidationError("Plantilla no encontrada o inactiva")
        return value
    
    def validate(self, data):
        """Valida que no haya duplicados de producto-template"""
        product_id = data.get('product_id')
        template_id = data.get('template_id')
        
        if ProductLanding.objects.filter(
            product_id=product_id,
            template_id=template_id
        ).exists():
            raise serializers.ValidationError("Ya existe esta relación producto-plantilla")
        
        return data
    
    def get_full_url_example(self, obj):
        """Retorna un ejemplo de URL completa con parámetros"""
        return obj.get_full_url(
            product_slug="para-los-que-van-iniciando",
            category_slug="pesas-y-barras"
        )
