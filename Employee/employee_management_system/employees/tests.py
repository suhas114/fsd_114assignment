from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Employee


class EmployeeAccessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='tester', password='test-password'
        )
        self.employee = Employee.objects.create(
            name='Test Employee',
            email='employee@example.com',
            mobile_no='1234567890',
            designation='Tester',
            gender='M',
            course='Testing',
            image='',
        )

    def test_management_pages_require_login(self):
        protected_urls = [
            reverse('dashboard'),
            reverse('employee_list'),
            reverse('add_employee'),
            reverse('edit_employee', args=[self.employee.pk]),
            reverse('delete_employee', args=[self.employee.pk]),
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith('/login/?next='))

    def test_delete_is_not_allowed_with_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete_employee', args=[self.employee.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Employee.objects.filter(pk=self.employee.pk).exists())

    def test_authenticated_post_can_delete_employee(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_employee', args=[self.employee.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())

    def test_edit_updates_mobile_number(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('edit_employee', args=[self.employee.pk]),
            {
                'name': 'Updated Employee',
                'email': 'employee@example.com',
                'mobile_no': '9876543210',
                'designation': 'Developer',
                'gender': 'F',
                'course': 'Development',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.mobile_no, '9876543210')
        self.assertEqual(self.employee.name, 'Updated Employee')

    def test_logout_requires_post(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
