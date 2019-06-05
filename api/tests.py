from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.utils import IntegrityError
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.models import Employee
from api.serializers import EmployeeSerializer


UserModel = get_user_model()


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


class BaseAPITest(APITestCase):
    """Base class responsible for setting up necessary config."""

    def setUp(self):
        """
        Set up necessary objects for testing this class.
        """
        super().setUp()

        # create test user for authentication
        self.test_user = UserModel.objects.create_user(
            'test_user', 'test@luizalabs.com', 'test123456'
        )

    def _request_token_authentication(self, user, password):
        token_request_data = {
            'username': user,
            'password': password,
        }
        response = self.client.post(
            reverse('api-token-auth'),
            data=token_request_data
        )
        return response


class JWTAuthenticationTests(BaseAPITest):
    """Test class for API authentication access functionality."""

    def test_authentication_with_wrong_credentials(self):
        """Authentication response should deny login request."""
        response = self._request_token_authentication('test_user', 'WRONG_PASS')
        self.assertEqual(response.status_code, 400)

    def test_authentication_with_right_credentials(self):
        """Authentication response should allow login request."""
        response = self._request_token_authentication('test_user', 'test123456')
        self.assertEqual(response.status_code, 200)

        content = response.json()
        self.assertTrue('token' in content)

    def test_access_without_authentication(self):
        """
        All routes except the authentication ones should
        return "Not Allowed" or "Not authenticated" message,
        blocking the user to access data.
        """
        response = self.client.get(reverse('employee-list'))
        content = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            content['detail'], 'Authentication credentials were not provided.'
        )

    def test_access_with_wrong_authentication(self):
        """
        All routes except the authentication ones should
        return "Not Allowed" or "Not authenticated" message,
        blocking the user to access data.
        """
        auth = 'JWT'

        response = self.client.get(
            reverse('employee-list'), HTTP_AUTHORIZATION=auth
        )
        content = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            content['detail'], 'Invalid Authorization header. No credentials provided.'
        )

    def test_access_with_right_authentication(self):
        """
        API should allow route access and return
        expected results from requests.
        """
        response = self._request_token_authentication('test_user', 'test123456')
        content = response.json()
        auth = 'JWT {}'.format(content['token'])

        response = self.client.get(
            reverse('employee-list'), HTTP_AUTHORIZATION=auth
        )
        content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', content)
        self.assertIn('results', content)



class EmployeeAPIViewTests(BaseAPITest):
    """Test class for EmployeeView class."""

    def setUp(self):
        """
        Set up necessary objects for testing this class.
        """
        super().setUp()

        response = self._request_token_authentication('test_user', 'test123456')
        content = response.json()
        self.auth_token = 'JWT {}'.format(content['token'])

        Employee.objects.bulk_create([
            Employee(name='John Doe',
                     email='john.doe@luizalabs.com',
                     department='Development',
                     gender='M'),
            Employee(name='Jane Doe',
                     email='jane.doe@luizalabs.com',
                     department='Marketing',
                     gender='F'),
            Employee(name='Richard Roe',
                     email='richard.roe@luizalabs.com',
                     department='Sales',
                     gender='M'),
        ])

    def test_employee_basic_request(self):
        """
        employee_basic_request returns True if Employee response
        retrieves all employees.
        """
        response = self.client.get(reverse('employee-list'), HTTP_AUTHORIZATION=self.auth_token)
        self.assertEqual(200, response.status_code)

        employees = Employee.objects.all()
        employees_serialized_data = {
            'count': employees.count(),
            'next': None,
            'previous': None,
        }
        employees_serialized_data['results'] = EmployeeSerializer(instance=employees, many=True).data

        response_data = response.json()
        self.assertEqual(employees_serialized_data, response_data)

    def test_employee_name_filter(self):
        """
        employee_name_filter returns True if Employee response
        retrieves only employees whose names contain query string case insensitive.
        """
        response = self.client.get(reverse('employee-list'), data={'name': 'doe'}, HTTP_AUTHORIZATION=self.auth_token)
        self.assertEqual(200, response.status_code)

        employees = Employee.objects.filter(name__contains='Doe')
        employees_serialized_data = {
            'count': employees.count(),
            'next': None,
            'previous': None,
        }
        employees_serialized_data['results'] = EmployeeSerializer(instance=employees, many=True).data

        response_data = response.json()
        self.assertEqual(employees_serialized_data, response_data)

    def test_employee_email_filter(self):
        """
        employee_email_filter returns True if Employee response
        retrieves only employees whose emails contain query string case insensitive.
        """
        response = self.client.get(reverse('employee-list') , data={'email': 'LUIZALABS.COM'}, HTTP_AUTHORIZATION=self.auth_token)
        self.assertEqual(200, response.status_code)

        employees = Employee.objects.filter(email__contains='luizalabs.com')
        employees_serialized_data = {
            'count': employees.count(),
            'next': None,
            'previous': None,
        }
        employees_serialized_data['results'] = EmployeeSerializer(instance=employees, many=True).data

        response_data = response.json()
        self.assertEqual(employees_serialized_data, response_data)

    def test_employee_department_filter(self):
        """
        employee_department_filter returns True if Employee response
        retrieves only employees whose departments contain query string case insensitive.
        """
        response = self.client.get(reverse('employee-list') , data={'department': 'dev'}, HTTP_AUTHORIZATION=self.auth_token)
        self.assertEqual(200, response.status_code)

        employees = Employee.objects.filter(department__contains='Dev')
        employees_serialized_data = {
            'count': employees.count(),
            'next': None,
            'previous': None,
        }
        employees_serialized_data['results'] = EmployeeSerializer(instance=employees, many=True).data

        response_data = response.json()
        self.assertEqual(employees_serialized_data, response_data)

    def test_employee_gender_filter(self):
        """
        employee_gender_filter returns True if Employee response
        retrieves only employees whose genders contain query string case sensitive.
        """
        response = self.client.get(reverse('employee-list') , data={'gender': 'F'}, HTTP_AUTHORIZATION=self.auth_token)
        self.assertEqual(200, response.status_code)

        employees = Employee.objects.filter(gender='F')
        employees_serialized_data = {
            'count': employees.count(),
            'next': None,
            'previous': None,
        }
        employees_serialized_data['results'] = EmployeeSerializer(instance=employees, many=True).data

        response_data = response.json()
        self.assertEqual(employees_serialized_data, response_data)
