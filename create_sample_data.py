#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from app.landing.models import LandingTemplate, Landing

# Crear templates de ejemplo
hero_template = LandingTemplate.objects.create(
    name="Hero Template",
    slug="hero-template",
    template_type="hero",
    config={
        "title": "Título Hero",
        "subtitle": "Subtítulo Hero",
        "button_text": "Comprar Ahora",
        "background_color": "#1f2937"
    }
)

product_template = LandingTemplate.objects.create(
    name="Product Template",
    slug="product-template",
    template_type="product",
    config={
        "title": "Título Producto",
        "description": "Descripción del producto",
        "price_color": "#f59e0b",
        "features": ["Feature 1", "Feature 2", "Feature 3"]
    }
)

# Crear landings de ejemplo
landing1 = Landing.objects.create(
    name="Landing Hero Producto 1",
    slug="landing-hero-1",
    product_id=1,
    template=hero_template,
    config={
        "custom_title": "Producto Increíble",
        "custom_subtitle": "El mejor producto del mercado"
    }
)

landing2 = Landing.objects.create(
    name="Landing Producto 1",
    slug="landing-product-1",
    product_id=1,
    template=product_template,
    config={
        "custom_title": "Detalles del Producto",
        "custom_price": "$99.99"
    }
)

landing3 = Landing.objects.create(
    name="Landing Hero Producto 2",
    slug="landing-hero-2",
    product_id=2,
    template=hero_template,
    config={
        "custom_title": "Otro Producto",
        "custom_subtitle": "También increíble"
    }
)

print("✅ Datos de ejemplo creados exitosamente!")
print(f"Templates creados: {LandingTemplate.objects.count()}")
print(f"Landings creados: {Landing.objects.count()}")
