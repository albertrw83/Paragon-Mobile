from django.db import models
from django.contrib.auth.models import User
from collections import Counter
from django.forms import ChoiceField
from django.utils import timezone
from datetime import date
from decimal import *
import os
from django.db.models import Count
from django.db.models import Q
import urllib.parse


#define company properties


def upload_company_jsa_path(instance, filename):
    path= "companies/"+instance.name+"_"+str(instance.pk)+"/jsa"
    return path
    
def upload_company_time_sheet(instance, filename):
    path= "companies/"+instance.name+"_"+str(instance.pk)+"/time_sheet"
    return path

class Company(models.Model):
    company_key = models.CharField(max_length=64, null=True, blank=True)
    name= models.CharField(max_length=128)
    job_safety_analysis = models.FileField(max_length=500, null=True, blank=True, upload_to = upload_company_jsa_path) 
    time_sheet = models.FileField(max_length=500, null=True, blank=True, upload_to = upload_company_time_sheet) 
    
    def __str__(self):
        return f"{self.name}"

STATUS_PENDING = 'pending'
STATUS_APPROVED = 'approved'
STATUS_REJECTED = 'rejected'
STATUS_LIST = [
    (STATUS_PENDING, "Pending"),
    (STATUS_APPROVED, "Approved"),
    (STATUS_REJECTED, "Rejected")
]

#define test equipment
class TestEquipment(models.Model):
    name = models.CharField(max_length=64, unique=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class TypeManager(models.Manager):
    def create_type(self, name):
        type = self.create(name=name)
        # do something with the book
        return type

def upload_type_te_path(instance, filename):
    path= "types/"+instance.name+"_"+str(instance.pk)+"/test_sheet"
    return path
def upload_type_tg_path(instance, filename):
    path= "types/"+instance.name+"_"+str(instance.pk)+"/test_guide"
    return path
def upload_type_neta_path(instance, filename):
    path= "types/"+instance.name+"_"+str(instance.pk)+"/teststandards/neta"
    return path
def upload_type_ansi_path(instance, filename):
    path= "types/"+instance.name+"_"+str(instance.pk)+"/teststandards/ansi"
    return path
    
class Type(models.Model):
    name = models.CharField(max_length=256)
    type_folder = models.URLField(null = True, blank = True) #Need to ensure all items are in url format first
    mandatory_type_test_equipment = models.ManyToManyField(TestEquipment, blank=True, related_name="mandatory_type_test_equipment")
    optional_type_test_equipment = models.ManyToManyField(TestEquipment, blank=True, related_name="optional_type_test_equipment")
    type_notes = models.TextField(null=True, blank=True) #notes that will apply to all equipment of this type
    test_sheet = models.FileField(max_length=500, null=True, blank=True, upload_to = upload_type_te_path) 
    type_test_guide = models.FileField(max_length=500, null=True, blank=True, upload_to = upload_type_tg_path)
    neta_standards = models.FileField(max_length=500, null=True, blank=True, upload_to = upload_type_neta_path)
    ansi_standards = models.FileField(max_length=500, null=True, blank=True, upload_to = upload_type_ansi_path)
    ts_page_quantity = models.IntegerField(null=True, blank=True, default=1)
    quote_default = models.FloatField(null=True, blank=True)#this will override the type value
    is_private = models.BooleanField(default=False)
    is_test_sheet = models.BooleanField(default=False)
    is_insulation_resistance=models.BooleanField(default=False)
    is_lv_ic_or_mc_breaker=models.BooleanField(default=False)
    is_mv_or_hv_breaker=models.BooleanField(default=False)
    is_contact_resistance=models.BooleanField(default=False)
    is_trip_unit=models.BooleanField(default=False)
    is_primary_injection=models.BooleanField(default=False)
    is_secondary_injection=models.BooleanField(default=False)
    is_power_fused=models.BooleanField(default=False)
    is_breaker=models.BooleanField(default=False)
    is_hipot=models.BooleanField(default=False)
    is_inspection=models.BooleanField(default=False)
    is_transformer=models.BooleanField(default=False)
    is_winding_resistance=models.BooleanField(default=False)
    is_liquid_type=models.BooleanField(default=False)
    is_cable=models.BooleanField(default=False)
    is_switchgear=models.BooleanField(default=False)
    is_cable_vlf_withstand_test=models.BooleanField(default=False)
    is_ttr=models.BooleanField(default=False)
    is_xfmr_insulation_resistance=models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_LIST, null=True, blank=True, max_length=16)
    is_bus_resistance=models.BooleanField(default=False)
    # @property
    # def is_(self):
    #     if self.hierarchy_level:
    #         return f'{20 * self.hierarchy_level}px'


    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="eq_type_company")
    objects = TypeManager()

    def __str__(self):
        return f"{self.name}"

def type_folder_path(instance, filename):
    try:
        eq_type=instance.eq_type
        path= "types/"+eq_type.name +"_"+str(eq_type.pk)+"/type_folder/"+filename
        return path
    except Job.MultipleObjectsReturned:
        return False

def type_ts_path(instance, filename):
    try:
        ts_type=instance.ts_type
        path= "types/"+ts_type.name +"_"+str(ts_type.pk)+"/type_ts/"+filename
        return path
    except Job.MultipleObjectsReturned:
        return False

class TypeNotes(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='type_notes')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='modify_type_notes')
    note = models.TextField(null=True, blank=True)
    eq_type = models.ForeignKey(Type, null=True, on_delete=models.CASCADE, blank=True, related_name="note_model")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_note = models.ForeignKey('self', on_delete=models.CASCADE, related_name="sub_notes", null=True)
    is_private = models.BooleanField(default=False)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="company_type_note")

    @property
    def hierarchy_level(self):
        return get_hierarchy_level(self)

    @property
    def margin(self):
        if self.hierarchy_level:
            return f'{20 * self.hierarchy_level}px'

    @property
    def sub_note_ids(self):
        sub_note_ids = get_note_ids(self)
        sub_note_ids = [str(i) for i in sub_note_ids]
        return '-'.join(sub_note_ids)

    @property
    def author_name(self):
        user = self.author
        if user:
            return f'{user.first_name} {user.last_name}'
        return 'Anonymous'


class TypeFolder(models.Model):
    type_file=models.FileField(max_length=500, null=True, blank = True, upload_to = type_folder_path)
    file_name = models.CharField(max_length=256, null=True, blank=True)
    file_url=models.URLField(max_length=500, null=True, blank=True)
    eq_type = models.ForeignKey(Type, null=True, on_delete=models.CASCADE, blank=True, related_name="eq_type")
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="company_type_file")    
    @property
    def hostname(self):
        return urllib.parse.urlparse(self.file_url).hostname
    def filename(self):
        return os.path.basename(self.type_file.name)

class TypeTestStandards(models.Model):
    ts_file=models.FileField(max_length=500, null=True, blank = True, upload_to = type_ts_path)
    ts_standard = models.CharField(max_length=256, null=True, blank=True)
    ts_name = models.CharField(max_length=256, null=True, blank=True)
    ts_description = models.TextField(null=True, blank=True)
    ts_url=models.URLField(max_length=500, null=True, blank=True)
    ts_type = models.ForeignKey(Type, null=True, on_delete=models.CASCADE, blank=True, related_name="eq_type_standards")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('UserProperties', on_delete=models.CASCADE, null=True, blank=True, related_name="user_test_standard")
    is_private = models.BooleanField(default=False)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="company_ts")

    def filename(self):
        return os.path.basename(self.ts_file.name)

def type_testguide_path(instance, filename):
    try:
        eq_type=instance.eq_type
        path= "types/"+eq_type.name +"_"+str(eq_type.pk)+"/type_testguides/"+filename
        return path
    except Job.MultipleObjectsReturned:
        return False
        
class TypeTestGuide(models.Model):
    type_test_guide=models.FileField(max_length=1000, null=True, blank=True, upload_to = type_testguide_path)
    eq_type=models.ForeignKey(Type, null=True, on_delete=models.CASCADE, blank=True, related_name="type_test")
    title = models.TextField(null = True, blank = True)
    definition = models.TextField(null = True, blank = True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="company_type_video")
    def filename(self):
        return os.path.basename(self.type_test_guide.name)

class ManufacturerManager(models.Manager):
    def create_manufacturer(self, name):
        manufacturer = self.create(name=name)
        
        return manufacturer

class Manufacturer(models.Model):
    name = models.CharField(max_length=64, unique=True)
    customer_support = models.TextField(null = True, blank=True)

    objects = ManufacturerManager()
    def __str__(self):
        return f"{self.name}"

class ModelManager(models.Manager):
    def create_model(self, name):
        model = self.create(name=name)
        return model

def upload_model_te_path(instance, filename):
    path= "models/"+instance.name+"_"+str(instance.pk)+"/test_sheet"
    return path
def upload_model_tg_path(instance, filename):
    path= "models/"+instance.name+"_"+str(instance.pk)+"/test_guide"
    return path

class Model(models.Model):
    name = models.CharField(max_length=128, blank=False)
    model_id = models.CharField(max_length=128, blank=True) #A model number, id, or any other designation for this piece of equipment
    model_test_sheet = models.FileField(max_length=500, null=True, blank=True, upload_to = upload_model_te_path)
    mandatory_model_test_equipment =  models.ManyToManyField(TestEquipment, blank=True, related_name="mandatory_model_test_equipment")
    optional_model_test_equipment =  models.ManyToManyField(TestEquipment, blank=True, related_name="optional_model_test_equipment")
    model_folder = models.URLField(max_length=300, null=True, blank=True)
    model_test_guide = models.FileField(max_length=500, null=True, blank=True, upload_to = upload_model_tg_path)
    model_notes = models.TextField(null=True, blank=True)
    model_customer_support = models.TextField(null = True, blank = True)
    model_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="model_type", null=True, blank=True)
    model_manufacturer =  models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="model_manufacturer", null=True, blank=True)
    model_manual = models.FileField(max_length=500, null=True, blank=True)
    quote_default = models.FloatField(null=True, blank=True)#this will override the type value
    is_private = models.BooleanField(default=False)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="model_company")
    status = models.CharField(choices=STATUS_LIST, null=True, blank=True, max_length=16)
    objects = ModelManager()
    def __str__(self):
        return f"{self.name}"

class ModelNotes(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='model_notes')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='modify_model_notes')
    note = models.TextField(null=True, blank=True)
    model = models.ForeignKey(Model, null=True, on_delete=models.CASCADE, blank=True, related_name="note_model")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_note = models.ForeignKey('self', on_delete=models.CASCADE, related_name="sub_notes", null=True)
    is_private = models.BooleanField(default=False)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="company_model_note")

    @property
    def hierarchy_level(self):
        return get_hierarchy_level(self)

    @property
    def margin(self):
        if self.hierarchy_level:
            return f'{20 * self.hierarchy_level}px'

    @property
    def sub_note_ids(self):
        sub_note_ids = get_note_ids(self)
        sub_note_ids = [str(i) for i in sub_note_ids]
        return '-'.join(sub_note_ids)

    @property
    def author_name(self):
        user = self.author
        if user:
            return f'{user.first_name} {user.last_name}'
        return 'Anonymous'
    
