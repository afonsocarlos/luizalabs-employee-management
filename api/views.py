from rest_framework import viewsets

from api.models import Employee
from api.serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employees to be
    listed, added, editted, and removed.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        """
        This view should return a list of all the employees for the
        filtered by the fields specified in the request
        """
        employees = Employee.objects.all()

        name = self.request.query_params.get('name')
        email = self.request.query_params.get('email')
        department = self.request.query_params.get('department')
        gender = self.request.query_params.get('gender')
        birthdate = self.request.query_params.get('birthdate')
        birthdate_before = self.request.query_params.get('birthdate_before')
        birthdate_after = self.request.query_params.get('birthdate_after')
        hire_date = self.request.query_params.get('hire_date')
        hire_date_before = self.request.query_params.get('hire_date_before')
        hire_date_after = self.request.query_params.get('hire_date_after')

        if name is not None:
            employees = employees.filter(name__icontains=name)

        if email is not None:
            employees = employees.filter(email__icontains=email)

        if department is not None:
            employees = employees.filter(department__icontains=department)

        if gender is not None:
            employees = employees.filter(gender=gender)

        if birthdate is not None:
            employees = employees.filter(birthdate=birthdate)
        elif birthdate_before is not None:
            employees = employees.filter(birthdate__lt=birthdate_before)
        elif birthdate_after is not None:
            employees = employees.filter(birthdate__gt=birthdate_after)

        if hire_date is not None:
            employees = employees.filter(hire_date=hire_date)
        elif hire_date_before is not None:
            employees = employees.filter(hire_date__lt=hire_date_before)
        elif hire_date_after is not None:
            employees = employees.filter(hire_date__gt=hire_date_after)

        return employees
