from django.core.management.base import BaseCommand
from django.db import transaction
from app.landing.models import LandingTemplate, ProductLanding
from app.landing.seeds.default_data import DEFAULT_LANDING_TEMPLATES, DEFAULT_PRODUCT_LANDINGS


class Command(BaseCommand):
    help = 'Carga datos por defecto para las plantillas de landing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Fuerza la recreación de datos existentes',
        )
        parser.add_argument(
            '--template-only',
            action='store_true',
            help='Solo carga plantillas sin productos',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Iniciando carga de datos por defecto...')
        )

        try:
            with transaction.atomic():
                self._load_templates(options['force'])
                
                if not options['template_only']:
                    self._load_product_landings(options['force'])
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Datos cargados exitosamente!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error al cargar datos: {str(e)}')
            )
            raise

    def _load_templates(self, force=False):
        """Carga las plantillas por defecto"""
        self.stdout.write('📋 Cargando plantillas...')
        
        for template_data in DEFAULT_LANDING_TEMPLATES:
            template, created = LandingTemplate.objects.get_or_create(
                base_url=template_data['base_url'],
                defaults=template_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Plantilla creada: {template.name}')
                )
            elif force:
                # Actualizar plantilla existente
                for key, value in template_data.items():
                    setattr(template, key, value)
                template.save()
                self.stdout.write(
                    self.style.WARNING(f'🔄 Plantilla actualizada: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⏭️ Plantilla ya existe: {template.name}')
                )

    def _load_product_landings(self, force=False):
        """Carga las relaciones producto-plantilla por defecto"""
        self.stdout.write('🔗 Cargando relaciones producto-plantilla...')
        
        for landing_data in DEFAULT_PRODUCT_LANDINGS:
            try:
                template = LandingTemplate.objects.get(
                    base_url=landing_data['template_base_url']
                )
                
                product_landing, created = ProductLanding.objects.get_or_create(
                    product_id=landing_data['product_id'],
                    template=template,
                    defaults={
                        'is_primary': landing_data.get('is_primary', False),
                        'is_active': landing_data.get('is_active', True),
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Relación creada: Producto {landing_data["product_id"]} -> {template.name}'
                        )
                    )
                elif force:
                    # Actualizar relación existente
                    product_landing.is_primary = landing_data.get('is_primary', False)
                    product_landing.is_active = landing_data.get('is_active', True)
                    product_landing.save()
                    self.stdout.write(
                        self.style.WARNING(
                            f'🔄 Relación actualizada: Producto {landing_data["product_id"]} -> {template.name}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⏭️ Relación ya existe: Producto {landing_data["product_id"]} -> {template.name}'
                        )
                    )
                    
            except LandingTemplate.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Plantilla no encontrada: {landing_data["template_base_url"]}'
                    )
                ) 