def model_folder_path(instance, filename):
    try:
        model=instance.model
        path= "models/"+model.name +"_"+str(model.pk)+"/model_folder/"+filename
        return path
    except Job.MultipleObjectsReturned:
        return False

class ModelFolder(models.Model):
    model_file=models.FileField(max_length=500, null=True, blank = True, upload_to = model_folder_path)
    file_url=models.URLField(max_length=500, null=True, blank=True)
    file_name = models.CharField(max_length=256, null=True, blank=True)
    model = models.ForeignKey(Model, null=True, on_delete=models.CASCADE, blank=True, related_name="model")
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="company_model_file")

    @property
    def hostname(self):
        return urllib.parse.urlparse(self.file_url).hostname

    def filename(self):
        return os.path.basename(self.model_file.name)

def model_testguide_path(instance, filename):
    try:
        model=instance.model
        path= "models/"+model.name +"_"+str(model.pk)+"/model_testguides/"+filename
        return path
    except Job.MultipleObjectsReturned:
        return False
class ModelTestGuide(models.Model):
    model_test_guide=models.FileField(max_length=1000, null=True, blank=True, upload_to = model_testguide_path)
    model=models.ForeignKey(Model, null=True, on_delete=models.CASCADE, blank=True, related_name="model_test")
    title = models.TextField(null = True, blank = True)
    definition = models.TextField(null = True, blank = True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="company_model_video")
    def filename(self):
        return os.path.basename(self.model_test_guide.name)

class EquipmentManager(models.Manager):
    def create_equipment(self, site_id):
        equipment = self.create(site_id=site_id)
        # do something with the book
        return equipment


def upload_test_results_path(instance, filename):
    
    # import pdb; pdb.set_trace()

    eq_job=Job.objects.get(equipment = instance.pk)
    job_path=eq_job.job_name+"_"+str(eq_job.pk)
    path= "jobs/" + job_path+"/"+"equipment/"+instance.site_id+"_"+str(instance.pk)+"/test_results/"+filename
    return path

def upload_eq_testsheet_template_path(instance, filename):
    
    # import pdb; pdb.set_trace()
    eq_job=Job.objects.get(equipment = instance.pk)
    job_path=eq_job.job_name+"_"+str(eq_job.pk)
    path= "jobs/" + job_path+"/"+"equipment/"+instance.site_id+"_"+str(instance.pk)+"/testsheet_template/"+filename
    return path

def upload_nameplate_path(instance, filename):
    
    # import pdb; pdb.set_trace()
    eq_job = Job.objects.filter(equipment = instance.pk).first()
    eq_site = instance.job_site
    if eq_job:
        job_path=eq_job.job_name+"_"+str(eq_job.pk)
        path= "jobs/" + job_path+"/"+"equipment/"+instance.site_id+"_"+str(instance.pk)+"/nameplate/"+filename
    elif eq_site:
        site_path=eq_site.name+"_"+str(eq_site.pk)
        path= "jobsites/" + site_path+"/"+"equipment/"+instance.site_id+"_"+str(instance.pk)+"/nameplate/"+filename
    else:
        return False
    return path

# class EquipmentFiles(models.Model):
#     eq_file = models.FileField(max_length=500, null=True, blank = True, upload_to = upload_test_results_path)

class Equipment(models.Model):
    
    def save(self, *args, **kwargs):
        self.change_key += 1
        job = self.equipments.first()
        job.save()
        super().save(*args, **kwargs)  # Call the "real" save() method.
    change_key = models.IntegerField(null=True, blank=True, default=0)
    equipment_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="type", null=True, blank=True)
    site_id = models.TextField(max_length=1000)
    job_site = models.ForeignKey('JobSite', on_delete=models.CASCADE, related_name="equipment_jobsite", null=True, blank=True)
    parent_equipment = models.ForeignKey('self', on_delete=models.CASCADE, related_name="sub_equipments", null=True, blank=True)
    manual = models.TextField(max_length=64, null = True, blank = True) # needs to link to them manual
    scope = models.TextField(default = 'refer to overall job scope (default)') #scope for this specific piece of equipment
    notes = models.TextField(null=True, blank=True)
    completion = models.BooleanField(default=False)
    test_sheet_template = models.FileField(max_length=500, null=True, blank = True, upload_to = upload_eq_testsheet_template_path)
    test_results = models.FileField(max_length=500, null=True, blank = True, upload_to = upload_test_results_path)
    # test_results = models.ManyToManyField(EquipmentFiles, )
    nameplate = models.FileField(max_length=1000, null=True, blank = True, upload_to = upload_nameplate_path)
    trashed = models.BooleanField(default=False)
    equipment_model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="equipment_model", null=True, blank=True)
    serial_number = models.CharField(max_length=256, null=True, blank=True)
    equipment_location = models.TextField(null = True, blank = True)
    equipment_mold = models.ForeignKey('self', on_delete=models.CASCADE, related_name="casting", null=True, blank=True)
    is_testing = models.BooleanField(default=True)

    #define test equipment requirements.
    mandatory_test_equipment =  models.ManyToManyField(TestEquipment, blank=True, related_name="mandatory_test_equipment")
    optional_test_equipment =  models.ManyToManyField(TestEquipment, blank=True, related_name="optional_test_equipment")
    is_insulation_resistance=models.BooleanField(default=False)
    is_contact_resistance=models.BooleanField(default=False)
    is_trip_unit=models.BooleanField(default=False)
    is_primary_injection=models.BooleanField(default=False)
    is_secondary_injection=models.BooleanField(default=False)
    is_power_fused=models.BooleanField(default=False)
    is_breaker=models.BooleanField(default=False)
    is_hipot=models.BooleanField(default=False)
    is_inspection=models.BooleanField(default=False)
    is_transformer=models.BooleanField(default=False)
    is_winding_resistance=models.BooleanField(default=False)
    is_liquid_type=models.BooleanField(default=False)
    is_cable=models.BooleanField(default=False)
    is_switchgear=models.BooleanField(default=False)
    is_cable_vlf_withstand_test=models.BooleanField(default=False)
    is_ttr=models.BooleanField(default=False)
    is_xfmr_insulation_resistance=models.BooleanField(default=False)
    is_winding_resistance=models.BooleanField(default=False)

    objects = EquipmentManager()

    def __str__(self):
        return f"{self.site_id}"
    @property
    def site_id_data(self):
        if self.equipment_mold:
            return self.equipment_mold.site_id
        else:
            return self.site_id
    @property
    def classification(self):
        man = self.equipment_model.model_manufacturer.name
        mod = self.equipment_model.name
        typ = self.equipment_model.model_type.name
        return man+' '+mod+' '+typ

    @property
    def equipment_type_data(self):
        if self.equipment_mold:
            return self.equipment_mold.equipment_type
        else:
            return self.equipment_type
    @property
    def parent_equipment_data(self):
        if self.equipment_mold:
            return self.equipment_mold.parent_equipment
        else:
            return self.parent_equipment
    @property
    def equipment_type_data(self):
        if self.equipment_mold:
            return self.equipment_mold.equipment_type
        else:
            return self.equipment_type
    @property
    def manual_data(self):
        if self.manual:
            return self.equipment_mold.manual
        else:
            return self.manual
    @property
    def nameplate_data(self):
        if self.equipment_mold:
            return self.equipment_mold.nameplate
        else:
            return self.nameplate
    @property
    def equipment_model_data(self):
        if self.equipment_mold:
            return self.equipment_mold.equipment_model
        else:
            return self.equipment_model
    @property
    def serial_number_data(self):
        if self.equipment_mold:
            return self.equipment_mold.serial_number
        else:
            return self.serial_number
    @property
    def equipment_location_data(self):
        if self.equipment_mold:
            return self.equipment_mold.equipment_location
        else:
            return self.equipment_location
    @property
    def is_trip_unit_data(self):
        if self.equipment_mold:
            return self.equipment_mold.is_trip_unit
        else:
            return self.is_trip_unit
    @property
    def is_power_fused_data(self):
        if self.equipment_mold:
            return self.equipment_mold.is_power_fused
        else:
            return self.is_power_fused
    @property
    def is_breaker_data(self):
        if self.equipment_mold:
            return self.equipment_mold.is_breaker
        else:
            return self.is_breaker
    @property
    def is_transformer_data(self):
        if self.equipment_mold:
            return self.equipment_mold.is_transformer
        else:
            return self.is_transformer
    @property
    def is_liquid_type_data(self):
        if self.equipment_mold:
            return self.equipment_mold.is_liquid_type
        else:
            return self.is_liquid_type
    @property
    def is_cable_data(self):
        if self.equipment_mold:
            return self.equipment_mold.is_cable
        else:
            return self.is_cable
            
    @property
    def is_switchgear_data(self):
        if self.equipment_mold:
            return self.equipment_mold.is_switchgear
        else:
            return self.is_switchgear
            
    @property
    def is_site_equipment(self):
        return self.job_site != None
    
    @property
    def main_parent_equipment(self):
        return get_main_parent(self)

    @property
    def sub_equipment_ids(self):
        return get_sub_equipment_ids(self)

    @property
    def sub_equipments_trashed_count(self):
        return self.sub_equipments.filter(trashed=True).count()

    @property
    def sub_equipments_untrashed_count(self):
        return self.sub_equipments.filter(trashed=False).count()

    @property
    def eq_level(self):
        return get_eq_level(self)

    @property
    def margin(self):
        if self.eq_level:
            return f'{20 * self.eq_level}px'
    @property
    def untrashed_subs(self):
        if self.sub_equipments.filter(trashed=False).exists():
            return True
        else:
            return False
    @property
    def descendants(self):
        desc_ids = []
        subs = get_sub_equipment_ids(self)
    @property
    def lineage(self):
        return get_lineage(self)
    # @property
    # def is_addable(self):
    #     if self.
def get_eq_level(eq, level=0):
    parent_eq = eq.parent_equipment
    if parent_eq:
        level = get_eq_level(parent_eq, level+1)
    return level


# def flatten(eq, list=[]):
#     desc_ids = []
#     if eq.sub_equipments:
#         for sub_eq in eq.sub_equipments:
#             desc_ids.append(sub_eq.pk)
#             get_desc_ids(sub_eq)
#     if desc_ids:
#         return desc_ids
#     else:
#         return False
        
def get_lineage(equipment):
    lineage = []
    if equipment.parent_equipment:        
        lineage.extend([equipment.parent_equipment])
        lineage.extend(get_lineage(equipment.parent_equipment))
    return lineage

def get_sub_equipment_ids(equipment):
    sub_ids = []
    sub_equipment_ids = list(equipment.sub_equipments.values_list('id', flat=True))
    sub_ids.extend(sub_equipment_ids)
    for sub_id in sub_equipment_ids:
        sub_equipment = Equipment.objects.get(id=sub_id)
        if sub_equipment.sub_equipments.exists():
            sub_ids.extend(get_sub_equipment_ids(sub_equipment))
    return sub_ids


def get_main_parent(equipment):
    if not equipment.parent_equipment:
        return equipment
    return get_main_parent(equipment.parent_equipment)


