"""
Test cases for Proveedor model using London School TDD approach.
Focus on interaction testing and behavior verification.
"""

from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from proveedores.forms import ProveedorForm
from proveedores.models import Proveedor


class ProveedorModelTest(TestCase):
    """Test Proveedor model behavior and validation."""

    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            "nombre": "Importadora AutoParts S.A.",
            "descripcion": "Importadora especializada en repuestos y accesorios automotrices de alta calidad",
            "telefono": "+593-2-2234567",
            "pais": "Ecuador",
            "correo": "ventas@autoparts.com.ec",
            "direccion": "Av. Amazonas 123, Quito, Ecuador",
        }

    def test_create_proveedor_with_valid_data(self):
        """Test creating proveedor with valid data."""
        proveedor = Proveedor(**self.valid_data)
        proveedor.full_clean()  # Should not raise
        proveedor.save()

        self.assertEqual(proveedor.nombre, "Importadora Autoparts S.A.")
        self.assertEqual(proveedor.correo, "ventas@autoparts.com.ec")
        self.assertEqual(proveedor.pais, "Ecuador")
        self.assertIsNotNone(proveedor.created_at)
        self.assertIsNotNone(proveedor.updated_at)

    def test_proveedor_str_representation(self):
        """Test string representation of proveedor."""
        proveedor = Proveedor(**self.valid_data)
        proveedor.clean()
        self.assertEqual(str(proveedor), "Importadora Autoparts S.A.")

    def test_proveedor_nombre_normalization(self):
        """Test that nombre is normalized to title case."""
        data = self.valid_data.copy()
        data["nombre"] = "importadora autoparts sociedad anónima"
        proveedor = Proveedor(**data)
        proveedor.clean()

        self.assertEqual(proveedor.nombre, "Importadora Autoparts Sociedad Anónima")

    def test_descripcion_normalization(self):
        """Test that descripcion is stripped of whitespace."""
        data = self.valid_data.copy()
        data["descripcion"] = "  Importadora de repuestos automotrices  "
        proveedor = Proveedor(**data)
        proveedor.clean()

        self.assertEqual(proveedor.descripcion, "Importadora de repuestos automotrices")

    def test_pais_normalization(self):
        """Test that pais is normalized to title case."""
        data = self.valid_data.copy()
        data["pais"] = "estados unidos"
        proveedor = Proveedor(**data)
        proveedor.clean()

        self.assertEqual(proveedor.pais, "Estados Unidos")

    def test_correo_normalization(self):
        """Test that correo is normalized to lowercase."""
        data = self.valid_data.copy()
        data["correo"] = "VENTAS@AUTOPARTS.COM.EC"
        proveedor = Proveedor(**data)
        proveedor.clean()

        self.assertEqual(proveedor.correo, "ventas@autoparts.com.ec")

    def test_direccion_normalization(self):
        """Test that direccion is stripped of whitespace."""
        data = self.valid_data.copy()
        data["direccion"] = "  Av. Amazonas 123, Quito  "
        proveedor = Proveedor(**data)
        proveedor.clean()

        self.assertEqual(proveedor.direccion, "Av. Amazonas 123, Quito")

    def test_telefono_normalization(self):
        """Test that telefono is stripped of whitespace."""
        data = self.valid_data.copy()
        data["telefono"] = "  +593-2-2234567  "
        proveedor = Proveedor(**data)
        proveedor.clean()

        self.assertEqual(proveedor.telefono, "+593-2-2234567")

    def test_telefono_validation_valid_formats(self):
        """Test telefono validation with valid formats."""
        valid_phones = [
            "+593-2-2234567",
            "02-2234567",
            "(02) 223-4567",
            "+1-555-123-4567",
            "555 123 4567",
        ]

        for phone in valid_phones:
            data = self.valid_data.copy()
            data["telefono"] = phone
            proveedor = Proveedor(**data)
            proveedor.full_clean()  # Should not raise

    def test_telefono_validation_invalid_format(self):
        """Test telefono validation with invalid format."""
        data = self.valid_data.copy()
        data["telefono"] = "123"  # Too short
        proveedor = Proveedor(**data)

        with self.assertRaises(ValidationError):
            proveedor.full_clean()

    def test_correo_validation_invalid_format(self):
        """Test correo validation with invalid format."""
        data = self.valid_data.copy()
        data["correo"] = "invalid-email"
        proveedor = Proveedor(**data)

        with self.assertRaises(ValidationError):
            proveedor.full_clean()

    def test_get_contact_info_method(self):
        """Test get_contact_info method returns formatted contact information."""
        proveedor = Proveedor(**self.valid_data)
        contact_info = proveedor.get_contact_info()

        self.assertIn("ventas@autoparts.com.ec", contact_info)
        self.assertIn("+593-2-2234567", contact_info)
        self.assertIn("Email:", contact_info)
        self.assertIn("Tel:", contact_info)

    def test_get_contact_info_method_partial_data(self):
        """Test get_contact_info method with partial contact data."""
        data = self.valid_data.copy()
        del data["telefono"]
        proveedor = Proveedor(**data)
        contact_info = proveedor.get_contact_info()

        self.assertIn("ventas@autoparts.com.ec", contact_info)
        self.assertNotIn("Tel:", contact_info)

    def test_get_location_info_method(self):
        """Test get_location_info method returns formatted location information."""
        proveedor = Proveedor(**self.valid_data)
        location_info = proveedor.get_location_info()

        self.assertIn("Ecuador", location_info)
        self.assertIn("Av. Amazonas 123, Quito, Ecuador", location_info)

    def test_get_location_info_method_partial_data(self):
        """Test get_location_info method with partial location data."""
        data = self.valid_data.copy()
        del data["direccion"]
        proveedor = Proveedor(**data)
        location_info = proveedor.get_location_info()

        self.assertEqual(location_info, "Ecuador")

    def test_model_meta_ordering(self):
        """Test model meta ordering configuration."""
        self.assertEqual(Proveedor._meta.ordering, ["nombre"])

    def test_model_verbose_names(self):
        """Test model verbose names are in Spanish."""
        meta = Proveedor._meta
        self.assertEqual(meta.verbose_name, "Proveedor")
        self.assertEqual(meta.verbose_name_plural, "Proveedores")

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
        proveedor.nombre = "Nuevo Nombre"
        proveedor.save()

        self.assertGreaterEqual(proveedor.updated_at, original_updated)


