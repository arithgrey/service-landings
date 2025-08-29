from django.test import TestCase
from app.landing.models import LandingTemplate, Landing

class BasicTest(TestCase):
    def test_create_template(self):
        template = LandingTemplate.objects.create(
            name="Test Template",
            slug="test-template",
            template_type="hero"
        )
        self.assertEqual(template.name, "Test Template")
        self.assertTrue(template.is_active)
    
    def test_create_landing(self):
        template = LandingTemplate.objects.create(
            name="Test Template",
            slug="test-template",
            template_type="hero"
        )
        
        landing = Landing.objects.create(
            name="Test Landing",
            slug="test-landing",
            product_id=1,
            template=template
        )
        
        self.assertEqual(landing.name, "Test Landing")
        self.assertEqual(landing.product_id, 1)
        self.assertEqual(landing.template, template)