def equipment_folder_path(instance, filename):
    try:
        equipment=instance.equipment
        job=Job.objects.get(equipment=equipment)
        
        job_path=job.job_name+"_"+str(job.pk)
        path= "jobs/"+job_path+"/equipment/"+equipment.site_id +"_"+str(equipment.pk)+"/equipment_folder/"+filename
        return path
    except Job.MultipleObjectsReturned:
        return False

class EquipmentFolder(models.Model):
    equipment_file=models.FileField(max_length=500, null=True, blank = True, upload_to = equipment_folder_path)
    file_name = models.CharField(max_length=256, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, null=True, on_delete=models.CASCADE, blank=True, related_name="equipment")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='author_eq_file')
    def extension(self):
        name, extension = os.path.splitext(self.equipment_file.name)
        return extension
    def filename(self):
        return os.path.basename(self.equipment_file.name)
    @property
    def author_name(self):
        user = self.author
        if user:
            return f'{user.first_name} {user.last_name}'
        return 'Anonymous'

class EquipmentLink(models.Model):
    link_name = models.CharField(max_length=256, null=True, blank=True)
    link_url=models.URLField(max_length=500, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, null=True, on_delete=models.CASCADE, blank=True, related_name="equipment_link")
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="company_eq_link")    
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='author_eq_link')
    @property
    def hostname(self):
        return urllib.parse.urlparse(self.link_url).hostname
    @property
    def author_name(self):
        user = self.author
        if user:
            return f'{user.first_name} {user.last_name}'
        return 'Anonymous'