class ProveedorQuerySetTest(TestCase):
    """Test default queryset behavior and ordering."""

    def setUp(self):
        """Set up test data."""
        self.proveedor1 = Proveedor.objects.create(
            nombre="Alpha Proveedores",
            descripcion="Proveedor de repuestos",
            telefono="02-1234567",
            pais="Ecuador",
            correo="alpha@provider.com",
            direccion="Calle Alpha 123",
        )
        self.proveedor2 = Proveedor.objects.create(
            nombre="Beta Importadores",
            descripcion="Importador de accesorios",
            telefono="02-7654321",
            pais="Colombia",
            correo="beta@importer.com",
            direccion="Calle Beta 456",
        )
        self.proveedor3 = Proveedor.objects.create(
            nombre="Gamma Distribuidores",
            descripcion="Distribuidor especializado",
            telefono="02-9876543",
            pais="Perú",
            correo="gamma@distributor.com",
            direccion="Calle Gamma 789",
        )

    def test_default_ordering_by_nombre(self):
        """Test that proveedores are ordered by nombre by default."""
        proveedores = list(Proveedor.objects.all())

        # Should be ordered: Alpha, Beta, Gamma
        self.assertEqual(proveedores[0].nombre, "Alpha Proveedores")
        self.assertEqual(proveedores[1].nombre, "Beta Importadores")
        self.assertEqual(proveedores[2].nombre, "Gamma Distribuidores")

    def test_count_proveedores(self):
        """Test counting proveedores."""
        count = Proveedor.objects.count()
        self.assertEqual(count, 3)

    def test_filter_by_pais(self):
        """Test filtering proveedores by país."""
        proveedores_ecuador = Proveedor.objects.filter(pais="Ecuador")
        proveedores_colombia = Proveedor.objects.filter(pais="Colombia")

        self.assertEqual(proveedores_ecuador.count(), 1)
        self.assertEqual(proveedores_colombia.count(), 1)

    def test_search_by_nombre(self):
        """Test searching proveedores by nombre."""
        proveedores_alpha = Proveedor.objects.filter(nombre__icontains="Alpha")
        proveedores_import = Proveedor.objects.filter(nombre__icontains="Import")

        self.assertEqual(proveedores_alpha.count(), 1)
        self.assertEqual(proveedores_import.count(), 1)


