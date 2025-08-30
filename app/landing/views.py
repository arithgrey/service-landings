from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import LandingTemplate, ProductLanding
from .serializers import LandingTemplateSerializer, ProductLandingSerializer


class LandingTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet para las plantillas de landing"""
    
    queryset = LandingTemplate.objects.all()
    serializer_class = LandingTemplateSerializer
    
    def get_queryset(self):
        """Filtra plantillas activas por defecto"""
        queryset = LandingTemplate.objects.all()
        if self.action == 'list':
            queryset = queryset.filter(is_active=True)
        return queryset
    
    @action(detail=False, methods=["get"])
    def by_type(self, request):
        """Obtiene plantillas por tipo"""
        template_type = request.query_params.get("type")
        if template_type:
            templates = self.get_queryset().filter(template_type=template_type)
        else:
            templates = self.get_queryset()
        
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def template_types(self, request):
        """Obtiene las opciones válidas de template_type"""
        from .models import LandingTemplate
        field = LandingTemplate._meta.get_field('template_type')
        choices = [{"value": choice[0], "label": choice[1]} for choice in field.choices]
        return Response({"template_types": choices})


class ProductLandingViewSet(viewsets.ModelViewSet):
    """ViewSet para la relación Producto-Plantilla"""
    
    queryset = ProductLanding.objects.all().select_related('template')
    serializer_class = ProductLandingSerializer
    
    def get_queryset(self):
        """Filtra relaciones activas por defecto"""
        queryset = ProductLanding.objects.select_related('template')
        if self.action == 'list':
            queryset = queryset.filter(is_active=True)
        return queryset
    
    @action(detail=False, methods=["get"])
    def by_product(self, request):
        """Obtiene todas las plantillas de un producto específico"""
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response(
                {"error": "product_id es requerido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product_id = int(product_id)
        except ValueError:
            return Response(
                {"error": "product_id debe ser un número"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product_landings = self.get_queryset().filter(product_id=product_id)
        serializer = self.get_serializer(product_landings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def by_template(self, request):
        """Obtiene todos los productos de una plantilla específica"""
        template_id = request.query_params.get('template_id')
        if not template_id:
            return Response(
                {"error": "template_id es requerido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            template_id = int(template_id)
        except ValueError:
            return Response(
                {"error": "template_id debe ser un número"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product_landings = self.get_queryset().filter(template_id=template_id)
        serializer = self.get_serializer(product_landings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def primary_landings(self, request):
        """Obtiene las landings principales de productos"""
        product_landings = self.get_queryset().filter(is_primary=True)
        serializer = self.get_serializer(product_landings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def by_type(self, request):
        """Obtiene relaciones por tipo de landing"""
        landing_type = request.query_params.get('type')
        if not landing_type:
            return Response(
                {"error": "type es requerido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product_landings = self.get_queryset().filter(landing_type=landing_type)
        serializer = self.get_serializer(product_landings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def landing_types(self, request):
        """Obtiene las opciones válidas de landing_type"""
        from .models import ProductLanding
        field = ProductLanding._meta.get_field('landing_type')
        choices = [{"value": choice[0], "label": choice[1]} for choice in field.choices]
        return Response({"landing_types": choices})