class EquipmentNotes(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='equipment_notes')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='modify_equipment_notes')
    note = models.TextField(null=True, blank=True)
    equipment = models.ForeignKey(Equipment, null=True, on_delete=models.CASCADE, blank=True, related_name="note_equipment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_note = models.ForeignKey('self', on_delete=models.CASCADE, related_name="sub_notes", null=True)

    @property
    def truncated(self):
        return (self.note[:26] + '..') if len(self.note) > 28 else (self.note+"\"")

    @property
    def hierarchy_level(self):
        return get_hierarchy_level(self)

    @property
    def margin(self):
        if self.hierarchy_level:
            return f'{20 * self.hierarchy_level}px'

    @property
    def sub_note_ids(self):
        sub_note_ids = get_note_ids(self)
        sub_note_ids = [str(i) for i in sub_note_ids]
        return '-'.join(sub_note_ids)

    @property
    def author_name(self):
        user = self.author
        if user:
            return f'{user.first_name} {user.last_name}'
        return 'Anonymous'

#this section defines test sheet models
def calculate_ttr_error(tap, expected_ttr):
    try:
        ttr = Decimal(expected_ttr)
    except:
        return "---"
    try:
        error = (tap - ttr) / ttr
        return error * 100
    except Exception as e:
        return "---"


class TestSheet(models.Model):
    eq_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="sheet_type", null=True, blank=True)
    eq_model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="sheet_model", null=True, blank=True)
    eq = models.OneToOneField(Equipment, on_delete=models.CASCADE, related_name="sheet_eq", null=True, blank=True)
    #all test sheets
    is_complete = models.BooleanField(default=False)
    date_tested =  models.DateField(auto_now_add=False, null=True, blank=True)
    @property
    def date_tested_formatted(self):
        if self.date_tested:
            return self.date_tested.strftime( "%Y""-""%m""-" "%d")
        else:
            return ""
    testers = models.CharField(max_length=256, null=True, blank=True)
    date_manufactured = models.DateField(auto_now_add=False, null=True, blank=True)
    @property
    def date_manufactured_formatted(self):
        if self.date_manufactured:
            return self.date_manufactured.strftime( "%Y""-""%m""-" "%d")
        else:
            return ""
    equipment_voltage = models.DecimalField(max_digits=25, decimal_places=5, null=True, blank=True)
    is_dc_equipment_voltage=models.BooleanField(default=False)
    system_voltage = models.DecimalField(max_digits=25, decimal_places=5, null=True, blank=True)
    is_dc_system_voltage = models.BooleanField(default=False)
    interrupting_capacity = models.DecimalField(max_digits=25, decimal_places=5, null=True, blank=True)
    interrupting_voltage = models.DecimalField(max_digits=25, decimal_places=5, null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    operating_voltage= models.DecimalField(max_digits=15, decimal_places=7, null=True, blank=True)
    is_dc_operating_voltage=models.BooleanField(default=False)
    #inspection
    inspect_clean=models.BooleanField(default=False)
    inspect_insulation=models.BooleanField(default=False)
    inspect_cubicle=models.BooleanField(default=False)
    inspect_racking=models.BooleanField(default=False)
    inspect_contacts=models.BooleanField(default=False)
    inspect_ground_connections=models.BooleanField(default=False)
    inspect_open_close=models.BooleanField(default=False)
   
    #all breakers
    control_voltage = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    is_dc_control_voltage=models.BooleanField(default=False)
    trip_coil_voltage = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    is_dc_trip_voltage=models.BooleanField(default=False)
    insulation_resistance_ph_to_ph_test_voltage = models.IntegerField(null=True, blank=True)
    insulation_resistance_ph_to_ph_a_b = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    insulation_resistance_ph_to_ph_a_b_units = models.CharField(max_length=64, null=True, blank=True)    
    insulation_resistance_ph_to_ph_b_c = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    insulation_resistance_ph_to_ph_b_c_units = models.CharField(max_length=64, null=True, blank=True)    
    insulation_resistance_ph_to_ph_c_a = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    insulation_resistance_ph_to_ph_c_a_units = models.CharField(max_length=64, null=True, blank=True)        
    insulation_resistance_ln_to_ld_test_voltage =models.IntegerField(null=True, blank=True)
    insulation_resistance_ln_to_ld_a =models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    insulation_resistance_ln_to_ld_a_units = models.CharField(max_length=64, null=True, blank=True)    
    insulation_resistance_ln_to_ld_b =models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    insulation_resistance_ln_to_ld_b_units = models.CharField(max_length=64, null=True, blank=True)    
    insulation_resistance_ln_to_ld_c =models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    insulation_resistance_ln_to_ld_c_units = models.CharField(max_length=64, null=True, blank=True)    
    insulation_resistance_ph_to_gr_test_voltage= models.IntegerField(null=True, blank=True)
    insulation_resistance_ph_to_gr_a_g = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    insulation_resistance_ph_to_gr_a_g_units = models.CharField(max_length=64, null=True, blank=True)
    insulation_resistance_ph_to_gr_b_g = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    insulation_resistance_ph_to_gr_b_g_units = models.CharField(max_length=64, null=True, blank=True)
    insulation_resistance_ph_to_gr_c_g = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    insulation_resistance_ph_to_gr_c_g_units = models.CharField(max_length=64, null=True, blank=True)
    contact_resistance_current = models.IntegerField(null=True, blank=True)     
    contact_resistance_a = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    contact_resistance_a_units = models.CharField(max_length=64, null=True, blank=True)     
    contact_resistance_b = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    contact_resistance_b_units = models.CharField(max_length=64, null=True, blank=True)     
    contact_resistance_c = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    contact_resistance_c_units = models.CharField(max_length=64, null=True, blank=True)     
    fuse_resistance_a = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 
    fuse_resistance_b = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 
    fuse_resistance_c = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 
    fuse_resistance_a_units = models.CharField(max_length=64, null=True, blank=True)
    fuse_resistance_b_units = models.CharField(max_length=64, null=True, blank=True)
    fuse_resistance_c_units = models.CharField(max_length=64, null=True, blank=True)

    control_wiring_insulation_resistance = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 

    #power fuses
    fuse_manufacturer=models.CharField(max_length=128, null=True, blank=True)
    fuse_type=models.CharField(max_length=128, null=True, blank=True)
    fuse_size=models.IntegerField(null=True, blank=True)

    #secondary fuses
    fuse_resistance_secondary_a = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 
    fuse_resistance_secondary_b = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 
    fuse_resistance_secondary_c = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 
    fuse_resistance_secondary_a_units = models.CharField(max_length=64, null=True, blank=True)    
    fuse_resistance_secondary_b_units = models.CharField(max_length=64, null=True, blank=True)
    fuse_resistance_secondary_c_units = models.CharField(max_length=64, null=True, blank=True)
    
    #lv mcb specific fields
    frame_size = models.IntegerField(null=True, blank=True)
    mount_style = models.CharField(max_length=128, null=True, blank=True)
    trip_unit_model = models.TextField(null=True, blank=True)
    trip_unit_manufacturer =models.CharField(max_length=128, null=True, blank=True)
    trip_unit_serial_number =models.CharField(max_length=128, null=True, blank=True)
    trip_unit_rating_plug =models.IntegerField(null=True, blank=True)
    trip_unit_curve =models.TextField(null=True, blank=True)
    trip_unit_phase_ct_high = models.IntegerField(null=True, blank=True)
    trip_unit_phase_ct_low = models.IntegerField(null=True, blank=True)

    settings_af_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_af_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_af_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_af_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_af_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_af_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_af_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_al_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_al_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_al_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_al_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_al_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_al_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    settings_al_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)

    is_primary_injection= models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_setting_ltpu =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_setting_ltd =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_setting_stpu =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_setting_std =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_setting_inst =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_setting_gfpu =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_setting_gfd =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_testamps_ltd =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_testamps_std =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_testamps_inst =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_testamps_gfd =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_xpu_ltd =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_xpu_std =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_xpu_inst =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pi_xpu_gfd =  models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_af_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_af_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_af_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_af_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_af_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_af_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_af_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_al_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_al_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_al_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_al_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_al_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_al_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    a_al_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_af_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_af_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_af_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_af_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_af_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_af_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_af_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_al_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_al_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_al_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_al_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_al_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_al_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    b_al_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_af_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_af_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_af_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_af_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_af_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_af_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_af_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_al_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_al_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_al_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_al_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_al_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_al_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    c_al_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_af_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_af_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_af_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_af_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_af_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_af_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_af_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_al_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_al_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_al_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_al_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_al_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_al_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    min_al_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_af_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_af_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_af_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_af_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_af_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_af_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_af_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_al_ltpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_al_ltd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_al_stpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_al_std = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_al_inst = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_al_gfpu = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    max_al_gfd = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    si_pu_a=models.IntegerField(null=True, blank=True)
    si_pu_b=models.IntegerField(null=True, blank=True)
    si_pu_c=models.IntegerField(null=True, blank=True)
    si_lt_current_a=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    si_lt_current_b=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    si_lt_current_c=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    si_lt_d_a=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    si_lt_d_b=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    si_lt_d_c=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 
    si_st_current_a=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 
    si_st_current_b=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 
    si_st_current_c=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)     
    si_st_d_a=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    si_st_d_b=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    si_st_d_c=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    si_inst_current_a=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 
    si_inst_current_b=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True) 
    si_inst_current_c=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    
    #mv breaker specific fields
    protection_device = models.CharField(max_length=256, null=True, blank=True)
    trip_device = models.TextField(null=True, blank=True) 
    operations_counter_af=models.IntegerField(null=True, blank=True)
    operations_counter_al=models.IntegerField(null=True, blank=True)
    heaters_operational =models.BooleanField(default=True)

    hipot_test_voltage = models.IntegerField(null=True, blank=True)
    hipot_ptp_ab=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    hipot_ptp_bc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    hipot_ptp_ca=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    hipot_ltl_a=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    hipot_ltl_b=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    hipot_ltl_c=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    hipot_ptg_a=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    hipot_ptg_b=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    hipot_ptg_c=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    
    insulation_condition = models.CharField(max_length=64, null=True, blank=True)
    mechanical_condition = models.CharField(max_length=64, null=True, blank=True)
    cubicle_condition = models.CharField(max_length=64, null=True, blank=True)
    shutter_condition = models.CharField(max_length=64, null=True, blank=True)
    racking_condition = models.CharField(max_length=64, null=True, blank=True)
    finger_condition = models.CharField(max_length=64, null=True, blank=True)
    vacuum_bottle_condition = models.CharField(max_length=64, null=True, blank=True)

    #all xfmr
    power_rating = models.IntegerField(null=True, blank=True) #store in VA output kVA or mVA depending out number of decimals
    power_rating_units = models.CharField(max_length=64, null=True, blank=True)
    primary_winding_config = models.CharField(max_length=64, null=True, blank=True)
    secondary_winding_config = models.CharField(max_length=64, null=True, blank=True)
    # insulation_type = models.CharField(max_length=64, null=True, blank=True)
    primary_voltage=models.IntegerField(null=True, blank=True)
    secondary_voltage=models.IntegerField(null=True, blank=True)
    temp_rise=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    temp_rise_units=models.CharField(max_length=64, null=True, blank=True)
    impedance=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    impedance_at=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    xfmr_class=models.CharField(max_length=256, null=True, blank=True)
    ambient_temp=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    ambient_temp_units=models.CharField(max_length=64, null=True, blank=True)
    tap_qty=models.IntegerField(null=True, blank=True, default=5)
    tap_position=models.IntegerField(null=True, blank=True)
    #winding resistance test
    wr_h1_h2=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    wr_h2_h3=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    wr_h3_h1=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    wr_x0_x1=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    wr_x0_x2=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    wr_x0_x3=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    #insulation resistance
    insulation_resistance_hi_g=models.DecimalField(max_digits=25, decimal_places=5, null=True, blank=True)
    insulation_resistance_hi_lo=models.DecimalField(max_digits=25, decimal_places=5, null=True, blank=True)
    insulation_resistance_lo_g=models.DecimalField(max_digits=25, decimal_places=5, null=True, blank=True)
    insulation_resistance_hi_g_test_voltage=models.IntegerField(null=True, blank=True)
    insulation_resistance_hi_lo_test_voltage=models.IntegerField(null=True, blank=True)
    insulation_resistance_lo_g_test_voltage=models.IntegerField(null=True, blank=True)
    insulation_resistance_hi_g_units=models.CharField(max_length=64, null=True, blank=True)
    insulation_resistance_hi_lo_units=models.CharField(max_length=64, null=True, blank=True)
    insulation_resistance_lo_g_units=models.CharField(max_length=64, null=True, blank=True)
        #hv-lv
        #hv-n(or g)
        #lv-n(or g)
    #polarization index
    
    #switchgear booleans
    switchgear_nameplate_drawings = models.BooleanField(default=False)
    switchgear_inspect_cords_connectors = models.BooleanField(default=False)
    switchgear_anchorage_alignment = models.BooleanField(default=False)
    switchgear_clean = models.BooleanField(default=False)
    switchgear_fuse_cb_match_drawings = models.BooleanField(default=False)
    switchgear_ct_vt_ratios_match_drawings = models.BooleanField(default=False)
    switchgear_wiring_tight_secure = models.BooleanField(default=False)
    switchgear_connection_inspection = models.BooleanField(default=False)
    switchgear_op_sequence_correct = models.BooleanField(default=False)
    switchgear_moving_parts_lubricated = models.BooleanField(default=False)
    switchgear_insulators_no_damage = models.BooleanField(default=False)
    switchgear_barrier_installation_correct = models.BooleanField(default=False)
    switchgear_active_components_exercised = models.BooleanField(default=False)
    switchgear_indicating_devices = models.BooleanField(default=False)
    switchgear_filters_vents_clear = models.BooleanField(default=False)
    switchgear_instrument_transformers_inspected = models.BooleanField(default=False)
    switchgear_surge_arresters_inspected = models.BooleanField(default=False)
    switchgear_cpts_undamaged = models.BooleanField(default=False)
    switchgear_space_heaters = models.BooleanField(default=False)
    switchgear_phasing_verified = models.BooleanField(default=False)
    cpt_secondary_wiring_drawings = models.BooleanField(default=False)
    v_i_t_secondary_wiring_drawings = models.BooleanField(default=False)
    v_i_t_secondary_voltage_design = models.BooleanField(default=False)
    v_i_t_inspect_cords_connectors = models.BooleanField(default=False)
    v_i_t_nameplate_drawings = models.BooleanField(default=False)
    v_i_t_physical_mechanical_condition = models.BooleanField(default=False)
    v_i_t_correct_connection = models.BooleanField(default=False)
    v_i_t_clearances_primary_secondary = models.BooleanField(default=False)
    v_i_t_clean = models.BooleanField(default=False)
    v_i_t_connection_inspection = models.BooleanField(default=False)
    v_i_t_grounding_contact = models.BooleanField(default=False)
    v_i_t_fuze_sizes = models.BooleanField(default=False)
    v_i_t_lubrication = models.BooleanField(default=False)
    v_i_t_as_left = models.BooleanField(default=False)

    #ttr ratio test. Use a for loop for each in tap_qty
    tap_one_volts=models.IntegerField(null=True, blank=True)
    tap_one_ratio=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    ttr_upper_tolerance=models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    ttr_lower_tolerance=models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)

    #cable test properties
    # source_point = models.CharField(max_length=256, null=True, blank=True)
    # end_point = models.CharField(max_length=256, null=True, blank=True)
    # system_voltage=models.IntegerField(null=True, blank=True)
    # volt

    @property
    def tap_one_expected_ttr(self):
        try:
            ratio = Decimal(self.tap_one_volts*1000)//(self.secondary_voltage)
            return ratio/1000
        except:
            return ""    
    tap_one_h12_x02_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_one_h12_x02_ttr_error(self):
        return calculate_ttr_error(self.tap_one_h12_x02_ttr, self.tap_one_expected_ttr)
    tap_one_h23_x03_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_one_h23_x03_ttr_error(self):
        return calculate_ttr_error(self.tap_one_h23_x03_ttr, self.tap_one_expected_ttr)
    tap_one_h31_x01_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_one_h31_x01_ttr_error(self):
        return calculate_ttr_error(self.tap_one_h31_x01_ttr, self.tap_one_expected_ttr)
    tap_two_volts=models.IntegerField(null=True, blank=True)
    tap_two_ratio=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_two_expected_ttr(self):
        try:
            ratio = (self.tap_two_volts*1000)//(self.secondary_voltage)
            return ratio/1000
        except:
            return "--"
    tap_two_h12_x02_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_two_h12_x02_ttr_error(self):
        return calculate_ttr_error(self.tap_two_h12_x02_ttr, self.tap_two_expected_ttr)
    tap_two_h23_x03_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_two_h23_x03_ttr_error(self):
        return calculate_ttr_error(self.tap_two_h23_x03_ttr, self.tap_two_expected_ttr)
    tap_two_h31_x01_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_two_h31_x01_ttr_error(self):
        return calculate_ttr_error(self.tap_two_h31_x01_ttr, self.tap_two_expected_ttr)
    tap_three_volts=models.IntegerField(null=True, blank=True)
    tap_three_ratio=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_three_expected_ttr(self):
        try:
            ratio = (self.tap_three_volts*1000)//(self.secondary_voltage)
            return ratio/1000
        except:
            return ""
    tap_three_h12_x02_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_three_h12_x02_ttr_error(self):
        return calculate_ttr_error(self.tap_three_h12_x02_ttr, self.tap_three_expected_ttr)
    tap_three_h23_x03_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_three_h23_x03_ttr_error(self):
        return calculate_ttr_error(self.tap_three_h23_x03_ttr, self.tap_three_expected_ttr)
    tap_three_h31_x01_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_three_h31_x01_ttr_error(self):
        return calculate_ttr_error(self.tap_three_h31_x01_ttr, self.tap_three_expected_ttr)
    tap_four_volts=models.IntegerField(null=True, blank=True)
    tap_four_ratio=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_four_expected_ttr(self):
        try:
            ratio = (self.tap_four_volts*1000)//(self.secondary_voltage)
            return ratio/1000
        except:
            return ""
    tap_four_h12_x02_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_four_h12_x02_ttr_error(self):
        return calculate_ttr_error(self.tap_four_h12_x02_ttr, self.tap_four_expected_ttr)
    tap_four_h23_x03_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_four_h23_x03_ttr_error(self):
        return calculate_ttr_error(self.tap_four_h23_x03_ttr, self.tap_four_expected_ttr)
    tap_four_h31_x01_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_four_h31_x01_ttr_error(self):
        return calculate_ttr_error(self.tap_four_h31_x01_ttr, self.tap_four_expected_ttr)
    tap_five_volts=models.IntegerField(null=True, blank=True)
    tap_five_ratio=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_five_expected_ttr(self):
        try:
            ratio = (self.tap_five_volts*1000)//(self.secondary_voltage)
            return ratio/1000
        except:
            return ""
    tap_five_h12_x02_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_five_h12_x02_ttr_error(self):
        return calculate_ttr_error(self.tap_five_h12_x02_ttr, self.tap_five_expected_ttr)
    tap_five_h23_x03_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_five_h23_x03_ttr_error(self):
        return calculate_ttr_error(self.tap_five_h23_x03_ttr, self.tap_five_expected_ttr)
    tap_five_h31_x01_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_five_h31_x01_ttr_error(self):
        return calculate_ttr_error(self.tap_five_h31_x01_ttr, self.tap_five_expected_ttr)
    tap_six_volts=models.IntegerField(null=True, blank=True)
    tap_six_ratio=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_six_expected_ttr(self):
        try:
            ratio = (self.tap_six_volts*1000)//(self.secondary_voltage)
            return ratio/1000
        except:
            return ""
    tap_six_h12_x02_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_six_h12_x02_ttr_error(self):
        return calculate_ttr_error(self.tap_six_h12_x02_ttr, self.tap_six_expected_ttr)
    tap_six_h23_x03_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_six_h23_x03_ttr_error(self):
        return calculate_ttr_error(self.tap_six_h23_x03_ttr, self.tap_six_expected_ttr)
    tap_six_h31_x01_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_six_h31_x01_ttr_error(self):
        return calculate_ttr_error(self.tap_six_h31_x01_ttr, self.tap_six_expected_ttr)
    tap_seven_volts=models.IntegerField(null=True, blank=True)
    tap_seven_ratio=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_seven_expected_ttr(self):
        try:
            ratio = (self.tap_seven_volts*1000)//(self.secondary_voltage)
            return ratio/1000
        except:
            return ""
    tap_seven_h12_x02_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_seven_h12_x02_ttr_error(self):
        return calculate_ttr_error(self.tap_seven_h12_x02_ttr, self.tap_seven_expected_ttr)
    tap_seven_h23_x03_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_seven_h23_x03_ttr_error(self):
        return calculate_ttr_error(self.tap_seven_h23_x03_ttr, self.tap_seven_expected_ttr)
    tap_seven_h31_x01_ttr=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    @property
    def tap_seven_h31_x01_ttr_error(self):
        return calculate_ttr_error(self.tap_seven_h31_x01_ttr, self.tap_seven_expected_ttr)


    #mv oil-filled xfmrs
    is_oil_sample_required=models.BooleanField(default=True)
    tap_af = models.IntegerField(null=True, blank=True)
    tap_al = models.IntegerField(null=True, blank=True)
    fluid_type =  models.TextField(null=True, blank=True) 
    fluid_capacity = models.TextField(null=True, blank=True) 
    fluid_capacity_units = models.CharField(max_length=64, null=True, blank=True)
    liquid_level = models.TextField(null=True, blank=True) 
    liquid_temp = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    liquid_temp_units = models.CharField(max_length=64, null=True, blank=True)
    winding_temp = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    winding_temp_units = models.CharField(max_length=64, null=True, blank=True)
    pressure = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    pressure_units = models.CharField(max_length=64, null=True, blank=True)
    weight = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    weight_units = models.CharField(max_length=64, null=True, blank=True)
    

    #cables
    cable_voltage_rating = models.DecimalField(max_digits=15, decimal_places=7, null=True, blank=True)
    operating_cable_voltage= models.DecimalField(max_digits=15, decimal_places=7, null=True, blank=True)
    cable_amp_rating= models.IntegerField(null=True, blank=True)
    cable_length= models.IntegerField(null=True, blank=True)
    cable_length_units = models.CharField(max_length=64, null=True, blank=True)
    cable_insulation_type= models.CharField(max_length=64, null=True, blank=True)
    cable_insulation_thickness = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    cable_insulation_thickness_units = models.CharField(max_length=64, null=True, blank=True)
    cable_insulation_material= models.CharField(max_length=64, null=True, blank=True)
    cable_insulation_rating =models.IntegerField(null=True, blank=True)
    cable_size = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    cable_size_units = models.CharField(max_length=64, null=True, blank=True)
    cable_conductor_material= models.CharField(max_length=64, null=True, blank=True)
    is_cable_shielded= models.BooleanField(default=True)
    cable_starting_point= models.CharField(max_length=64, null=True, blank=True)
    cable_ending_point= models.CharField(max_length=64, null=True, blank=True)
    cable_starting_termination_type= models.CharField(max_length=64, null=True, blank=True)
    cable_ending_termination_type= models.CharField(max_length=64, null=True, blank=True)
    
    #cable inspection
    is_cable_data_specs_match = models.BooleanField(default=False)
    is_no_physical_damage = models.BooleanField(default=False)
    is_connection_verification = models.BooleanField(default=False)
    is_compression_match = models.BooleanField(default=False)
    is_shield_supports_terminations = models.BooleanField(default=False)
    is_bend_radius = models.BooleanField(default=False)
    is_fireproofing = models.BooleanField(default=False)
    is_window_ct_correct = models.BooleanField(default=False)
    is_id_arrangments_correct = models.BooleanField(default=False)
    is_cable_jacket_insulation_ok = models.BooleanField(default=False)

    shield_continuity_a = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    shield_continuity_b = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    shield_continuity_c = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)

    #cable testing VLF
    is_cable_vlf_withstand_test=models.BooleanField(default=True)
    is_cable_dc_test = models.BooleanField(default=True)
    max_test_voltage = models.IntegerField(null=True, blank=True)
    voltage_step_size = models.IntegerField(null=True, blank=True)
    cable_hipot_quantity = models.IntegerField(null=True, blank=True)
    duration_per_step = models.IntegerField(null=True, blank=True)
    cable_withstand_time= models.IntegerField(null=True, blank=True)
    cable_withstand_units = models.CharField(max_length=64, null=True, blank=True)

    cable_test_voltage=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    test_frequency=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    one_min_cable_test=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    one_min_cable_test_resistance_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    one_min_cable_test_current_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    one_min_cable_test_resistance_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    one_min_cable_test_current_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    one_min_cable_test_resistance_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    one_min_cable_test_current_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    five_min_cable_test=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    five_min_cable_test_resistance_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    five_min_cable_test_current_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    five_min_cable_test_resistance_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    five_min_cable_test_current_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    five_min_cable_test_resistance_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    five_min_cable_test_current_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    ten_min_cable_test=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    ten_min_cable_test_resistance_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    ten_min_cable_test_current_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    ten_min_cable_test_resistance_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    ten_min_cable_test_current_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    ten_min_cable_test_resistance_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    ten_min_cable_test_current_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fifteen_min_cable_test=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fifteen_min_cable_test_resistance_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fifteen_min_cable_test_current_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fifteen_min_cable_test_resistance_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fifteen_min_cable_test_current_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fifteen_min_cable_test_resistance_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fifteen_min_cable_test_current_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twenty_min_cable_test=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twenty_min_cable_test_resistance_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twenty_min_cable_test_current_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twenty_min_cable_test_resistance_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twenty_min_cable_test_current_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twenty_min_cable_test_resistance_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twenty_min_cable_test_current_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twentyfive_min_cable_test=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twentyfive_min_cable_test_resistance_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twentyfive_min_cable_test_current_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twentyfive_min_cable_test_resistance_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twentyfive_min_cable_test_current_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twentyfive_min_cable_test_resistance_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    twentyfive_min_cable_test_current_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    thirty_min_cable_test=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    thirty_min_cable_test_resistance_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    thirty_min_cable_test_current_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    thirty_min_cable_test_resistance_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    thirty_min_cable_test_current_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    thirty_min_cable_test_resistance_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    thirty_min_cable_test_current_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fourtyfive_min_cable_test=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fourtyfive_min_cable_test_resistance_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fourtyfive_min_cable_test_current_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fourtyfive_min_cable_test_resistance_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fourtyfive_min_cable_test_current_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fourtyfive_min_cable_test_resistance_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    fourtyfive_min_cable_test_current_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    sixty_min_cable_test=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    sixty_min_cable_test_resistance_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    sixty_min_cable_test_current_pha=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    sixty_min_cable_test_resistance_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    sixty_min_cable_test_current_phb=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    sixty_min_cable_test_resistance_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    sixty_min_cable_test_current_phc=models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    
    #RELAY BOOLEAN FIELDS
    relay_tighten_case = models.BooleanField(default=False)
    relay_inspect_gasket = models.BooleanField(default=False)
    relay_inspect_shorting = models.BooleanField(default=False)
    relay_foreign_material = models.BooleanField(default=False)
    relay_verify_reset = models.BooleanField(default=False)
    relay_clean_glass = models.BooleanField(default=False)
    relay_inspect_disk_solts = models.BooleanField(default=False)
    relay_disk_clearance = models.BooleanField(default=False)
    relay_spring_convolutions = models.BooleanField(default=False)
    relay_disk_free_travel = models.BooleanField(default=False)
    relay_tightness_hardware = models.BooleanField(default=False)
    relay_burnish_contacts = models.BooleanField(default=False)
    relay_inspect_bearings = models.BooleanField(default=False)
    relay_verify_settings = models.BooleanField(default=False)
    #LV SWITCH BOOLEAN FIELDS
    switch_verify_mechanical_support = models.BooleanField(default=False)
    fuse_sizes_types_drawings_ect = models.BooleanField(default=False)
    
    #MV AIR SWITCH BOOLEAN FIELDS
    switch_verify_expulsion_limiting_devices = models.BooleanField(default=False)
    switch_verify_motor_operator_limit = models.BooleanField(default=False)
    switch_alignment_travel_stops_arc_interrupter = models.BooleanField(default=False)
    #MVVB BOOLEAN FIELDS
    mvvb_maintenance_tools_gauges = models.BooleanField(default=False)
    mvvb_mechanical_operation_tests = models.BooleanField(default=False)
    mvvb_critical_distances = models.BooleanField(default=False)
    mvvb_fit_alignment = models.BooleanField(default=False)
    mvvb_racking_mechanism = models.BooleanField(default=False)
    mvvb_current_carrying_parts = models.BooleanField(default=False)
    mvvb_contact_timing_test = models.BooleanField(default=False)
    mvvb_trip_close_coil_analysis = models.BooleanField(default=False)
    mvvb_mechanism_motion_analysis = models.BooleanField(default=False)
    #VT CT CPT
    clearances_primary_secondary_wiring = models.BooleanField(default=False)
    #SF6 BREAKER BOOLEAN FIELDS
    sf6_gas_sample = models.BooleanField(default=False)
    sf6_gas_leaks = models.BooleanField(default=False)
    #METER BOOLEAN FIELDS
    unit_grounded_manufacturer = models.BooleanField(default=False)
    unit_connected_manfacturer_drawings = models.BooleanField(default=False)
    parameters_ratios_ect = models.BooleanField(default=False)
    correct_aux_in_out = models.BooleanField(default=False)
    measurements_indications_consistant_standards = models.BooleanField(default=False)

    connections_with_system_requirements = models.BooleanField(default=False)
    clearances_primary_secondary_wiring = models.BooleanField(default=False)
    grounding_connections_contact = models.BooleanField(default=False)
    #MEDIUM VOLTAGE AIR BREAKER BOOLEAN FIELDS
    mvab_arc_chutes_intact = models.BooleanField(default=False)
    mvab_check_binding_friction_ect = models.BooleanField(default=False)
    mvab_puffer_operation = models.BooleanField(default=False)
    #OIL BREAKER BOOLEAN FIELDS
    ofcb_oil_level_tanks_bushings  = models.BooleanField(default=False)
    ofcb_vents_clear = models.BooleanField(default=False)
    ofcb_hydraulic_air_inspected = models.BooleanField(default=False)
    ofcb_alarms_pressure_switches_operators = models.BooleanField(default=False)
    ofcb_inspect_bottom_for_parts_debris = models.BooleanField(default=False)
    ofcb_lift_rod_ect = models.BooleanField(default=False)
    ofcb_contact_sequence = models.BooleanField(default=False)
    ofcb_refill_tanks = models.BooleanField(default=False)
    #DRY TRANSFORMER BOOLEAN FIELDS
    xfmr_resilient_mounts = models.BooleanField(default=False)
    xfmr_temp_indicators = models.BooleanField(default=False)
    xfmr_fans_oc_protection = models.BooleanField(default=False)
    xfmr_manufacture_inspections_mechanical_tests = models.BooleanField(default=False)
    xfmr_as_left_verified = models.BooleanField(default=False)
    xfmr_surge_arrestors_present = models.BooleanField(default=False)
    #OIL FILLED TRANSFORMER BOOLEAN FIELDS
    oil_xfmr_impact_recorder = models.BooleanField(default=False)
    oil_xfmr_dew_point = models.BooleanField(default=False)
    oil_xfmr_pcb_content_labeling = models.BooleanField(default=False)
    oil_xfmr_shipping_bracing = models.BooleanField(default=False)
    oil_xfmr_bushings_clean = models.BooleanField(default=False)
    oil_xfmr_alarm_temperature = models.BooleanField(default=False)
    oil_xfmr_alarm_control_trip_indicators_devices = models.BooleanField(default=False)
    oil_xfmr_verify_liquid_level = models.BooleanField(default=False)
    oil_xfmr_verify_valve_positions = models.BooleanField(default=False)
    oil_xfmr_verify_positive_pressure = models.BooleanField(default=False)
    oil_xfmr_load_tap_changer = models.BooleanField(default=False)
    oil_xfmr_denergized_as_left = models.BooleanField(default=False)
    #INSULATED/MOLDED-CASE BOOLEAN FIELDS
    insul_mol_lvcb_smooth_op = models.BooleanField(default=False)
    insul_mol_lvcb_inspect_mech_chutes = models.BooleanField(default=False)
    insul_mol_lvcb_adjustments_protective_settings = models.BooleanField(default=False)
    #LOW VOLTAGE CB BOOLEAN FIELDS
    lvcb_contacts_condition_alignment = models.BooleanField(default=False)
    lvcb_primary_secondary_dimensions_correct = models.BooleanField(default=False)
    lvcb_operator_mechanism_accordance_manufacturer_data = models.BooleanField(default=False)
    lvcb_cell_fit_element_alignment = models.BooleanField(default=False)

    #Switchgear
    bus_contact_resistance_quantity = models.IntegerField(null=True, blank=True)


    # #properties inherited from equipment MOLD
    @property
    def equipment_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.equipment_voltage
        else:
            return self.equipment_voltage      
    @property
    def system_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.system_voltage
        else:
            return self.system_voltage      
    @property
    def is_dc_equipment_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.is_dc_equipment_voltage 
        else:
            return self.is_dc_equipment_voltage 
    @property
    def is_dc_system_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.is_dc_system_voltage
        else:
            return self.is_dc_system_voltage  
    @property
    def is_dc_equipment_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.is_dc_equipment_voltage 
        else:
            return self.is_dc_equipment_voltage     
    @property
    def interrupting_capacity_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.interrupting_capacity
        else:
            return self.interrupting_capacity      
    @property
    def interrupting_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.interrupting_voltage
        else:
            return self.interrupting_voltage      
    @property
    def operating_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.operating_voltage
        else:
            return self.operating_voltage      
    @property
    def is_dc_operating_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.is_dc_operating_voltage 
        else:
            return self.is_dc_operating_voltage 
    def control_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.control_voltage
        else:
            return self.control_voltage
    @property
    def is_dc_control_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.is_dc_control_voltage 
        else:
            return self.is_dc_control_voltage 
    @property
    def trip_coil_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.trip_coil_voltage  
        else:
            return self.trip_coil_voltage  
    @property
    def is_dc_trip_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.is_dc_trip_voltage 
        else:
            return self.is_dc_trip_voltage 
    @property
    def fuse_manufacturer_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.fuse_manufacturer 
        else:
            return self.fuse_manufacturer 
    @property
    def fuse_type_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.fuse_type 
        else:
            return self.fuse_type 
    @property
    def fuse_size_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.fuse_size 
        else:
            return self.fuse_size 
    @property
    def frame_size_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.frame_size 
        else:
            return self.frame_size 
    @property
    def mount_style_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.mount_style 
        else:
            return self.mount_style 
    @property
    def trip_unit_model_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.trip_unit_model 
        else:
            return self.trip_unit_model 
    @property
    def trip_unit_manufacturer_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.trip_unit_manufacturer  
        else:
            return self.trip_unit_manufacturer  
    @property
    def trip_unit_serial_number_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.trip_unit_serial_number  
        else:
            return self.trip_unit_serial_number  
    # @property
    # def trip_unit_rating_plug_data(self):
    #     if self.eq.equipment_mold:
    #         return self.eq.equipment_mold.sheet_eq.trip_unit_rating_plug  
    #     else:
    #         return self.trip_unit_rating_plug  
    @property
    def trip_unit_curve_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.trip_unit_curve  
        else:
            return self.trip_unit_curve  
    @property
    def trip_unit_phase_ct_high_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.trip_unit_phase_ct_high 
        else:
            return self.trip_unit_phase_ct_high 
    @property
    def trip_unit_phase_ct_low_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.trip_unit_phase_ct_low 
        else:
            return self.trip_unit_phase_ct_low 
    @property
    def protection_device_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.protection_device 
        else:
            return self.protection_device 
    @property
    def trip_device_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.trip_device 
        else:
            return self.trip_device 
    @property
    def power_rating_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.power_rating 
        else:
            return self.power_rating 
    @property
    def power_rating_units_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.power_rating_units 
        else:
            return self.power_rating_units 
    @property
    def primary_winding_config_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.primary_winding_config 
        else:
            return self.primary_winding_config 
    @property
    def secondary_winding_config_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.secondary_winding_config 
        else:
            return self.secondary_winding_config 
    @property
    def primary_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.primary_voltage 
        else:
            return self.primary_voltage 
    @property
    def secondary_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.secondary_voltage 
        else:
            return self.secondary_voltage 
    @property
    def temp_rise_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.temp_rise 
        else:
            return self.temp_rise 
    @property
    def temp_rise_units_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.temp_rise_units 
        else:
            return self.temp_rise_units 
    @property
    def impedance_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.impedance 
        else:
            return self.impedance 
    @property
    def impedance_at_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.impedance_at  
        else:
            return self.impedance_at  
    @property
    def xfmr_class_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.xfmr_class 
        else:
            return self.xfmr_class 
    @property
    def tap_qty_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_qty 
        else:
            return self.tap_qty 
    @property
    def tap_one_volts_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_one_volts 
        else:
            return self.tap_one_volts 
    @property
    def tap_one_ratio_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_one_ratio 
        else:
            return self.tap_one_ratio 
    @property
    def ttr_upper_tolerance_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.ttr_upper_tolerance 
        else:
            return self.ttr_upper_tolerance 
    @property
    def ttr_lower_tolerance_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.ttr_lower_tolerance 
        else:
            return self.ttr_lower_tolerance 
    @property
    def tap_two_volts_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_two_volts 
        else:
            return self.tap_two_volts 
    @property
    def tap_two_ratio_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_two_ratio 
        else:
            return self.tap_two_ratio 
    @property
    def tap_three_volts_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_three_volts 
        else:
            return self.tap_three_volts 
    @property
    def tap_three_ratio_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_three_ratio 
        else:
            return self.tap_three_ratio 
    @property
    def tap_four_volts_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_four_volts 
        else:
            return self.tap_four_volts 
    @property
    def tap_four_ratio_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_four_ratio 
        else:
            return self.tap_four_ratio 
    @property
    def tap_five_volts_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_five_volts 
        else:
            return self.tap_five_volts 
    @property
    def tap_five_ratio_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_five_ratio 
        else:
            return self.tap_five_ratio 
    @property
    def tap_six_volts_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_six_volts 
        else:
            return self.tap_six_volts 
    @property
    def tap_six_ratio_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_six_ratio 
        else:
            return self.tap_six_ratio 
    @property
    def tap_seven_volts_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_seven_volts 
        else:
            return self.tap_seven_volts 
    @property
    def tap_seven_ratio_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.tap_seven_ratio 
        else:
            return self.tap_seven_ratio 
    @property
    def fluid_type_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.fluid_type 
        else:
            return self.fluid_type 
    @property
    def fluid_capacity_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.fluid_capacity 
        else:
            return self.fluid_capacity 
    @property
    def fluid_capacity_units_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.fluid_capacity_units 
        else:
            return self.fluid_capacity_units 
    @property
    def weight_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.weight 
        else:
            return self.weight 
    @property
    def weight_units_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.weight_units 
        else:
            return self.weight_units 
    @property
    def cable_voltage_rating_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_voltage_rating 
        else:
            return self.cable_voltage_rating 
    @property
    def operating_cable_voltage_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.operating_cable_voltage 
        else:
            return self.operating_cable_voltage 
    @property
    def cable_amp_rating_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_amp_rating 
        else:
            return self.cable_amp_rating 
    @property
    def cable_length_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_length 
        else:
            return self.cable_length 
    @property
    def cable_length_units_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_length_units 
        else:
            return self.cable_length_units 
    @property
    def cable_insulation_type_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_insulation_type 
        else:
            return self.cable_insulation_type 
    @property
    def cable_insulation_thickness_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_insulation_thickness 
        else:
            return self.cable_insulation_thickness 
    @property
    def cable_insulation_thickness_units_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_insulation_thickness_units 
        else:
            return self.cable_insulation_thickness_units 
    @property
    def cable_insulation_material_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_insulation_material
        else:
            return self.cable_insulation_material
    @property
    def cable_insulation_rating_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_insulation_rating
        else:
            return self.cable_insulation_rating
    @property
    def cable_size_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_size 
        else:
            return self.cable_size 
    @property
    def cable_size_units_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_size_units
        else:
            return self.cable_size_units
    @property
    def cable_conductor_material_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_conductor_material 
        else:
            return self.cable_conductor_material 
    @property
    def is_cable_shielded_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.is_cable_shielded 
        else:
            return self.is_cable_shielded 
    @property
    def cable_starting_point_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_starting_point 
        else:
            return self.cable_starting_point 
    @property
    def cable_ending_point_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_ending_point 
        else:
            return self.cable_ending_point 

    @property
    def cable_starting_termination_type_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_starting_termination_type 
        else:
            return self.cable_starting_termination_type 

    @property
    def cable_ending_termination_type_data(self):
        if self.eq.equipment_mold:
            return self.eq.equipment_mold.sheet_eq.cable_ending_termination_type 
        else:
            return self.cable_ending_termination_type 