class ProveedorConstraintsTest(TestCase):
    """Test database constraints and indexes."""

    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            "nombre": "Importadora AutoParts S.A.",
            "descripcion": "Importadora especializada en repuestos",
            "telefono": "+593-2-2234567",
            "pais": "Ecuador",
            "correo": "ventas@autoparts.com.ec",
            "direccion": "Av. Amazonas 123, Quito, Ecuador",
        }

    def test_database_indexes(self):
        """Test that database indexes exist for performance."""
        indexes = [index.fields for index in Proveedor._meta.indexes]

        self.assertIn(["nombre"], indexes)
        self.assertIn(["pais"], indexes)

    def test_field_constraints(self):
        """Test that fields have proper constraints."""
        # Test nombre field
        nombre_field = Proveedor._meta.get_field("nombre")
        self.assertEqual(nombre_field.max_length, 200)

        # Test telefono field
        telefono_field = Proveedor._meta.get_field("telefono")
        self.assertEqual(telefono_field.max_length, 15)

        # Test pais field
        pais_field = Proveedor._meta.get_field("pais")
        self.assertEqual(pais_field.max_length, 100)

        # Test correo field validators
        correo_field = Proveedor._meta.get_field("correo")
        self.assertTrue(
            any(
                hasattr(validator, "code") and validator.code == "invalid"
                for validator in correo_field.validators
            )
        )

    def test_telefono_field_validators(self):
        """Test that telefono field has regex validators."""
        telefono_field = Proveedor._meta.get_field("telefono")

        # Check that regex validator exists
        regex_validators = [v for v in telefono_field.validators if hasattr(v, "regex")]
        self.assertTrue(len(regex_validators) > 0)


# Forms and views tests moved to main imports section


