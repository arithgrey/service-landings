import os
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from app.landing.models import LandingTemplate, ProductLanding
from decouple import config

@receiver(post_migrate)
def create_default_templates(sender, **kwargs):
    if not config('DJANGO_RUNNING_MIGRATIONS', default=False, cast=bool):
        return
    
    if sender.name != 'app.landing':
        return
    
    print("-------------CREANDO PLANTILLAS POR DEFECTO-----------")
    
    # Crear plantilla de Deportes
    deportes_template, created = LandingTemplate.objects.get_or_create(
        base_url="kits-para-pasar-al-siguiente-nivel",
        defaults={
            "name": "Deportes Template",
            "template_type": "hero",
            "config": {
                "title": "Kits para Pasar al Siguiente Nivel",
                "subtitle": "Equipamiento deportivo profesional",
                "button_text": "Ver Productos",
                "background_color": "#059669",
                "accent_color": "#10b981"
            }
        }
    )
    
    if created:
        print(f"Plantilla creada: {deportes_template.name}")
    else:
        print(f"Plantilla existente: {deportes_template.name}")
    
    # Crear plantilla de Testimonios
    testimonios_template, created = LandingTemplate.objects.get_or_create(
        base_url="testimonios-clientes-satisfechos",
        defaults={
            "name": "Testimonios Template",
            "template_type": "testimonial",
            "config": {
                "title": "Lo que dicen nuestros clientes",
                "subtitle": "Testimonios reales de usuarios satisfechos",
                "button_text": "Ver más testimonios",
                "background_color": "#1f2937",
                "accent_color": "#f59e0b"
            }
        }
    )
    
    if created:
        print(f"Plantilla creada: {testimonios_template.name}")
    else:
        print(f"Plantilla existente: {testimonios_template.name}")
    
    print("✅ Plantillas por defecto configuradas correctamente")
    print(f"Total plantillas: {LandingTemplate.objects.count()}")
    
    # Crear relaciones de ejemplo entre productos y plantillas
    print("-------------CREANDO RELACIONES PRODUCTO-PLANTILLA-----------")
    
    # Relación 1: Producto 123 con plantilla Deportes (principal)
    product_landing_1, created = ProductLanding.objects.get_or_create(
        product_id=123,
        template=deportes_template,
        defaults={
            "landing_type": "default",
            "is_primary": True
        }
    )
    
    if created:
        print(f"Relación creada: Producto 123 - Plantilla Deportes (Principal)")
    else:
        print(f"Relación existente: Producto 123 - Plantilla Deportes (Principal)")
    
    # Relación 2: Producto 456 con plantilla Deportes (promocional)
    product_landing_2, created = ProductLanding.objects.get_or_create(
        product_id=456,
        template=deportes_template,
        defaults={
            "landing_type": "promotional",
            "is_primary": False
        }
    )
    
    if created:
        print(f"Relación creada: Producto 456 - Plantilla Deportes (Promocional)")
    else:
        print(f"Relación existente: Producto 456 - Plantilla Deportes (Promocional)")
    
    # Relación 3: Producto 789 con plantilla Testimonios (estacional)
    product_landing_3, created = ProductLanding.objects.get_or_create(
        product_id=789,
        template=testimonios_template,
        defaults={
            "landing_type": "seasonal",
            "is_primary": False
        }
    )
    
    if created:
        print(f"Relación creada: Producto 789 - Plantilla Testimonios (Estacional)")
    else:
        print(f"Relación existente: Producto 789 - Plantilla Testimonios (Estacional)")
    
    print(f"Total relaciones producto-plantilla: {ProductLanding.objects.count()}")
    print("✅ Relaciones producto-plantilla configuradas correctamente")