class CableTestData(models.Model):
    test_sheet = models.ForeignKey(TestSheet, on_delete=models.CASCADE, related_name="cable_test_data", null=True, blank=True)
    test_result_key = models.IntegerField(null=True, blank=True)
    time = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    test_voltage = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    phase_a = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    phase_b = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    phase_c = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    phase_a_units=models.CharField(max_length=64, null=True, blank=True)
    phase_b_units=models.CharField(max_length=64, null=True, blank=True)
    phase_c_units=models.CharField(max_length=64, null=True, blank=True)
    notes =  models.CharField(max_length=256, null=True, blank=True)

class BusContactTestData(models.Model):
    test_sheet = models.ForeignKey(TestSheet, on_delete=models.CASCADE, related_name="bus_test_data", null=True, blank=True)
    test_result_key = models.IntegerField(null=True, blank=True)
    starting_section = models.TextField(null=True, blank=True)
    ending_section = models.TextField(null=True, blank=True)
    phase_a = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    phase_b = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    phase_c = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    phase_a_units=models.CharField(max_length=64, null=True, blank=True)
    phase_b_units=models.CharField(max_length=64, null=True, blank=True)
    phase_c_units=models.CharField(max_length=64, null=True, blank=True)
    notes =  models.CharField(max_length=256, null=True, blank=True)

