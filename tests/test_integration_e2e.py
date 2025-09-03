import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from app.landing.models import LandingTemplate, ProductLanding
from app.landing.seeds.default_data import DEFAULT_LANDING_TEMPLATES, DEFAULT_PRODUCT_LANDINGS


class TestLandingTemplateIntegration(TestCase):
    """Tests de integración end-to-end para LandingTemplate"""
    
    def setUp(self):
        self.client = APIClient()
        self.template_data = DEFAULT_LANDING_TEMPLATES[0]
    
    def test_create_landing_template_e2e(self):
        """Test E2E: Crear plantilla de landing y verificar persistencia"""
        # Crear plantilla
        template = LandingTemplate.objects.create(**self.template_data)
        
        # Verificar que se guardó en la base de datos
        saved_template = LandingTemplate.objects.get(id=template.id)
        self.assertEqual(saved_template.name, "¿Cuál es el proceso - Pago contra entrega?")
        self.assertEqual(saved_template.base_url, "kits-para-pasar-al-siguiente-nivel")
        self.assertEqual(saved_template.template_type, "single_product")
        self.assertTrue(saved_template.is_active)
    
    def test_landing_template_api_e2e(self):
        """Test E2E: API de plantillas de landing"""
        # Crear plantilla
        template = LandingTemplate.objects.create(**self.template_data)
        
        # Test GET /api/landing-templates/
        response = self.client.get(reverse('landingtemplate-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Test GET /api/landing-templates/{id}/
        response = self.client.get(reverse('landingtemplate-detail', kwargs={'pk': template.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], template.name)
        self.assertEqual(response.data['base_url'], template.base_url)
    
    def test_landing_template_url_generation_e2e(self):
        """Test E2E: Generación de URLs de plantillas"""
        template = LandingTemplate.objects.create(**self.template_data)
        
        # Verificar URL completa
        full_url = template.get_full_url()
        expected_url = "https://enidservice.com/kits-para-pasar-al-siguiente-nivel?"
        self.assertEqual(full_url, expected_url)
        
        # Verificar URL con parámetros
        full_url_with_params = template.get_full_url(domain="https://test.com")
        expected_url_with_params = "https://test.com/kits-para-pasar-al-siguiente-nivel?"
        self.assertEqual(full_url_with_params, expected_url_with_params)


class TestProductLandingIntegration(TestCase):
    """Tests de integración end-to-end para ProductLanding"""
    
    def setUp(self):
        self.client = APIClient()
        self.template = LandingTemplate.objects.create(**DEFAULT_LANDING_TEMPLATES[0])
    
    def test_create_product_landing_e2e(self):
        """Test E2E: Crear relación producto-plantilla"""
        product_landing_data = {
            'product_id': 1001,
            'template': self.template,
            'is_primary': True,
            'is_active': True
        }
        
        product_landing = ProductLanding.objects.create(**product_landing_data)
        
        # Verificar persistencia
        saved_pl = ProductLanding.objects.get(id=product_landing.id)
        self.assertEqual(saved_pl.product_id, 1001)
        self.assertEqual(saved_pl.template, self.template)
        self.assertTrue(saved_pl.is_primary)
        self.assertTrue(saved_pl.is_active)
    
    def test_product_landing_url_generation_e2e(self):
        """Test E2E: Generación de URLs con parámetros de producto"""
        product_landing = ProductLanding.objects.create(
            product_id=1001,
            template=self.template,
            is_primary=True
        )
        
        # URL con slug de producto
        url_with_product = product_landing.get_full_url(product_slug="kit-basico")
        expected_url = "https://enidservice.com/kits-para-pasar-al-siguiente-nivel?product=kit-basico"
        self.assertEqual(url_with_product, expected_url)
        
        # URL con slug de categoría
        url_with_category = product_landing.get_full_url(category_slug="fitness")
        expected_url = "https://enidservice.com/kits-para-pasar-al-siguiente-nivel?category=fitness"
        self.assertEqual(url_with_category, expected_url)
        
        # URL con ambos parámetros
        url_with_both = product_landing.get_full_url(
            product_slug="kit-basico", 
            category_slug="fitness"
        )
        expected_url = "https://enidservice.com/kits-para-pasar-al-siguiente-nivel?product=kit-basico&category=fitness"
        self.assertEqual(url_with_both, expected_url)
    
    def test_get_primary_landing_e2e(self):
        """Test E2E: Obtener landing principal de un producto"""
        # Limpiar datos existentes para este test
        ProductLanding.objects.filter(product_id=9999).delete()
        
        # Crear landing principal
        primary_landing = ProductLanding.objects.create(
            product_id=9999,
            template=self.template,
            is_primary=True,
            is_active=True
        )
        
        # Obtener landing principal
        primary = ProductLanding.get_primary_landing(9999)
        self.assertEqual(primary, self.template)
        
        # Obtener todas las landings del producto
        all_landings = ProductLanding.get_product_landings(9999)
        self.assertEqual(all_landings.count(), 1)
    
    def test_product_landing_unique_constraint_e2e(self):
        """Test E2E: Constraint único producto-plantilla"""
        # Crear primera relación
        ProductLanding.objects.create(
            product_id=1001,
            template=self.template,
            is_primary=True
        )
        
        # Intentar crear duplicado debe fallar
        with self.assertRaises(Exception):
            ProductLanding.objects.create(
                product_id=1001,
                template=self.template,
                is_primary=False
            )


class TestLoadDefaultDataIntegration(TestCase):
    """Tests de integración para el comando load_default_data"""
    
    def setUp(self):
        from django.core.management import call_command
        self.call_command = call_command
    
    def test_load_default_data_e2e(self):
        """Test E2E: Cargar datos por defecto"""
        # Ejecutar comando
        self.call_command('load_default_data')
        
        # Verificar que se creó la plantilla
        template = LandingTemplate.objects.get(base_url="kits-para-pasar-al-siguiente-nivel")
        self.assertEqual(template.name, "¿Cuál es el proceso - Pago contra entrega?")
        self.assertEqual(template.template_type, "single_product")
        self.assertTrue(template.is_active)
    
    def test_load_default_data_idempotent_e2e(self):
        """Test E2E: Comando es idempotente (puede ejecutarse múltiples veces)"""
        # Ejecutar primera vez
        self.call_command('load_default_data')
        count_first = LandingTemplate.objects.count()
        
        # Ejecutar segunda vez
        self.call_command('load_default_data')
        count_second = LandingTemplate.objects.count()
        
        # Debe tener la misma cantidad
        self.assertEqual(count_first, count_second)
    
    def test_load_default_data_force_e2e(self):
        """Test E2E: Cargar datos con --force"""
        # Cargar datos iniciales
        self.call_command('load_default_data')
        
        # Modificar plantilla
        template = LandingTemplate.objects.get(base_url="kits-para-pasar-al-siguiente-nivel")
        template.name = "Nombre Modificado"
        template.save()
        
        # Cargar con --force
        self.call_command('load_default_data', force=True)
        
        # Verificar que se restauró el nombre original
        template.refresh_from_db()
        self.assertEqual(template.name, "¿Cuál es el proceso - Pago contra entrega?")


class TestLandingTemplateModelValidation(TestCase):
    """Tests de validación de modelos"""
    
    def test_landing_template_required_fields_e2e(self):
        """Test E2E: Campos requeridos de LandingTemplate"""
        # Crear plantilla con datos mínimos
        template_data = {
            'name': 'Test Template',
            'base_url': 'test-template',
            'template_type': 'single_product'
        }
        
        template = LandingTemplate.objects.create(**template_data)
        
        # Verificar valores por defecto
        self.assertTrue(template.is_active)
        self.assertIsNotNone(template.created_at)
        self.assertIsNotNone(template.updated_at)
    
    def test_landing_template_base_url_unique_e2e(self):
        """Test E2E: Base URL debe ser único"""
        template_data = {
            'name': 'Test Template',
            'base_url': 'test-template',
            'template_type': 'single_product'
        }
        
        # Crear primera plantilla
        LandingTemplate.objects.create(**template_data)
        
        # Intentar crear segunda con mismo base_url debe fallar
        with self.assertRaises(Exception):
            LandingTemplate.objects.create(**template_data)
    
    def test_product_landing_foreign_key_e2e(self):
        """Test E2E: Relación ForeignKey ProductLanding -> LandingTemplate"""
        template = LandingTemplate.objects.create(
            name='Test Template',
            base_url='test-template',
            template_type='single_product'
        )
        
        product_landing = ProductLanding.objects.create(
            product_id=1001,
            template=template,
            is_primary=True
        )
        
        # Verificar relación
        self.assertEqual(product_landing.template, template)
        self.assertEqual(template.product_landings.count(), 1)
        
        # Eliminar template debe eliminar product_landing (CASCADE)
        template.delete()
        self.assertEqual(ProductLanding.objects.count(), 0) 