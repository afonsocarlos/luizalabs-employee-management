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