#create a class for user properties that has a onetoone relationship with it's associated user.
class UserProperties(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")

    #company of user
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE, related_name="user_company")
    #define user types as booleans
    is_fsr=models.BooleanField(default=True)
    is_manager=models.BooleanField(default=False)
    is_coordinator = models.BooleanField(default=False)
    is_salesman = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_support = models.BooleanField(default=False)

    #create nickname
    nickname = models.CharField(max_length=64, null=True, blank=True)

    #define universal properties
    home_base = models.CharField(max_length=128, null=True, blank=True)
    phone_number = models.CharField(max_length=64, null=True, blank=True)

    #relate support user to appropriate Types
    equipment_types_supported = models.ManyToManyField(Type, blank=True, related_name="equipment_types_supported")
    equipment_models_supported = models.ManyToManyField(Model, blank=True, related_name="equipment_models_supported")

    help_username = models.CharField(max_length=64, null=True, blank=True)

    #notification subscriptions
    is_all_notifications = models.BooleanField(default=False)
    job_notifications = models.ManyToManyField('Job', blank=True, related_name="job_notifications_user")
    equipment_notifications = models.ManyToManyField(Equipment, blank=True, related_name="equipment_notifications_user")

    #define fsr properties
    burn_rate = models.IntegerField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)


    #define manager Properties

    #define coordinator Properties
    #define customer Properties

    #Display nickname with real name in parinthasese if it exists
    def __str__(self):
        if self.nickname:
            return f"{self.nickname} ({self.user.first_name} {self.user.last_name})"
        else:
            return f"{self.user.first_name} {self.user.last_name}"

