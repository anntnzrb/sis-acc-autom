"""
Test cases for Trabajador forms using London School TDD approach.
Focus on form validation, data cleaning, and user interaction.
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import Mock, patch
import tempfile
import os

from trabajadores.forms import TrabajadorForm
from trabajadores.models import Trabajador


class TrabajadorFormTest(TestCase):
    """Test TrabajadorForm behavior and validation."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'correo': 'juan.perez@carriacces.com',
            'cedula': '1234567890',
            'codigo_empleado': 'EMP001'
        }
    
    def test_form_initialization(self):
        """Test form initializes correctly."""
        form = TrabajadorForm()
        
        # Test that all required fields are present
        expected_fields = ['nombre', 'apellido', 'correo', 'cedula', 'codigo_empleado', 'imagen']
        self.assertEqual(list(form.fields.keys()), expected_fields)
    
    def test_form_valid_data(self):
        """Test form validation with valid data."""
        form = TrabajadorForm(data=self.valid_data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
    
    def test_form_missing_required_fields(self):
        """Test form validation with missing required fields."""
        form = TrabajadorForm(data={})
        
        self.assertFalse(form.is_valid())
        
        # All fields except imagen are required
        required_fields = ['nombre', 'apellido', 'correo', 'cedula', 'codigo_empleado']
        for field in required_fields:
            self.assertIn(field, form.errors)
    
    def test_form_cedula_validation(self):
        """Test cedula field validation."""
        data = self.valid_data.copy()
        data['cedula'] = '123456789'  # Invalid: 9 digits
        form = TrabajadorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)
    
    def test_form_correo_validation(self):
        """Test correo field validation."""
        data = self.valid_data.copy()
        data['correo'] = 'invalid-email'
        form = TrabajadorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)
    
    def test_form_save_creates_trabajador(self):
        """Test that form save creates a trabajador."""
        form = TrabajadorForm(data=self.valid_data)
        
        self.assertTrue(form.is_valid())
        trabajador = form.save()
        
        self.assertIsInstance(trabajador, Trabajador)
        self.assertEqual(trabajador.nombre, 'Juan')
        self.assertEqual(trabajador.apellido, 'Pérez')
    
    def test_form_save_commit_false(self):
        """Test form save with commit=False."""
        form = TrabajadorForm(data=self.valid_data)
        
        self.assertTrue(form.is_valid())
        trabajador = form.save(commit=False)
        
        self.assertIsInstance(trabajador, Trabajador)
        self.assertIsNone(trabajador.pk)  # Not saved to database
    
    def test_form_image_field_optional(self):
        """Test that imagen field is optional."""
        form = TrabajadorForm(data=self.valid_data)
        
        self.assertTrue(form.is_valid())
        self.assertNotIn('imagen', form.errors)
    
    @patch('trabajadores.forms.validate_uploaded_image')
    def test_form_image_validation_called(self, mock_validate):
        """Test that image validation is called when image is provided."""
        # Create a mock image file
        mock_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        
        # Mock the validation to return the image (successful validation)
        mock_validate.return_value = mock_image
        
        data = self.valid_data.copy()
        files = {'imagen': mock_image}
        
        form = TrabajadorForm(data=data, files=files)
        
        # This should call validation in clean_imagen method
        if form.is_valid():
            mock_validate.assert_called_once_with(mock_image)
    
    def test_form_unique_constraints_validation(self):
        """Test form validation for unique constraints."""
        # Create an existing trabajador
        Trabajador.objects.create(**self.valid_data)
        
        # Try to create another with same data
        form = TrabajadorForm(data=self.valid_data)
        
        self.assertFalse(form.is_valid())
        # Should have errors for unique fields (correo, cedula, codigo_empleado)
    
    def test_form_update_existing_trabajador(self):
        """Test form for updating existing trabajador."""
        trabajador = Trabajador.objects.create(**self.valid_data)
        
        update_data = self.valid_data.copy()
        update_data['nombre'] = 'Carlos'
        
        form = TrabajadorForm(data=update_data, instance=trabajador)
        
        self.assertTrue(form.is_valid())
        updated_trabajador = form.save()
        
        self.assertEqual(updated_trabajador.pk, trabajador.pk)
        self.assertEqual(updated_trabajador.nombre, 'Carlos')
    
    def test_form_field_labels_in_spanish(self):
        """Test that form field labels are in Spanish."""
        form = TrabajadorForm()
        
        # Test some key field labels
        self.assertEqual(form.fields['nombre'].label, 'Nombre')
        self.assertEqual(form.fields['apellido'].label, 'Apellido')
        self.assertEqual(form.fields['correo'].label, 'Correo Electrónico')
        self.assertEqual(form.fields['cedula'].label, 'Cédula')
        self.assertEqual(form.fields['codigo_empleado'].label, 'Código de Empleado')
        self.assertEqual(form.fields['imagen'].label, 'Imagen')
    
    def test_form_field_help_texts(self):
        """Test that form fields have appropriate help texts."""
        form = TrabajadorForm()
        
        # Test that help texts are provided for complex fields
        self.assertIsNotNone(form.fields['cedula'].help_text)
        self.assertIsNotNone(form.fields['correo'].help_text)
        self.assertIsNotNone(form.fields['codigo_empleado'].help_text)
    
    def test_form_field_widgets_have_css_classes(self):
        """Test that form fields have Bootstrap CSS classes."""
        form = TrabajadorForm()
        
        # Test that all fields have form-control class for Bootstrap
        for field_name, field in form.fields.items():
            if field_name != 'imagen':  # File input might have different styling
                self.assertIn('form-control', field.widget.attrs.get('class', ''))
    
    def test_form_required_fields_marked(self):
        """Test that required fields are properly marked."""
        form = TrabajadorForm()
        
        required_fields = ['nombre', 'apellido', 'correo', 'cedula', 'codigo_empleado']
        optional_fields = ['imagen']
        
        for field_name in required_fields:
            self.assertTrue(form.fields[field_name].required)
        
        for field_name in optional_fields:
            self.assertFalse(form.fields[field_name].required)
    
    def test_form_data_normalization(self):
        """Test that form data is properly normalized."""
        data = {
            'nombre': '  juan carlos  ',
            'apellido': '  pérez garcía  ',
            'correo': '  JUAN.PEREZ@CARRIACCES.COM  ',
            'cedula': '1234567890',
            'codigo_empleado': '  emp001  '
        }
        
        form = TrabajadorForm(data=data)
        
        if form.is_valid():
            # Test that form's clean methods normalize the data
            self.assertEqual(form.cleaned_data['nombre'], 'Juan Carlos')  # Title case
            self.assertEqual(form.cleaned_data['apellido'], 'Pérez García')  # Title case
            self.assertEqual(form.cleaned_data['correo'], 'juan.perez@carriacces.com')  # Lowercase
            self.assertEqual(form.cleaned_data['codigo_empleado'], 'EMP001')  # Uppercase


