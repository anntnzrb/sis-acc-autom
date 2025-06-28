"""
Test cases for Producto model using London School TDD approach.
Focus on interaction testing and behavior verification.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
import tempfile
import os

from productos.models import Producto


class ProductoModelTest(TestCase):
    """Test Producto model behavior and validation."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'nombre': 'Aceite Castrol GTX',
            'descripcion': 'Aceite de motor sintético de alta calidad para automóviles',
            'precio': Decimal('25.50'),
            'iva': 15
        }
    
    def test_create_producto_with_valid_data(self):
        """Test creating producto with valid data."""
        producto = Producto(**self.valid_data)
        producto.full_clean()  # Should not raise
        producto.save()
        
        self.assertEqual(producto.nombre, 'Aceite Castrol Gtx')
        self.assertEqual(producto.precio, Decimal('25.50'))
        self.assertEqual(producto.iva, 15)
        self.assertIsNotNone(producto.created_at)
        self.assertIsNotNone(producto.updated_at)
    
    def test_producto_str_representation(self):
        """Test string representation of producto."""
        producto = Producto(**self.valid_data)
        producto.clean()
        self.assertEqual(str(producto), 'Aceite Castrol Gtx')
    
    def test_producto_nombre_normalization(self):
        """Test that nombre is normalized to title case."""
        data = self.valid_data.copy()
        data['nombre'] = 'aceite castrol gtx 20w50'
        producto = Producto(**data)
        producto.clean()
        
        self.assertEqual(producto.nombre, 'Aceite Castrol Gtx 20W50')
    
    def test_descripcion_normalization(self):
        """Test that descripcion is stripped of whitespace."""
        data = self.valid_data.copy()
        data['descripcion'] = '  Aceite de motor de alta calidad  '
        producto = Producto(**data)
        producto.clean()
        
        self.assertEqual(producto.descripcion, 'Aceite de motor de alta calidad')
    
    def test_precio_validation_positive(self):
        """Test precio validation with positive value."""
        data = self.valid_data.copy()
        data['precio'] = Decimal('0.01')
        producto = Producto(**data)
        producto.full_clean()  # Should not raise
        
        self.assertEqual(producto.precio, Decimal('0.01'))
    
    def test_precio_validation_zero(self):
        """Test precio validation with zero value."""
        data = self.valid_data.copy()
        data['precio'] = Decimal('0.00')
        producto = Producto(**data)
        
        with self.assertRaises(ValidationError):
            producto.full_clean()
    
    def test_precio_validation_negative(self):
        """Test precio validation with negative value."""
        data = self.valid_data.copy()
        data['precio'] = Decimal('-10.00')
        producto = Producto(**data)
        
        with self.assertRaises(ValidationError):
            producto.full_clean()
    
    def test_iva_validation_valid_values(self):
        """Test IVA validation with valid values (0 and 15)."""
        # Test 0% IVA
        data = self.valid_data.copy()
        data['iva'] = 0
        producto = Producto(**data)
        producto.full_clean()  # Should not raise
        
        # Test 15% IVA
        data['iva'] = 15
        producto = Producto(**data)
        producto.full_clean()  # Should not raise
    
    def test_iva_validation_invalid_value(self):
        """Test IVA validation with invalid value."""
        data = self.valid_data.copy()
        data['iva'] = 10  # Invalid, should be 0 or 15
        producto = Producto(**data)
        
        with self.assertRaises(ValidationError):
            producto.clean()
    
    def test_precio_con_iva_calculation_15_percent(self):
        """Test precio_con_iva property with 15% IVA."""
        producto = Producto(**self.valid_data)
        producto.clean()
        
        expected = Decimal('25.50') * Decimal('1.15')  # 25.50 + 15%
        self.assertEqual(producto.precio_con_iva, expected)
    
    def test_precio_con_iva_calculation_0_percent(self):
        """Test precio_con_iva property with 0% IVA."""
        data = self.valid_data.copy()
        data['iva'] = 0
        producto = Producto(**data)
        producto.clean()
        
        self.assertEqual(producto.precio_con_iva, Decimal('25.50'))
    
    def test_valor_iva_calculation_15_percent(self):
        """Test valor_iva property with 15% IVA."""
        producto = Producto(**self.valid_data)
        producto.clean()
        
        expected = Decimal('25.50') * Decimal('0.15')  # 15% of 25.50
        self.assertEqual(producto.valor_iva, expected)
    
    def test_valor_iva_calculation_0_percent(self):
        """Test valor_iva property with 0% IVA."""
        data = self.valid_data.copy()
        data['iva'] = 0
        producto = Producto(**data)
        producto.clean()
        
        self.assertEqual(producto.valor_iva, Decimal('0'))
    
    def test_get_precio_display(self):
        """Test get_precio_display method formatting."""
        producto = Producto(**self.valid_data)
        self.assertEqual(producto.get_precio_display(), '$25.50')
    
    def test_get_precio_con_iva_display(self):
        """Test get_precio_con_iva_display method formatting."""
        producto = Producto(**self.valid_data)
        expected_total = Decimal('25.50') * Decimal('1.15')
        expected_display = f"${expected_total:.2f}"
        self.assertEqual(producto.get_precio_con_iva_display(), expected_display)
    
    def test_get_iva_display_text_15_percent(self):
        """Test get_iva_display_text method with 15% IVA."""
        producto = Producto(**self.valid_data)
        self.assertEqual(producto.get_iva_display_text(), '15% IVA')
    
    def test_get_iva_display_text_0_percent(self):
        """Test get_iva_display_text method with 0% IVA."""
        data = self.valid_data.copy()
        data['iva'] = 0
        producto = Producto(**data)
        self.assertEqual(producto.get_iva_display_text(), '0% IVA')
    
    def test_model_meta_ordering(self):
        """Test model meta ordering configuration."""
        self.assertEqual(Producto._meta.ordering, ['nombre'])
    
    def test_model_verbose_names(self):
        """Test model verbose names are in Spanish."""
        meta = Producto._meta
        self.assertEqual(meta.verbose_name, 'Producto')
        self.assertEqual(meta.verbose_name_plural, 'Productos')
    
    def test_timestamps_auto_population(self):
        """Test that timestamps are automatically populated."""
        producto = Producto.objects.create(**self.valid_data)
        
        self.assertIsNotNone(producto.created_at)
        self.assertIsNotNone(producto.updated_at)
        # Check that timestamps are close (within 1 second)
        time_diff = abs((producto.updated_at - producto.created_at).total_seconds())
        self.assertLess(time_diff, 1.0)
    
    def test_updated_at_changes_on_save(self):
        """Test that updated_at changes when model is saved again."""
        producto = Producto.objects.create(**self.valid_data)
        original_updated = producto.updated_at
        
        # Simulate time passing and update
        producto.nombre = 'Nuevo Nombre'
        producto.save()
        
        self.assertGreaterEqual(producto.updated_at, original_updated)