#notification model definition

# class Notification(models.Model):

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     verb = models.CharField(max_length=255)
#     note = models.TextField(null=True, blank=True)

#     timestamp = models.DateTimeField(auto_now_add=True)
#     read = models.BooleanField(default=False)

#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey()

#     def __str__(self):
#         return f'{self.id} | {self.user.first_name} {self.user.last_name} | notification'

#     @property
#     def get_absolute_url(self):
#         return reverse('notification:notification', args=[self.id])

# class InternalEntries(models.Manager):
class JobSite(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    owner = models.CharField(max_length=128, null=True, blank=True)
    facility_manager = models.CharField(max_length=128, null=True, blank=True)
    
    address = models.CharField(max_length=300, null=True, blank=True)
    nav_link = models.URLField(max_length=300, null=True, blank=True)#google maps or maps link
    site_navigation = models.TextField(null=True, blank=True) # how to get around on site
    site_contact = models.TextField(null=True, blank=True)
    site_contact_info= models.TextField(null=True, blank=True)
    other_contacts= models.TextField(null=True, blank=True)
    
    food_accomodations=models.TextField(null=True, blank=True)#i.e. Leaving site for food, packing lunch, food available onsite, ect.
    lodging_recommendations=models.TextField(null=True, blank=True)#i.e. Recommend hotels in Junction City, book hotels ASAP, ect.

    #site safety
    is_safety_training=models.BooleanField(default=False)
    safety_training_item_requirements=models.TextField(null=True, blank=True) #any items or documents required specifically for safety training
    safety_training_time=models.TextField(null=True, blank=True)#includes days/times available,
    safety_training_location=models.TextField(null=True, blank=True)
    safety_training_procedure=models.TextField(null=True, blank=True)
    safety_rules=models.TextField(null=True, blank=True)#can be a runthrough of all safety rules or "reference site files" and upload an already existing document
    is_hardhat=models.BooleanField(default=False)
    is_safety_glasses=models.BooleanField(default=False)
    is_safety_shoes=models.BooleanField(default=False)
    is_safety_vest=models.BooleanField(default=False)
    is_safety_gloves=models.BooleanField(default=False)
    is_fr_clothes=models.BooleanField(default=False)
    is_h2s_monitor=models.BooleanField(default=False)
    additional_ppe_requirements = models.TextField(null=True, blank=True)#do we add booleans here with all the specific requirements? probably yes

    #site access
    documents_required_for_access=models.TextField(null=True, blank=True)
    background_checks=models.BooleanField(default=False)
    background_check_procedure=models.TextField(null=True, blank=True)
    access_requirements=models.TextField(null=True, blank=True)
    entry_procedure=models.TextField(null=True, blank=True)

    #site rules and other 
    restricted_items=models.TextField(null=True, blank=True)#list restricted items like guns, knives, alchohol, tobacco, recreational drugs
    driving_vehicles=models.TextField(null=True, blank=True)
    parking_considerations = models.TextField(null=True, blank=True)
    other_site_rules= models.TextField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="jobsite_company")

    @property
    def get_jobs(self):
        return self.job_site.filter(trashed=False)

    @property
    def get_eq_count(self):
        eq = 0
        for job in self.job_site.filter(trashed=False):
            eq += job.get_eq_count
        if eq<1:
            eq=1
        return eq
    # @property
    # def job_eq_count(self):
    #     if self.job_site:
    #         return sel.job_site.all
    #     else:
    #         return 0 
            
    #site files and notes
    def __str__(self):
        return f"{self.name} "

def jobsite_folder_path(instance, filename):
    
    try:
        jobsite=instance.jobsite
        jobsite_path=jobsite.name+"_"+str(jobsite.pk)
        path= "jobsites/"+jobsite_path+"/jobsite_folder/"+filename
        return path
    except JobSite.MultipleObjectsReturned:
        return False

class JobSiteFolder(models.Model):
    jobsite_file=models.FileField(max_length=500, null=True, blank = True, upload_to = jobsite_folder_path)
    file_name = models.CharField(max_length=256, null=True, blank=True)
    file_url=models.URLField(max_length=500, null=True, blank=True)
    jobsite = models.ForeignKey(JobSite, null=True, on_delete=models.CASCADE, blank=True, related_name="jobsite")
    created_at = models.DateTimeField(auto_now_add=True)    
    @property
    def hostname(self):
        return urllib.parse.urlparse(self.file_url).hostname
    def filename(self):
        return os.path.basename(self.jobsite_file.name)

class JobSiteNotes(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='site_notes')
    note = models.TextField(null=True, blank=True)
    jobsite = models.ForeignKey(JobSite, null=True, on_delete=models.CASCADE, blank=True, related_name="note_jobsite")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class JobManager(models.Manager):
    def create_job(self, job_name, user):
        job = self.create(job_name=job_name, created_by=user)
        # return job
        return job

def maint_file_path(instance, filename):
    
    try:
        maint=instance.maint_event
        path = "well/"+str(maint.well.pk)+"maint"+str(maint.pk)+"maint_folder"+filename
        return path
    except Well.MultipleObjectsReturned:
        return False


class Well(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    nav_link = models.URLField(max_length=300, null=True, blank=True)
    motor = models.CharField(max_length=256, null=True, blank=True)
    oil_type= models.CharField(max_length=256, null=True, blank=True)
    fuel_type= models.CharField(max_length=256, null=True, blank=True)

    oil_filter = models.TextField(null=True, blank=True)
    air_filter = models.TextField(null=True, blank=True)
    oil_capacity= models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    hours_last = models.IntegerField(null=True, blank=True)
    hours_next = models.IntegerField(null=True, blank=True)    
    overhaul_frequency = models.IntegerField(null=True, blank=True)

    start_date = models.DateField(null=True, blank=True, max_length=80)
    man_date = models.DateField(null=True, blank=True, max_length=80)
    
    @property
    def last_date(self):
        maints = self.maint_well.all()
        if maints:
            x=self.oil_change_date
            return x.strftime('%Y-%m-%d')
        else:
            None
        
class WellNotes(models.Model):
    note = models.TextField(null=True, blank=True)
    well = models.ForeignKey(Well, null=True, on_delete=models.CASCADE, blank=True, related_name="note_well")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MaintEvent(models.Model):
    well = models.ForeignKey(Well, null=True, on_delete=models.CASCADE, blank=True, related_name="maint_well")    
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    oil_change_date = models.DateField(null=True, blank=True, max_length=80)
    hours = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True)
    completed = models.IntegerField(null=True, blank=True)    

    @property
    def date(self):
        if self.oil_change_date:
            x=self.oil_change_date
            return x.strftime('%Y-%m-%d')
        else:
            None

class MaintNotes(models.Model):
    note = models.TextField(null=True, blank=True)
    maint = models.ForeignKey(MaintEvent, null=True, on_delete=models.CASCADE, blank=True, related_name="note_maint")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MaintFile(models.Model):
    maint_file=models.FileField(max_length=500, null=True, blank = True, upload_to = maint_file_path)
    file_name = models.CharField(max_length=256, null=True, blank=True)
    maint_event = models.ForeignKey(MaintEvent, null=True, on_delete=models.CASCADE, blank=True, related_name="maint_event_file")
    created_at = models.DateTimeField(auto_now_add=True)
    def filename(self):
        return os.path.basename(self.maint_file.name)

    
