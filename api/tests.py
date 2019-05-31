from django.test import TestCase
from django.db.utils import IntegrityError

from api.models import Employee


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
