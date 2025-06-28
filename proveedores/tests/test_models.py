"""
Test cases for Proveedor model using London School TDD approach.
Focus on interaction testing and behavior verification.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from proveedores.models import Proveedor


class ProveedorModelTest(TestCase):
    """Test Proveedor model behavior and validation."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'nombre': 'Importadora AutoParts S.A.',
            'descripcion': 'Importadora especializada en repuestos y accesorios automotrices de alta calidad',
            'telefono': '+593-2-2234567',
            'pais': 'Ecuador',
            'correo': 'ventas@autoparts.com.ec',
            'direccion': 'Av. Amazonas 123, Quito, Ecuador'
        }
    
    def test_create_proveedor_with_valid_data(self):
        """Test creating proveedor with valid data."""
        proveedor = Proveedor(**self.valid_data)
        proveedor.full_clean()  # Should not raise
        proveedor.save()
        
        self.assertEqual(proveedor.nombre, 'Importadora Autoparts S.A.')
        self.assertEqual(proveedor.correo, 'ventas@autoparts.com.ec')
        self.assertEqual(proveedor.pais, 'Ecuador')
        self.assertIsNotNone(proveedor.created_at)
        self.assertIsNotNone(proveedor.updated_at)
    
    def test_proveedor_str_representation(self):
        """Test string representation of proveedor."""
        proveedor = Proveedor(**self.valid_data)
        proveedor.clean()
        self.assertEqual(str(proveedor), 'Importadora Autoparts S.A.')
    
    def test_proveedor_nombre_normalization(self):
        """Test that nombre is normalized to title case."""
        data = self.valid_data.copy()
        data['nombre'] = 'importadora autoparts sociedad anónima'
        proveedor = Proveedor(**data)
        proveedor.clean()
        
        self.assertEqual(proveedor.nombre, 'Importadora Autoparts Sociedad Anónima')
    
    def test_descripcion_normalization(self):
        """Test that descripcion is stripped of whitespace."""
        data = self.valid_data.copy()
        data['descripcion'] = '  Importadora de repuestos automotrices  '
        proveedor = Proveedor(**data)
        proveedor.clean()
        
        self.assertEqual(proveedor.descripcion, 'Importadora de repuestos automotrices')
    
    def test_pais_normalization(self):
        """Test that pais is normalized to title case."""
        data = self.valid_data.copy()
        data['pais'] = 'estados unidos'
        proveedor = Proveedor(**data)
        proveedor.clean()
        
        self.assertEqual(proveedor.pais, 'Estados Unidos')
    
    def test_correo_normalization(self):
        """Test that correo is normalized to lowercase."""
        data = self.valid_data.copy()
        data['correo'] = 'VENTAS@AUTOPARTS.COM.EC'
        proveedor = Proveedor(**data)
        proveedor.clean()
        
        self.assertEqual(proveedor.correo, 'ventas@autoparts.com.ec')
    
    def test_direccion_normalization(self):
        """Test that direccion is stripped of whitespace."""
        data = self.valid_data.copy()
        data['direccion'] = '  Av. Amazonas 123, Quito  '
        proveedor = Proveedor(**data)
        proveedor.clean()
        
        self.assertEqual(proveedor.direccion, 'Av. Amazonas 123, Quito')
    
    def test_telefono_normalization(self):
        """Test that telefono is stripped of whitespace."""
        data = self.valid_data.copy()
        data['telefono'] = '  +593-2-2234567  '
        proveedor = Proveedor(**data)
        proveedor.clean()
        
        self.assertEqual(proveedor.telefono, '+593-2-2234567')
    
    def test_telefono_validation_valid_formats(self):
        """Test telefono validation with valid formats."""
        valid_phones = [
            '+593-2-2234567',
            '02-2234567',
            '(02) 223-4567',
            '+1-555-123-4567',
            '555 123 4567'
        ]
        
        for phone in valid_phones:
            data = self.valid_data.copy()
            data['telefono'] = phone
            proveedor = Proveedor(**data)
            proveedor.full_clean()  # Should not raise
    
    def test_telefono_validation_invalid_format(self):
        """Test telefono validation with invalid format."""
        data = self.valid_data.copy()
        data['telefono'] = '123'  # Too short
        proveedor = Proveedor(**data)
        
        with self.assertRaises(ValidationError):
            proveedor.full_clean()
    
    def test_correo_validation_invalid_format(self):
        """Test correo validation with invalid format."""
        data = self.valid_data.copy()
        data['correo'] = 'invalid-email'
        proveedor = Proveedor(**data)
        
        with self.assertRaises(ValidationError):
            proveedor.full_clean()
    
    def test_get_contact_info_method(self):
        """Test get_contact_info method returns formatted contact information."""
        proveedor = Proveedor(**self.valid_data)
        contact_info = proveedor.get_contact_info()
        
        self.assertIn('ventas@autoparts.com.ec', contact_info)
        self.assertIn('+593-2-2234567', contact_info)
        self.assertIn('Email:', contact_info)
        self.assertIn('Tel:', contact_info)
    
    def test_get_contact_info_method_partial_data(self):
        """Test get_contact_info method with partial contact data."""
        data = self.valid_data.copy()
        del data['telefono']
        proveedor = Proveedor(**data)
        contact_info = proveedor.get_contact_info()
        
        self.assertIn('ventas@autoparts.com.ec', contact_info)
        self.assertNotIn('Tel:', contact_info)
    
    def test_get_location_info_method(self):
        """Test get_location_info method returns formatted location information."""
        proveedor = Proveedor(**self.valid_data)
        location_info = proveedor.get_location_info()
        
        self.assertIn('Ecuador', location_info)
        self.assertIn('Av. Amazonas 123, Quito, Ecuador', location_info)
    
    def test_get_location_info_method_partial_data(self):
        """Test get_location_info method with partial location data."""
        data = self.valid_data.copy()
        del data['direccion']
        proveedor = Proveedor(**data)
        location_info = proveedor.get_location_info()
        
        self.assertEqual(location_info, 'Ecuador')
    
    def test_model_meta_ordering(self):
        """Test model meta ordering configuration."""
        self.assertEqual(Proveedor._meta.ordering, ['nombre'])
    
    def test_model_verbose_names(self):
        """Test model verbose names are in Spanish."""
        meta = Proveedor._meta
        self.assertEqual(meta.verbose_name, 'Proveedor')
        self.assertEqual(meta.verbose_name_plural, 'Proveedores')
    
    def test_timestamps_auto_population(self):
        """Test that timestamps are automatically populated."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        
        self.assertIsNotNone(proveedor.created_at)
        self.assertIsNotNone(proveedor.updated_at)
        # Check that timestamps are close (within 1 second)
        time_diff = abs((proveedor.updated_at - proveedor.created_at).total_seconds())
        self.assertLess(time_diff, 1.0)
    
    def test_updated_at_changes_on_save(self):
        """Test that updated_at changes when model is saved again."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        original_updated = proveedor.updated_at
        
        # Simulate time passing and update
        proveedor.nombre = 'Nuevo Nombre'
        proveedor.save()
        
        self.assertGreaterEqual(proveedor.updated_at, original_updated)