class Job(models.Model):
    
    def save(self, *args, **kwargs):
        self.change_key += 1        
        print(self.change_key)
        super().save(*args, **kwargs)  # Call the "real" save() method.
    change_key = models.IntegerField(null=False, blank=False, default=0)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, blank=True, related_name="job_company")
    job_number = models.CharField(max_length=64, null=True, blank=True)
    job_site = models.ForeignKey(JobSite, null=True, on_delete=models.CASCADE, blank=True, related_name="job_site")
    customer_name= models.CharField(max_length=128, null=True, blank=True)
    job_name = models.CharField(max_length=128, null=True)
    site_contact = models.CharField(max_length=64, null=True, blank=True)
    site_contact_info= models.TextField(null=True, blank=True)
    project_manager = models.CharField(max_length=64, null=True, blank=True)

    #Define the Job Scope
    is_startup=models.BooleanField(default=False)
    is_preventative_maintenance=models.BooleanField(default=False)
    is_troubleshooting=models.BooleanField(default=False)
    is_warranty=models.BooleanField(default=False)
    is_standard_testing=models.BooleanField(default=False)
    is_neta_testing=models.BooleanField(default=False)
    job_scope_details = models.TextField(null=True, blank=True)#All additional details about the job scope

    #Define the time of the job
    start_date = models.DateField(null=True, blank=True, max_length=80)
    @property
    def start_date_formatted(self):
        if self.start_date:
            return self.start_date.strftime( "%Y""-""%m""-" "%d")
        else:
            return ""
    end_date = models.DateField(null=True, blank=True, max_length=80)
    @property
    def end_date_formatted(self):
        if self.end_date:
            return self.end_date.strftime( "%Y""-""%m""-" "%d")
        else:
            return ""
    work_schedule = models.TextField(null=True, blank=True, max_length=2000)#job work schedule

    #Define Miscillaneous Details about the Job
    food_accomodations=models.TextField(null=True, blank=True)#i.e. Leaving site for food, packing lunch, food available onsite, ect.
    lodging_recommendations=models.TextField(null=True, blank=True)#i.e. Recommend hotels in Junction City, book hotels ASAP, ect.
    weather_considerations=models.TextField(null=True, blank=True)#Temperature, Precipitation Dangers and Delays, wind, streneous working conditions

    equipment = models.ManyToManyField(Equipment, blank=True, related_name="equipments")
    
    test_equipment = models.ManyToManyField(TestEquipment, blank=True, related_name="jobs")

    address = models.CharField(max_length=300, null=True, blank=True)
    nav_link = models.URLField(max_length=300, null=True, blank=True)#google maps or maps link
    site_navigation = models.TextField(null=True, blank=True) #once you reach the address, work location, site navigation, entry procedures, ect.
    #site_considerations = models.TextField(max_length=2000, null=True, blank=True)
    #Define individual site Considerations
    is_safety_training_required=models.BooleanField(default=False)
    safety_training_time=models.TextField(null=True, blank=True)#includes days/times available,
    safety_training_location=models.TextField(null=True, blank=True)
    escort_considerations=models.TextField(null=True, blank=True)#designate if and when escorts are required on site
    restricted_items=models.TextField(null=True, blank=True)#list restricted items like guns, knives, alchohol, tobacco, recreational drugs

    #Define fields for PPE requirements
    is_hardhat=models.BooleanField(default=False)
    is_safety_glasses=models.BooleanField(default=False)
    is_safety_shoes=models.BooleanField(default=False)
    is_safety_vest=models.BooleanField(default=False)
    is_safety_gloves=models.BooleanField(default=False)
    is_fr_clothes=models.BooleanField(default=False)
    is_h2s_monitor=models.BooleanField(default=False)
    is_mv_voltage_detector=models.BooleanField(default=False)
    is_insulated_gloves=models.BooleanField(default=False)
    is_8cal_protection=models.BooleanField(default=False)
    is_40cal_protection=models.BooleanField(default=False)
    is_harness=models.BooleanField(default=False)
    is_grounding_cluster=models.BooleanField(default=False)
    grounding_wire_size=models.CharField(null=True, blank=True, max_length=64)
    grounding_clamp_style=models.CharField(null=True, blank=True, max_length=64)
    grounding_cluster_quantity=models.IntegerField(null=True, blank=True)
    other_ppe_requirements=models.TextField(null=True, blank=True)#list any additional ppe Requirements

    #for cleaner html, a string is compiled here that lists the required safety equipment.
    @property
    def safety_equipment_string(self):
        seb=""
        if self.is_hardhat==True:
            seb+="hardhat"
        if self.is_safety_glasses==True:
            seb+="\nsafety glasses"
        if self.is_safety_shoes==True:
            seb+="\nsafety shoes"
        if self.is_safety_vest==True:
            seb+="\nhi-visibility vest"
        if self.is_safety_gloves==True:
            seb+="\nsafety gloves"
        if self.is_fr_clothes:
            seb+="\nstandard flame retardant clothes"
        if self.is_8cal_protection==True:
            seb+="\n8 cal protection gear"
        if self.is_40cal_protection==True:
            seb+="\n40 cal protection gear"
        if self.is_harness==True:
            seb+="\nharness"
        if self.is_mv_voltage_detector==True:
            seb+="\nmedium voltage proximity detector"
        if self.is_insulated_gloves==True:
            seb+="\ninsulated gloves"
        if self.is_h2s_monitor==True:
            seb+="\nH2S monitor"
        if self.other_ppe_requirements==True:
            seb+=self.other_ppe_requirements
        if seb=="":
            seb="No Safety Equipment is required for this job"
        
        
        return seb

    #Define Site Safety Considerations
    is_6ft_work=models.BooleanField(default=False)
    is_switching_required=models.BooleanField(default=False)#switching by service provider required
    switching_specifications=models.TextField(null=True, blank=True)#switch type, voltage, amperage, arc flash
    is_live_work_required=models.BooleanField(default=False)
    live_work_voltage=models.CharField(null=True, blank=True, max_length=128)
    is_ungaurded_holes=models.BooleanField(default=False)
    is_confined_space=models.BooleanField(default=False)#is confined space work required
    chemical_hazards=models.TextField(null=True, blank=True)#specify chemicals and danger mitigation
    permit_requirements=models.TextField(null=True, blank=True)#when are permits required and what is the procedure for getting permits

    #Pricing
    is_time_and_materials=models.BooleanField(default=False)
    quoted_price = models.IntegerField(null=True, default=0)
    costs = models.IntegerField(null=True, blank=True)#running total of costs on the jobs


    #Tools and Equipment Required for the job
    is_standard_handtools=models.BooleanField(default=False)
    extension_cords=models.TextField(null=True, blank=True)#length and quantity
    generators=models.TextField(null=True, blank=True)#size, type, and quantity
    gasoline=models.IntegerField(default=0) #number of gallons
    diesel=models.IntegerField(default=0) #number of gallons
    ladders=models.TextField(null=True, blank=True)#height and quantity
    harness_lanyard=models.TextField(null=True, blank=True)#quantity of harness's and quantity/styles of lanyards
    torque_wrenches=models.TextField(null=True, blank=True)#drive size, torque rating, and quantity
    tables=models.IntegerField(default=0)
    chairs=models.IntegerField(default=0)
    lifts=models.TextField(null=True, blank=True)#lift types and quantities
    is_bus_bender=models.BooleanField(default=False)
    is_fork_lift=models.BooleanField(default=False)
    is_trailer=models.BooleanField(default=False)
    additional_tools = models.TextField(null=True, blank=True) #additional tools to bring for the job

    #communication and testing cables, non-standard test sets, modifications to listed test equipment
    specialty_test_equipment = models.TextField(null=True, blank=True)

    material = models.TextField(max_length=2000, null=True, blank=True) #materials to be brought to the job

    #folder for job

    #users associated with job
    user_properties = models.ManyToManyField(UserProperties, blank=True, related_name="user_properties")

    #job status
    trashed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    completion = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="jobs")
    objects = JobManager()

    #create feedback strings for job completion
    @property
    def test_equipments_name(self):
        """
        This returns name of test sets related to equipments
        """
        test_equipments = [i[0].name for i in self.test_equipments]
        job_te = self.test_equipment.values_list('name', flat=True)

        return list(set(test_equipments) - set(job_te))

    @property
    def job_complete(self):
        if self.completion==True:
            return "Finished"
        else:
            return "Incomplete"

    @property
    def get_eq_count(self):
        eq = self.equipment.filter(trashed=False).count()
        if eq<1:
            eq=1
        return eq
    def get_eq(self):
        return self.equipment.filter(trashed = False)        
    @property
    def fsrs(self):
        return [user for user in self.user_properties.all() if user.is_fsr and user.company == self.company]
    #property below, test_equipments, holds every unique type of test equipment recommended from all equipment belonging to the job.
    @property
    def test_equipments(self):
        # te3 = TestEquipment.filter()
        te2 = self.equipment.filter(trashed=False).prefetch_related('mandatory_test_equipment')
       
        try:

            equipments = (self.equipment.
                          annotate(mte_count=Count('mandatory_test_equipment'),
                                   ote_count=Count('optional_test_equipment'))
                          .filter(Q(mte_count__gt=0) | Q(ote_count__gt=0), trashed=False, ))
            te = {}
            for equipment in equipments:
                for test_equipment in equipment.mandatory_test_equipment.all():
                    te_name = test_equipment
                    if not te.get(te_name):
                        te[test_equipment] = 1
                    else:
                        te[test_equipment] += 1

                for test_equipment in equipment.optional_test_equipment.all():
                    te_name = test_equipment
                    if not te.get(te_name):
                        te[test_equipment] = 1
                    else:
                        te[test_equipment] += 1

            for job_te in self.test_equipment.all():
                if not te.get(job_te):
                    te[job_te] = 1
                else:
                    te[job_te] += 1

        except:
            te = {}
        return te.items()

    #create counters for # of pieces of equipment, number of fsr's, and number of unique pieces of test equipment
    @property
    def equipment_count(self):
        if self.equipment.filter(trashed=False):
            return self.equipment.filter(trashed=False).count()#Returns untrashed equipment
        else:
            return 0
    @property
    def fsr_count(self):

        return len(self.fsrs)#Returns fsrs
    @property
    def test_equipment_count(self):
        return len(self.test_equipments)

    def __str__(self):
        return f"Job: {self.job_name} Job Number: {self.job_number}"

    @property
    def fuels(self):
        if not self.gasoline and not self.diesel:
            return
        fuels = ''
        if self.gasoline:
            fuels += f'{self.gasoline} gallon/s of gasoline'

        if self.gasoline and self.diesel:
            fuels += ' and '

        if self.diesel:
            fuels += f'{self.diesel} gallon/s of diesel'

        return fuels

    #every job has associated equipment, fsrs, and test equipment.
    #those are represented in tables and connected through manytoMany relationships.

def job_folder_path(instance, filename):
    
    try:
        job=instance.job
        job_path=job.job_name+"_"+str(job.pk)
        path= "jobs/"+job_path+"/job_folder/"+filename
        return path
    except Job.MultipleObjectsReturned:
        return False


class JobFolder(models.Model):
    job_file=models.FileField(max_length=500, null=True, blank = True, upload_to = job_folder_path)
    file_name = models.CharField(max_length=256, null=True, blank=True)
    job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE, blank=True, related_name="job")
    created_at = models.DateTimeField(auto_now_add=True)
    def filename(self):
        return os.path.basename(self.job_file.name)


class JobNotes(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='job_notes')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='modify_job_notes')
    note = models.TextField(null=True, blank=True)
    job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE, blank=True, related_name="note_job")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_note = models.ForeignKey('self', on_delete=models.CASCADE, related_name="sub_notes", null=True)

    @property
    def truncated(self):
        return (self.note[:30] + '..') if len(self.note) > 32 else (self.note+"\"")

    @property
    def hierarchy_level(self):
        return get_hierarchy_level(self)

    @property
    def margin(self):
        if self.hierarchy_level:
            return f'{20 * self.hierarchy_level}px'

    @property
    def sub_note_ids(self):
        sub_note_ids = get_note_ids(self)
        sub_note_ids = [str(i) for i in sub_note_ids]
        return '-'.join(sub_note_ids)

    @property
    def author_name(self):
        user = self.author
        if user:
            return f'{user.first_name} {user.last_name}'
        return 'Anonymous'


def get_note_ids(note):
    sub_ids = []
    sub_note_ids = list(note.sub_notes.values_list('id', flat=True))
    sub_ids.extend(sub_note_ids)
    for sub_id in sub_note_ids:
        sub_note = JobNotes.objects.get(id=sub_id)
        if sub_note.sub_notes.exists():
            sub_ids.extend(get_note_ids(sub_note))

    return sub_ids


def get_hierarchy_level(job_note, level=0):
    parent_note = job_note.parent_note
    if parent_note:
        level = get_hierarchy_level(parent_note, level+1)
    return level


def feedback_file_path(instance, filename):    
    path= "feedback/"+filename
    return path


class FeedbackFile(models.Model):
    feedback_file=models.FileField(max_length=500, null=True, blank = True, upload_to = feedback_file_path)
    created_at = models.DateTimeField(auto_now_add=True)
    def filename(self):
        return os.path.basename(self.feedback_file.name)


class FeedbackNote(models.Model):
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WorkingNote(models.Model):
    note = models.TextField(null=True, blank=True)