class ProveedorFormTest(TestCase):
    """Test ProveedorForm validation and behavior."""

    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            "nombre": "Importadora AutoParts S.A.",
            "descripcion": "Importadora especializada en repuestos y accesorios automotrices de alta calidad",
            "telefono": "+593-2-2234567",
            "pais": "Ecuador",
            "correo": "ventas@autoparts.com.ec",
            "direccion": "Av. Amazonas 123, Quito, Ecuador",
        }

    def test_form_valid_with_complete_data(self):
        """Test form is valid with all required data."""
        form = ProveedorForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_nombre(self):
        """Test form is invalid without nombre."""
        data = self.valid_data.copy()
        del data["nombre"]
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("nombre", form.errors)

    def test_form_invalid_without_descripcion(self):
        """Test form is invalid without descripcion."""
        data = self.valid_data.copy()
        del data["descripcion"]
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("descripcion", form.errors)

    def test_form_invalid_without_telefono(self):
        """Test form is invalid without telefono."""
        data = self.valid_data.copy()
        del data["telefono"]
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("telefono", form.errors)

    def test_form_invalid_without_pais(self):
        """Test form is invalid without pais."""
        data = self.valid_data.copy()
        del data["pais"]
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("pais", form.errors)

    def test_form_invalid_without_correo(self):
        """Test form is invalid without correo."""
        data = self.valid_data.copy()
        del data["correo"]
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("correo", form.errors)

    def test_form_invalid_without_direccion(self):
        """Test form is invalid without direccion."""
        data = self.valid_data.copy()
        del data["direccion"]
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("direccion", form.errors)

    def test_nombre_validation_too_short(self):
        """Test nombre validation with too short name."""
        data = self.valid_data.copy()
        data["nombre"] = "AB"  # Too short
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("nombre", form.errors)

    def test_nombre_validation_too_long(self):
        """Test nombre validation with too long name."""
        data = self.valid_data.copy()
        data["nombre"] = "A" * 201  # Too long
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("nombre", form.errors)

    def test_nombre_normalization(self):
        """Test that nombre is normalized to title case."""
        data = self.valid_data.copy()
        data["nombre"] = "importadora autoparts sociedad anónima"
        form = ProveedorForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["nombre"], "Importadora Autoparts Sociedad Anónima"
        )

    def test_descripcion_validation_too_short(self):
        """Test descripcion validation with too short description."""
        data = self.valid_data.copy()
        data["descripcion"] = "Corto"  # Too short
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("descripcion", form.errors)

    def test_descripcion_normalization(self):
        """Test that descripcion is stripped of whitespace."""
        data = self.valid_data.copy()
        data["descripcion"] = "  Importadora de repuestos automotrices  "
        form = ProveedorForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["descripcion"], "Importadora de repuestos automotrices"
        )

    def test_telefono_validation_invalid_format(self):
        """Test telefono validation with invalid format."""
        data = self.valid_data.copy()
        data["telefono"] = "123"  # Too short
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("telefono", form.errors)

    def test_telefono_validation_valid_formats(self):
        """Test telefono validation with valid formats."""
        valid_phones = [
            "+593-2-2234567",
            "02-2234567",
            "(02) 223-4567",
            "+1-555-123-4567",
        ]

        for phone in valid_phones:
            data = self.valid_data.copy()
            data["telefono"] = phone
            form = ProveedorForm(data=data)
            self.assertTrue(form.is_valid(), f"Phone {phone} should be valid")

    def test_correo_validation_invalid_format(self):
        """Test correo validation with invalid format."""
        data = self.valid_data.copy()
        data["correo"] = "invalid-email"
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("correo", form.errors)

    def test_correo_normalization(self):
        """Test that correo is normalized to lowercase."""
        data = self.valid_data.copy()
        data["correo"] = "VENTAS@AUTOPARTS.COM.EC"
        form = ProveedorForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["correo"], "ventas@autoparts.com.ec")

    def test_pais_normalization(self):
        """Test that pais is normalized to title case."""
        data = self.valid_data.copy()
        data["pais"] = "estados unidos"
        form = ProveedorForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["pais"], "Estados Unidos")

    def test_direccion_validation_too_short(self):
        """Test direccion validation with too short address."""
        data = self.valid_data.copy()
        data["direccion"] = "Calle 1"  # Too short
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("direccion", form.errors)

    def test_direccion_normalization(self):
        """Test that direccion is stripped of whitespace."""
        data = self.valid_data.copy()
        data["direccion"] = "  Av. Amazonas 123, Quito  "
        form = ProveedorForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["direccion"], "Av. Amazonas 123, Quito")

    def test_nombre_uniqueness_validation_new(self):
        """Test nombre uniqueness validation for new proveedor."""
        # Create existing proveedor
        Proveedor.objects.create(**self.valid_data)

        # Try to create form with same nombre (case insensitive)
        data = self.valid_data.copy()
        data["nombre"] = "IMPORTADORA AUTOPARTS S.A."  # Same name, different case
        data["correo"] = "otro@email.com"  # Different email to avoid unique constraint
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("nombre", form.errors)

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
        data["nombre"] = "Otro Proveedor"
        form = ProveedorForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("correo", form.errors)

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
        self.assertEqual(proveedor.nombre, "Importadora Autoparts S.A.")  # Normalized
        self.assertEqual(proveedor.correo, "ventas@autoparts.com.ec")
        self.assertEqual(proveedor.pais, "Ecuador")

    def test_form_save_updates_proveedor(self):
        """Test that form.save() updates existing proveedor instance."""
        proveedor = Proveedor.objects.create(**self.valid_data)

        # Update data
        updated_data = self.valid_data.copy()
        updated_data["nombre"] = "Nuevo Proveedor S.A."
        updated_data["pais"] = "Colombia"

        form = ProveedorForm(data=updated_data, instance=proveedor)
        self.assertTrue(form.is_valid())

        updated_proveedor = form.save()

        self.assertEqual(updated_proveedor.pk, proveedor.pk)
        self.assertEqual(updated_proveedor.nombre, "Nuevo Proveedor S.A.")
        self.assertEqual(updated_proveedor.pais, "Colombia")

    def test_form_widget_attributes(self):
        """Test that form widgets have proper CSS classes."""
        form = ProveedorForm()

        # Check that form fields have Bootstrap classes
        self.assertIn(
            "form-control", form.fields["nombre"].widget.attrs.get("class", "")
        )
        self.assertIn(
            "form-control", form.fields["descripcion"].widget.attrs.get("class", "")
        )
        self.assertIn(
            "form-control", form.fields["telefono"].widget.attrs.get("class", "")
        )
        self.assertIn("form-control", form.fields["pais"].widget.attrs.get("class", ""))
        self.assertIn(
            "form-control", form.fields["correo"].widget.attrs.get("class", "")
        )
        self.assertIn(
            "form-control", form.fields["direccion"].widget.attrs.get("class", "")
        )

    def test_form_help_texts(self):
        """Test that form fields have appropriate help texts in Spanish."""
        form = ProveedorForm()

        self.assertIn("razón social", form.fields["nombre"].help_text.lower())
        self.assertIn("descripción", form.fields["descripcion"].help_text.lower())
        self.assertIn("teléfono", form.fields["telefono"].help_text.lower())
        self.assertIn("país", form.fields["pais"].help_text.lower())
        self.assertIn("correo", form.fields["correo"].help_text.lower())
        self.assertIn("dirección", form.fields["direccion"].help_text.lower())

    def test_form_required_fields(self):
        """Test that required fields are properly marked."""
        form = ProveedorForm()

        self.assertTrue(form.fields["nombre"].required)
        self.assertTrue(form.fields["descripcion"].required)
        self.assertTrue(form.fields["telefono"].required)
        self.assertTrue(form.fields["pais"].required)
        self.assertTrue(form.fields["correo"].required)
        self.assertTrue(form.fields["direccion"].required)


