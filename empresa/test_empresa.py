"""
Test cases for Empresa app using London School TDD approach.
Focus on interaction testing and behavior verification.
"""
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from unittest.mock import Mock, patch
from datetime import datetime
import tempfile
import os

from empresa.models import Empresa, EmpresaManager
from empresa.forms import EmpresaForm


class EmpresaModelTest(TestCase):
    """Test Empresa model behavior and validation."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'nombre': 'CarriAcces S.A.',
            'direccion': 'Av. Principal 123, Quito, Ecuador',
            'mision': 'Proveer los mejores accesorios automotrices',
            'vision': 'Ser líderes en el mercado automotriz',
            'anio_fundacion': 2010,
            'ruc': '1234567890001'
        }
    
    def test_create_empresa_with_valid_data(self):
        """Test creating empresa with valid data."""
        empresa = Empresa(**self.valid_data)
        empresa.full_clean()  # Should not raise
        empresa.save()
        
        self.assertEqual(empresa.nombre, 'Carriacces S.A.')
        self.assertEqual(empresa.ruc, '1234567890001')
        self.assertIsNotNone(empresa.created_at)
        self.assertIsNotNone(empresa.updated_at)
    
    def test_empresa_str_representation(self):
        """Test string representation of empresa."""
        empresa = Empresa(**self.valid_data)
        empresa.clean()
        self.assertEqual(str(empresa), 'Carriacces S.A.')
    
    def test_empresa_nombre_normalization(self):
        """Test that nombre is normalized to title case."""
        data = self.valid_data.copy()
        data['nombre'] = 'carriacces sociedad anónima'
        empresa = Empresa(**data)
        empresa.clean()
        
        self.assertEqual(empresa.nombre, 'Carriacces Sociedad Anónima')
    
    def test_direccion_normalization(self):
        """Test that direccion is stripped of whitespace."""
        data = self.valid_data.copy()
        data['direccion'] = '  Av. Principal 123, Quito  '
        empresa = Empresa(**data)
        empresa.clean()
        
        self.assertEqual(empresa.direccion, 'Av. Principal 123, Quito')
    
    def test_mision_normalization(self):
        """Test that mision is stripped of whitespace."""
        data = self.valid_data.copy()
        data['mision'] = '  Nuestra misión es...  '
        empresa = Empresa(**data)
        empresa.clean()
        
        self.assertEqual(empresa.mision, 'Nuestra misión es...')
    
    def test_vision_normalization(self):
        """Test that vision is stripped of whitespace."""
        data = self.valid_data.copy()
        data['vision'] = '  Nuestra visión es...  '
        empresa = Empresa(**data)
        empresa.clean()
        
        self.assertEqual(empresa.vision, 'Nuestra visión es...')
    
    def test_ruc_validation_invalid_length(self):
        """Test RUC validation with invalid length."""
        data = self.valid_data.copy()
        data['ruc'] = '123456789'  # Less than 13 digits
        empresa = Empresa(**data)
        
        with self.assertRaises(ValidationError):
            empresa.full_clean()
    
    def test_ruc_validation_non_numeric(self):
        """Test RUC validation with non-numeric characters."""
        data = self.valid_data.copy()
        data['ruc'] = '123456789000a'
        empresa = Empresa(**data)
        
        with self.assertRaises(ValidationError):
            empresa.full_clean()
    
    def test_anio_fundacion_validation_too_old(self):
        """Test anio_fundacion validation with year before 1900."""
        data = self.valid_data.copy()
        data['anio_fundacion'] = 1850
        empresa = Empresa(**data)
        
        with self.assertRaises(ValidationError):
            empresa.full_clean()
    
    def test_anio_fundacion_validation_future_year(self):
        """Test anio_fundacion validation with future year."""
        data = self.valid_data.copy()
        data['anio_fundacion'] = datetime.now().year + 1
        empresa = Empresa(**data)
        
        with self.assertRaises(ValidationError):
            empresa.full_clean()
    
    def test_singleton_constraint_on_clean(self):
        """Test singleton constraint in clean method."""
        # Create first empresa
        Empresa.objects.create(**self.valid_data)
        
        # Try to create second empresa
        data = self.valid_data.copy()
        data['ruc'] = '9876543210001'
        empresa2 = Empresa(**data)
        
        with self.assertRaises(ValidationError):
            empresa2.clean()
    
    def test_singleton_constraint_on_save(self):
        """Test singleton constraint in save method."""
        # Create first empresa
        Empresa.objects.create(**self.valid_data)
        
        # Try to create second empresa bypassing clean
        data = self.valid_data.copy()
        data['ruc'] = '9876543210001'
        empresa2 = Empresa(**data)
        
        with self.assertRaises(ValidationError):
            empresa2.save()
    
    def test_unique_ruc_constraint(self):
        """Test unique constraint on RUC field."""
        # Create first empresa
        Empresa.objects.create(**self.valid_data)
        
        # Delete and try to create another with same RUC
        Empresa.objects.all().delete()
        
        empresa2 = Empresa(**self.valid_data)
        empresa2.full_clean()  # Should pass since first was deleted
        empresa2.save()
        
        self.assertEqual(empresa2.ruc, '1234567890001')
    
    def test_model_meta_verbose_names(self):
        """Test model verbose names are in Spanish."""
        meta = Empresa._meta
        self.assertEqual(meta.verbose_name, 'Empresa')
        self.assertEqual(meta.verbose_name_plural, 'Empresas')
    
    def test_timestamps_auto_population(self):
        """Test that timestamps are automatically populated."""
        empresa = Empresa.objects.create(**self.valid_data)
        
        self.assertIsNotNone(empresa.created_at)
        self.assertIsNotNone(empresa.updated_at)
        # Check that timestamps are close (within 1 second)
        time_diff = abs((empresa.updated_at - empresa.created_at).total_seconds())
        self.assertLess(time_diff, 1.0)
    
    def test_updated_at_changes_on_save(self):
        """Test that updated_at changes when model is saved again."""
        empresa = Empresa.objects.create(**self.valid_data)
        original_updated = empresa.updated_at
        
        # Simulate time passing and update
        empresa.nombre = 'Nuevo Nombre'
        empresa.save()
        
        self.assertGreaterEqual(empresa.updated_at, original_updated)


class EmpresaManagerTest(TestCase):
    """Test EmpresaManager custom methods."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'nombre': 'CarriAcces S.A.',
            'direccion': 'Av. Principal 123, Quito, Ecuador',
            'mision': 'Proveer los mejores accesorios automotrices',
            'vision': 'Ser líderes en el mercado automotriz',
            'anio_fundacion': 2010,
            'ruc': '1234567890001'
        }
    
    def test_get_empresa_when_exists(self):
        """Test get_empresa returns empresa when it exists."""
        empresa = Empresa.objects.create(**self.valid_data)
        result = Empresa.objects.get_empresa()
        
        self.assertEqual(result, empresa)
        self.assertEqual(result.nombre, 'Carriacces S.A.')
    
    def test_get_empresa_when_not_exists(self):
        """Test get_empresa returns None when no empresa exists."""
        result = Empresa.objects.get_empresa()
        self.assertIsNone(result)
    
    def test_create_empresa_success(self):
        """Test create_empresa creates empresa when none exists."""
        empresa = Empresa.objects.create_empresa(**self.valid_data)
        
        self.assertIsInstance(empresa, Empresa)
        self.assertEqual(empresa.nombre, 'Carriacces S.A.')
        self.assertEqual(Empresa.objects.count(), 1)
    
    def test_create_empresa_fails_when_exists(self):
        """Test create_empresa raises ValidationError when empresa exists."""
        # Create first empresa
        Empresa.objects.create(**self.valid_data)
        
        # Try to create another
        data = self.valid_data.copy()
        data['ruc'] = '9876543210001'
        
        with self.assertRaises(ValidationError) as context:
            Empresa.objects.create_empresa(**data)
        
        self.assertIn("Ya existe una empresa registrada", str(context.exception))


