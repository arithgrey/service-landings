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
