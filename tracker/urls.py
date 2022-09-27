from django.urls import path, include
from . import views, constructors
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
router = routers.DefaultRouter()
# url for the CRUD
router.register(r'get_jobs_info', views.GetJobsView,basename="jobs")
from .models import Job, JobFolder, UserProperties, Type, Manufacturer, WorkingNote, Model, ModelFolder, Equipment, EquipmentFolder, EquipmentLink, TestEquipment, JobNotes, EquipmentNotes, TypeFolder, TypeTestGuide, ModelTestGuide, JobSite, JobSiteNotes, JobSiteFolder, Company, TestSheet, Well, WellNotes, MaintEvent, MaintFile, MaintNotes

urlpatterns = [
    path("", views.home, name="home"),
    path('', include(router.urls)),
    # path("get_jobs_info/", views.get_jobs_info, name="get_jobs_info"),
    path("get_test_info/", views.get_test_info, name="get_test_info"),
    path("get_eq_info/<int:eq_id>", views.get_eq_info, name="get_eq_info"),
    path("get_job_info/<int:job_id>", views.get_job_info, name="get_job_info"),
    path("birdseye", views.birdseye, name="birdseye"),
    path("jobs", views.jobs, name="jobs"),
    path("job/<int:job_id>", views.job, name="job"),
    path("equipment/<int:equipment_id>/edit", constructors.edit_equipment, name="edit_equipment"),
    path("fsr<int:fsr_id>", views.fsr_info, name="fsr_info"),
    path("<int:job_id>/add_fsr", constructors.add_fsr, name="add_fsr"),
    path("<int:job_id>/<int:fsr_id>/remove_fsr", constructors.remove_fsr, name="remove_fsr"),
    #job folder
    path("job<int:job_id>_folder", views.job_folder, name="job_folder"),
    path("job_folder<int:job_id>/addfile", constructors.add_job_files, name="add_job_files"),
    path("job_site<int:jobsite_id>/addfile", constructors.add_jobsite_files, name="add_jobsite_files"),
    path("job_folder<int:file_id>/removefile", constructors.remove_job_files, name="remove_job_files"),
    #archived trashed and completed jobs. Contains both view and constructor urls
    path("job_archive", views.job_archive, name="job_archive"),
    path("archive_job/<int:job_id>", constructors.archive_job, name="archive_job"),
    path("unarchive_job/<int:job_id>", constructors.unarchive_job, name="unarchive_job"),
    path("job_trash", views.job_trash, name="job_trash"),
    path("trash_job/<int:job_id>", constructors.trash_job, name="trash_job"),
    path("untrash_job/<int:job_id>", constructors.untrash_job, name="untrash_job"),
    path("complete_job/<int:job_id>", constructors.complete_job, name="complete_job"),
    path("uncomplete_job/<int:job_id>", constructors.uncomplete_job, name="uncomplete_job"),
    path("equipment_batch_actions/<int:job_id>", constructors.equipment_batch_actions, name="equipment_batch_actions"),

    path("equipment_batch_actions/<int:job_site_id>", constructors.equipment_batch_actions, name="job_site_equipment_batch_actions"),
    path("equipment<int:equipment_id>_folder", views.equipment_folder, name="equipment_folder"),
    path("equipment_folder<int:equipment_id>/addfile", constructors.add_equipment_files, name="add_equipment_files"),
    path("equipment_folder<int:file_id>/removefile", constructors.remove_equipment_files, name="remove_equipment_files"),
    path("equipment_link<int:equipment_id>/addlink", constructors.add_equipment_links, name="add_equipment_links"),
    path("model<int:model_id>_folder", views.model_folder, name="model_folder"),
    path("model_folder<int:model_id>/addfile", constructors.add_model_files, name="add_model_files"),
    path("model_folder<int:file_id>/removefile", constructors.remove_model_files, name="remove_model_files"),
    path("model_video<int:model_id>/addvideo", constructors.add_model_video, name="add_model_video"),    
    path("copy_private_model<int:model_id>/create_copy", constructors.copy_private_model, name="copy_private_model"),
    path("copy_private_type<int:type_id>/create_copy", constructors.copy_private_type, name="copy_private_type"),
    path("type_folder<int:type_id>/addfile", constructors.add_type_files, name="add_type_files"),    
    path("type_test_standard<int:type_id>/addts", constructors.add_test_standard, name="add_test_standard"),
    path("type_folder<int:file_id>/removefile", constructors.remove_type_files, name="remove_type_files"),
    path("type_video<int:type_id>/addvideo", constructors.add_type_video, name="add_type_video"),
    
    path("equipment<int:equipment_id>/addresults", constructors.add_test_results, name="add_test_results"),
    path("equipment<int:equipment_id>/removeresults", constructors.remove_test_results, name="remove_test_results"),
    path("equipment<int:equipment_id>/edit_test_results", constructors.edit_test_results, name="edit_test_results"),
    

    path("equipment<int:equipment_id>/addnameplate", constructors.add_nameplate, name="add_nameplate"),    
    path("equipment<int:equipment_id>/removenameplate", constructors.remove_nameplate, name="remove_nameplate"),
    
    
    #job notes
    path("job<int:job_id>/addnote", constructors.add_job_note, name="add_job_note"),
    #job site notes
    path("jobsite<int:jobsite_id>/addnote", constructors.add_jobsite_note, name="add_jobsite_note"),

    #create test sets
    path("create_test_eq_view", views.create_test_eq_view, name="create_test_eq_view"),
    path("create_test_eq", constructors.create_test_eq, name="create_test_eq"),
    path("delete_test_eq/<int:te_id>", constructors.delete_test_eq, name="delete_test_eq"),
    path("edit_test_eq/<int:te_id>", constructors.edit_test_eq, name="edit_test_eq"),
    path("test_equipment", views.test_equipment, name="test_equipment"),
    #link to view for type creation form
    path("create_type_view", views.create_type_view, name="create_type_view"),
    #type constructor path
    path("create_type", constructors.create_type, name="create_type"),
    path("edit_type/<int:type_id>", constructors.edit_type, name="edit_type"),

    #link to view for manufacturer creation form
    path("create_manufacturer_view", views.create_manufacturer_view, name="create_manufacturer_view"),
    #manufacturer constructer path
    path("create_manufacturer", constructors.create_manufacturer, name="create_manufacturer"),

    #link to view for model creation form
    path("create_model_view", views.create_model_view, name="create_model_view"),
    #model constructor path
    path("create_model", constructors.create_model, name="create_model"),
    path("edit_model/<int:model_id>", constructors.edit_model, name="edit_model"),
    path("edit_manufacturer/<int:manufacturer_id>", constructors.edit_manufacturer, name="edit_manufacturer"),

    path("add_jobsite_eq/job<int:job_id>", constructors.add_jobsite_eq, name="add_jobsite_eq"),
    path("add_equipment_page/job<int:job_id>", views.add_equipment_page, name="add_equipment_page"),
    path("add_equipment_page/job_site<int:job_site_id>", views.add_equipment_page, name="add_equipment_to_job_site_page"),
    path("equipment<int:equipment_id>/sub_equipment/job<int:job_id>", views.add_equipment_page, name="add_sub_equipment_page"),
    path("equipment<int:equipment_id>/sub_equipment/job_site<int:job_site_id>", views.add_equipment_page, name="add_sub_equipment_job_site_page"),
    path("<int:job_id>/add_equipment", constructors.add_equipment, name="add_equipment"),
    path("<int:job_site_id>/add_site_equipment", constructors.add_site_equipment, name="add_site_equipment"),
    path("<int:equipment_id>/trash_equipment", constructors.trash_equipment, name="trash_equipment"),
    path("<int:equipment_id>/untrash_equipment", constructors.untrash_equipment, name="untrash_equipment"),
    path("trashed_equipment/<int:job_id>", views.trashed_equipment, name="trashed_equipment"),
    path("trashed_job_site_equipment/<int:job_site_id>", views.trashed_job_site_equipment, name="trashed_job_site_equipment"),
    path("trashed_equipment/<int:job_id>/restore", constructors.restore_equipments, name="restore_equipment"),

    path("trashed_job_site_equipment/<int:job_site_id>/restore", constructors.restore_job_site_equipments, name="restore_job_site_equipments"),
    path("complete_equipment/<int:equipment_id>", constructors.complete_equipment, name="complete_equipment"),
    
    #equipment notes
    path("equipment<int:equipment_id>/addnote", constructors.add_equipment_note, name="add_equipment_note"),    
    path("equipment/add_new_note", constructors.add_new_equipment_note, name="add_new_equipment_note"),    

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_profile_view", views.create_profile_view, name="create_profile_view"),
    path("create_profile", constructors.create_profile, name="create_profile"),

    path("types", views.types, name="types"),
    path("eq_types<int:type_id>", views.eq_type, name="eq_type"),
    path("types/create_equipment", constructors.create_equipment, name="create_equipment"),

    path("models", views.models, name="models"),
    path("eq_model<int:model_id>", views.eq_model, name="eq_model"),

    path("manufacturers", views.manufacturers, name="manufacturers"),
    path("eq_manufacturer<int:manufacturer_id>", views.eq_manufacturer, name="eq_manufacturer"),

    #create url to open a particular piece of equipment belonging to a job
    
    path("report_cover_page<int:job_id>", views.report_cover_page, name="report_cover_page"),
    path("compiled_test_report/<int:job_id>", views.compile_test_report, name="compile_test_report"),
    path("equipment_in_scope<int:job_id>", views.equipment_in_scope, name="equipment_in_scope"),
    path("equipment<int:equipment_id>", views.equipment, name="equipment"),
    path("equipment_test_sheet<int:equipment_id>", views.equipment_test_sheet, name="equipment_test_sheet"),
    # path("multi_test_sheet<int:equipment_id>", views.multi_test_sheet, name="multi_test_sheet"),
    path("equipment_test_sheet_download<int:equipment_id>", views.equipment_test_sheet_download, name="equipment_test_sheet_download"),
    path("blank_test_sheet<int:equipment_id>", views.blank_test_sheet, name="blank_test_sheet"),
    path("download_xlsx<int:equipment_id>", constructors.download_xlsx, name="download_xlsx"),
    path("upload_sync_xlsx<int:equipment_id>", constructors.upload_sync_xlsx, name="upload_sync_xlsx"),
    #path("equipmentedit/<int: job_id>/<int: equipment_id>", views.edit_equipment, name="edit_equipment"),
    path("create_job/<str:add_type>", views.new_job, name="new_job"),
    path("edit_jobsite/<int:jobsite_id>", constructors.edit_jobsite, name="edit_jobsite"),
    path("edit_job/<int:job_id>", constructors.edit_job, name="edit_job"),
    path("edit_job_test_equipments/<int:job_id>", constructors.edit_job_test_equipments, name="edit_job_test_equipment"),
    path("jobs/create_job", constructors.create_job, name="create_job"),
    path("jobs/create_job/quick", constructors.create_job_quick, name="create_job_quick"),
    path("edit_site_id/<int:job_id>", constructors.edit_site_id, name="edit_site_id"),
    path("edit_site_id_free", constructors.edit_site_id, name="edit_site_id_free"),
    path("copy_job/<int:job_id>", constructors.copy_job, name="copy_job"),
    #create job site
    path("create_job_site_view", views.create_job_site_view, name="create_job_site_view"),
    path("create_job_site", constructors.create_job_site, name="create_job_site"),
    #job site management
    path("job_sites", views.job_sites, name="job_sites"),
    path("job_site/<int:jobsite_id>", views.job_site, name="job_site"),

    #manipulate existing notes
    path("edit_note/<str:note_type>/<int:note_id>", constructors.edit_note, name="edit_note"),
    path("delete_note/<str:note_type>/<int:note_id>", constructors.delete_note, name="delete_note"),
    path("reply_note/<str:note_type>/<int:note_id>", constructors.reply_note, name="reply_note"),
    path("add_note/<str:note_type>", constructors.add_note, name="add_note"),

    
    path("profile", views.profile, name="profile"),
    path("feedback", views.feedback, name="feedback"),#view feedback information
    path("working_page", views.working_page, name="working_page"),
    path("working_update", constructors.working_update, name="working_update"),
    path("add_feedback_file", constructors.add_feedback_file, name="add_feedback_file"),
    path("add_feedback_note", constructors.add_feedback_note, name="add_feedback_note"),
    path("edit_feedback_note/<int:note_id>", constructors.edit_feedback_note, name="edit_feedback_note"),
    #to sign into microsft api
    path('signin', views.sign_in, name='signin'),
    path('callback', views.callback, name='callback'),
    path('signout', views.sign_out, name='signout'),
    #ag wells 
    path("agwells", views.agwells, name="agwells"),
    path("agwell/<int:well_id>", views.agwell, name="agwell"),
    path("ag_new_well", constructors.ag_new_well, name="ag_new_well"),
    path("ag_new_maint/<int:well_id>", constructors.ag_new_maint, name="ag_new_maint"),
    path("ag_edit_well/<int:well_id>", constructors.ag_edit_well, name="ag_edit_well"),
    path("ag_edit_maint/<int:maint_id>", constructors.ag_edit_maint, name="ag_edit_maint"),
    path("add_maint_file/<int:maint_id>", constructors.add_maint_file, name="add_maint_file")
]
