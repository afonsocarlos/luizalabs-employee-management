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

        if name is not None:
            employees = employees.filter(name__icontains=name)

        if email is not None:
            employees = employees.filter(email__icontains=email)

        if department is not None:
            employees = employees.filter(department__icontains=department)

        return employees
