from rest_framework import serializers
from .models import Job, TestSheet, Equipment

   
class EquipmentSerializer(serializers.ModelSerializer):
    classification = serializers.ReadOnlyField()
    class Meta:
        model = Equipment
        fields = ['equipment_type', 'classification', 'site_id', 'job_site', 'parent_equipment', 'manual', 'scope', 'notes', 'completion', 'trashed', 'equipment_model', 'serial_number', 'equipment_location', 'equipment_mold', 'is_testing', 'mandatory_test_equipment', 'optional_test_equipment']
   
class JobSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    class Meta:
        model = Job
        fields = ['job_number', 'customer_name', 'job_name', 'equipment']
          
class TestSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSheet
        fields = ['eq_type', 'eq_model', 'eq', 'is_complete', 'date_tested', 'testers', 'date_manufactured', 'equipment_voltage', 'is_dc_equipment_voltage', 'system_voltage', 'interrupting_capacity', 'interrupting_voltage', 'humidity']