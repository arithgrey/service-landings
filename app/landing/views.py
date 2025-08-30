from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import LandingTemplate, Landing, ProductLanding
from .serializers import (
    LandingTemplateSerializer, LandingSerializer, 
    LandingDetailSerializer, ProductLandingsSerializer
)

class LandingTemplateViewSet(viewsets.ModelViewSet):
    queryset = LandingTemplate.objects.all()
    serializer_class = LandingTemplateSerializer
    
    def get_queryset(self):
        queryset = LandingTemplate.objects.all()
        if self.action == 'list':
            queryset = queryset.filter(is_active=True)
        return queryset

class LandingViewSet(viewsets.ModelViewSet):
    queryset = Landing.objects.all()
    serializer_class = LandingSerializer
    
    def get_queryset(self):
        queryset = Landing.objects.select_related('template')
        if self.action == 'list':
            queryset = queryset.filter(is_active=True)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LandingDetailSerializer
        return LandingSerializer
    
    @action(detail=False, methods=['get'])
    def by_product(self, request):
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({"error": "product_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product_id = int(product_id)
        except ValueError:
            return Response({"error": "product_id debe ser un número"}, status=status.HTTP_400_BAD_REQUEST)
        
        landings = self.get_queryset().filter(product_id=product_id)
        
        data = {
            'product_id': product_id,
            'landings': landings
        }
        
        serializer = ProductLandingsSerializer(data)
        return Response(serializer.data)


class ProductLandingViewSet(viewsets.ModelViewSet):
    """ViewSet para la relación Producto-Landing"""
    
    queryset = ProductLanding.objects.all()
    serializer_class = ProductLandingSerializer
    
    def get_queryset(self):
        """Filtra relaciones activas por defecto"""
        queryset = ProductLanding.objects.select_related("landing", "landing__template")
        if self.action == "list":
            queryset = queryset.filter(is_active=True)
        return queryset
    
    @action(detail=False, methods=["get"])
    def by_product(self, request):
        """Obtiene todas las landings de un producto específico"""
        product_id = request.query_params.get("product_id")
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
    def by_landing(self, request):
        """Obtiene todos los productos de una landing específica"""
        landing_id = request.query_params.get("landing_id")
        if not landing_id:
            return Response(
                {"error": "landing_id es requerido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            landing_id = int(landing_id)
        except ValueError:
            return Response(
                {"error": "landing_id debe ser un número"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product_landings = self.get_queryset().filter(landing_id=landing_id)
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
        landing_type = request.query_params.get("type")
        if not landing_type:
            return Response(
                {"error": "type es requerido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product_landings = self.get_queryset().filter(landing_type=landing_type)
        serializer = self.get_serializer(product_landings, many=True)
        return Response(serializer.data)