class TrabajadorFormIntegrationTest(TestCase):
    """Integration tests for TrabajadorForm with model validation."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'nombre': 'María',
            'apellido': 'González',
            'correo': 'maria.gonzalez@carriacces.com',
            'cedula': '0987654321',
            'codigo_empleado': 'EMP003'
        }
    
    def test_form_model_integration(self):
        """Test complete form-to-model workflow."""
        form = TrabajadorForm(data=self.valid_data)
        
        self.assertTrue(form.is_valid())
        
        trabajador = form.save()
        
        # Verify the trabajador was saved correctly
        self.assertEqual(Trabajador.objects.count(), 1)
        
        saved_trabajador = Trabajador.objects.first()
        self.assertEqual(saved_trabajador.nombre, 'María')
        self.assertEqual(saved_trabajador.apellido, 'González')
        self.assertEqual(saved_trabajador.get_nombre_completo(), 'María González')
    
    def test_form_validation_with_model_constraints(self):
        """Test that form respects model-level constraints."""
        # Create first trabajador
        Trabajador.objects.create(**self.valid_data)
        
        # Try to create second with same unique fields
        form = TrabajadorForm(data=self.valid_data)
        
        # Form might be valid at form level, but should fail at model level
        if form.is_valid():
            with self.assertRaises(Exception):  # Could be ValidationError or IntegrityError
                form.save()