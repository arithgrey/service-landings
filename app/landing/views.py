from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import LandingTemplate, Landing
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
