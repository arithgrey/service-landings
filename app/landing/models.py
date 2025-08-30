from django.db import models
from django.core.validators import MinLengthValidator

class LandingTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('hero', 'Hero Section'),
        ('product', 'Product Showcase'),
        ('testimonial', 'Testimonials'),
        ('features', 'Features'),
        ('pricing', 'Pricing'),
        ('cta', 'Call to Action'),
    ]
    
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    slug = models.SlugField(unique=True)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    config = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Landing(models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    slug = models.SlugField(unique=True)
    product_id = models.IntegerField()
    template = models.ForeignKey(LandingTemplate, on_delete=models.CASCADE, related_name='landings')
    config = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_full_config(self):
        full_config = self.template.config.copy()
        full_config.update(self.config)
        return full_config
    
    @property
    def url_path(self):
        return f"/landing/{self.slug}/"
    
    @classmethod
    def get_active_by_product(cls, product_id):
        return cls.objects.filter(product_id=product_id, is_active=True).select_related('template')

    def get_full_url(self, product_slug=None, category_slug=None):
        """Genera la URL completa con parámetros dinámicos"""
        base_url = f"/{self.slug}"
        params = []
        
        if product_slug:
            params.append(f"product={product_slug}")
        if category_slug:
            params.append(f"category={category_slug}")
        
        if params:
            base_url += "?" + "&".join(params)
        
        return base_url
    
    def get_example_urls(self):
        """Retorna ejemplos de URLs que se pueden generar"""
        return [
            f"/{self.slug}?product=para-los-que-van-iniciando&category=pesas-y-barras",
            f"/{self.slug}?product=intermedios&category=equipamiento",
            f"/{self.slug}?product=avanzados&category=accesorios",
        ]


class ProductLanding(models.Model):
    """Modelo para la relación muchos a muchos entre productos y landings"""
    
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
    landing = models.ForeignKey(
        Landing,
        on_delete=models.CASCADE,
        related_name='product_landings',
        help_text="Landing asociada al producto"
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
    custom_config = models.JSONField(
        default=dict,
        help_text="Configuración personalizada para este producto en esta landing"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si la relación está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', '-created_at']
        verbose_name = "Relación Producto-Landing"
        verbose_name_plural = "Relaciones Producto-Landing"
        unique_together = ['product_id', 'landing']
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['landing']),
            models.Index(fields=['is_primary']),
            models.Index(fields=['is_active']),
            models.Index(fields=['landing_type']),
        ]
    
    def __str__(self):
        return f"Producto {self.product_id} - {self.landing.name}"
    
    def get_full_url(self, product_slug=None, category_slug=None):
        """Genera la URL completa con parámetros dinámicos"""
        return self.landing.get_full_url(product_slug, category_slug)
    
    def get_custom_config(self):
        """Obtiene la configuración personalizada para este producto"""
        base_config = self.landing.config.copy()
        base_config.update(self.custom_config)
        return base_config
    
    @classmethod
    def get_primary_landing(cls, product_id):
        """Obtiene la landing principal de un producto"""
        try:
            return cls.objects.get(
                product_id=product_id,
                is_primary=True,
                is_active=True
            ).landing
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_product_landings(cls, product_id):
        """Obtiene todas las landings de un producto"""
        return cls.objects.filter(
            product_id=product_id,
            is_active=True
        ).select_related('landing', 'landing__template')