class ProveedorQuerySetTest(TestCase):
    """Test default queryset behavior and ordering."""
    
    def setUp(self):
        """Set up test data."""
        self.proveedor1 = Proveedor.objects.create(
            nombre='Alpha Proveedores',
            descripcion='Proveedor de repuestos',
            telefono='02-1234567',
            pais='Ecuador',
            correo='alpha@provider.com',
            direccion='Calle Alpha 123'
        )
        self.proveedor2 = Proveedor.objects.create(
            nombre='Beta Importadores',
            descripcion='Importador de accesorios',
            telefono='02-7654321',
            pais='Colombia',
            correo='beta@importer.com',
            direccion='Calle Beta 456'
        )
        self.proveedor3 = Proveedor.objects.create(
            nombre='Gamma Distribuidores',
            descripcion='Distribuidor especializado',
            telefono='02-9876543',
            pais='Perú',
            correo='gamma@distributor.com',
            direccion='Calle Gamma 789'
        )
    
    def test_default_ordering_by_nombre(self):
        """Test that proveedores are ordered by nombre by default."""
        proveedores = list(Proveedor.objects.all())
        
        # Should be ordered: Alpha, Beta, Gamma
        self.assertEqual(proveedores[0].nombre, 'Alpha Proveedores')
        self.assertEqual(proveedores[1].nombre, 'Beta Importadores')
        self.assertEqual(proveedores[2].nombre, 'Gamma Distribuidores')
    
    def test_count_proveedores(self):
        """Test counting proveedores."""
        count = Proveedor.objects.count()
        self.assertEqual(count, 3)
    
    def test_filter_by_pais(self):
        """Test filtering proveedores by país."""
        proveedores_ecuador = Proveedor.objects.filter(pais='Ecuador')
        proveedores_colombia = Proveedor.objects.filter(pais='Colombia')
        
        self.assertEqual(proveedores_ecuador.count(), 1)
        self.assertEqual(proveedores_colombia.count(), 1)
    
    def test_search_by_nombre(self):
        """Test searching proveedores by nombre."""
        proveedores_alpha = Proveedor.objects.filter(nombre__icontains='Alpha')
        proveedores_import = Proveedor.objects.filter(nombre__icontains='Import')
        
        self.assertEqual(proveedores_alpha.count(), 1)
        self.assertEqual(proveedores_import.count(), 1)


class ProveedorConstraintsTest(TestCase):
    """Test database constraints and indexes."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'nombre': 'Importadora AutoParts S.A.',
            'descripcion': 'Importadora especializada en repuestos',
            'telefono': '+593-2-2234567',
            'pais': 'Ecuador',
            'correo': 'ventas@autoparts.com.ec',
            'direccion': 'Av. Amazonas 123, Quito, Ecuador'
        }
    
    def test_database_indexes(self):
        """Test that database indexes exist for performance."""
        indexes = [index.fields for index in Proveedor._meta.indexes]
        
        self.assertIn(['nombre'], indexes)
        self.assertIn(['pais'], indexes)
    
    def test_field_constraints(self):
        """Test that fields have proper constraints."""
        # Test nombre field
        nombre_field = Proveedor._meta.get_field('nombre')
        self.assertEqual(nombre_field.max_length, 200)
        
        # Test telefono field
        telefono_field = Proveedor._meta.get_field('telefono')
        self.assertEqual(telefono_field.max_length, 15)
        
        # Test pais field
        pais_field = Proveedor._meta.get_field('pais')
        self.assertEqual(pais_field.max_length, 100)
        
        # Test correo field validators
        correo_field = Proveedor._meta.get_field('correo')
        self.assertTrue(any(
            hasattr(validator, 'code') and validator.code == 'invalid'
            for validator in correo_field.validators
        ))
    
    def test_telefono_field_validators(self):
        """Test that telefono field has regex validators."""
        telefono_field = Proveedor._meta.get_field('telefono')
        
        # Check that regex validator exists
        regex_validators = [
            v for v in telefono_field.validators 
            if hasattr(v, 'regex')
        ]
        self.assertTrue(len(regex_validators) > 0)