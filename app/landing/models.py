from django.db import models
from django.urls import reverse


class LandingTemplate(models.Model):
    """Modelo para las plantillas de landing pages"""
    
    TEMPLATE_TYPES = [
        ('hero', 'Hero Section'),
        ('product', 'Product Showcase'),
        ('testimonial', 'Testimonials'),
        ('features', 'Features'),
        ('pricing', 'Pricing'),
        ('cta', 'Call to Action'),
    ]
    
    name = models.CharField(max_length=100, help_text="Nombre de la plantilla")
    base_url = models.CharField(
        max_length=200, 
        unique=True, 
        help_text="URL base de la plantilla (ej: kits-para-pasar-al-siguiente-nivel)"
    )
    template_type = models.CharField(
        max_length=50,
        choices=TEMPLATE_TYPES,
        help_text="Tipo de plantilla"
    )
    config = models.JSONField(
        default=dict,
        help_text="Configuración de la plantilla"
    )
    is_active = models.BooleanField(default=True, help_text="Indica si la plantilla está activa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Plantilla de Landing"
        verbose_name_plural = "Plantillas de Landing"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('landingtemplate-detail', kwargs={'pk': self.pk})
    
    def get_full_url(self, domain="https://enidservice.com"):
        """Genera la URL completa con el dominio"""
        return f"{domain}/{self.base_url}?"


class ProductLanding(models.Model):
    """Modelo para la relación entre productos y plantillas de landing"""
    
    LANDING_TYPES = [
        ('default', 'Landing por Defecto'),
        ('promotional', 'Landing Promocional'),
        ('seasonal', 'Landing Estacional'),
        ('category', 'Landing por Categoría'),
        ('custom', 'Landing Personalizada'),
    ]
    
    product_id = models.IntegerField(
        help_text="ID del producto en el servicio enid-store"
    )
    template = models.ForeignKey(
        LandingTemplate,
        on_delete=models.CASCADE,
        related_name='product_landings',
        help_text="Plantilla de landing asociada al producto"
    )
    landing_type = models.CharField(
        max_length=50,
        choices=LANDING_TYPES,
        default='custom',
        help_text="Tipo de landing para este producto"
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Indica si es la landing principal del producto"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si la relación está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', '-created_at']
        verbose_name = "Relación Producto-Plantilla"
        verbose_name_plural = "Relaciones Producto-Plantilla"
        unique_together = ['product_id', 'template']
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['template']),
            models.Index(fields=['is_primary']),
            models.Index(fields=['is_active']),
            models.Index(fields=['landing_type']),
        ]
    
    def __str__(self):
        return f"Producto {self.product_id} - {self.template.name}"
    
    def get_full_url(self, product_slug=None, category_slug=None, domain="https://enidservice.com"):
        """Genera la URL completa con parámetros dinámicos"""
        base_url = f"{domain}/{self.template.base_url}?"
        params = []
        
        if product_slug:
            params.append(f"product={product_slug}")
        if category_slug:
            params.append(f"category={category_slug}")
        
        if params:
            base_url += "&".join(params)
        
        return base_url
    
    @classmethod
    def get_primary_landing(cls, product_id):
        """Obtiene la landing principal de un producto"""
        try:
            return cls.objects.get(
                product_id=product_id,
                is_primary=True,
                is_active=True
            ).template
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_product_landings(cls, product_id):
        """Obtiene todas las landings de un producto"""
        return cls.objects.filter(
            product_id=product_id,
            is_active=True
        ).select_related('template')
