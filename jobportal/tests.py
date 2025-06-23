from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.datastructures import MultiValueDict

from .forms import RegistrationForm, ClientCreation, AdCreation, ResponseForm, PaymentForm
from .models import Advertisement, Client as ClientModel, BusinessType, Region, District, Position, Response, Contacts, \
    Client

User = get_user_model()


class RegistrationFormTests(TestCase):
    def test_valid_reg_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')

    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': '1234',
            'password2': '5678'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class ClientFormTests(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name='Středočeský kraj')
        self.district = District.objects.create(name='Praha 1', region_id=self.region)
        self.business_type = BusinessType.objects.create(name='Restaurace')

    def test_valid_client_form(self):
        form_data = {
            'business_name': 'GastroTest s.r.o.',
            'business_type': self.business_type.pk,
            'VAT_number': 'CZ12345678',
            'address': 'Hlavní 12',
            'city': 'Praha',
            'district': self.district.pk,
            'contact_email': 'info@gastro.cz',
            'contact_phone': '123456789'
        }
        form = ClientCreation(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_required(self):
        form_data = {
            'business_name': '',
            'business_type': '',
            'VAT_number': '',
            'address': '',
            'city': '',
            'district': '',
            'contact_email': 'invalid',
            'contact_phone': ''
        }
        form = ClientCreation(data=form_data)
        self.assertFalse(form.is_valid())


class AdCreationFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name='Číšník')

    def test_valid_ad_form(self):
        form_data = {
            'title': 'Hledáme číšníka',
            'text_content': 'Práce na HPP.',
            'position': self.position.pk,
            'salary': '35 000 Kč',
        }
        form = AdCreation(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_ad_form(self):
        form_data = {
            'title': '',
            'text_content': '',
            'position': '',
            'salary': ''
        }
        form = AdCreation(data=form_data)
        self.assertFalse(form.is_valid())


class ResponseFormTests(TestCase):
    def setUp(self):
        self.model_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        self.region = Region.objects.create(name='Test Region')
        self.district = District.objects.create(name='Test District', region_id=self.region)
        self.business_type = BusinessType.objects.create(name='Restaurace')
        self.client_model = ClientModel.objects.create(
            user=self.model_user,
            business_type=self.business_type,
            address='Ulice 1',
            city='Praha',
            district=self.district,
            business_name='Firma',
            VAT_number='CZ123',
            contact_email='firma@example.com',
            contact_phone='123456789'
        )
        self.position = Position.objects.create(name='Číšník')
        self.ad = Advertisement.objects.create(
            client=self.client_model,
            position=self.position,
            title='Nabídka práce',
            text_content='Popis nabídky',
            salary='N/A'
        )

    def test_valid_response(self):
        file = SimpleUploadedFile("cv.pdf", b"cv content", content_type="application/pdf")
        form_data = {
            'name': 'Jan Novák',
            'email': 'jan@example.com',
            'message': 'Mám zájem o tuto pozici.',
        }
        files = MultiValueDict({'cv': [file]})
        form = ResponseForm(data=form_data, files=files)
        self.assertTrue(form.is_valid())

        response = form.save(commit=False)
        response.advertisement = self.ad
        response.save()

        self.assertEqual(Response.objects.count(), 1)

    def test_invalid_email_and_cv(self):
        invalid_file = SimpleUploadedFile("malware.exe", b"bad content", content_type="application/x-msdownload")
        form_data = {
            'name': 'Jan Novák',
            'email': 'neplatny-email',
            'message': 'Zpráva'
        }
        files = MultiValueDict({'cv': [invalid_file]})
        form = ResponseForm(data=form_data, files=files)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('cv', form.errors)

class PaymentFormTests(TestCase):
    def test_valid_payment(self):
        form = PaymentForm(data={
            'card_number': '1234123412341234',
            'cardholder_name': 'Jan Novák',
            'expiry_date': '12/30',
            'cvv': '123'
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_payment(self):
        form = PaymentForm(data={
            'card_number': '123',
            'cardholder_name': '',
            'expiry_date': '99/99',
            'cvv': 'abc'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('card_number', form.errors)
        self.assertIn('cardholder_name', form.errors)
        self.assertIn('cvv', form.errors)


class ViewTests(TestCase):
    def setUp(self):
        self.business_type = BusinessType.objects.create(name='Restaurace')
        self.region = Region.objects.create(name='Praha')
        self.district = District.objects.create(name='Praha 1', region_id=self.region)

        self.user = User.objects.create_user(username='firmauser', password='testpass')

        self.client_model = ClientModel.objects.create(
            user=self.user,
            business_type=self.business_type,
            business_name='Firma',
            VAT_number='CZ123',
            address='Ulice 1',
            city='Praha',
            district=self.district,
            contact_email='firma@example.com',
            contact_phone='123456789'
            )

    def test_registration_view(self):
        response = self.client.post('/registration/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testheslo123',
            'password2': 'testheslo123',
            'business_name': 'Nová firma',
            'VAT_number': 'CZ999',
            'address': 'Ulice 9',
            'city': 'Brno',
            'district': self.district.pk,
            'business_type': self.business_type.pk,
            'contact_email': 'kontakt@nova.cz',
            'contact_phone': '123456789'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(ClientModel.objects.filter(business_name='Nová firma').exists())


class ModelsTestCase(TestCase):
    def setUp(self):
        self.business_type = BusinessType.objects.create(name="Restaurace")
        self.region = Region.objects.create(name="Praha")
        self.district = District.objects.create(name="Praha 1", region_id=self.region)
        self.position = Position.objects.create(name="Kuchař")
        self.user = (User.objects.create_user(username="user1", password="pass"))
        self.client = Client.objects.create(
            user=self.user,
            business_type=self.business_type,
            business_name="Firma",
            VAT_number="CZ123",
            address="Ulice 1",
            city="Praha",
            district=self.district,
            contact_email="firma@example.com",
            contact_phone="123456789"
        )
        self.ad = Advertisement.objects.create(
            position=self.position,
            title="Nabídka práce",
            text_content="Práce v restauraci",
            salary="30000 Kč",
            client=self.client,
            created_by=self.user
        )
        self.response = Response.objects.create(
            advertisement=self.ad,
            name="Jan Novák",
            email="jan@example.com",
            message="Mám zájem",
        )
        self.contact = Contacts.objects.create(
            name="Kontakt Osoba",
            role="Manager",
            email="kontakt@example.com",
            phone="987654321"
        )

    def test_str_and_repr(self):
        self.assertEqual(str(self.business_type), "Restaurace")
        self.assertEqual(repr(self.business_type), "Restaurace")

        self.assertEqual(str(self.region), "Praha")
        self.assertEqual(repr(self.region), "Praha")

        self.assertEqual(str(self.district), "Praha 1")
        self.assertEqual(repr(self.district), "Praha 1")

        self.assertEqual(str(self.position), "Kuchař")
        self.assertEqual(repr(self.position), "Kuchař")

        self.assertEqual(str(self.client), "Firma (Ulice 1)")
        self.assertEqual(repr(self.client), "Firma (Ulice 1)")

        self.assertEqual(str(self.ad), "Nabídka práce")
        self.assertEqual(repr(self.ad), "Nabídka práce")

        self.assertEqual(str(self.response), "Nabídka práce")
        self.assertEqual(repr(self.response), "Nabídka práce")

        self.assertEqual(str(self.contact), "Kontakt Osoba")
        self.assertEqual(repr(self.contact), "Kontakt Osoba")

    def test_advertisement_publish(self):
        self.assertFalse(self.ad.published)
        self.assertIsNone(self.ad.published_date)

        self.ad.publish()

        self.assertTrue(self.ad.published)
        self.assertIsNotNone(self.ad.published_date)
        self.assertTrue(self.ad.published_date <= timezone.now())


class ClientViewIntegrationTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name='Test Region')
        self.district = District.objects.create(name='Test District', region_id=self.region)
        self.business_type = BusinessType.objects.create(name='Test Business')

    def test_create_client_via_view(self):
        response = self.client.post(reverse('registration'), data={
            'business_name': 'Test Firma',
            'business_type': self.business_type.pk,
            'VAT_number': 'CZ123456',
            'address': 'Test Address',
            'city': 'Test City',
            'district': self.district.pk,
            'contact_email': 'test@example.com',
            'contact_phone': '123456789',
            'username': 'testuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'email': 'testuser@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Client.objects.filter(business_name='Test Firma').exists())