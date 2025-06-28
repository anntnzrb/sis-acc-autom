"""
Test cases for Trabajadores app using London School TDD approach.
Focus on interaction testing and behavior verification.
"""

from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.urls import reverse

from trabajadores.models import Trabajador
from trabajadores.forms import TrabajadorForm


class TrabajadorModelTest(TestCase):
    """Test Trabajador model behavior and validation."""

    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "correo": "juan.perez@carriacces.com",
            "cedula": "1234567890",
            "codigo_empleado": "EMP001",
        }

    def test_create_trabajador_with_valid_data(self):
        """Test creating trabajador with valid data."""
        trabajador = Trabajador(**self.valid_data)
        trabajador.full_clean()  # Should not raise
        trabajador.save()

        self.assertEqual(trabajador.nombre, "Juan")
        self.assertEqual(trabajador.apellido, "Pérez")
        self.assertEqual(trabajador.correo, "juan.perez@carriacces.com")
        self.assertEqual(trabajador.cedula, "1234567890")
        self.assertEqual(trabajador.codigo_empleado, "EMP001")
        self.assertIsNotNone(trabajador.created_at)
        self.assertIsNotNone(trabajador.updated_at)

    def test_trabajador_str_representation(self):
        """Test string representation of trabajador."""
        trabajador = Trabajador(**self.valid_data)
        trabajador.clean()
        self.assertEqual(str(trabajador), "Juan Pérez")

    def test_get_nombre_completo_method(self):
        """Test get_nombre_completo method."""
        trabajador = Trabajador(**self.valid_data)
        trabajador.clean()
        self.assertEqual(trabajador.get_nombre_completo(), "Juan Pérez")

    def test_nombre_normalization(self):
        """Test that nombre is normalized to title case."""
        data = self.valid_data.copy()
        data["nombre"] = "juan carlos"
        trabajador = Trabajador(**data)
        trabajador.clean()

        self.assertEqual(trabajador.nombre, "Juan Carlos")

    def test_apellido_normalization(self):
        """Test that apellido is normalized to title case."""
        data = self.valid_data.copy()
        data["apellido"] = "pérez gonzález"
        trabajador = Trabajador(**data)
        trabajador.clean()

        self.assertEqual(trabajador.apellido, "Pérez González")

    def test_correo_normalization(self):
        """Test that correo is normalized to lowercase."""
        data = self.valid_data.copy()
        data["correo"] = "JUAN.PEREZ@CARRIACCES.COM"
        trabajador = Trabajador(**data)
        trabajador.clean()

        self.assertEqual(trabajador.correo, "juan.perez@carriacces.com")

    def test_codigo_empleado_normalization(self):
        """Test that codigo_empleado is normalized to uppercase."""
        data = self.valid_data.copy()
        data["codigo_empleado"] = "emp001"
        trabajador = Trabajador(**data)
        trabajador.clean()

        self.assertEqual(trabajador.codigo_empleado, "EMP001")

    def test_cedula_validation_invalid_length(self):
        """Test cedula validation with invalid length."""
        data = self.valid_data.copy()
        data["cedula"] = "123456789"  # 9 digits
        trabajador = Trabajador(**data)

        with self.assertRaises(ValidationError):
            trabajador.full_clean()

    def test_cedula_validation_non_numeric(self):
        """Test cedula validation with non-numeric characters."""
        data = self.valid_data.copy()
        data["cedula"] = "123456789a"
        trabajador = Trabajador(**data)

        with self.assertRaises(ValidationError):
            trabajador.full_clean()

    def test_correo_validation_invalid_format(self):
        """Test correo validation with invalid email format."""
        data = self.valid_data.copy()
        data["correo"] = "invalid-email"
        trabajador = Trabajador(**data)

        with self.assertRaises(ValidationError):
            trabajador.full_clean()

    def test_unique_correo_constraint(self):
        """Test unique constraint on correo field."""
        # Create first trabajador
        Trabajador.objects.create(**self.valid_data)

        # Try to create another with same correo
        data = self.valid_data.copy()
        data["cedula"] = "9876543210"
        data["codigo_empleado"] = "EMP002"
        trabajador2 = Trabajador(**data)

        with self.assertRaises(ValidationError):
            trabajador2.full_clean()

    def test_unique_cedula_constraint(self):
        """Test unique constraint on cedula field."""
        # Create first trabajador
        Trabajador.objects.create(**self.valid_data)

        # Try to create another with same cedula
        data = self.valid_data.copy()
        data["correo"] = "otro@carriacces.com"
        data["codigo_empleado"] = "EMP002"
        trabajador2 = Trabajador(**data)

        with self.assertRaises(ValidationError):
            trabajador2.full_clean()

    def test_unique_codigo_empleado_constraint(self):
        """Test unique constraint on codigo_empleado field."""
        # Create first trabajador
        Trabajador.objects.create(**self.valid_data)

        # Try to create another with same codigo
        data = self.valid_data.copy()
        data["correo"] = "otro@carriacces.com"
        data["cedula"] = "9876543210"
        trabajador2 = Trabajador(**data)

        with self.assertRaises(ValidationError):
            trabajador2.full_clean()

    def test_model_meta_verbose_names(self):
        """Test model verbose names are in Spanish."""
        meta = Trabajador._meta
        self.assertEqual(meta.verbose_name, "Trabajador")
        self.assertEqual(meta.verbose_name_plural, "Trabajadores")

    def test_model_ordering(self):
        """Test model ordering by apellido and nombre."""
        # Create trabajadores in different order
        Trabajador.objects.create(
            nombre="Carlos",
            apellido="Zambrano",
            correo="carlos@test.com",
            cedula="1111111111",
            codigo_empleado="EMP001",
        )
        Trabajador.objects.create(
            nombre="Ana",
            apellido="Pérez",
            correo="ana@test.com",
            cedula="2222222222",
            codigo_empleado="EMP002",
        )
        Trabajador.objects.create(
            nombre="Luis",
            apellido="Pérez",
            correo="luis@test.com",
            cedula="3333333333",
            codigo_empleado="EMP003",
        )

        trabajadores = list(Trabajador.objects.all())

        # Should be ordered by apellido, then nombre
        self.assertEqual(trabajadores[0].nombre, "Ana")
        self.assertEqual(trabajadores[1].nombre, "Luis")
        self.assertEqual(trabajadores[2].nombre, "Carlos")

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
        trabajador.nombre = "Carlos"
        trabajador.save()

        self.assertGreaterEqual(trabajador.updated_at, original_updated)


