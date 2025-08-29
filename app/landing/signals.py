import os
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from app.landing.models import LandingTemplate, Landing
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
            "product_id": 999,  # ID especial para landing por defecto
            "template": deportes_template,
            "config": {
                "custom_title": "Kits para Pasar al Siguiente Nivel",
                "custom_subtitle": "Equipamiento deportivo de alta calidad",
                "custom_button_text": "Explorar Kits",
                "custom_background_color": "#059669",
                "custom_accent_color": "#10b981",
                "is_default": True
            }
        }
    )
    
    if created:
        print(f"Landing por defecto creada: {deportes_landing.name}")
        print(f"Slug: {deportes_landing.slug}")
        print(f"Product ID: {deportes_landing.product_id}")
        print(f"Template: {deportes_landing.template.name}")
    else:
        print(f"Landing por defecto existente: {deportes_landing.name}")
    
    print("✅ Landing por defecto 'Deportes' configurada correctamente")
    print(f"Total templates: {LandingTemplate.objects.count()}")
    print(f"Total landings: {Landing.objects.count()}")