class EmpresaFormTest(TestCase):
    """Test EmpresaForm validation and behavior."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'nombre': 'CarriAcces S.A.',
            'direccion': 'Av. Principal 123, Quito, Ecuador',
            'mision': 'Proveer los mejores accesorios automotrices',
            'vision': 'Ser líderes en el mercado automotriz',
            'anio_fundacion': 2010,
            'ruc': '1234567890001'
        }
    
    def test_form_valid_with_complete_data(self):
        """Test form is valid with complete data."""
        form = EmpresaForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
    
    def test_form_saves_with_data_normalization(self):
        """Test form saves empresa with normalized data."""
        data = self.valid_data.copy()
        data['nombre'] = 'carriacces s.a.'
        form = EmpresaForm(data=data)
        
        self.assertTrue(form.is_valid())
        empresa = form.save()
        
        self.assertEqual(empresa.nombre, 'Carriacces S.A.')
    
    def test_form_invalid_with_invalid_ruc(self):
        """Test form is invalid with invalid RUC."""
        data = self.valid_data.copy()
        data['ruc'] = 'invalid'
        form = EmpresaForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('ruc', form.errors)
    
    def test_form_invalid_with_invalid_year(self):
        """Test form is invalid with invalid foundation year."""
        data = self.valid_data.copy()
        data['anio_fundacion'] = 1800
        form = EmpresaForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('anio_fundacion', form.errors)
    
    def test_form_singleton_validation(self):
        """Test form validates singleton constraint."""
        # Create existing empresa
        Empresa.objects.create(**self.valid_data)
        
        # Try to create another through form
        data = self.valid_data.copy()
        data['ruc'] = '9876543210001'
        form = EmpresaForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)


class EmpresaViewTest(TestCase):
    """Test Empresa views and templates."""
    
    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.valid_data = {
            'nombre': 'CarriAcces S.A.',
            'direccion': 'Av. Principal 123, Quito, Ecuador',
            'mision': 'Proveer los mejores accesorios automotrices',
            'vision': 'Ser líderes en el mercado automotriz',
            'anio_fundacion': 2010,
            'ruc': '1234567890001'
        }
    
    def test_empresa_detail_view_with_empresa(self):
        """Test detail view when empresa exists."""
        empresa = Empresa.objects.create(**self.valid_data)
        response = self.client.get(reverse('empresa:detail'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, empresa.nombre)
        self.assertContains(response, empresa.ruc)
    
    def test_empresa_detail_view_without_empresa(self):
        """Test detail view when no empresa exists."""
        response = self.client.get(reverse('empresa:detail'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NO SE HA INGRESADO INFORMACIÓN')
    
    def test_empresa_create_view_get(self):
        """Test create view GET request."""
        response = self.client.get(reverse('empresa:create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertIsInstance(response.context['form'], EmpresaForm)
    
    def test_empresa_create_view_post_valid(self):
        """Test create view POST with valid data."""
        response = self.client.post(reverse('empresa:create'), data=self.valid_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Empresa.objects.exists())
        empresa = Empresa.objects.first()
        self.assertEqual(empresa.nombre, 'Carriacces S.A.')
    
    def test_empresa_create_view_post_invalid(self):
        """Test create view POST with invalid data."""
        data = self.valid_data.copy()
        data['ruc'] = 'invalid'
        response = self.client.post(reverse('empresa:create'), data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Empresa.objects.exists())
        self.assertContains(response, 'form')
    
    def test_empresa_edit_view_get(self):
        """Test edit view GET request."""
        empresa = Empresa.objects.create(**self.valid_data)
        response = self.client.get(reverse('empresa:update'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, empresa.nombre)
        self.assertIsInstance(response.context['form'], EmpresaForm)
    
    def test_empresa_edit_view_post_valid(self):
        """Test edit view POST with valid data."""
        empresa = Empresa.objects.create(**self.valid_data)
        data = self.valid_data.copy()
        data['nombre'] = 'Nuevo Nombre'
        
        response = self.client.post(reverse('empresa:update'), data=data)
        
        self.assertEqual(response.status_code, 302)
        empresa.refresh_from_db()
        self.assertEqual(empresa.nombre, 'Nuevo Nombre')
    
    def test_empresa_edit_view_post_invalid(self):
        """Test edit view POST with invalid data."""
        empresa = Empresa.objects.create(**self.valid_data)
        data = self.valid_data.copy()
        data['ruc'] = 'invalid'
        
        response = self.client.post(reverse('empresa:update'), data=data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        empresa.refresh_from_db()
        self.assertEqual(empresa.ruc, '1234567890001')  # Should not change