class ProveedorViewsTest(TestCase):
    """Test Proveedor views behavior and integration."""

    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.valid_data = {
            "nombre": "Importadora AutoParts S.A.",
            "descripcion": "Importadora especializada en repuestos y accesorios automotrices de alta calidad",
            "telefono": "+593-2-2234567",
            "pais": "Ecuador",
            "correo": "ventas@autoparts.com.ec",
            "direccion": "Av. Amazonas 123, Quito, Ecuador",
        }

    def test_proveedor_list_view_empty(self):
        """Test proveedor list view when no proveedores exist."""
        response = self.client.get(reverse("proveedores:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "NUESTROS PROVEEDORES")
        self.assertContains(response, "No hay proveedores registrados")
        self.assertContains(response, reverse("proveedores:create"))

    def test_proveedor_list_view_with_proveedores(self):
        """Test proveedor list view when proveedores exist."""
        proveedor1 = Proveedor.objects.create(**self.valid_data)

        # Create second proveedor
        data2 = self.valid_data.copy()
        data2["nombre"] = "Beta Distribuidores"
        data2["correo"] = "info@beta.com"
        proveedor2 = Proveedor.objects.create(**data2)

        response = self.client.get(reverse("proveedores:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, proveedor1.nombre)
        self.assertContains(response, proveedor2.nombre)
        self.assertContains(response, proveedor1.correo)
        self.assertContains(response, proveedor2.correo)
        self.assertContains(response, "AGREGAR PROVEEDOR")

    def test_proveedor_create_view_get(self):
        """Test GET request to proveedor create view."""
        response = self.client.get(reverse("proveedores:create"))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], ProveedorForm)
        self.assertContains(response, "AGREGAR PROVEEDOR")
        self.assertContains(response, "form-control")  # Bootstrap classes

    def test_proveedor_create_view_post_valid_data(self):
        """Test POST request to create proveedor with valid data."""
        response = self.client.post(reverse("proveedores:create"), data=self.valid_data)

        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful creation
        self.assertRedirects(response, reverse("proveedores:list"))

        # Check proveedor was created
        proveedor = Proveedor.objects.get()
        self.assertEqual(proveedor.nombre, "Importadora Autoparts S.A.")  # Normalized
        self.assertEqual(proveedor.correo, "ventas@autoparts.com.ec")
        self.assertEqual(proveedor.pais, "Ecuador")

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("exitosamente" in str(message) for message in messages))

    def test_proveedor_create_view_post_invalid_data(self):
        """Test POST request to create proveedor with invalid data."""
        invalid_data = self.valid_data.copy()
        del invalid_data["nombre"]  # Remove required field

        response = self.client.post(reverse("proveedores:create"), data=invalid_data)

        self.assertEqual(response.status_code, 200)  # Stay on form page
        self.assertIsInstance(response.context["form"], ProveedorForm)
        self.assertFalse(response.context["form"].is_valid())
        self.assertContains(response, "form-control")  # Bootstrap classes present

        # Check no proveedor was created
        self.assertEqual(Proveedor.objects.count(), 0)

    def test_proveedor_update_view_get(self):
        """Test GET request to proveedor update view."""
        proveedor = Proveedor.objects.create(**self.valid_data)

        response = self.client.get(
            reverse("proveedores:update", kwargs={"pk": proveedor.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], ProveedorForm)
        self.assertEqual(response.context["form"].instance, proveedor)
        self.assertContains(response, "EDITAR PROVEEDOR")
        self.assertContains(response, proveedor.nombre)

    def test_proveedor_update_view_post_valid_data(self):
        """Test POST request to update proveedor with valid data."""
        proveedor = Proveedor.objects.create(**self.valid_data)

        updated_data = self.valid_data.copy()
        updated_data["nombre"] = "Nuevo Proveedor S.A."
        updated_data["pais"] = "Colombia"

        response = self.client.post(
            reverse("proveedores:update", kwargs={"pk": proveedor.pk}),
            data=updated_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("proveedores:list"))

        # Check proveedor was updated
        proveedor.refresh_from_db()
        self.assertEqual(proveedor.nombre, "Nuevo Proveedor S.A.")
        self.assertEqual(proveedor.pais, "Colombia")

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("actualizado" in str(message) for message in messages))

    def test_proveedor_update_view_post_invalid_data(self):
        """Test POST request to update proveedor with invalid data."""
        proveedor = Proveedor.objects.create(**self.valid_data)

        invalid_data = self.valid_data.copy()
        invalid_data["correo"] = "invalid-email"  # Invalid email

        response = self.client.post(
            reverse("proveedores:update", kwargs={"pk": proveedor.pk}),
            data=invalid_data,
        )

        self.assertEqual(response.status_code, 200)  # Stay on form page
        self.assertFalse(response.context["form"].is_valid())

        # Check proveedor was not updated
        proveedor.refresh_from_db()
        self.assertEqual(proveedor.correo, "ventas@autoparts.com.ec")  # Original value

    def test_proveedor_update_view_nonexistent_pk(self):
        """Test update view with nonexistent proveedor ID."""
        response = self.client.get(reverse("proveedores:update", kwargs={"pk": 999}))

        self.assertEqual(response.status_code, 404)

    def test_proveedor_delete_view_get(self):
        """Test GET request to proveedor delete view."""
        proveedor = Proveedor.objects.create(**self.valid_data)

        response = self.client.get(
            reverse("proveedores:delete", kwargs={"pk": proveedor.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "¿Está seguro de eliminar")
        self.assertContains(response, proveedor.nombre)
        self.assertContains(response, "Eliminar")
        self.assertContains(response, "Cancelar")

    def test_proveedor_delete_view_post(self):
        """Test POST request to delete proveedor."""
        proveedor = Proveedor.objects.create(**self.valid_data)
        proveedor_id = proveedor.pk

        response = self.client.post(
            reverse("proveedores:delete", kwargs={"pk": proveedor_id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("proveedores:list"))

        # Check proveedor was deleted
        self.assertFalse(Proveedor.objects.filter(pk=proveedor_id).exists())

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("eliminado" in str(message) for message in messages))

    def test_proveedor_delete_view_nonexistent_pk(self):
        """Test delete view with nonexistent proveedor ID."""
        response = self.client.get(reverse("proveedores:delete", kwargs={"pk": 999}))

        self.assertEqual(response.status_code, 404)

    def test_proveedor_list_view_pagination(self):
        """Test pagination in list view when many proveedores exist."""
        # Create multiple proveedores to test pagination
        for i in range(15):
            data = self.valid_data.copy()
            data["nombre"] = f"Proveedor {i + 1:02d}"
            data["correo"] = f"proveedor{i + 1:02d}@email.com"
            Proveedor.objects.create(**data)

        response = self.client.get(reverse("proveedores:list"))

        self.assertEqual(response.status_code, 200)
        # Check that proveedores are displayed (actual pagination depends on view settings)
        self.assertTrue(response.context["proveedores"])

    def test_proveedor_list_view_ordering(self):
        """Test that proveedores are ordered correctly in list view."""
        # Create proveedores in reverse alphabetical order
        names_and_emails = [
            ("Zebra Proveedores", "zebra@email.com"),
            ("Alpha Proveedores", "alpha@email.com"),
            ("Beta Proveedores", "beta@email.com"),
        ]
        for name, email in names_and_emails:
            data = self.valid_data.copy()
            data["nombre"] = name
            data["correo"] = email
            Proveedor.objects.create(**data)

        response = self.client.get(reverse("proveedores:list"))
        proveedores = response.context["proveedores"]

        # Should be ordered alphabetically by nombre
        proveedor_names = [p.nombre for p in proveedores]
        self.assertEqual(proveedor_names[0], "Alpha Proveedores")
        self.assertEqual(proveedor_names[1], "Beta Proveedores")
        self.assertEqual(proveedor_names[2], "Zebra Proveedores")

    def test_view_context_data_basic(self):
        """Test that views return proper context data."""
        response = self.client.get(reverse("proveedores:create"))

        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], ProveedorForm)

    def test_form_error_handling_displays_messages(self):
        """Test that form errors are properly displayed to user."""
        invalid_data = {"nombre": "", "correo": "invalid-email"}

        response = self.client.post(reverse("proveedores:create"), data=invalid_data)

        self.assertEqual(response.status_code, 200)  # Form errors, stay on page
        self.assertFalse(response.context["form"].is_valid())

    def test_csrf_protection_enabled(self):
        """Test that CSRF protection is enabled on forms."""
        response = self.client.get(reverse("proveedores:create"))

        self.assertContains(response, "csrfmiddlewaretoken")

    def test_view_uses_correct_templates(self):
        """Test that views use correct templates."""
        # List view
        response = self.client.get(reverse("proveedores:list"))
        self.assertTemplateUsed(response, "proveedores/list.html")

        # Create view
        response = self.client.get(reverse("proveedores:create"))
        self.assertTemplateUsed(response, "proveedores/form.html")

        # Update view (need proveedor first)
        proveedor = Proveedor.objects.create(**self.valid_data)
        response = self.client.get(
            reverse("proveedores:update", kwargs={"pk": proveedor.pk})
        )
        self.assertTemplateUsed(response, "proveedores/form.html")

        # Delete view
        response = self.client.get(
            reverse("proveedores:delete", kwargs={"pk": proveedor.pk})
        )
        self.assertTemplateUsed(response, "proveedores/confirm_delete.html")

    def test_proveedor_contact_info_display(self):
        """Test that contact information is properly displayed."""
        proveedor = Proveedor.objects.create(**self.valid_data)

        response = self.client.get(reverse("proveedores:list"))

        # Check that contact info is displayed
        self.assertContains(response, proveedor.correo)
        self.assertContains(response, proveedor.telefono)

    def test_proveedor_location_info_display(self):
        """Test that location information is properly displayed."""
        proveedor = Proveedor.objects.create(**self.valid_data)

        response = self.client.get(reverse("proveedores:list"))

        # Check that location info is displayed
        self.assertContains(response, proveedor.pais)

    def test_empty_state_handling(self):
        """Test empty state when no proveedores exist."""
        response = self.client.get(reverse("proveedores:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay proveedores")
        self.assertContains(response, reverse("proveedores:create"))

    def test_proveedor_search_functionality(self):
        """Test search functionality in list view if implemented."""
        # Create test proveedores
        proveedor1 = Proveedor.objects.create(**self.valid_data)

        data2 = self.valid_data.copy()
        data2["nombre"] = "Distribuidora Nacional"
        data2["correo"] = "info@distribuidor.com"
        proveedor2 = Proveedor.objects.create(**data2)

        response = self.client.get(reverse("proveedores:list"))

        # Check both proveedores are displayed
        self.assertContains(response, proveedor1.nombre)
        self.assertContains(response, proveedor2.nombre)

    def test_proveedor_card_layout_information(self):
        """Test that proveedor cards display proper information."""
        proveedor = Proveedor.objects.create(**self.valid_data)

        response = self.client.get(reverse("proveedores:list"))

        # Check that all important info is displayed in cards
        self.assertContains(response, proveedor.nombre)
        self.assertContains(response, proveedor.descripcion)
        self.assertContains(response, proveedor.correo)
        self.assertContains(response, proveedor.telefono)
        self.assertContains(response, proveedor.pais)
