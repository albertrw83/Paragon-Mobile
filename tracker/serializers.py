from rest_framework import serializers
from .models import Job, JobFolder, Type, Manufacturer, EquipmentFolder, Model, ModelFolder, Equipment, TestEquipment, CableTestData, \
    UserProperties, JobNotes, EquipmentNotes, EquipmentLink, TypeFolder, TypeTestStandards, TypeTestGuide, ModelTestGuide, JobSite, \
    JobSiteNotes, BusContactTestData, JobSiteFolder, Company, FeedbackFile, FeedbackNote, WorkingNote, TestSheet, TypeNotes, ModelNotes, Well, WellNotes, MaintEvent, MaintFile, MaintNotes, STATUS_PENDING
from django.contrib.auth.models import User


class TestEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestEquipment
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    mandatory_type_test_equipment =TestEquipmentSerializer(many=True, read_only=True)
    optional_type_test_equipment =TestEquipmentSerializer(many=True, read_only=True)
    class Meta:
        model = Type
        fields = '__all__'

class ModelSerializer(serializers.ModelSerializer):
    mandatory_model_test_equipment =TestEquipmentSerializer(many=True, read_only=True)
    optional_model_test_equipment =TestEquipmentSerializer(many=True, read_only=True)
    class Meta:
        model = Model
        fields = '__all__'

class EquipmentNotesSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField()    
    class Meta:
        model = EquipmentNotes
        fields = '__all__'

class EquipmentFilesSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField()
    class Meta:
        model = EquipmentFolder
        fields = '__all__'

class EquipmentLinkSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField()
    class Meta:
        model = EquipmentLink
        fields = '__all__'

class TestSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSheet
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    classification = serializers.ReadOnlyField()
    equipment_type = TypeSerializer(read_only=True)
    equipment_model = ModelSerializer(read_only=True)
    note_equipment = EquipmentNotesSerializer(many=True, read_only=True)
    equipment = EquipmentFilesSerializer(many=True, read_only=True)
    sheet_eq = TestSheetSerializer(read_only=True)
    mandatory_test_equipment = TestEquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'

class JobSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSite
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    test_equipment = TestEquipmentSerializer(many=True, read_only=True)
    job_site = JobSiteSerializer(read_only=True)
    class Meta:
        model = Job
        fields = '__all__'

