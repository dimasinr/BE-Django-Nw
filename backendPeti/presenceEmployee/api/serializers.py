from rest_framework import serializers
from presenceEmployee.models import PresenceEmployee
from userapp.serializer import UserDetailsSerializer

class PresenceEmployeeSerializers(serializers.ModelSerializer):
    employee = UserDetailsSerializer(read_only=True)

    class Meta:
        model = PresenceEmployee
        fields = ['id', 'employee', 'working_date', 'start_from', 'end_from','working_hour',
                  'lembur_start', 'lembur_end','lembur_hour', 'years', 'months', 'days', 'ket', 'is_lock']
        index_together = [
            ('employee', 'working_date'),
            ('working_date', 'start_from'),
            ('working_date', 'end_from'),
            ('working_date', 'lembur_start'),
            ('working_date', 'lembur_end'),
            ('employee', 'working_date', 'working_hour_total'),
        ]

class PresenceEmployeeAnalisisSerializers(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()

    def get_employee(self, obj):
        return obj.employee.name

    class Meta:
        model = PresenceEmployee
        fields = ['id', 'employee', 'working_date', 'start_from', 'end_from','working_hour',
                  'lembur_start', 'lembur_end','lembur_hour', 'years', 'months', 'days', 'ket', 'is_lock']
        index_together = [
            ('employee', 'working_date'),
            ('working_date', 'start_from'),
            ('working_date', 'end_from'),
            ('working_date', 'lembur_start'),
            ('working_date', 'lembur_end'),
            ('employee', 'working_date', 'working_hour_total'),
        ]