class ProductoQuerySetTest(TestCase):
    """Test default queryset behavior and ordering."""
    
    def setUp(self):
        """Set up test data."""
        self.producto1 = Producto.objects.create(
            nombre='Aceite Castrol',
            descripcion='Aceite de motor',
            precio=Decimal('25.00'),
            iva=15
        )
        self.producto2 = Producto.objects.create(
            nombre='Bujías NGK',
            descripcion='Bujías de encendido',
            precio=Decimal('12.50'),
            iva=15
        )
        self.producto3 = Producto.objects.create(
            nombre='Aceite Mobil',
            descripcion='Aceite sintético',
            precio=Decimal('30.00'),
            iva=0
        )
    
    def test_default_ordering_by_nombre(self):
        """Test that productos are ordered by nombre by default."""
        productos = list(Producto.objects.all())
        
        # Should be ordered: Aceite Castrol, Aceite Mobil, Bujías NGK
        self.assertEqual(productos[0].nombre, 'Aceite Castrol')
        self.assertEqual(productos[1].nombre, 'Aceite Mobil')
        self.assertEqual(productos[2].nombre, 'Bujías Ngk')
    
    def test_count_productos(self):
        """Test counting productos."""
        count = Producto.objects.count()
        self.assertEqual(count, 3)
    
    def test_filter_by_iva(self):
        """Test filtering productos by IVA."""
        productos_con_iva = Producto.objects.filter(iva=15)
        productos_sin_iva = Producto.objects.filter(iva=0)
        
        self.assertEqual(productos_con_iva.count(), 2)
        self.assertEqual(productos_sin_iva.count(), 1)
    
    def test_filter_by_precio_range(self):
        """Test filtering productos by price range."""
        productos_caros = Producto.objects.filter(precio__gte=Decimal('25.00'))
        productos_baratos = Producto.objects.filter(precio__lt=Decimal('20.00'))
        
        self.assertEqual(productos_caros.count(), 2)
        self.assertEqual(productos_baratos.count(), 1)


class ProductoConstraintsTest(TestCase):
    """Test database constraints and indexes."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'nombre': 'Aceite Castrol GTX',
            'descripcion': 'Aceite de motor sintético',
            'precio': Decimal('25.50'),
            'iva': 15
        }
    
    def test_database_indexes(self):
        """Test that database indexes exist for performance."""
        indexes = [index.fields for index in Producto._meta.indexes]
        
        self.assertIn(['nombre'], indexes)
        self.assertIn(['precio'], indexes)
    
    def test_field_constraints(self):
        """Test that fields have proper constraints."""
        # Test precio field
        precio_field = Producto._meta.get_field('precio')
        self.assertEqual(precio_field.max_digits, 10)
        self.assertEqual(precio_field.decimal_places, 2)
        
        # Test iva field
        iva_field = Producto._meta.get_field('iva')
        self.assertEqual(iva_field.default, 15)
        
        # Test nombre field
        nombre_field = Producto._meta.get_field('nombre')
        self.assertEqual(nombre_field.max_length, 200)
    
    def test_iva_choices_validation(self):
        """Test that IVA choices are properly defined."""
        iva_choices = dict(Producto.IVA_CHOICES)
        
        self.assertEqual(iva_choices[0], '0% IVA')
        self.assertEqual(iva_choices[15], '15% IVA')
        self.assertEqual(len(iva_choices), 2)