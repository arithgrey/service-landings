import os
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from app.landing.models import LandingTemplate, Landing, ProductLanding
from decouple import config

@receiver(post_migrate)
def create_default_landing(sender, **kwargs):
    if not config('DJANGO_RUNNING_MIGRATIONS', default=False, cast=bool):
        return
    
    if sender.name != 'app.landing':
        return
    
    print("-------------CREANDO LANDING POR DEFECTO-----------")
    
    # Crear template de Deportes
    deportes_template, created = LandingTemplate.objects.get_or_create(
        slug="deportes-template",
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
        print(f"Template creado: {deportes_template.name}")
    else:
        print(f"Template existente: {deportes_template.name}")
    
    # Crear landing por defecto de Deportes
    deportes_landing, created = Landing.objects.get_or_create(
        slug="kits-para-pasar-al-siguiente-nivel",
        defaults={
            "name": "Deportes",
            "template": deportes_template,
            "config": {
                "custom_title": "Kits para Pasar al Siguiente Nivel",
                "custom_subtitle": "Equipamiento deportivo de alta calidad",
                "custom_button_text": "Explorar Kits",
                "custom_background_color": "#059669",
                "custom_accent_color": "#10b981",
                "is_default": True,
                "example_urls": [
                    "https://enidservice.com/kits-para-pasar-al-siguiente-nivel?product=para-los-que-van-iniciando&category=pesas-y-barras",
                    "http://localhost:5173/kits-para-pasar-al-siguiente-nivel?product=para-los-que-van-iniciando&category=pesas-y-barras"
                ]
            }
        }
    )
    
    if created:
        print(f"Landing por defecto creada: {deportes_landing.name}")
        print(f"Slug: {deportes_landing.slug}")
        print(f"Template: {deportes_landing.template.name}")
    else:
        print(f"Landing por defecto existente: {deportes_landing.name}")
    
    print("✅ Landing por defecto 'Deportes' configurada correctamente")
    print(f"Total templates: {LandingTemplate.objects.count()}")
    print(f"Total landings: {Landing.objects.count()}")
    
    # Crear relaciones de ejemplo entre productos y landings
    print("-------------CREANDO RELACIONES PRODUCTO-LANDING-----------")
    
    # Relación 1: Producto 123 con landing Deportes (principal)
    product_landing_1, created = ProductLanding.objects.get_or_create(
        product_id=123,
        landing=deportes_landing,
        defaults={
            "landing_type": "default",
            "is_primary": True,
            "custom_config": {
                "product_specific_title": "Kits Deportivos para Producto 123",
                "product_specific_subtitle": "Equipamiento especializado para este producto"
            }
        }
    )
    
    if created:
        print(f"Relación creada: Producto 123 - Landing Deportes (Principal)")
    else:
        print(f"Relación existente: Producto 123 - Landing Deportes (Principal)")
    
    # Relación 2: Producto 456 con landing Deportes (promocional)
    product_landing_2, created = ProductLanding.objects.get_or_create(
        product_id=456,
        landing=deportes_landing,
        defaults={
            "landing_type": "promotional",
            "is_primary": False,
            "custom_config": {
                "product_specific_title": "Oferta Especial - Producto 456",
                "product_specific_subtitle": "Promoción limitada para este producto"
            }
        }
    )
    
    if created:
        print(f"Relación creada: Producto 456 - Landing Deportes (Promocional)")
    else:
        print(f"Relación existente: Producto 456 - Landing Deportes (Promocional)")
    
    # Relación 3: Producto 789 con landing Deportes (estacional)
    product_landing_3, created = ProductLanding.objects.get_or_create(
        product_id=789,
        landing=deportes_landing,
        defaults={
            "landing_type": "seasonal",
            "is_primary": False,
            "custom_config": {
                "product_specific_title": "Temporada Deportiva - Producto 789",
                "product_specific_subtitle": "Equipamiento para la temporada actual"
            }
        }
    )
    
    if created:
        print(f"Relación creada: Producto 789 - Landing Deportes (Estacional)")
    else:
        print(f"Relación existente: Producto 789 - Landing Deportes (Estacional)")
    
    print(f"Total relaciones producto-landing: {ProductLanding.objects.count()}")
    print("✅ Relaciones producto-landing configuradas correctamente")
