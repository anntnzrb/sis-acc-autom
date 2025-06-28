"""
Management command to populate proveedores with mock data from South America.
"""
from django.core.management.base import BaseCommand
from proveedores.models import Proveedor


class Command(BaseCommand):
    help = "Populate proveedores with mock data from South American countries"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing proveedores before adding new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing proveedores...'))
            Proveedor.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing proveedores cleared.'))

        # Check if proveedores already exist
        if Proveedor.objects.exists() and not options['clear']:
            self.stdout.write(
                self.style.WARNING(
                    'Proveedores already exist. Use --clear to remove them first.'
                )
            )
            return

        # Mock supplier data from different South American countries
        proveedores_data = [
            {
                'nombre': 'AutoPartes Colombia S.A.S.',
                'descripcion': 'Empresa líder en la distribución de autopartes y accesorios automotrices en Colombia. Especializada en sistemas de audio, llantas deportivas y componentes electrónicos para vehículos. Más de 15 años de experiencia en el mercado latinoamericano.',
                'telefono': '+57 1 4567890',
                'pais': 'Colombia',
                'correo': 'ventas@autopartescolombia.com',
                'direccion': 'Carrera 15 #85-32, Zona Industrial, Bogotá D.C.'
            },
            {
                'nombre': 'TecnoAuto Argentina',
                'descripcion': 'Proveedor especializado en tecnología automotriz y sistemas de iluminación LED para vehículos. Distribuidor oficial de marcas reconocidas internacionalmente. Ofrecemos productos de alta calidad con garantía extendida y soporte técnico especializado.',
                'telefono': '+54 11 9876543',
                'pais': 'Argentina',
                'correo': 'contacto@tecnoautoarg.com.ar',
                'direccion': 'Av. Córdoba 1234, Villa Crespo, Buenos Aires (C1414)'
            },
            {
                'nombre': 'AutoSupply Brasil Ltda.',
                'descripcion': 'Importadora y distribuidora de accesorios automotrices premium. Especialistas en sistemas de audio de alta fidelidad, llantas deportivas y accesorios de tuning. Atendemos todo el territorio brasileño con envíos express.',
                'telefono': '+55 11 3456789',
                'pais': 'Brasil',
                'correo': 'comercial@autosupplybr.com.br',
                'direccion': 'Rua das Indústrias, 567 - Vila Leopoldina, São Paulo - SP, 05307-020'
            },
            {
                'nombre': 'Motortech Chile Spa',
                'descripcion': 'Empresa chilena especializada en tecnología automotriz avanzada y componentes de alta performance. Distribuidor exclusivo de sistemas de suspensión deportiva y productos de tuning para el mercado sudamericano.',
                'telefono': '+56 2 9876543',
                'pais': 'Chile',
                'correo': 'ventas@motortechchile.cl',
                'direccion': 'Av. Providencia 2250, Providencia, Santiago - Región Metropolitana'
            },
            {
                'nombre': 'Auto Repuestos Peru SAC',
                'descripcion': 'Líder en distribución de repuestos y accesorios automotrices en Perú. Especializado en partes eléctricas, sistemas de encendido y componentes de motor. Red de distribución nacional con más de 20 años de experiencia.',
                'telefono': '+51 1 7654321',
                'pais': 'Perú',
                'correo': 'info@autorepuestosperu.pe',
                'direccion': 'Jr. Puno 1456, La Victoria, Lima 13 - Lima'
            },
            {
                'nombre': 'VehiParts Ecuador Cía. Ltda.',
                'descripcion': 'Importadora ecuatoriana de autopartes originales y aftermarket. Especializada en sistemas de frenos, transmisión y dirección. Proveedor confiable para talleres y distribuidores en Ecuador y países vecinos.',
                'telefono': '+593 2 3456789',
                'pais': 'Ecuador',
                'correo': 'comercial@vehipartsec.com',
                'direccion': 'Av. 6 de Diciembre N24-253 y Bello Horizonte, Quito - Pichincha'
            }
        ]

        self.stdout.write(self.style.SUCCESS('Creating mock proveedores...'))

        for proveedor_data in proveedores_data:
            # Create proveedor
            proveedor = Proveedor.objects.create(
                nombre=proveedor_data['nombre'],
                descripcion=proveedor_data['descripcion'],
                telefono=proveedor_data['telefono'],
                pais=proveedor_data['pais'],
                correo=proveedor_data['correo'],
                direccion=proveedor_data['direccion']
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Created proveedor: {proveedor.nombre} - {proveedor.pais}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(proveedores_data)} proveedores!'
            )
        )