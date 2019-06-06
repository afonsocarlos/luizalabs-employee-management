from rest_framework import serializers

from api.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """EmployeeSerializer serializes Employee model. """

    class Meta:
        model = Employee
        fields = ('id', 'name', 'email', 'department', 'gender', 'birthdate', 'hire_date')

