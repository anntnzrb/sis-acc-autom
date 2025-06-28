"""
Management command to populate products with mock data.
"""
import os
import urllib.request
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from productos.models import Producto


class Command(BaseCommand):
    help = "Populate products with mock data including images"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing products before adding new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing products...'))
            Producto.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing products cleared.'))

        # Check if products already exist
        if Producto.objects.exists() and not options['clear']:
            self.stdout.write(
                self.style.WARNING(
                    'Products already exist. Use --clear to remove them first.'
                )
            )
            return

        # Mock product data for automotive accessories (CarriAcces)
        productos_data = [
            {
                'nombre': 'Llantas Deportivas Aleación',
                'descripcion': 'Llantas deportivas de aleación de 17 pulgadas, diseño moderno con acabado negro mate. Perfectas para mejorar el rendimiento y la estética de tu vehículo. Compatible con la mayoría de automóviles compactos y sedanes.',
                'precio': Decimal('450.00'),
                'iva': 15,
                'imagen_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&q=80',
                'imagen_name': 'llantas_deportivas.jpg'
            },
            {
                'nombre': 'Sistema Audio Premium',
                'descripcion': 'Sistema de audio premium con tecnología Bluetooth 5.0, sonido surround y ecualizador digital. Incluye amplificador de 4 canales y subwoofer integrado. Fácil instalación con kit completo incluido.',
                'precio': Decimal('320.75'),
                'iva': 15,
                'imagen_local': 'sistema_audio.png',
                'imagen_name': 'sistema_audio.png'
            },
            {
                'nombre': 'Kit Iluminación LED Interior',
                'descripcion': 'Kit completo de iluminación LED para interior del vehículo. Incluye tiras LED RGB multicolor con control remoto, instalación plug-and-play. Crea ambiente personalizado con 16 millones de colores disponibles.',
                'precio': Decimal('89.99'),
                'iva': 0,
                'imagen_url': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=500&q=80',
                'imagen_name': 'led_interior.jpg'
            }
        ]

        # Create media directory if it doesn't exist
        media_productos_dir = os.path.join(settings.MEDIA_ROOT, 'productos')
        os.makedirs(media_productos_dir, exist_ok=True)

        self.stdout.write(self.style.SUCCESS('Creating mock products...'))

        for producto_data in productos_data:
            # Handle image (download or copy local)
            imagen_path = None
            try:
                imagen_name = producto_data.pop('imagen_name')
                imagen_local_path = os.path.join(media_productos_dir, imagen_name)
                
                if 'imagen_local' in producto_data:
                    # Copy from project root
                    imagen_local = producto_data.pop('imagen_local')
                    source_path = os.path.join(settings.BASE_DIR, imagen_local)
                    self.stdout.write(f'Copying local image: {imagen_name}...')
                    
                    import shutil
                    shutil.copy2(source_path, imagen_local_path)
                    imagen_path = f'productos/{imagen_name}'
                    
                elif 'imagen_url' in producto_data:
                    # Download from URL
                    imagen_url = producto_data.pop('imagen_url')
                    self.stdout.write(f'Downloading image: {imagen_name}...')
                    urllib.request.urlretrieve(imagen_url, imagen_local_path)
                    imagen_path = f'productos/{imagen_name}'
                
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Could not process image: {e}')
                )

            # Create product
            producto = Producto.objects.create(
                nombre=producto_data['nombre'],
                descripcion=producto_data['descripcion'],
                precio=producto_data['precio'],
                iva=producto_data['iva'],
                imagen=imagen_path
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Created product: {producto.nombre} - ${producto.precio}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(productos_data)} products!'
            )
        )