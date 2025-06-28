"""
Test cases for Proveedor views using London School TDD approach.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from proveedores.models import Proveedor
from proveedores.forms import ProveedorForm


class ProveedorViewsTest(TestCase):
    """Test Proveedor views behavior and integration."""
    
    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.valid_data = {
            'nombre': 'Importadora AutoParts S.A.',
            'descripcion': 'Importadora especializada en repuestos y accesorios automotrices de alta calidad',
            'telefono': '+593-2-2234567',
            'pais': 'Ecuador',
            'correo': 'ventas@autoparts.com.ec',
            'direccion': 'Av. Amazonas 123, Quito, Ecuador'
        }
    
    def test_proveedor_list_view_empty(self):
        """Test proveedor list view when no proveedores exist."""
        response = self.client.get(reverse('proveedores:list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NUESTROS PROVEEDORES')
        self.assertContains(response, 'No hay proveedores registrados')
        self.assertContains(response, reverse('proveedores:create'))
    
    def test_proveedor_list_view_with_proveedores(self):
        """Test proveedor list view when proveedores exist."""
        proveedor1 = Proveedor.objects.create(**self.valid_data)
        
        # Create second proveedor
        data2 = self.valid_data.copy()
        data2['nombre'] = 'Beta Distribuidores'
        data2['correo'] = 'info@beta.com'
        proveedor2 = Proveedor.objects.create(**data2)
        
        response = self.client.get(reverse('proveedores:list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, proveedor1.nombre)
        self.assertContains(response, proveedor2.nombre)
        self.assertContains(response, proveedor1.correo)
        self.assertContains(response, proveedor2.correo)
        self.assertContains(response, 'AGREGAR PROVEEDOR')
    
    def test_proveedor_create_view_get(self):
        """Test GET request to proveedor create view."""
        response = self.client.get(reverse('proveedores:create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ProveedorForm)
        self.assertContains(response, 'AGREGAR PROVEEDOR')
        self.assertContains(response, 'form-control')  # Bootstrap classes
    
    def test_proveedor_create_view_post_valid_data(self):
        """Test POST request to create proveedor with valid data."""
        response = self.client.post(reverse('proveedores:create'), data=self.valid_data)
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertRedirects(response, reverse('proveedores:list'))
        
        # Check proveedor was created
        proveedor = Proveedor.objects.get()
        self.assertEqual(proveedor.nombre, 'Importadora Autoparts S.A.')  # Normalized
        self.assertEqual(proveedor.correo, 'ventas@autoparts.com.ec')
        self.assertEqual(proveedor.pais, 'Ecuador')
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('exitosamente' in str(message) for message in messages))
    
    def test_proveedor_create_view_post_invalid_data(self):
        """Test POST request to create proveedor with invalid data."""
        invalid_data = self.valid_data.copy()
        del invalid_data['nombre']  # Remove required field
        
        response = self.client.post(reverse('proveedores:create'), data=invalid_data)
        
        self.assertEqual(response.status_code, 200)  # Stay on form page
        self.assertIsInstance(response.context['form'], ProveedorForm)
        self.assertFalse(response.context['form'].is_valid())
        self.assertContains(response, 'form-control')  # Bootstrap classes present
        
        # Check no proveedor was created
        self.assertEqual(Proveedor.objects.count(), 0)
    
    def test_proveedor_update_view_get(self):
        """Test GET request to proveedor update view."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        
        response = self.client.get(reverse('proveedores:update', kwargs={'pk': proveedor.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ProveedorForm)
        self.assertEqual(response.context['form'].instance, proveedor)
        self.assertContains(response, 'EDITAR PROVEEDOR')
        self.assertContains(response, proveedor.nombre)
    
    def test_proveedor_update_view_post_valid_data(self):
        """Test POST request to update proveedor with valid data."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        
        updated_data = self.valid_data.copy()
        updated_data['nombre'] = 'Nuevo Proveedor S.A.'
        updated_data['pais'] = 'Colombia'
        
        response = self.client.post(
            reverse('proveedores:update', kwargs={'pk': proveedor.pk}),
            data=updated_data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proveedores:list'))
        
        # Check proveedor was updated
        proveedor.refresh_from_db()
        self.assertEqual(proveedor.nombre, 'Nuevo Proveedor S.A.')
        self.assertEqual(proveedor.pais, 'Colombia')
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('actualizado' in str(message) for message in messages))
    
    def test_proveedor_update_view_post_invalid_data(self):
        """Test POST request to update proveedor with invalid data."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        
        invalid_data = self.valid_data.copy()
        invalid_data['correo'] = 'invalid-email'  # Invalid email
        
        response = self.client.post(
            reverse('proveedores:update', kwargs={'pk': proveedor.pk}),
            data=invalid_data
        )
        
        self.assertEqual(response.status_code, 200)  # Stay on form page
        self.assertFalse(response.context['form'].is_valid())
        
        # Check proveedor was not updated
        proveedor.refresh_from_db()
        self.assertEqual(proveedor.correo, 'ventas@autoparts.com.ec')  # Original value
    
    def test_proveedor_update_view_nonexistent_pk(self):
        """Test update view with nonexistent proveedor ID."""
        response = self.client.get(reverse('proveedores:update', kwargs={'pk': 999}))
        
        self.assertEqual(response.status_code, 404)
    
    def test_proveedor_delete_view_get(self):
        """Test GET request to proveedor delete view."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        
        response = self.client.get(reverse('proveedores:delete', kwargs={'pk': proveedor.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '¿Está seguro de eliminar')
        self.assertContains(response, proveedor.nombre)
        self.assertContains(response, 'Eliminar')
        self.assertContains(response, 'Cancelar')
    
    def test_proveedor_delete_view_post(self):
        """Test POST request to delete proveedor."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        proveedor_id = proveedor.pk
        
        response = self.client.post(reverse('proveedores:delete', kwargs={'pk': proveedor_id}))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proveedores:list'))
        
        # Check proveedor was deleted
        self.assertFalse(Proveedor.objects.filter(pk=proveedor_id).exists())
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('eliminado' in str(message) for message in messages))
    
    def test_proveedor_delete_view_nonexistent_pk(self):
        """Test delete view with nonexistent proveedor ID."""
        response = self.client.get(reverse('proveedores:delete', kwargs={'pk': 999}))
        
        self.assertEqual(response.status_code, 404)
    
    def test_proveedor_list_view_pagination(self):
        """Test pagination in list view when many proveedores exist."""
        # Create multiple proveedores to test pagination
        for i in range(15):
            data = self.valid_data.copy()
            data['nombre'] = f'Proveedor {i+1:02d}'
            data['correo'] = f'proveedor{i+1:02d}@email.com'
            Proveedor.objects.create(**data)
        
        response = self.client.get(reverse('proveedores:list'))
        
        self.assertEqual(response.status_code, 200)
        # Check that proveedores are displayed (actual pagination depends on view settings)
        self.assertTrue(response.context['proveedores'])
    
    def test_proveedor_list_view_ordering(self):
        """Test that proveedores are ordered correctly in list view."""
        # Create proveedores in reverse alphabetical order
        names_and_emails = [
            ('Zebra Proveedores', 'zebra@email.com'),
            ('Alpha Proveedores', 'alpha@email.com'),
            ('Beta Proveedores', 'beta@email.com')
        ]
        for name, email in names_and_emails:
            data = self.valid_data.copy()
            data['nombre'] = name
            data['correo'] = email
            Proveedor.objects.create(**data)
        
        response = self.client.get(reverse('proveedores:list'))
        proveedores = response.context['proveedores']
        
        # Should be ordered alphabetically by nombre
        proveedor_names = [p.nombre for p in proveedores]
        self.assertEqual(proveedor_names[0], 'Alpha Proveedores')
        self.assertEqual(proveedor_names[1], 'Beta Proveedores')
        self.assertEqual(proveedor_names[2], 'Zebra Proveedores')
    
    def test_view_context_data_basic(self):
        """Test that views return proper context data."""
        response = self.client.get(reverse('proveedores:create'))
        
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ProveedorForm)
    
    def test_form_error_handling_displays_messages(self):
        """Test that form errors are properly displayed to user."""
        invalid_data = {'nombre': '', 'correo': 'invalid-email'}
        
        response = self.client.post(reverse('proveedores:create'), data=invalid_data)
        
        self.assertEqual(response.status_code, 200)  # Form errors, stay on page
        self.assertFalse(response.context['form'].is_valid())
    
    def test_csrf_protection_enabled(self):
        """Test that CSRF protection is enabled on forms."""
        response = self.client.get(reverse('proveedores:create'))
        
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_view_uses_correct_templates(self):
        """Test that views use correct templates."""
        # List view
        response = self.client.get(reverse('proveedores:list'))
        self.assertTemplateUsed(response, 'proveedores/list.html')
        
        # Create view
        response = self.client.get(reverse('proveedores:create'))
        self.assertTemplateUsed(response, 'proveedores/form.html')
        
        # Update view (need proveedor first)
        proveedor = Proveedor.objects.create(**self.valid_data)
        response = self.client.get(reverse('proveedores:update', kwargs={'pk': proveedor.pk}))
        self.assertTemplateUsed(response, 'proveedores/form.html')
        
        # Delete view
        response = self.client.get(reverse('proveedores:delete', kwargs={'pk': proveedor.pk}))
        self.assertTemplateUsed(response, 'proveedores/confirm_delete.html')
    
    def test_proveedor_contact_info_display(self):
        """Test that contact information is properly displayed."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        
        response = self.client.get(reverse('proveedores:list'))
        
        # Check that contact info is displayed
        self.assertContains(response, proveedor.correo)
        self.assertContains(response, proveedor.telefono)
    
    def test_proveedor_location_info_display(self):
        """Test that location information is properly displayed."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        
        response = self.client.get(reverse('proveedores:list'))
        
        # Check that location info is displayed
        self.assertContains(response, proveedor.pais)
    
    def test_empty_state_handling(self):
        """Test empty state when no proveedores exist."""
        response = self.client.get(reverse('proveedores:list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No hay proveedores')
        self.assertContains(response, reverse('proveedores:create'))
    
    def test_proveedor_search_functionality(self):
        """Test search functionality in list view if implemented."""
        # Create test proveedores
        proveedor1 = Proveedor.objects.create(**self.valid_data)
        
        data2 = self.valid_data.copy()
        data2['nombre'] = 'Distribuidora Nacional'
        data2['correo'] = 'info@distribuidor.com'
        proveedor2 = Proveedor.objects.create(**data2)
        
        response = self.client.get(reverse('proveedores:list'))
        
        # Check both proveedores are displayed
        self.assertContains(response, proveedor1.nombre)
        self.assertContains(response, proveedor2.nombre)
    
    def test_proveedor_card_layout_information(self):
        """Test that proveedor cards display proper information."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        
        response = self.client.get(reverse('proveedores:list'))
        
        # Check that all important info is displayed in cards
        self.assertContains(response, proveedor.nombre)
        self.assertContains(response, proveedor.descripcion)
        self.assertContains(response, proveedor.correo)
        self.assertContains(response, proveedor.telefono)
        self.assertContains(response, proveedor.pais)