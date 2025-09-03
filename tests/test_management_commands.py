from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from io import StringIO
from app.landing.models import LandingTemplate, ProductLanding


class TestLoadDefaultDataCommand(TestCase):
    """Tests específicos para el comando load_default_data"""
    
    def test_load_default_data_success(self):
        """Test: Comando ejecuta exitosamente"""
        out = StringIO()
        
        # Ejecutar comando
        call_command('load_default_data', stdout=out)
        
        # Verificar salida
        output = out.getvalue()
        self.assertIn('🚀 Iniciando carga de datos por defecto...', output)
        self.assertIn('✅ Datos cargados exitosamente!', output)
        
        # Verificar que se creó la plantilla
        template = LandingTemplate.objects.get(base_url="kits-para-pasar-al-siguiente-nivel")
        self.assertEqual(template.name, "¿Cuál es el proceso - Pago contra entrega?")
    
    def test_load_default_data_template_only(self):
        """Test: Comando con --template-only"""
        out = StringIO()
        
        # Ejecutar comando solo plantillas
        call_command('load_default_data', template_only=True, stdout=out)
        
        # Verificar que se creó la plantilla
        template = LandingTemplate.objects.get(base_url="kits-para-pasar-al-siguiente-nivel")
        self.assertEqual(template.name, "¿Cuál es el proceso - Pago contra entrega?")
        
        # Verificar que no hay relaciones producto-plantilla
        self.assertEqual(ProductLanding.objects.count(), 0)
    
    def test_load_default_data_force_update(self):
        """Test: Comando con --force actualiza plantillas existentes"""
        # Crear plantilla inicial
        template = LandingTemplate.objects.create(
            name="Nombre Original",
            base_url="kits-para-pasar-al-siguiente-nivel",
            template_type="single_product"
        )
        
        out = StringIO()
        
        # Ejecutar comando con --force
        call_command('load_default_data', force=True, stdout=out)
        
        # Verificar que se actualizó
        template.refresh_from_db()
        self.assertEqual(template.name, "¿Cuál es el proceso - Pago contra entrega?")
        
        # Verificar salida
        output = out.getvalue()
        self.assertIn('🔄 Plantilla actualizada', output)
    
    def test_load_default_data_skip_existing(self):
        """Test: Comando salta plantillas existentes sin --force"""
        # Crear plantilla inicial
        template = LandingTemplate.objects.create(
            name="Nombre Original",
            base_url="kits-para-pasar-al-siguiente-nivel",
            template_type="single_product"
        )
        
        out = StringIO()
        
        # Ejecutar comando sin --force
        call_command('load_default_data', stdout=out)
        
        # Verificar que NO se actualizó
        template.refresh_from_db()
        self.assertEqual(template.name, "Nombre Original")
        
        # Verificar salida
        output = out.getvalue()
        self.assertIn('⏭️ Plantilla ya existe', output)
    
    def test_load_default_data_multiple_executions(self):
        """Test: Múltiples ejecuciones del comando"""
        out = StringIO()
        
        # Primera ejecución
        call_command('load_default_data', stdout=out)
        count_first = LandingTemplate.objects.count()
        
        # Segunda ejecución
        call_command('load_default_data', stdout=out)
        count_second = LandingTemplate.objects.count()
        
        # Debe mantener la misma cantidad
        self.assertEqual(count_first, count_second)
        
        # Verificar que la plantilla existe
        template = LandingTemplate.objects.get(base_url="kits-para-pasar-al-siguiente-nivel")
        self.assertEqual(template.name, "¿Cuál es el proceso - Pago contra entrega?")


class TestWaitForDbCommand(TestCase):
    """Tests para el comando wait_for_db"""
    
    def test_wait_for_db_success(self):
        """Test: Comando espera exitosamente"""
        out = StringIO()
        
        # Ejecutar comando
        call_command('wait_for_db', stdout=out)
        
        # Verificar salida
        output = out.getvalue()
        self.assertIn('⏳ Esperando a que la base de datos esté lista...', output)
        self.assertIn('✅ Base de datos lista!', output)
    
    def test_wait_for_db_with_timeout(self):
        """Test: Comando con timeout personalizado"""
        out = StringIO()
        
        # Ejecutar comando con timeout
        call_command('wait_for_db', timeout=30, stdout=out)
        
        # Verificar salida
        output = out.getvalue()
        self.assertIn('✅ Base de datos lista!', output) 