class TrabajadorFormTest(TestCase):
    """Test TrabajadorForm validation and behavior."""

    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "correo": "juan.perez@carriacces.com",
            "cedula": "1234567890",
            "codigo_empleado": "EMP001",
        }

    def test_form_valid_with_complete_data(self):
        """Test form is valid with complete data."""
        form = TrabajadorForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_saves_with_data_normalization(self):
        """Test form saves trabajador with normalized data."""
        data = self.valid_data.copy()
        data["nombre"] = "juan carlos"
        data["apellido"] = "pérez gonzález"
        data["correo"] = "JUAN@CARRIACCES.COM"
        data["codigo_empleado"] = "emp001"

        form = TrabajadorForm(data=data)
        self.assertTrue(form.is_valid())
        trabajador = form.save()

        self.assertEqual(trabajador.nombre, "Juan Carlos")
        self.assertEqual(trabajador.apellido, "Pérez González")
        self.assertEqual(trabajador.correo, "juan@carriacces.com")
        self.assertEqual(trabajador.codigo_empleado, "EMP001")

    def test_form_invalid_with_missing_required_fields(self):
        """Test form is invalid with missing required fields."""
        # Test each required field
        required_fields = ["nombre", "apellido", "correo", "cedula", "codigo_empleado"]

        for field in required_fields:
            with self.subTest(field=field):
                data = self.valid_data.copy()
                del data[field]
                form = TrabajadorForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_form_nombre_validation_too_short(self):
        """Test form validation with nombre too short."""
        data = self.valid_data.copy()
        data["nombre"] = "A"
        form = TrabajadorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("nombre", form.errors)

    def test_form_nombre_validation_non_alpha(self):
        """Test form validation with nombre containing non-alpha characters."""
        data = self.valid_data.copy()
        data["nombre"] = "Juan123"
        form = TrabajadorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("nombre", form.errors)

    def test_form_apellido_validation_too_short(self):
        """Test form validation with apellido too short."""
        data = self.valid_data.copy()
        data["apellido"] = "P"
        form = TrabajadorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("apellido", form.errors)

    def test_form_apellido_validation_non_alpha(self):
        """Test form validation with apellido containing non-alpha characters."""
        data = self.valid_data.copy()
        data["apellido"] = "Pérez123"
        form = TrabajadorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("apellido", form.errors)

    def test_form_cedula_validation_invalid_format(self):
        """Test form validation with invalid cedula format."""
        invalid_cedulas = ["123456789", "12345678901", "abcdefghij", "123456789a"]

        for cedula in invalid_cedulas:
            with self.subTest(cedula=cedula):
                data = self.valid_data.copy()
                data["cedula"] = cedula
                form = TrabajadorForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn("cedula", form.errors)

    def test_form_codigo_empleado_validation_too_short(self):
        """Test form validation with codigo_empleado too short."""
        data = self.valid_data.copy()
        data["codigo_empleado"] = "AB"
        form = TrabajadorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("codigo_empleado", form.errors)

    def test_form_duplicate_correo_validation_create(self):
        """Test form validates unique correo on create."""
        # Create existing trabajador
        Trabajador.objects.create(**self.valid_data)

        # Try to create another with same correo
        data = self.valid_data.copy()
        data["cedula"] = "9876543210"
        data["codigo_empleado"] = "EMP002"
        form = TrabajadorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("correo", form.errors)

    def test_form_duplicate_cedula_validation_create(self):
        """Test form validates unique cedula on create."""
        # Create existing trabajador
        Trabajador.objects.create(**self.valid_data)

        # Try to create another with same cedula
        data = self.valid_data.copy()
        data["correo"] = "otro@carriacces.com"
        data["codigo_empleado"] = "EMP002"
        form = TrabajadorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("cedula", form.errors)

    def test_form_duplicate_codigo_validation_create(self):
        """Test form validates unique codigo_empleado on create."""
        # Create existing trabajador
        Trabajador.objects.create(**self.valid_data)

        # Try to create another with same codigo
        data = self.valid_data.copy()
        data["correo"] = "otro@carriacces.com"
        data["cedula"] = "9876543210"
        form = TrabajadorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("codigo_empleado", form.errors)

    def test_form_duplicate_validation_on_edit_same_instance(self):
        """Test form allows same values when editing same instance."""
        # Create trabajador
        trabajador = Trabajador.objects.create(**self.valid_data)

        # Edit same trabajador with same data
        form = TrabajadorForm(data=self.valid_data, instance=trabajador)
        self.assertTrue(form.is_valid())

    def test_form_duplicate_validation_on_edit_different_instance(self):
        """Test form validates duplicates when editing different instance."""
        # Create two trabajadores
        Trabajador.objects.create(**self.valid_data)

        data2 = self.valid_data.copy()
        data2["correo"] = "otro@carriacces.com"
        data2["cedula"] = "9876543210"
        data2["codigo_empleado"] = "EMP002"
        trabajador2 = Trabajador.objects.create(**data2)

        # Try to edit trabajador2 with trabajador1's correo
        data2["correo"] = self.valid_data["correo"]
        form = TrabajadorForm(data=data2, instance=trabajador2)

        self.assertFalse(form.is_valid())
        self.assertIn("correo", form.errors)


