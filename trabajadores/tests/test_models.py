"""
Test cases for Trabajador model using London School TDD approach.
Focus on interaction testing and behavior verification.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import Mock, patch
from decimal import Decimal
import tempfile
import os

from trabajadores.models import Trabajador


class TrabajadorModelTest(TestCase):
    """Test Trabajador model behavior and validation."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'correo': 'juan.perez@carriacces.com',
            'cedula': '1234567890',
            'codigo_empleado': 'EMP001'
        }
    
    def test_create_trabajador_with_valid_data(self):
        """Test creating a trabajador with valid data."""
        trabajador = Trabajador(**self.valid_data)
        trabajador.full_clean()  # Should not raise
        trabajador.save()
        
        self.assertEqual(trabajador.nombre, 'Juan')
        self.assertEqual(trabajador.apellido, 'Pérez')
        self.assertEqual(trabajador.get_nombre_completo(), 'Juan Pérez')
    
    def test_trabajador_str_representation(self):
        """Test string representation of trabajador."""
        trabajador = Trabajador(**self.valid_data)
        self.assertEqual(str(trabajador), 'Juan Pérez')
    
    def test_trabajador_nombre_normalization(self):
        """Test that nombre is normalized to title case."""
        data = self.valid_data.copy()
        data['nombre'] = 'juan carlos'
        trabajador = Trabajador(**data)
        trabajador.clean()
        
        self.assertEqual(trabajador.nombre, 'Juan Carlos')
    
    def test_trabajador_apellido_normalization(self):
        """Test that apellido is normalized to title case."""
        data = self.valid_data.copy()
        data['apellido'] = 'pérez garcía'
        trabajador = Trabajador(**data)
        trabajador.clean()
        
        self.assertEqual(trabajador.apellido, 'Pérez García')
    
    def test_correo_normalization(self):
        """Test that correo is normalized to lowercase."""
        data = self.valid_data.copy()
        data['correo'] = 'JUAN.PEREZ@CARRIACCES.COM'
        trabajador = Trabajador(**data)
        trabajador.clean()
        
        self.assertEqual(trabajador.correo, 'juan.perez@carriacces.com')
    
    def test_codigo_empleado_normalization(self):
        """Test that codigo_empleado is normalized to uppercase."""
        data = self.valid_data.copy()
        data['codigo_empleado'] = 'emp001'
        trabajador = Trabajador(**data)
        trabajador.clean()
        
        self.assertEqual(trabajador.codigo_empleado, 'EMP001')
    
    def test_cedula_validation_invalid_format(self):
        """Test cedula validation with invalid format."""
        data = self.valid_data.copy()
        data['cedula'] = '123456789'  # 9 digits instead of 10
        trabajador = Trabajador(**data)
        
        with self.assertRaises(ValidationError):
            trabajador.full_clean()
    
    def test_cedula_validation_non_numeric(self):
        """Test cedula validation with non-numeric characters."""
        data = self.valid_data.copy()
        data['cedula'] = '123456789a'
        trabajador = Trabajador(**data)
        
        with self.assertRaises(ValidationError):
            trabajador.full_clean()
    
    def test_correo_validation_invalid_format(self):
        """Test correo validation with invalid format."""
        data = self.valid_data.copy()
        data['correo'] = 'invalid-email'
        trabajador = Trabajador(**data)
        
        with self.assertRaises(ValidationError):
            trabajador.full_clean()
    
    def test_unique_correo_constraint(self):
        """Test unique constraint on correo field."""
        # Create first trabajador
        Trabajador.objects.create(**self.valid_data)
        
        # Try to create second with same correo
        data = self.valid_data.copy()
        data['cedula'] = '0987654321'
        data['codigo_empleado'] = 'EMP002'
        trabajador2 = Trabajador(**data)
        
        with self.assertRaises(ValidationError):
            trabajador2.full_clean()
    
    def test_unique_cedula_constraint(self):
        """Test unique constraint on cedula field."""
        # Create first trabajador
        Trabajador.objects.create(**self.valid_data)
        
        # Try to create second with same cedula
        data = self.valid_data.copy()
        data['correo'] = 'otro@carriacces.com'
        data['codigo_empleado'] = 'EMP002'
        trabajador2 = Trabajador(**data)
        
        with self.assertRaises(ValidationError):
            trabajador2.full_clean()
    
    def test_unique_codigo_empleado_constraint(self):
        """Test unique constraint on codigo_empleado field."""
        # Create first trabajador
        Trabajador.objects.create(**self.valid_data)
        
        # Try to create second with same codigo_empleado
        data = self.valid_data.copy()
        data['correo'] = 'otro@carriacces.com'
        data['cedula'] = '0987654321'
        trabajador2 = Trabajador(**data)
        
        with self.assertRaises(ValidationError):
            trabajador2.full_clean()
    
    @patch('trabajadores.models.validate_uploaded_image')
    def test_imagen_validation_called(self, mock_validate):
        """Test that image validation is called when imagen is provided."""
        # Create a simple uploaded file for testing
        image_file = SimpleUploadedFile(
            name='test.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        
        # Mock the validation to return the file (successful validation)
        mock_validate.return_value = image_file
        
        trabajador = Trabajador(**self.valid_data)
        trabajador.imagen = image_file
        
        # Call clean method to trigger validation
        trabajador.clean()
        mock_validate.assert_called_once_with(image_file)
    
    def test_get_nombre_completo_method(self):
        """Test get_nombre_completo method returns formatted name."""
        trabajador = Trabajador(**self.valid_data)
        self.assertEqual(trabajador.get_nombre_completo(), 'Juan Pérez')
    
    def test_model_meta_ordering(self):
        """Test model meta ordering configuration."""
        self.assertEqual(Trabajador._meta.ordering, ['apellido', 'nombre'])
    
    def test_model_verbose_names(self):
        """Test model verbose names are in Spanish."""
        meta = Trabajador._meta
        self.assertEqual(meta.verbose_name, 'Trabajador')
        self.assertEqual(meta.verbose_name_plural, 'Trabajadores')
    
    def test_timestamps_auto_population(self):
        """Test that timestamps are automatically populated."""
        trabajador = Trabajador.objects.create(**self.valid_data)
        
        self.assertIsNotNone(trabajador.created_at)
        self.assertIsNotNone(trabajador.updated_at)
        # Check that timestamps are close (within 1 second)
        time_diff = abs((trabajador.updated_at - trabajador.created_at).total_seconds())
        self.assertLess(time_diff, 1.0)
    
    def test_updated_at_changes_on_save(self):
        """Test that updated_at changes when model is saved again."""
        trabajador = Trabajador.objects.create(**self.valid_data)
        original_updated = trabajador.updated_at
        
        # Simulate time passing and update
        trabajador.nombre = 'Carlos'
        trabajador.save()
        
        self.assertGreaterEqual(trabajador.updated_at, original_updated)


class TrabajadorQuerySetTest(TestCase):
    """Test custom queryset methods if implemented."""
    
    def setUp(self):
        """Set up test data."""
        self.trabajador1 = Trabajador.objects.create(
            nombre='Ana',
            apellido='García',
            correo='ana.garcia@carriacces.com',
            cedula='1111111111',
            codigo_empleado='EMP001'
        )
        self.trabajador2 = Trabajador.objects.create(
            nombre='Carlos',
            apellido='López',
            correo='carlos.lopez@carriacces.com',
            cedula='2222222222',
            codigo_empleado='EMP002'
        )
    
    def test_default_ordering(self):
        """Test that trabajadores are ordered by apellido, nombre by default."""
        trabajadores = list(Trabajador.objects.all())
        
        # García comes before López alphabetically
        self.assertEqual(trabajadores[0].apellido, 'García')
        self.assertEqual(trabajadores[1].apellido, 'López')
    
    def test_count_trabajadores(self):
        """Test counting trabajadores."""
        count = Trabajador.objects.count()
        self.assertEqual(count, 2)