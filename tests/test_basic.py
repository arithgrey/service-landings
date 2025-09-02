from django.test import TestCase
from app.landing.models import LandingTemplate, ProductLanding

class BasicTest(TestCase):
    def test_create_template(self):
        template = LandingTemplate.objects.create(
            name="Test Template",
            base_url="test-template",
            template_type="hero"
        )
        self.assertEqual(template.name, "Test Template")
        self.assertTrue(template.is_active)
    
    def test_create_product_landing(self):
        template = LandingTemplate.objects.create(
            name="Test Template",
            base_url="test-template",
            template_type="hero"
        )
        
        landing = ProductLanding.objects.create(
            product_id=1,
            template=template,
            is_primary=True
        )
        
        self.assertEqual(landing.product_id, 1)
        self.assertEqual(landing.template, template)
        self.assertTrue(landing.is_primary)