class TrabajadorViewTest(TestCase):
    """Test Trabajador views and templates."""

    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.valid_data = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "correo": "juan.perez@carriacces.com",
            "cedula": "1234567890",
            "codigo_empleado": "EMP001",
        }

    def test_trabajador_list_view_empty(self):
        """Test list view when no trabajadores exist."""
        response = self.client.get(reverse("trabajadores:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "NUESTRO PERSONAL")
        self.assertEqual(response.context["total_trabajadores"], 0)

    def test_trabajador_list_view_with_trabajadores(self):
        """Test list view with existing trabajadores."""
        trabajador = Trabajador.objects.create(**self.valid_data)
        response = self.client.get(reverse("trabajadores:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, trabajador.get_nombre_completo())
        self.assertContains(response, trabajador.correo)
        self.assertEqual(response.context["total_trabajadores"], 1)

    def test_trabajador_create_view_get(self):
        """Test create view GET request."""
        response = self.client.get(reverse("trabajadores:create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AGREGAR TRABAJADOR")
        self.assertIsInstance(response.context["form"], TrabajadorForm)

    def test_trabajador_create_view_post_valid(self):
        """Test create view POST with valid data."""
        response = self.client.post(
            reverse("trabajadores:create"), data=self.valid_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Trabajador.objects.exists())
        trabajador = Trabajador.objects.first()
        self.assertEqual(trabajador.nombre, "Juan")
        self.assertEqual(trabajador.apellido, "Pérez")

    def test_trabajador_create_view_post_invalid(self):
        """Test create view POST with invalid data."""
        data = self.valid_data.copy()
        data["cedula"] = "invalid"
        response = self.client.post(reverse("trabajadores:create"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Trabajador.objects.exists())
        self.assertContains(response, "form")

    def test_trabajador_update_view_get(self):
        """Test update view GET request."""
        trabajador = Trabajador.objects.create(**self.valid_data)
        response = self.client.get(
            reverse("trabajadores:update", kwargs={"pk": trabajador.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "EDITAR TRABAJADOR")
        self.assertContains(response, trabajador.nombre)
        self.assertIsInstance(response.context["form"], TrabajadorForm)

    def test_trabajador_update_view_post_valid(self):
        """Test update view POST with valid data."""
        trabajador = Trabajador.objects.create(**self.valid_data)
        data = self.valid_data.copy()
        data["nombre"] = "Carlos"

        response = self.client.post(
            reverse("trabajadores:update", kwargs={"pk": trabajador.pk}), data=data
        )

        self.assertEqual(response.status_code, 302)
        trabajador.refresh_from_db()
        self.assertEqual(trabajador.nombre, "Carlos")

    def test_trabajador_update_view_post_invalid(self):
        """Test update view POST with invalid data."""
        trabajador = Trabajador.objects.create(**self.valid_data)
        data = self.valid_data.copy()
        data["cedula"] = "invalid"

        response = self.client.post(
            reverse("trabajadores:update", kwargs={"pk": trabajador.pk}), data=data
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")
        trabajador.refresh_from_db()
        self.assertEqual(trabajador.cedula, "1234567890")  # Should not change

    def test_trabajador_delete_view_get(self):
        """Test delete view GET request."""
        trabajador = Trabajador.objects.create(**self.valid_data)
        response = self.client.get(
            reverse("trabajadores:delete", kwargs={"pk": trabajador.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ELIMINAR TRABAJADOR")
        self.assertContains(response, trabajador.get_nombre_completo())

    def test_trabajador_delete_view_post(self):
        """Test delete view POST request."""
        trabajador = Trabajador.objects.create(**self.valid_data)
        response = self.client.post(
            reverse("trabajadores:delete", kwargs={"pk": trabajador.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Trabajador.objects.exists())

    def test_trabajador_list_view_pagination(self):
        """Test list view pagination."""
        # Create more than paginate_by trabajadores
        for i in range(15):
            Trabajador.objects.create(
                nombre=f"Trabajador{i}",
                apellido="Test",
                correo=f"test{i}@carriacces.com",
                cedula=f"{1000000000 + i}",
                codigo_empleado=f"EMP{i:03d}",
            )

        response = self.client.get(reverse("trabajadores:list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["trabajadores"]), 12)  # paginate_by = 12

    def test_trabajador_views_context_data(self):
        """Test that views provide correct context data."""
        trabajador = Trabajador.objects.create(**self.valid_data)

        # Test list view context
        response = self.client.get(reverse("trabajadores:list"))
        self.assertEqual(response.context["title"], "NUESTRO PERSONAL")

        # Test create view context
        response = self.client.get(reverse("trabajadores:create"))
        self.assertEqual(response.context["title"], "AGREGAR TRABAJADOR")
        self.assertEqual(response.context["action"], "Crear")

        # Test update view context
        response = self.client.get(
            reverse("trabajadores:update", kwargs={"pk": trabajador.pk})
        )
        self.assertEqual(response.context["title"], "EDITAR TRABAJADOR")
        self.assertEqual(response.context["action"], "Actualizar")
        self.assertEqual(response.context["trabajador"], trabajador)

        # Test delete view context
        response = self.client.get(
            reverse("trabajadores:delete", kwargs={"pk": trabajador.pk})
        )
        self.assertEqual(response.context["title"], "ELIMINAR TRABAJADOR")
        self.assertEqual(response.context["trabajador"], trabajador)
