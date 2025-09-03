from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    help = 'Espera hasta que la base de datos esté lista'

    def add_arguments(self, parser):
        parser.add_argument(
            '--timeout',
            type=int,
            default=60,
            help='Timeout en segundos (default: 60)',
        )

    def handle(self, *args, **options):
        self.stdout.write('⏳ Esperando a que la base de datos esté lista...')
        
        timeout = options['timeout']
        start_time = time.time()
        
        while True:
            try:
                # Intentar conectar a la base de datos
                db_conn = connections['default']
                db_conn.cursor()
                self.stdout.write(
                    self.style.SUCCESS('✅ Base de datos lista!')
                )
                break
                
            except OperationalError:
                elapsed_time = time.time() - start_time
                
                if elapsed_time > timeout:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Timeout: La base de datos no está lista después de {timeout} segundos'
                        )
                    )
                    raise
                
                self.stdout.write(
                    self.style.WARNING(
                        f'⏳ Base de datos no lista... ({elapsed_time:.1f}s/{timeout}s)'
                    )
                )
                time.sleep(1) 