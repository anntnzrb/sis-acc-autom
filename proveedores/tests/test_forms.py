"""
Test cases for Proveedor forms using London School TDD approach.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError

from proveedores.forms import ProveedorForm
from proveedores.models import Proveedor


class ProveedorFormTest(TestCase):
    """Test ProveedorForm validation and behavior."""
    
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
    
    def test_form_valid_with_complete_data(self):
        """Test form is valid with all required data."""
        form = ProveedorForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_without_nombre(self):
        """Test form is invalid without nombre."""
        data = self.valid_data.copy()
        del data['nombre']
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
    
    def test_form_invalid_without_descripcion(self):
        """Test form is invalid without descripcion."""
        data = self.valid_data.copy()
        del data['descripcion']
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('descripcion', form.errors)
    
    def test_form_invalid_without_telefono(self):
        """Test form is invalid without telefono."""
        data = self.valid_data.copy()
        del data['telefono']
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)
    
    def test_form_invalid_without_pais(self):
        """Test form is invalid without pais."""
        data = self.valid_data.copy()
        del data['pais']
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('pais', form.errors)
    
    def test_form_invalid_without_correo(self):
        """Test form is invalid without correo."""
        data = self.valid_data.copy()
        del data['correo']
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)
    
    def test_form_invalid_without_direccion(self):
        """Test form is invalid without direccion."""
        data = self.valid_data.copy()
        del data['direccion']
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('direccion', form.errors)
    
    def test_nombre_validation_too_short(self):
        """Test nombre validation with too short name."""
        data = self.valid_data.copy()
        data['nombre'] = 'AB'  # Too short
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
    
    def test_nombre_validation_too_long(self):
        """Test nombre validation with too long name."""
        data = self.valid_data.copy()
        data['nombre'] = 'A' * 201  # Too long
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
    
    def test_nombre_normalization(self):
        """Test that nombre is normalized to title case."""
        data = self.valid_data.copy()
        data['nombre'] = 'importadora autoparts sociedad anónima'
        form = ProveedorForm(data=data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['nombre'], 'Importadora Autoparts Sociedad Anónima')
    
    def test_descripcion_validation_too_short(self):
        """Test descripcion validation with too short description."""
        data = self.valid_data.copy()
        data['descripcion'] = 'Corto'  # Too short
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('descripcion', form.errors)
    
    def test_descripcion_normalization(self):
        """Test that descripcion is stripped of whitespace."""
        data = self.valid_data.copy()
        data['descripcion'] = '  Importadora de repuestos automotrices  '
        form = ProveedorForm(data=data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['descripcion'], 'Importadora de repuestos automotrices')
    
    def test_telefono_validation_invalid_format(self):
        """Test telefono validation with invalid format."""
        data = self.valid_data.copy()
        data['telefono'] = '123'  # Too short
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)
    
    def test_telefono_validation_valid_formats(self):
        """Test telefono validation with valid formats."""
        valid_phones = [
            '+593-2-2234567',
            '02-2234567',
            '(02) 223-4567',
            '+1-555-123-4567'
        ]
        
        for phone in valid_phones:
            data = self.valid_data.copy()
            data['telefono'] = phone
            form = ProveedorForm(data=data)
            self.assertTrue(form.is_valid(), f"Phone {phone} should be valid")
    
    def test_correo_validation_invalid_format(self):
        """Test correo validation with invalid format."""
        data = self.valid_data.copy()
        data['correo'] = 'invalid-email'
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)
    
    def test_correo_normalization(self):
        """Test that correo is normalized to lowercase."""
        data = self.valid_data.copy()
        data['correo'] = 'VENTAS@AUTOPARTS.COM.EC'
        form = ProveedorForm(data=data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['correo'], 'ventas@autoparts.com.ec')
    
    def test_pais_normalization(self):
        """Test that pais is normalized to title case."""
        data = self.valid_data.copy()
        data['pais'] = 'estados unidos'
        form = ProveedorForm(data=data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['pais'], 'Estados Unidos')
    
    def test_direccion_validation_too_short(self):
        """Test direccion validation with too short address."""
        data = self.valid_data.copy()
        data['direccion'] = 'Calle 1'  # Too short
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('direccion', form.errors)
    
    def test_direccion_normalization(self):
        """Test that direccion is stripped of whitespace."""
        data = self.valid_data.copy()
        data['direccion'] = '  Av. Amazonas 123, Quito  '
        form = ProveedorForm(data=data)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['direccion'], 'Av. Amazonas 123, Quito')
    
    def test_nombre_uniqueness_validation_new(self):
        """Test nombre uniqueness validation for new proveedor."""
        # Create existing proveedor
        Proveedor.objects.create(**self.valid_data)
        
        # Try to create form with same nombre (case insensitive)
        data = self.valid_data.copy()
        data['nombre'] = 'IMPORTADORA AUTOPARTS S.A.'  # Same name, different case
        data['correo'] = 'otro@email.com'  # Different email to avoid unique constraint
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
    
    def test_nombre_uniqueness_validation_edit(self):
        """Test nombre uniqueness validation for existing proveedor (edit)."""
        # Create proveedor
        proveedor = Proveedor.objects.create(**self.valid_data)
        
        # Edit same proveedor with same nombre should be valid
        form = ProveedorForm(data=self.valid_data, instance=proveedor)
        
        self.assertTrue(form.is_valid())
    
    def test_correo_uniqueness_validation_new(self):
        """Test correo uniqueness validation for new proveedor."""
        # Create existing proveedor
        Proveedor.objects.create(**self.valid_data)
        
        # Try to create form with same correo
        data = self.valid_data.copy()
        data['nombre'] = 'Otro Proveedor'
        form = ProveedorForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)
    
    def test_correo_uniqueness_validation_edit(self):
        """Test correo uniqueness validation for existing proveedor (edit)."""
        # Create proveedor
        proveedor = Proveedor.objects.create(**self.valid_data)
        
        # Edit same proveedor with same correo should be valid
        form = ProveedorForm(data=self.valid_data, instance=proveedor)
        
        self.assertTrue(form.is_valid())
    
    def test_form_save_creates_proveedor(self):
        """Test that form.save() creates proveedor instance."""
        form = ProveedorForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
        proveedor = form.save()
        
        self.assertIsInstance(proveedor, Proveedor)
        self.assertEqual(proveedor.nombre, 'Importadora Autoparts S.A.')  # Normalized
        self.assertEqual(proveedor.correo, 'ventas@autoparts.com.ec')
        self.assertEqual(proveedor.pais, 'Ecuador')
    
    def test_form_save_updates_proveedor(self):
        """Test that form.save() updates existing proveedor instance."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        
        # Update data
        updated_data = self.valid_data.copy()
        updated_data['nombre'] = 'Nuevo Proveedor S.A.'
        updated_data['pais'] = 'Colombia'
        
        form = ProveedorForm(data=updated_data, instance=proveedor)
        self.assertTrue(form.is_valid())
        
        updated_proveedor = form.save()
        
        self.assertEqual(updated_proveedor.pk, proveedor.pk)
        self.assertEqual(updated_proveedor.nombre, 'Nuevo Proveedor S.A.')
        self.assertEqual(updated_proveedor.pais, 'Colombia')
    
    def test_form_widget_attributes(self):
        """Test that form widgets have proper CSS classes."""
        form = ProveedorForm()
        
        # Check that form fields have Bootstrap classes
        self.assertIn('form-control', form.fields['nombre'].widget.attrs.get('class', ''))
        self.assertIn('form-control', form.fields['descripcion'].widget.attrs.get('class', ''))
        self.assertIn('form-control', form.fields['telefono'].widget.attrs.get('class', ''))
        self.assertIn('form-control', form.fields['pais'].widget.attrs.get('class', ''))
        self.assertIn('form-control', form.fields['correo'].widget.attrs.get('class', ''))
        self.assertIn('form-control', form.fields['direccion'].widget.attrs.get('class', ''))
    
    def test_form_help_texts(self):
        """Test that form fields have appropriate help texts in Spanish."""
        form = ProveedorForm()
        
        self.assertIn('razón social', form.fields['nombre'].help_text.lower())
        self.assertIn('descripción', form.fields['descripcion'].help_text.lower())
        self.assertIn('teléfono', form.fields['telefono'].help_text.lower())
        self.assertIn('país', form.fields['pais'].help_text.lower())
        self.assertIn('correo', form.fields['correo'].help_text.lower())
        self.assertIn('dirección', form.fields['direccion'].help_text.lower())
    
    def test_form_required_fields(self):
        """Test that required fields are properly marked."""
        form = ProveedorForm()
        
        self.assertTrue(form.fields['nombre'].required)
        self.assertTrue(form.fields['descripcion'].required)
        self.assertTrue(form.fields['telefono'].required)
        self.assertTrue(form.fields['pais'].required)
        self.assertTrue(form.fields['correo'].required)
        self.assertTrue(form.fields['direccion'].required)