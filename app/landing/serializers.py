from rest_framework import serializers
from .models import LandingTemplate, Landing

class LandingTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingTemplate
        fields = ['id', 'name', 'slug', 'template_type', 'config', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class LandingSerializer(serializers.ModelSerializer):
    template = LandingTemplateSerializer(read_only=True)
    template_id = serializers.IntegerField(write_only=True)
    url_path = serializers.ReadOnlyField()
    
    class Meta:
        model = Landing
        fields = ['id', 'name', 'slug', 'product_id', 'template', 'template_id', 'config', 'is_active', 'url_path', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_template_id(self, value):
        try:
            template = LandingTemplate.objects.get(id=value, is_active=True)
        except LandingTemplate.DoesNotExist:
            raise serializers.ValidationError("Template no encontrado o inactivo")
        return value

class LandingDetailSerializer(LandingSerializer):
    full_config = serializers.SerializerMethodField()
    
    class Meta(LandingSerializer.Meta):
        fields = LandingSerializer.Meta.fields + ['full_config']
    
    def get_full_config(self, obj):
        return obj.get_full_config()

class ProductLandingsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    landings = LandingSerializer(many=True, read_only=True)
    count = serializers.SerializerMethodField()
    
    def get_count(self, obj):
        return len(obj['landings'])
