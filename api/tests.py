from django.test import TestCase
from django.db.utils import IntegrityError
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import Employee
from api.serializers import EmployeeSerializer


class EmployeeModelTests(TestCase):
    """Test class for Employee model."""

    def test_employee_unique_email(self):
        """
        employee_unique_email must raise an IntegrityError
        if employees' email aren't unique.
        """
        Employee.objects.create(name='John Doe',
                                email='test@luizalabs.com',
                                department='Development')
        with self.assertRaises(IntegrityError):
            Employee.objects.create(name='Jane Doe',
                                    email='test@luizalabs.com',
                                    department='Marketing')

    def test_employee_ordering(self):
        """
        employee_ordering returns True if employees are
        sorted alphabetically by default.
        """
        Employee.objects.create(name='John Doe',
                                email='john.doe@luizalabs.com',
                                department='Development')
        Employee.objects.create(name='Jane Doe',
                                email='jane.doe@luizalabs.com',
                                department='Marketing')
        Employee.objects.create(name='Richard Roe',
                                email='richard.roe@luizalabs.com',
                                department='Sales')

        names = sorted(['John Doe', 'Jane Doe', 'Richard Roe'])
        self.assertEqual(list(Employee.objects.values_list('name', flat=True)), names)


class EmployeeAPIViewTests(APITestCase):
    """Test class for EmployeeView class."""

    def setUp(self):
        """
        Set up necessary objects for testing this class.
        """
        super().setUp()

        Employee.objects.bulk_create([
            Employee(name='John Doe',
                     email='john.doe@luizalabs.com',
                     department='Development'),
            Employee(name='Jane Doe',
                     email='jane.doe@luizalabs.com',
                     department='Marketing'),
            Employee(name='Richard Roe',
                     email='richard.roe@luizalabs.com',
                     department='Sales'),
        ])

    def test_employee_basic_request(self):
        """
        employee_basic_request returns True if Employee response
        retrieves all employees.
        """
        response = self.client.get(reverse('employee-list'))
        self.assertEqual(200, response.status_code)

        employees_serialized_data = EmployeeSerializer(instance=Employee.objects.all(), many=True).data

        response_data = response.json()
        self.assertEqual(employees_serialized_data, response_data)
