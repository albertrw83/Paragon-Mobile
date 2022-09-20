
from http import HTTPStatus
from PyPDF2 import PdfFileWriter
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template.loader import get_template, render_to_string
import datetime
from datetime import datetime
import json

# from tracker.auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token, get_token # to get into microsft graph api
# from tracker.graph_helper import * # to get into microsft graph api

from .models import Job, JobFolder, BusContactTestData, EquipmentFolder, UserProperties, WorkingNote, Type, Manufacturer, Model, ModelNotes, ModelFolder, Equipment, TestEquipment, JobNotes,EquipmentLink, EquipmentNotes, TypeNotes, TypeFolder, TypeTestStandards, TypeTestGuide, ModelTestGuide, JobSite, JobSiteNotes, JobSiteFolder, Company, FeedbackFile, FeedbackNote, TestSheet, Well, WellNotes, MaintEvent, MaintFile, MaintNotes
from .serializers import JobSerializer, TestSheetSerializer, EquipmentSerializer
import pdfkit
import os

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    # get_job_info('GET')
    properties=UserProperties.objects.get(user=request.user)
    jobs = Job.objects.filter(archived=False, trashed=False, user_properties=properties, company=properties.company).order_by('-start_date')
    other_jobs = Job.objects.filter(archived=False, trashed=False, company=properties.company).exclude(user_properties=properties).order_by('-start_date')

    context = {
        "user": request.user,
        "jobs": jobs,
        "other_jobs": other_jobs,
        "properties": properties
    }
    if request.user.is_authenticated:
        return render(request, "jobs/home.html", context)

def get_jobs_info(request):
    print('333')
    print(request)
    print('333')
    x=0
    if request.method == 'GET':
        jobss = Job.objects.all()
        serializer = JobSerializer(jobss, many=True)
        x=2
        # print(serializer)
        return JsonResponse(serializer.data, safe=False)
    # print(x)
    return "fail"

def get_test_info(request):
    if request.method == 'GET':
        tests = TestSheet.objects.all()[:5]
        serializer = TestSheetSerializer(tests, many=True)
        # print(serializer)
        return JsonResponse(serializer.data, safe=False)
    x=3
    # print(x)
    return "fail"

def get_eq_info(request, eq_id):
    if request.method == 'GET':
        tests = Equipment.objects.get(pk=eq_id)
        print(tests.classification)
        serializer = EquipmentSerializer(tests)
        # print(serializer)
        return JsonResponse(serializer.data, safe=False)
    return "fail"

def get_job_info(request, job_id):
    print("loaded")
    # print(pk)
    if request.method == 'GET':
        job = Job.objects.get(pk=job_id)
        serializer = JobSerializer(job)
        x=2
        # print(serializer)
        return JsonResponse(serializer.data, safe=False)
    return "fail"

#this is from the microsft graph tutorial. redirects to microsft sign in
def sign_in(request):
  # Get the sign-in flow
  flow = get_sign_in_flow()

  # Save the expected flow so we can use it in the callback
  try:
    request.session['auth_flow'] = flow
  except Exception as e:
      x = 3
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(flow['auth_uri'])

#this is from the microsft graph tutorial. signs user out
def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))

def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)
  if error != None:
    context['errors'] = []
    context['errors'].append(error)
  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context

#this is from the microsft graph tutorial. 
def callback(request):
  # Make the token request
 
  result = get_token_from_code(request)
  

  #Get the user's profile
  user = get_user(result['access_token'])

  # Store user
  store_user(request, user)
  return HttpResponseRedirect(reverse('home'))

def birdseye(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    # if not request.user.is_authenticated:
    #     return render(request, "jobs/login.html", {"message": None})
    # jobs = []
    theone = Equipment.objects.filter(trashed=True)
    properties = None
    try:
        properties=UserProperties.objects.get(user=request.user)
        if properties.company:
            jobsites=JobSite.objects.all()
        else:
            properties = None
    except:
        properties=None
    #     pass    
    context = {
        "jobsites": jobsites,
        "theone": theone
    }    
    # try:
    if request.user.is_authenticated and properties:
        return render(request, "jobs/birdseye.html", context)  
    else:
        return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company reference key. Click Edit Profile above to add a key. Error code.: birdseye>first_except"})
    # except:
    #     return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company reference key. Click Edit Profile above to add a key. Error code: birdseye>final_except"})
   

def jobs(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    eqs = Equipment.objects.filter(equipments__isnull=False)
    context = initialize_context(request)
    try:
        properties=UserProperties.objects.get(user=request.user)
        if properties.company:
            my_jobs=Job.objects.filter(archived=False, trashed=False, user_properties=properties, company=properties.company).order_by('-pk')
            all_jobs=Job.objects.filter(archived=False, trashed=False, company=properties.company).order_by("-pk")
        else:
            return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company reference key. Click Edit Profile above to add a key. Error code.: birdseye>first_except"})
            my_jobs=Job.objects.filter(archived=False, trashed=False, user_properties=properties).order_by('-pk')
            all_jobs=Job.objects.filter(archived=False, trashed=False).order_by("-pk")
        not_my_jobs=[]
        for job in all_jobs:
            if not job in my_jobs:
                not_my_jobs.append(job)
        try:
            context.update({
                "my_jobs": my_jobs,
                "not_my_jobs": not_my_jobs,
                "eqs": eqs
            })
        except:
            pass
    except:
        properties=None
        pass
    
    try:
        if request.user.is_authenticated and properties.company:
            return render(request, "jobs/jobs.html", context)
        else:
            return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company reference key. Click Edit Profile above to add a key. Error code.: jobs>first_except"})
    except:
        # return render(request, "jobs/jobs.html", context)
        return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company reference key. Click Edit Profile above to add a key. Error code: jobs>final_except"})
   

def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    
    if request.user.id:
        return HttpResponseRedirect(reverse("jobs"))

    if username is None and password is None:
        return render(request, "jobs/login.html")

    user = authenticate(request, username=username, password=password)
    
    if user is not None:        
        
        login(request, user)
        properties = UserProperties.objects.filter(user=user).first()
        if properties and properties.company:
            return HttpResponseRedirect(reverse("home"))
        else:
            return HttpResponseRedirect(reverse("profile"))
    else:
        return render(request, "jobs/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "jobs/login.html", {"message": "Logged out."})

def register(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('create_profile_view')
    else:
        form=UserCreationForm()
    return render(request, 'jobs/register.html', {'form': form})

def create_profile_view(request):
    
    email_value='' #initiate email as empty string
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        user_properties=UserProperties.objects.get(user=request.user)
        email_value = request.user.email
    except:
        user_properties=None
        username = request.user.username
        #check that username has got some email properties
        if '@' in username or ',' in username:
            email_value = username
        else:
            email_value = ''
    context = {
        "user_properties": user_properties,
        "email": email_value
    }
    if request.user.is_authenticated:
        return render(request, "jobs/create_profile.html", context)

def job(request, job_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        user_properties=UserProperties.objects.get(user=request.user)
        job = Job.objects.get(pk=job_id)
        notes= JobNotes.objects.filter(job=job, parent_note__isnull=True).order_by('-updated_at')
        jobsite_notes = JobSiteNotes.objects.filter(jobsite=job.job_site).order_by('-updated_at')
        jobsite_files = JobSiteFolder.objects.filter(jobsite=job.job_site).order_by('-created_at')
        equipments=job.equipment.filter(Q(equipment_mold__isnull=True) | Q(equipment_mold__trashed=False), trashed=False, parent_equipment__isnull=True).order_by('-pk')
        eq_notes_list=[]
        eq_with_notes=[]
        finished_count=equipments.filter(completion=True).count()
        unfinished_count=equipments.filter(completion=False).count()
        job_files = JobFolder.objects.filter(job=job).exclude(job_file='').order_by('-pk')
        eq_files_list=[]
        eq_with_files=[]
        quoted_hours = 0
        for equipment in job.equipment.filter(trashed= False):
            eq_notes=EquipmentNotes.objects.filter(equipment=equipment, parent_note__isnull=True).order_by('-updated_at')
            if eq_notes:
                eq_with_notes.append(equipment)
            for note in eq_notes:
                eq_notes_list.append(note)

            eq_files=EquipmentFolder.objects.exclude(equipment_file='').filter(equipment=equipment).order_by('-created_at')
            if eq_files:
                eq_with_files.append(equipment)
            for eq_file in eq_files:
                eq_files_list.append(eq_file)
            #adding quoted default
            if equipment.equipment_model.quote_default:
                quoted_hours = quoted_hours+equipment.equipment_model.quote_default
            elif equipment.equipment_type.quote_default:
                quoted_hours = quoted_hours+equipment.equipment_type.quote_default

        fsrs = job.fsrs
        non_fsrs=[]
        for fsr in UserProperties.objects.filter(is_fsr=True, company = user_properties.company):
            if fsr not in fsrs:
                non_fsrs.append(fsr)
        #define strings that will be conditional on completion/archive/trash status'
        if (job.trashed==False):
            trash_button="Trash Job"
        else:
            trash_button="Untrash Job" 
        if (job.archived==False):
            archive_button="Archive Job"
        else:
            archive_button="Unarchive Job"


        if (job.completion==False):
            completion="Incomplete"
            complete_button="Mark Complete"
        else:
            completion="Finished"
            complete_button="Mark Incomplete"


    except Job.DoesNotExist:
        raise Http404("Job does not exist.")
    #check if user has permission to view this job
    if not job.company == user_properties.company:
        return render(request, "jobs/error.html", {"message": "This job does not belong to your company. Contact admin if you suspect this is an error."})

    existing_test_equipment_ids = [i[0].id for i in job.test_equipments]
    available_test_equipments = TestEquipment.objects.exclude(id__in=existing_test_equipment_ids)
    test_equipments = json.dumps(list(TestEquipment.objects.values_list('name', flat=True)))

    context= {
        "job": job,
        "job_id": job_id,
        "notes": notes,
        "fsrs": fsrs,
        "non_fsrs": non_fsrs,
        "equipments": equipments,
        "equipment_count": job.equipment_count,
        "fsr_count": job.fsr_count,
        "finished_count": finished_count,
        "unfinished_count": unfinished_count,
        "types": Type.objects.all(),
        "completion": completion,
        "trash_button": trash_button,
        "archive_button": archive_button,
        "complete_button": complete_button,
        "eq_notes_list": eq_notes_list,
        "eq_with_notes": eq_with_notes,
        "eq_files_list": eq_files_list,
        "eq_with_files": eq_with_files,
        "job_files": job_files,
        "jobsite_notes": jobsite_notes,
        "jobsite_files": jobsite_files,
        "quoted_hours": round(quoted_hours, 2),
        "default_quote": round(quoted_hours*255.0, 2),
        "available_test_equipments": available_test_equipments,
        "test_equipments": test_equipments,
    }
    
    # The below code can be activated to create a copy of a job when that job is viewed. Use only for copying jobs for example jobs
    # new_job = job
    # new = new_job
    # new.pk = None
    # newjob = new
    # newjob.save()
    if request.user.is_authenticated and user_properties.company:
        return render(request, "jobs/job.html", context)
    else:
        return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company key."})


def job_folder(request, job_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        job=Job.objects.get(pk=job_id)
        job_files = JobFolder.objects.filter(job=job).exclude(job_file='').order_by('-pk')
    except Job.DoesNotExist:
        raise Http404("Folder does not exist.")
    context = {
        "job": job,
        "job_files": job_files
    }
    if request.user.is_authenticated:
        return render(request, "jobs/job_folder.html", context)

#defines view for creating a new job
def new_job(request, add_type):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        user_properties=UserProperties.objects.get(user=request.user)
    except:
        user_properties=None
    context = {
        "job_sites": JobSite.objects.filter(company = user_properties.company).order_by('-pk'),
        "job_ids": json.dumps(list(Job.objects.values_list('job_number', flat=True)))
    }
    if request.user.is_authenticated and user_properties.company:
        if add_type == 'quick':
            companies = Company.objects.all()
            context['companies'] = companies

            return render(request, "jobs/new_job_quick.html", context)
        return render(request, "jobs/new_job.html", context)
    else:
        return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company key."})

def create_job_site_view(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    
    user_properties=UserProperties.objects.get(user=request.user)
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    if request.user.is_authenticated and user_properties.company:
        return render(request, "jobs/create_job_site.html")
    else:
        return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company key."})

def job_sites(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
        
    user_properties=UserProperties.objects.get(user=request.user)
    context = {
        "job_sites": JobSite.objects.filter(company = user_properties.company).order_by('-pk')
    }
    if request.user.is_authenticated:
        return render(request, "jobs/job_sites.html", context)
   
def job_site(request, jobsite_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    
    mfrs = Manufacturer.objects.all()

    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})

    try:
        user_properties=UserProperties.objects.get(user=request.user)
        jobsite=JobSite.objects.get(pk=jobsite_id)       
        if jobsite.company != user_properties.company:
            return render(request, "jobs/error.html", {"message": "Error: Company access requirements not met. If you arrived here by manually changing the url, you are not authorized to view this job site. If you arrived here by clicking a link, please contact admin."})

        flateq = Equipment.objects.filter(job_site=jobsite).all()
        job_id=0
        jobsite_notes = JobSiteNotes.objects.filter(jobsite=jobsite).order_by('-updated_at')
        jobsite_files = JobSiteFolder.objects.filter(jobsite=jobsite).order_by('-created_at')
        equipments = Equipment.objects.filter(job_site=jobsite, parent_equipment__isnull=True, trashed=False).order_by('site_id')
        jobs = Job.objects.filter(job_site=jobsite, company = user_properties.company).order_by('-start_date')
        active_jobs = Job.objects.filter(job_site=jobsite, trashed = False, archived = False, company=user_properties.company).order_by('-start_date')
        inactive_jobs = Job.objects.filter(job_site=jobsite, company=user_properties.company).exclude(trashed = False, archived = False).order_by('-start_date')
        context = {
            "jobsite": jobsite,
            "jobsite_notes": jobsite_notes,
            "jobsite_files": jobsite_files,
            "equipments": equipments,
            "job_id": job_id,
            "jobs": jobs,
            "active_jobs": active_jobs,
            "inactive_jobs": inactive_jobs,
            "flateq": flateq
        }
        # The below code can be activated to create a copy of a jobsite when that jobsite is viewed. Use only for copying jobsites for example jobs
        # new_jobsite = jobsite
        # new = new_jobsite
        # new.pk = None
        # newsite = new
        # newsite.save()
    except JobSite.DoesNotExist:
        raise Http404("Job site does not exist.")
    if request.user.is_authenticated:
        return render(request, "jobs/job_site.html", context)


def create_test_eq_view(request):
    
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    user_properties=UserProperties.objects.get(user=request.user)
    
    if request.user.is_authenticated and user_properties.company:
        return render(request, "jobs/create_test_eq.html")
    else:
        return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company key."})


#defines and renders view for creating a new type of equipment
def create_type_view(request):
    print("000000000")
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    test_equipments = TestEquipment.objects.all()
    equipment_types = Type.objects.all().order_by('-pk')
    user_properties=UserProperties.objects.get(user=request.user)
    #pass in existing types of equipment
    context= {
        "equipment_types": equipment_types,
        "test_equipments": test_equipments
        }
    if request.user.is_authenticated and user_properties.company:
        return render(request, "jobs/create_type.html", context)
    else:
        return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company key."})


def create_manufacturer_view(request):

    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})

    manufacturers= Manufacturer.objects.all()
    user_properties=UserProperties.objects.get(user=request.user)
    #pass in existing types of equipment
    context= {
        "manufacturers": manufacturers,
        }

    if request.user.is_authenticated and user_properties.company:
        return render(request, "jobs/create_manufacturer.html", context)
    else:
        return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company key."})

#defines and renders view for creating a new model of equipment
def create_model_view(request):

    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    test_equipments = TestEquipment.objects.all()
    equipment_types = Type.objects.all()
    manufacturers = Manufacturer.objects.all()
    equipment_models = Model.objects.all()
    eq_modelslist = []
    for em in equipment_models:
        eq_modelslist.append(em.model_manufacturer.name + em.model_type.name + em.name)
        eq_models=json.dumps(eq_modelslist)
    user_properties=UserProperties.objects.get(user=request.user)

    #pass in existing types of equipment
    context= {
        "equipment_types": equipment_types,
        "test_equipments": test_equipments,
        "manufacturers": manufacturers,
        "eq_models": eq_models
        }

    if request.user.is_authenticated and user_properties.company:
        return render(request, "jobs/create_model.html", context)
    else:
        return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company key."})
    

def model_folder(request, model_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        model=Model.objects.get(pk=model_id)
        model_files = ModelFolder.objects.filter(model=model).exclude(model_file='').order_by('-pk')
    except Model.DoesNotExist:
        raise Http404("Folder does not exist.")
    context = {
        "model": model,
        "model_files": model_files
    }
    if request.user.is_authenticated:
        return render(request, "jobs/model_folder.html", context)

def equipment(request, equipment_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    unattached_notes = JobNotes.objects.all()
    date_tested=""
    cable_test_q = ":1"
    bus_test_q = ":1"
    try:
        equipment=Equipment.objects.get(pk=equipment_id)
        op_counter = False
        if equipment.equipment_type.name.strip() in {"SF6 Circuit Breaker", "Medium Voltage Air Breaker", "Low Voltage Power Circuit Breaker", "Enclosed Medium Voltage Air Switch", "Medium Voltage Vacuum Breaker"}:
            op_counter = True
        try:
            test_results = TestSheet.objects.get(eq=equipment)
            if equipment.equipment_type.is_cable:
                cable_test_q = ":" + str(test_results.cable_hipot_quantity)
            try:
                date_tested = test_results.date_tested.strftime( "%Y""-""%m""-" "%d")
            except:
                date_tested=""
            if equipment.equipment_type.is_bus_resistance:
                bus_test_q = ":" + str(test_results.bus_contact_resistance_quantity)
                
        except:
            test_results = None
            pass
        job=Job.objects.filter(equipment=equipment).first()
        # notes=EquipmentNotes.objects.filter(equipment=equipment)
        notes = EquipmentNotes.objects.filter(equipment=equipment, parent_note__isnull=True).order_by('-updated_at')
        equipment_files = EquipmentFolder.objects.filter(equipment=equipment).exclude(equipment_file='').order_by('-pk')
        equipment_links = EquipmentLink.objects.filter(equipment=equipment).exclude(link_url='').order_by('-pk')
        model_te=None
        model_notes = None
        model_files=None
        model_guides=None
        if equipment.equipment_model:
            model_te=equipment.equipment_model.mandatory_model_test_equipment.all() | equipment.equipment_model.optional_model_test_equipment.all()
            model_test_equipments=model_te.distinct()
            model_notes = ModelNotes.objects.filter(model=equipment.equipment_model, parent_note__isnull=True).order_by('-updated_at')
            model_files=ModelFolder.objects.filter(model=equipment.equipment_model).exclude(model_file='', file_url='').order_by('-pk')            
            model_guides=ModelTestGuide.objects.filter(model=equipment.equipment_model).exclude(model_test_guide='').order_by('-pk')
        else:
            model_test_equipments=[]
        if equipment.equipment_type:
            type_te=equipment.equipment_type.mandatory_type_test_equipment.all() | equipment.equipment_type.optional_type_test_equipment.all()
            type_test_equipments=type_te.distinct()
            type_notes = TypeNotes.objects.filter(eq_type=equipment.equipment_type, parent_note__isnull=True).order_by('-updated_at')
            type_files=TypeFolder.objects.filter(eq_type=equipment.equipment_type).exclude(type_file='', file_url='').order_by('-pk')
            type_ts = TypeTestStandards.objects.filter(ts_type=equipment.equipment_type).order_by('-pk')
            type_guides=TypeTestGuide.objects.filter(eq_type=equipment.equipment_type).exclude(type_test_guide='').order_by('-pk')
        else:
            type_test_equipments=[]
        mandatory_test_equipment = equipment.mandatory_test_equipment.all()
        optional_test_equipment=equipment.optional_test_equipment.all()
        #merge test sets
        test_equipments= optional_test_equipment | mandatory_test_equipment
        #remove duplicates
        test_equipments=test_equipments.distinct()
        #retrieve which users are supporters for this equipments
        model_support=UserProperties.objects.filter(equipment_models_supported = equipment.equipment_model)
        type_support = UserProperties.objects.filter(equipment_types_supported = equipment.equipment_type)
        support_users = (model_support | type_support).distinct()
        #filter through test sheet templates to find dominant one
        if equipment.test_sheet_template!=False:
            test_sheet_template=equipment.test_sheet_template
        elif equipment.equipment_model.model_test_sheet:
            test_sheet_template = equipment.equipment_model.model_test_sheet
        elif equipment.equipment_type.test_sheet:
            test_sheet_template = equipment.equipment_type.test_sheet
        else:
            test_sheet_template = None

        available_test_equipments = TestEquipment.objects.all()
        test_equipment_list = json.dumps(list(TestEquipment.objects.values_list('name', flat=True)))
    except Equipment.DoesNotExist:
        raise Http404("Equipment does not exist.")


    #get user properties
    user_properties=UserProperties.objects.get(user=request.user)
    #check whether user has permission to view this equipment
    if not request.user.is_superuser:
        if job and not job.company == user_properties.company:
            return render(request, "jobs/error.html", {"message": "The job that this equipment is associated with does not belong to your company. Contact admin if you suspect this is an error."})

    #moving all notes to new individuals MUST REMOVE AFTER SUCCESSFULL TRANSFER
    # for eq_t in Type.objects.all():
    #     new_note = TypeNotes(note=eq_t.type_notes, eq_type=eq_t)
    #     new_note.save()
    # for eq_m in Model.objects.all():
    #     new_mnote = ModelNotes(note=eq_m.model_notes, model=eq_m)
        # new_mnote.save()
    #     # m_note_list = []
    #     # n_note=[]
    #     # for m_note in m_notes:
    #     #     m_note_list.append(m_note.note)
    #     # for m_note in m_notes:
    #     #     if m_note.note in m_note_list:
    #     #         m_note.delete()
    context = {
        "equipment": equipment,
        "cable_test_q":cable_test_q,
        "bus_test_q":bus_test_q,
        "types": Type.objects.all(),
        "models": Model.objects.all(),
        "test_equipments": test_equipments,
        "model_test_equipments": model_test_equipments,
        "type_test_equipments": type_test_equipments,
        "job": job,
        "support_users": support_users,
        "test_sheet_template": test_sheet_template,
        "notes": notes,
        "equipment_files": equipment_files,
        "equipment_links": equipment_links,
        "model_guides": model_guides,
        "type_guides": type_guides,
        "model_notes": model_notes,
        "model_files": model_files,
        "type_notes": type_notes,
        "type_ts": type_ts,
        "type_files": type_files,
        "test_results": test_results,
        "date_tested": date_tested,
        "job_site": equipment.job_site,
        "note_type": "equipment",
        "available_test_equipments": available_test_equipments,
        "test_equipment_list": test_equipment_list,
        "op_counter": op_counter
    }
    if request.user.is_authenticated:
        return render(request, "jobs/equipment.html", context)

def equipment_test_sheet(request, equipment_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    from io import BytesIO
    from PyPDF2 import PdfFileReader, PdfFileMerger

    equipment = Equipment.objects.filter(pk=equipment_id).first()
    #get the quantity of pages
    page_quantity = 1
    user_properties=UserProperties.objects.get(user=request.user)
    today = datetime.now()
    now=today.strftime("%b-%d-%Y %H:%M")
    now_date = today.date()
    job=Job.objects.get(equipment=equipment )
    
    op_counter = False
    if equipment.equipment_type.name.strip() in {"SF6 Circuit Breaker", "Medium Voltage Air Breaker", "Low Voltage Power Circuit Breaker", "Enclosed Medium Voltage Air Switch", "Medium Voltage Vacuum Breaker"}:
        op_counter = True
    context = {
        "equipment": equipment,
        "job": job,
        "test_sheet": equipment.sheet_eq,
        "user_properties": user_properties,
        "now": now,
        "now_date": now_date,
        "op_counter": op_counter
    }
    #render html to string and place strings in an array.
    strings_array = []    
    html_sheet = None
    if equipment.equipment_type.name.strip() == "Low Voltage Power Circuit Breaker":
        page_quantity=2
        strings_array.append(render_to_string('jobs/test_sheet_lv_ic_breaker.html', context))
        strings_array.append(render_to_string('jobs/test_sheet_primary_secondary.html', context))
    elif equipment.equipment_type.name.strip() in {"Low Voltage Molded Case Breaker", "Low Voltage Insulated Case Breaker"}:
        page_quantity=2
        strings_array.append(render_to_string('jobs/test_sheet_lv_mc_breaker.html', context))
        strings_array.append(render_to_string('jobs/test_sheet_primary_secondary.html', context))
    elif equipment.equipment_type.name.strip() == "Low Voltage Switch":
        context.update({'is_fuse': True})
        html_sheet = render_to_string('jobs/test_sheet_lv_switch.html', context)
    elif equipment.equipment_type.name.strip() in {"SF6 Circuit Breaker", "High Voltage Vacuum Breaker", "Medium Voltage Air Breaker"}:
        page_quantity=2
        strings_array.append(render_to_string('jobs/test_sheet_mv_breaker.html', context))
        strings_array.append(render_to_string('jobs/test_sheet_mv_breaker_2.html', context))
    elif equipment.equipment_type.name.strip() in {"Enclosed Medium Voltage Air Switch", "High Voltage Open Air Switch"}:
        context.update({'is_fuse': True})
        html_sheet = render_to_string('jobs/test_sheet_mv_air_switch.html', context)
    elif equipment.equipment_type.name.strip() == "Medium Voltage Cable":
        context.update({'cable_test_q': equipment.sheet_eq.cable_hipot_quantity})
        html_sheet = render_to_string('jobs/test_sheet_mv_cable.html', context)
    elif equipment.equipment_type.name.strip() == "Medium Voltage Vacuum Breaker":
        context.update({'is_mvvb': True})
        html_sheet = render_to_string('jobs/test_sheet_mv_breaker.html', context)
    elif equipment.equipment_type.name.strip() == "Medium Voltage Motor Contactor":
        context.update({'is_mvvb': True})
        context.update({'is_fuse': True})
        html_sheet = render_to_string('jobs/test_sheet_mv_breaker.html', context)
    elif equipment.equipment_type.name.strip() in {"Oil-filled Transformer", "Dry Type Medium Voltage Transformer"}:
        context.update({'is_fuse': False})
        page_quantity=2
        strings_array.append(render_to_string('jobs/test_sheet_transformer.html', context))
        strings_array.append(render_to_string('jobs/test_sheet_transformer_2.html', context))
    elif equipment.equipment_type.name.strip() == "Low Voltage Transformer":
        html_sheet = render_to_string('jobs/test_sheet_transformer.html', context)
    elif equipment.equipment_type.name.strip() == "Control Power Transformer (CPT)":
        context.update({'is_fuse': False, 'is_cpt': True})
        html_sheet = render_to_string('jobs/test_sheet_transformer.html', context)
    elif equipment.equipment_type.name.strip() == "Voltage Transformer (VT)":
        context.update({'is_fuse': True})
        page_quantity=2
        strings_array.append(render_to_string('jobs/test_sheet_transformer.html', context))
        strings_array.append(render_to_string('jobs/test_sheet_transformer_2.html', context))
    elif equipment.equipment_type.name.strip() == "Current Transformer (CT)":
        context.update({'is_ct': True})
        html_sheet = render_to_string('jobs/test_sheet_transformer.html', context)
    elif equipment.equipment_type.name.strip() == "Power Meter":
        html_sheet = render_to_string('jobs/test_sheet_meter.html', context)
    elif equipment.equipment_type.is_switchgear:
        bus_test_q = ":1"
        if equipment.equipment_type.is_bus_resistance:
            bus_test_q = ":" + str(equipment.sheet_eq.bus_contact_resistance_quantity)
        context.update({'bus_test_q': bus_test_q})
        page_quantity=2
        strings_array.append(render_to_string('jobs/test_sheet_gear1.html', context))
        strings_array.append(render_to_string('jobs/test_sheet_gear2.html', context))
    if page_quantity<2:
        if not html_sheet:
            return render(request, "jobs/error.html", {"message": "No test sheets have been built for this type. Contact Admin"})

    if page_quantity>1:
        pdfadder = PdfFileMerger(strict=False)
        for x in strings_array:
            pdf_content = pdfkit.from_string(x, 'interim/'+str(user_properties.pk)+'test_sheet_temp.pdf')
            pdf = PdfFileReader(open('interim/'+str(user_properties.pk)+'test_sheet_temp.pdf', 'rb'))
            pdfadder.append(pdf, import_bookmarks=False)    
        pdfadder.write('interim/'+str(user_properties.pk)+'combined_sheets.pdf')
        output_file = open('interim/'+str(user_properties.pk)+'combined_sheets.pdf', 'rb')
    else:
        output_file = pdfkit.from_string(html_sheet, None)
        
    response = HttpResponse(output_file, content_type="application/pdf")
    
    response["Content-Disposition"] = f"filename={equipment.site_id}.pdf"


    return response
    # if equipment.equipment_type.name == "Medium Voltage Switchgear":
    #     files_to_convert.append('jobs/test_sheet_gear1.html')
    #     files_to_convert.append('jobs/test_sheet_gear2.html')

    # for page in files_to_convert:
    #     html_sheet = ""
    #     html_sheet = render_to_string(page, context)



    # html_sheet = render_to_string('jobs/report_cover_page.html', context)
    # stream = BytesIO()
    # stream.write(pdfkit.from_string(html_sheet, None))
    # pdf_file_reader = PdfFileReader(stream)
    # for i in range(pdf_file_reader.getNumPages()):
    #     pdf_write.addPage(pdf_file_reader.getPage(i))


def compile_test_report(request, job_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    from io import BytesIO
    from PyPDF2 import PdfFileReader, PdfFileMerger    
    from django.core.exceptions import ObjectDoesNotExist

    job = Job.objects.filter(pk=job_id).first()
    if not job:
        raise Http404("test sheet error. Error code: get job failed")
    # pdf_file_object = BytesIO()
    # pdf_write = PdfFileWriter()
    user_properties=UserProperties.objects.get(user=request.user)
    today = datetime.now()
    now=today.strftime("%b-%d-%Y %H:%M")
    now_date = today.date()

    # Add cover page
    # context = {
    #     "job": job,
    #     "user_properties": user_properties,
    #     "now": now,
    #     "now_date": now_date
    # }
    # html_sheet = render_to_string('jobs/report_cover_page.html', context)
    # stream = BytesIO()
    # stream.write(pdfkit.from_string(html_sheet, None))
    # pdf_file_reader = PdfFileReader(stream)
    # for i in range(pdf_file_reader.getNumPages()):
    #     pdf_write.addPage(pdf_file_reader.getPage(i))

    equipments = job.equipment.filter(trashed=False).order_by('id')

    # Add equipment scope
    # context = {
    #     "job": job,
    #     "equipment": equipments,
    #     "user_properties": user_properties,
    #     "now": now
    # }
    # html_sheet = render_to_string('jobs/equipment_in_scope.html', context)
    # stream = BytesIO()
    # stream.write(pdfkit.from_string(html_sheet, None))
    # pdf_file_reader = PdfFileReader(stream)
    # for i in range(pdf_file_reader.getNumPages()):
    #     pdf_write.addPage(pdf_file_reader.getPage(i))

    strings_array = []
    for equipment in equipments:
        if equipment.equipment_type.is_test_sheet:
            try:
                op_counter = False
                if equipment.equipment_type.name.strip() in {"SF6 Circuit Breaker", "Medium Voltage Air Breaker", "Low Voltage Power Circuit Breaker", "Enclosed Medium Voltage Air Switch", "Medium Voltage Vacuum Breaker"}:
                    op_counter = True

                context = {
                    "equipment": equipment,
                    "job": job,
                    "test_sheet": equipment.sheet_eq,
                    "user_properties": user_properties,
                    "now": now,
                    "now_date": now_date,
                    "op_counter": op_counter
                }
                if equipment.equipment_type.name.strip() == "Low Voltage Power Circuit Breaker":
                    page_quantity=2
                    strings_array.append(render_to_string('jobs/test_sheet_lv_ic_breaker.html', context))
                    strings_array.append(render_to_string('jobs/test_sheet_primary_secondary.html', context))
                elif equipment.equipment_type.name.strip() in {"Low Voltage Molded Case Breaker", "Low Voltage Insulated Case Breaker"}:
                    page_quantity=2
                    strings_array.append(render_to_string('jobs/test_sheet_lv_mc_breaker.html', context))
                    strings_array.append(render_to_string('jobs/test_sheet_primary_secondary.html', context))
                elif equipment.equipment_type.name.strip() == "Low Voltage Switch":
                    context.update({'is_fuse': True})
                    strings_array.append(render_to_string('jobs/test_sheet_lv_switch.html', context))
                elif equipment.equipment_type.name.strip() in {"SF6 Circuit Breaker", "High Voltage Vacuum Breaker", "Medium Voltage Air Breaker"}:
                    page_quantity=2
                    strings_array.append(render_to_string('jobs/test_sheet_mv_breaker.html', context))
                    strings_array.append(render_to_string('jobs/test_sheet_mv_breaker_2.html', context))
                elif equipment.equipment_type.name.strip() in {"Enclosed Medium Voltage Air Switch", "High Voltage Open Air Switch"}:
                    context.update({'is_fuse': True})
                    strings_array.append(render_to_string('jobs/test_sheet_mv_air_switch.html', context))
                elif equipment.equipment_type.name.strip() == "Medium Voltage Cable":
                    context.update({'cable_test_q': equipment.sheet_eq.cable_hipot_quantity})
                    strings_array.append(render_to_string('jobs/test_sheet_mv_cable.html', context))
                elif equipment.equipment_type.name.strip() == "Medium Voltage Vacuum Breaker":
                    context.update({'is_mvvb': True})
                    strings_array.append(render_to_string('jobs/test_sheet_mv_breaker.html', context))
                elif equipment.equipment_type.name.strip() == "Medium Voltage Motor Contactor":
                    context.update({'is_mvvb': True})
                    context.update({'is_fuse': True})
                    strings_array.append(render_to_string('jobs/test_sheet_mv_breaker.html', context))
                elif equipment.equipment_type.name.strip() == "Oil-filled Transformer":
                    context.update({'is_fuse': False, 'is_oft': True})
                    page_quantity=2
                    strings_array.append(render_to_string('jobs/test_sheet_transformer.html', context))
                    strings_array.append(render_to_string('jobs/test_sheet_transformer_2.html', context))
                elif equipment.equipment_type.name.strip() == "Dry Type Medium Voltage Transformer":
                    context.update({'is_fuse': False})
                    page_quantity=2
                    strings_array.append(render_to_string('jobs/test_sheet_transformer.html', context))
                    strings_array.append(render_to_string('jobs/test_sheet_transformer_2.html', context))
                elif equipment.equipment_type.name.strip() == "Low Voltage Transformer":
                    strings_array.append(render_to_string('jobs/test_sheet_transformer.html', context))



                elif equipment.equipment_type.name.strip() == "Control Power Transformer (CPT)":
                    context.update({'is_fuse': False, 'is_cpt': True})
                    strings_array.append(render_to_string('jobs/test_sheet_transformer.html', context))
                elif equipment.equipment_type.name.strip() == "Voltage Transformer (VT)":
                    context.update({'is_fuse': True})
                    page_quantity=2
                    strings_array.append(render_to_string('jobs/test_sheet_transformer.html', context))
                    strings_array.append(render_to_string('jobs/test_sheet_transformer_2.html', context))
                elif equipment.equipment_type.name.strip() == "Current Transformer (CT)":
                    context.update({'is_ct': True})
                    strings_array.append(render_to_string('jobs/test_sheet_transformer.html', context))
                elif equipment.equipment_type.name.strip() == "Power Meter":
                    strings_array.append(render_to_string('jobs/test_sheet_meter.html', context))
                elif equipment.equipment_type.is_switchgear:
                    bus_test_q = ":1"
                    if equipment.equipment_type.is_bus_resistance:
                        bus_test_q = ":" + str(equipment.sheet_eq.bus_contact_resistance_quantity)
                    context.update({'bus_test_q': bus_test_q})
                    page_quantity=2
                    strings_array.append(render_to_string('jobs/test_sheet_gear1.html', context))
                    strings_array.append(render_to_string('jobs/test_sheet_gear2.html', context))
                
                pdfadder = PdfFileMerger(strict=False)
                
            except ObjectDoesNotExist:
                pass
    for x in strings_array:
        pdf_content = pdfkit.from_string(x, 'interim/'+str(user_properties.pk)+'test_sheet_temp.pdf')
        pdf = PdfFileReader(open('interim/'+str(user_properties.pk)+'test_sheet_temp.pdf', 'rb'))
        pdfadder.append(pdf, import_bookmarks=False)    
    pdfadder.write('interim/'+str(user_properties.pk)+'combined_sheets.pdf')
    output_file = open('interim/'+str(user_properties.pk)+'combined_sheets.pdf', 'rb')

    response = HttpResponse(output_file, content_type="application/pdf")
    response["Content-Disposition"] = f"filename={job.job_name}.pdf"
    return response


def report_cover_page(request, job_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        job=Job.objects.get(pk=job_id)
        user_properties=UserProperties.objects.get(user=request.user)
        today = datetime.now()
        now=today.strftime("%b-%d-%Y %H:%M")
        now_date = today.date()
        context = {
        "job": job,
        "user_properties": user_properties,
        "now": now,
        "now_date": now_date
        }
       
        html_sheet = render_to_string('jobs/report_cover_page.html', context)
        # import pdb; pdb.set_trace()

        pdf_content = pdfkit.from_string(html_sheet, None,)
        
        response = HttpResponse(pdf_content, content_type="application/pdf")
        

        # Download
        #response["Content-Disposition"] = "attachment; filename=sample5.pdf"

        # Viewing on the browser
        response["Content-Disposition"] = f"filename={job.job_name}.pdf"

        return response
       

    except Job.DoesNotExist:
        raise Http404("test sheet error. Error code: get job failed")
    

    if request.user.is_authenticated:
        return render(request, "jobs/report_cover_page.html", context)

def equipment_in_scope(request, job_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        job=Job.objects.get(pk=job_id)
        equipment=None
        user_properties=UserProperties.objects.get(user=request.user)
        today = datetime.now()
        now=today.strftime("%b-%d-%Y %H:%M")
        try:
            equipment = job.equipment.filter(trashed=False).order_by('-pk')
        except:
            pass
        context = {
        "job": job,
        "equipment": equipment,
        "user_properties": user_properties,
        "now": now
        }
        html_sheet = render_to_string('jobs/equipment_in_scope.html', context)
        # import pdb; pdb.set_trace()

        pdf_content = pdfkit.from_string(html_sheet, None)
        
        response = HttpResponse(pdf_content, content_type="application/pdf")
        

        # Download
        #response["Content-Disposition"] = "attachment; filename=sample5.pdf"

        # Viewing on the browser
        response["Content-Disposition"] = f"filename={job.job_name}.pdf"

        return response
       

    except Job.DoesNotExist:
        raise Http404("test sheet error. Error code: get job failed")
    

    if request.user.is_authenticated:
        return render(request, "jobs/equipment_in_scope.html", context)

def blank_test_sheet(request, equipment_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    is_test_results = False
    try:
        equipment=Equipment.objects.get(pk=equipment_id)
        user_properties=UserProperties.objects.get(user=request.user)
        today = datetime.now()
        now=today.strftime("%b-%d-%Y %H:%M")
        try:
            test_sheet = TestSheet.objects.get(eq_type=equipment.equipment_type)            
            is_test_results = True
        except:
            test_sheet = None
            return render(request, "jobs/error.html", {"message": "Error: Failed to load base test sheet for eq type. Contact Admin"})

        
        context = {
        "equipment": equipment,
        "job": job,
        "test_sheet":test_sheet,
        "user_properties": user_properties,
        "now": now
        }
        html_sheet=""
        pdf_content=None
        response = None
        
        if equipment.equipment_type.name == "Low Voltage Insulated Case Circuit Breaker":
            html_sheet = render_to_string('jobs/test_sheet_lv_ic_breaker.html', context)
            # import pdb; pdb.set_trace()
        elif equipment.equipment_type.name == "Low Voltage Molded Case Breaker":
            html_sheet = render_to_string('jobs/test_sheet_lv_mc_breaker.html', context)
        elif equipment.equipment_type.name == "Medium Voltage Motor Contactor":
            html_sheet = render_to_string('jobs/test_sheet_mv_contactor.html', context)
        pdf_content = pdfkit.from_string(html_sheet, None)
        
        response = HttpResponse(pdf_content, content_type="application/pdf")
        

        # Download
        #response["Content-Disposition"] = "attachment; filename=sample5.pdf"

        # Viewing on the browser
        response["Content-Disposition"] = f"filename={equipment.site_id}.pdf"

        return response
       

    except Equipment.DoesNotExist:
        raise Http404("test sheet error. Error code: get equipment failed")
    

    if request.user.is_authenticated:
        return render(request, "jobs/test_sheet_lv_ic_breaker.html", context)


# def equipment_test_sheet(request, equipment_id):
#     if not request.user.is_authenticated:
#         return render(request, "jobs/login.html", {"message": None})
#     is_test_results = False
#     try:
#         equipment=Equipment.objects.get(pk=equipment_id)
#         job=Job.objects.get(equipment=equipment)
#         user_properties=UserProperties.objects.get(user=request.user)
#         today = datetime.now()
#         now=today.strftime("%b-%d-%Y %H:%M")
#         try:
#             test_sheet = TestSheet.objects.get(eq=equipment)
#             is_test_results = True
#         except:
#             test_sheet = None
#             return render(request, "jobs/error.html", {"message": "Error: Failed to load base test sheet for eq type. Contact Admin"})
#         #determine variations
#         is_lviccb = False
#         is_lvmcb = False
#         is_mvvb = False
#         is_mvmc = False
#         is_oft=False
#         is_lvt = False
#         is_gear = False

#         if equipment.equipment_type.name == "Low Voltage Insulated Case Circuit Breaker":
#             is_lviccb = True
#         elif equipment.equipment_type.name == "Low Voltage Molded Case Breaker":
#             is_lvmcb = True  
#         elif equipment.equipment_type.name == "Medium Voltage Vacuum Breaker":
#             is_mvvb = True
#         elif equipment.equipment_type.name == "Medium Voltage Motor Contactor":
#             is_mvmc = True
#         elif equipment.equipment_type.name == "Oil-filled Transformer":
#             is_oft = True
#         elif equipment.equipment_type.name == "Low Voltage Transformer":
#             is_lvt = True
#         elif equipment.equipment_type.name == "Medium Voltage Motor Control Center":
#             is_gear = True
#         elif equipment.equipment_type.name == "Medium Voltage Cable":
#             is_mvcable = True
#         elif equipment.equipment_type.name == "Low Voltage Motor Control Center":
#             is_gear = True
#         elif equipment.equipment_type.name == "Medium Voltage Switchgear":
#             is_gear = True
#         elif equipment.equipment_type.name == "Low Voltage Switchgear":
#             is_gear = True
#         cable_test_q = 0
#         cable_test_q = test_sheet.cable_hipot_quantity

#         context = {
#         "equipment": equipment,
#         "job": job,
#         "test_sheet":test_sheet,
#         "cable_test_q":cable_test_q,
#         "user_properties": user_properties,
#         "now": now,
#         "is_lviccb": is_lviccb,
#         "is_lvmcb": is_lvmcb,
#         "is_mvvb": is_mvvb,
#         "is_mvmc": is_mvmc,
#         "is_oft": is_oft,
#         "is_lvt": is_lvt,
#         }
#         html_sheet=""
#         pdf_content=None
#         response = None
        
#         # try:
#         if equipment.equipment_type.name == "Low Voltage Insulated Case Circuit Breaker":
#             html_sheet = render_to_string('jobs/test_sheet_lv_ic_breaker.html', context)
#         elif equipment.equipment_type.name == "Low Voltage Molded Case Breaker":
#             html_sheet = render_to_string('jobs/test_sheet_lv_mc_breaker.html', context)
#         elif equipment.equipment_type.name == "Medium Voltage Vacuum Breaker":
#             html_sheet = render_to_string('jobs/test_sheet_mv_breaker.html', context)
#         elif equipment.equipment_type.name == "Medium Voltage Cable":
#             html_sheet = render_to_string('jobs/test_sheet_mv_cable.html', context)
#         elif equipment.equipment_type.name == "Medium Voltage Motor Contactor":
#             html_sheet = render_to_string('jobs/test_sheet_mv_contactor.html', context)
#         elif equipment.equipment_type.name == "Oil-filled Transformer":
#             html_sheet = render_to_string('jobs/test_sheet_transformer.html', context)
#         elif equipment.equipment_type.name == "Dry Type Medium Voltage Transformer":
#             html_sheet = render_to_string('jobs/test_sheet_transformer.html', context)
#         elif equipment.equipment_type.name == "Low Voltage Transformer":
#             html_sheet = render_to_string('jobs/test_sheet_transformer.html', context)
#         elif equipment.equipment_type.name == "Voltage Transformer (VT)- Medium Voltage":
#             html_sheet = render_to_string('jobs/test_sheet_transformer.html', context)
#         elif is_gear:
#             html_sheet = render_to_string('jobs/test_sheet_gear1.html', context)
#         pdf_content = pdfkit.from_string(html_sheet, None)
#         response = HttpResponse(pdf_content, content_type="application/pdf")
        

#         # Download
#         #response["Content-Disposition"] = "attachment; filename=sample5.pdf"

#         # Viewing on the browser
#         response["Content-Disposition"] = f"filename={equipment.site_id}.pdf"

#         return response
#         # except OSError:
#         #     return render(request, "jobs/error.html", {"message": "Internet Connection Error. If there are no issues with internet connection, contact admin."})

       

#     except Equipment.DoesNotExist:
#         raise Http404("test sheet error. Error code: get equipment failed")
    

#     if request.user.is_authenticated:
#         return render(request, "jobs/test_sheet_lv_ic_breaker.html", context)

def equipment_test_sheet_download(request, equipment_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        equipment=Equipment.objects.get(pk=equipment_id)
        job=Job.objects.get(equipment=equipment)
        context = {
        "equipment": equipment,
        "job": job
        }
       
        html_sheet = render_to_string('jobs/test_results_test.html', context)
        
        # import pdb; pdb.set_trace()

        pdf_content = pdfkit.from_string(html_sheet, None)
        
        response = HttpResponse(pdf_content, content_type="application/pdf")
        
        # Download
        response["Content-Disposition"] = "attachment; filename=sample5.pdf"

        # Viewing on the browser
        # response["Content-Disposition"] = f"filename={equipment.site_id}.pdf"

        return response
       

    except Equipment.DoesNotExist:
        raise Http404("test sheet does not exist. Error code: get equipment OR job failed")
    

    if request.user.is_authenticated:
        return render(request, "jobs/test_results_test.html", context)
# .
# .
# .
# .WORKING CODE TO BE REMOVED
# def add_eq_from_jobsite(request, job_id, equipment_id):
#     job = Job.objects.get(pk=job_id)
#     try:        
#         mold = Equipment.objects.get(pk = equipment_id)
#         parent_mold = None
#         parent_equipment = None
#         if mold.parent_equipment:
#             # this has a parent
#             parent_mold = mold.parent_equipment
#             if job.equipment.filter(equipment_mold = mold.parent_equipment).exists():
#                 #this is confirmation that the parent has been added to the job
#                 print(job.equipment.filter(equipment_mold = mold.parent_equipment).count())
#                 if job.equipment.filter(equipment_mold = mold.parent_equipment).count() < 2:
#                     #this makes sure there's not duplicate
#                     print(job.equipment.filter(equipment_mold = mold.parent_equipment).first())
#                     parent_equipment = job.equipment.filter(equipment_mold = mold.parent_equipment).first()
#                 else:
#                     return render(request, "jobs/error.html", {"message": "Duplicate parents in jobsite. Contact admin"})
#             else:
#                     return render(request, "jobs/error.html", {"message": "Parent Equipment has not been added"})
#         else:
#             # this is top level ancestor
#             print('no parent mold found')
#             parent_mold = None
        
#         temp = mold
#         temp.pk = None
#         eq = temp
#         eq.save()
#         equipment_type = eq.equipment_type
#         if equipment_type.is_test_sheet == True:
#             eq.is_insulation_resistance=equipment_type.is_insulation_resistance
#             eq.is_contact_resistance=equipment_type.is_contact_resistance
#             eq.is_trip_unit=equipment_type.is_trip_unit
#             eq.is_primary_injection=equipment_type.is_primary_injection
#             eq.is_secondary_injection=equipment_type.is_secondary_injection
#             eq.is_xfmr_insulation_resistance=equipment_type.is_xfmr_insulation_resistance
#             eq.is_power_fused=equipment_type.is_power_fused
#             eq.is_breaker=equipment_type.is_breaker
#             eq.is_hipot=equipment_type.is_hipot
#             eq.is_inspection=equipment_type.is_inspection
#             eq.is_transformer=equipment_type.is_transformer
#             eq.is_winding_resistance=equipment_type.is_winding_resistance
#             eq.is_ttr=equipment_type.is_ttr
#             eq.is_liquid_type=equipment_type.is_liquid_type
#             eq.is_cable=equipment_type.is_cable
#             eq.is_cable_vlf_withstand_test=equipment_type.is_cable_vlf_withstand_test
#             eq.save()
#         try:
#             blank_test_sheet=TestSheet(eq=eq)
#             blank_test_sheet.save()
#         except:
#             blank_test_sheet = None
#             equipment_type.is_test_sheet = False
#             equipment_type.save()
#             return render(request, "jobs/error.html", {"message": "Error generating new test sheet. 'is_test_sheet' set to 'False' for eq type."})


#         eq.equipment_mold = mold
#         eq.save()
#         job.equipment.add(eq)
#         job.save()
#         if parent_equipment and parent_mold:
#             eq.parent_equipment = parent_equipment
#             eq.save()
#         else:
#             (print("final fail"))
#         eq.save()
#     except:
#         return render(request, "jobs/error.html", {"message": "Add equipment failed"})

# def get_parent(equipment_id):
#     eq = Equipment.objects.get(pk=equipment_id)
#     if eq.parent_equipment:
#         return eq.parent_equipment.pk
#     else:
#         print("failed to get parent equipment")

# def get_ancestors(equipment_id):
#     eq = Equipment.objects.get(pk=equipment_id)
#     parent = eq.parent_equipment
#     i = 1
#     ancestors = []
#     while i > 0:
#         ancestors.append(get_parent(equipment_id))
#     if eq.parent_equipment:
#         if eq.parent_equipment.pk in batch:
#             get_ancestor(eq.parent_equipment, batch)
#         else:
#             return eq
#     else:
#         return eq
    
# def add_jobsite_eq(request, job_id):
#     job = Job.objects.get(pk=job_id)
#     eq_name = request.POST['adding_name']
#     parent_equipment = None
#     try:
#         mold = Equipment.objects.get(job_site = job.job_site, site_id = eq_name)
#         if mold.parent_equipment:
#             #in this case there is a parent equipment so we need to recursively loop until we find the top parent equipment
#             try:
#                 parent_equipment = mold.parent
#         temp = mold
#         temp.pk = None
#         eq = temp
#         eq.save()
#         equipment_type = eq.equipment_type
#         if equipment_type.is_test_sheet == True:
#             eq.is_insulation_resistance=equipment_type.is_insulation_resistance
#             eq.is_contact_resistance=equipment_type.is_contact_resistance
#             eq.is_trip_unit=equipment_type.is_trip_unit
#             eq.is_primary_injection=equipment_type.is_primary_injection
#             eq.is_secondary_injection=equipment_type.is_secondary_injection
#             eq.is_xfmr_insulation_resistance=equipment_type.is_xfmr_insulation_resistance
#             eq.is_power_fused=equipment_type.is_power_fused
#             eq.is_breaker=equipment_type.is_breaker
#             eq.is_hipot=equipment_type.is_hipot
#             eq.is_inspection=equipment_type.is_inspection
#             eq.is_transformer=equipment_type.is_transformer
#             eq.is_winding_resistance=equipment_type.is_winding_resistance
#             eq.is_ttr=equipment_type.is_ttr
#             eq.is_liquid_type=equipment_type.is_liquid_type
#             eq.is_cable=equipment_type.is_cable
#             eq.is_cable_vlf_withstand_test=equipment_type.is_cable_vlf_withstand_test
#             eq.save()
#         try:
#             blank_test_sheet=TestSheet(eq=eq)
#             blank_test_sheet.save()
#         except:
#             blank_test_sheet = None
#             equipment_type.is_test_sheet = False
#             equipment_type.save()
#             return render(request, "jobs/error.html", {"message": "Error generating new test sheet. 'is_test_sheet' set to 'False' for eq type."})


#         eq.equipment_mold = mold
#         eq.save()
#         job.equipment.add(eq)
#         job.save()
#         if parent_equipment:
#             eq.parent_equipment = parent_equipment
#             eq.save()

#         eq.save()

#     except:
#         return render(request, "jobs/error.html", {"message": "get eq failed. contact admin"})
        
    
#     return HttpResponseRedirect(reverse("job", args=(job_id, )))
        


# .
# .
# .
# .


def equipment_folder(request, equipment_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        equipment=Equipment.objects.get(pk=equipment_id)
        equipment_files = EquipmentFolder.objects.filter(equipment=equipment).exclude(equipment_file='').order_by('-pk')
    except Equipment.DoesNotExist:
        raise Http404("Folder does not exist.")
    context = {
        "equipment": equipment,
        "equipment_files": equipment_files
    }
    if request.user.is_authenticated:
        return render(request, "jobs/equipment_folder.html", context)


def add_equipment_page(request, job_id=None, equipment_id=None, job_site_id=None):
  
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    user_properties = UserProperties.objects.get(user=request.user)
    job = job_id and Job.objects.filter(pk=job_id).first()
    
    job_site = job_site_id and JobSite.objects.filter(pk=job_site_id).first()
    existing_equipment = job and job.equipment.filter(trashed=False)#creates variable with existing untrashed equipment
    parent_equipment = None
    if equipment_id:
        parent_equipment = Equipment.objects.get(pk=equipment_id)
        if not parent_equipment:
            return render(
                request,
                "jobs/error.html", {
                    "message": "Error attaching equipment. Please contact Admin"
                }
            )
    equipment_ids = []
    if job:
        for eq in job.equipment.all():
            equipment_ids.append(eq.site_id)
    json_equipment_ids = json.dumps(equipment_ids)
    types = Type.objects.all()
    manufacturers = Manufacturer.objects.all()
    test_equipments = TestEquipment.objects.all()
    test_equipment_list = json.dumps(list(TestEquipment.objects.values_list('name', flat=True)))
    models = Model.objects.all()
    #get list of all site_ids on the site
    stripped_trashed_site_ids = []
    stripped_trashed_ids = []
    if job_site_id:
        site_ids = json.dumps(list(Equipment.objects.filter(job_site=job_site, trashed=False).values_list('site_id', flat=True)))
        trashed_site_eq = Equipment.objects.filter(job_site=job_site, trashed=True).values_list('site_id', flat=True)
        stripped_trashed_site_ids=[sub[ : -31] for sub in trashed_site_eq]
        trashed_site_ids = json.dumps(list(stripped_trashed_site_ids))
    elif job_id:
        trashed_eq = job.equipment.filter(trashed=True).values_list('site_id', flat=True)
        stripped_trashed_ids=[sub[ : -31] for sub in trashed_eq]
        site_ids = json.dumps(list(Equipment.objects.filter(job_site=job.job_site).values_list('site_id', flat=True)))
        trashed_site_eq = Equipment.objects.filter(job_site=job.job_site, trashed=True).values_list('site_id', flat=True)
        stripped_trashed_site_ids=[sub[ : -31] for sub in trashed_site_eq]
        
    context = {
        "job": job,
        "types": types,
        "manufacturers": manufacturers,
        "models": models,
        "existing_equipment": existing_equipment,
        "test_equipments": test_equipments,
        "test_equipment_list": test_equipment_list,
        "json_equipment_ids": json_equipment_ids,
        "parent_equipment": parent_equipment,
        "job_site": job_site,
        "site_ids": site_ids,
        "stripped_trashed_site_ids":stripped_trashed_site_ids,
        "stripped_trashed_ids":stripped_trashed_ids
    }
    if request.user.is_authenticated and user_properties.company:
        return render(request, "jobs/add_equipment.html", context)
    else:
        return render(request, "jobs/error.html", {"message": "Your profile must be associated with a company to view this information. Contact us for a company key."})

    
def trashed_equipment(request, job_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    job = Job.objects.get(pk=job_id)
    equipments = job.equipment.filter(trashed=True, equipment_mold__trashed=False).order_by('-pk')
    context = {
        "job": job,
        "equipments": equipments,
        "trashed": True
    }
    if request.user.is_authenticated:
        return render(request, "jobs/trashed_equipment.html", context)


def trashed_job_site_equipment(request, job_site_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    job_site = JobSite.objects.get(pk=job_site_id)
    equipments = job_site.equipment_jobsite.filter(trashed=True).order_by('-pk')
    context = {
        "job_site": job_site,
        "equipments": equipments,
        "trashed": True
    }
    if request.user.is_authenticated:
        return render(request, "jobs/trashed_job_site_equipment.html", context)

def types(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        properties = UserProperties.objects.get(user=request.user)
        public_types = Type.objects.exclude(is_private=True).filter(status=None).order_by('name')
        # private_types = Type.objects.filter(is_private=True).filter(company = properties.company).order_by('name')
    except:
        properties = None
    context = {
        "types": public_types,
        "test_equipment": TestEquipment.objects.all()
    }
    if request.user.is_authenticated:
        return render(request, "jobs/types.html", context)

def eq_type(request, type_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        eq_type = Type.objects.get(pk=type_id)
        video_guides=TypeTestGuide.objects.filter(eq_type=eq_type).exclude(type_test_guide='').order_by("-pk")
        type_models = Model.objects.filter(model_type=eq_type).order_by("name")
        type_files = TypeFolder.objects.filter(eq_type=eq_type).exclude(type_file='', file_url='').order_by('-pk')     
        type_notes = eq_type.note_model.filter(parent_note__isnull=True)
        test_equipments = TestEquipment.objects.all()
        test_equipment_list = json.dumps(list(TestEquipment.objects.values_list('name', flat=True)))
        test_standards = TypeTestStandards.objects.filter(ts_type=eq_type)

    except Type.DoesNotExist:
        raise Http404("Type does not exist.")
    context= {
        "type": eq_type,
        "video_guides": video_guides,
        "type_models": type_models,
        "type_files": type_files,
        "type_notes": type_notes,
        "test_equipments": test_equipments,
        "test_equipment_list": test_equipment_list,
        "test_standards": test_standards,
    }
    return render(request, "jobs/eq_type.html", context)

def test_equipment(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    context = {
        "test_equipment": TestEquipment.objects.all().order_by('-pk')
    }
    if request.user.is_authenticated:
        return render(request, "jobs/test_equipment.html", context)

def manufacturers(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    context = {
        "manufacturers": Manufacturer.objects.all().order_by('name')
    }
    if request.user.is_authenticated:
        return render(request, "jobs/manufacturers.html", context)

def models(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    acme = Manufacturer.objects.get(name='ACME Electric')#this needs to be removed and was only placed here for demonstration purposes. Models should not be filtered from view.
    try:
        properties = UserProperties.objects.get(user=request.user)
        public_models=[]
        if properties.company.name == "Admin Company":
            public_models = Model.objects.all().exclude(is_private=True).filter(status=None).order_by('name')
        else:
            public_models = Model.objects.all().exclude(model_manufacturer=acme).filter(status=None).exclude(is_private=True).order_by('name')
        private_models = Model.objects.all().filter(is_private=True).filter(company = properties.company).order_by('name')
    except:
        properties = None
    context = {
        "models": public_models,
        "properties": properties
    }
    if request.user.is_authenticated:
        return render(request, "jobs/models.html", context)

def eq_model(request, model_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        eq_model = Model.objects.get(pk=model_id)
        model_files = ModelFolder.objects.filter(model=eq_model).exclude(model_file='', file_url='').order_by('-pk')
        video_guides=ModelTestGuide.objects.filter(model=eq_model).exclude(model_test_guide='').order_by("-pk")
    except:    
        raise Http404("Model does not exist.")

    try:
        properties = UserProperties.objects.get(user=request.user)
    except UserProperties.DoesNotExist:
        properties = None

    model_notes = eq_model.note_model.filter(parent_note__isnull=True)

    test_equipments = TestEquipment.objects.all()
    test_equipment_list = json.dumps(list(TestEquipment.objects.values_list('name', flat=True)))
    types = Type.objects.all().order_by('name')
    manufacturers = Manufacturer.objects.all().order_by('name')
    context= {
        "properties": properties,
        "model": eq_model,
        "model_files": model_files,
        "video_guides": video_guides,
        "model_notes": model_notes,
        "test_equipments": test_equipments,
        "test_equipment_list": test_equipment_list,
        "types": types,
        "manufacturers": manufacturers
    }
    return render(request, "jobs/eq_model.html", context)
    
def eq_manufacturer(request, manufacturer_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        eq_manufacturer = Manufacturer.objects.get(pk=manufacturer_id)
        models=Model.objects.filter(model_manufacturer=eq_manufacturer)
    except Manufacturer.DoesNotExist:
        raise Http404("Model does not exist.")
    context= {
        "manufacturer": eq_manufacturer,
        "models":models
    }
    return render(request, "jobs/eq_manufacturer.html", context)


def profile(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    user=request.user
    try:
        properties = UserProperties.objects.get(user=request.user)
    except UserProperties.DoesNotExist:
        properties = UserProperties.objects.create(user=request.user)
    except:
        return render(request, "jobs/error.html", {"message": "User profile load error. Contact Admin. 210-303-0471 or albert@blueskysw.com."})
    #create a list of user types (normally will just be one)
    user_types=[]
    if properties.is_fsr:
        user_types.append("Field Service Representative")
    elif properties.is_manager:
        user_types.append("Manager")
    elif properties.is_coordinator:
        user_types.append("Coordinator")
    elif properties.is_salesman:
        user_types.append("Salesman")
    elif properties.is_customer:
        user_types.append("Customer")
    else:
        user_types.append("Unassigned")

    #jobs associated with user
    equipment_supported= properties.equipment_models_supported.all()
    context = {
        "user": user,
        "user_id": user.id,
        "properties": properties,
        "user_types": user_types,
        "equipment_supported": equipment_supported

    }

    if request.user.is_authenticated:
        return render(request, "jobs/profile.html", context)

# FSR info shows the information for a fsr on a job

def fsr_info(request, fsr_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    try:
        users=get_user_model()
        user_base= users.objects.get(pk=fsr_id)
        properties = UserProperties.objects.get(user=request.user)
    except UserProperties.DoesNotExist:
        properties = None
         
    #create a list of user types (normally will just be one)
    user_types=[]
    if properties.is_fsr:
        user_types.append("Field Service Representative")
    if properties.is_manager:
        user_types.append("Manager")
    if properties.is_coordinator:
        user_types.append("Coordinator")
    if properties.is_salesman:
        user_types.append("Salesman")
    if properties.is_customer:
        user_types.append("Customer")
    if properties.is_support:
        user_types.append("Equipment Supporter")
    if not user_types:
        user_types.append("Unassigned")
    #pull equipment supported, if any
    equipment_supported = properties.equipment_models_supported.all()
    #jobs associated with user
    jobs=Job.objects.filter(user_properties = properties)
    context = {
        "properties": properties,
        "user_types": user_types,
        "jobs": jobs,
        "equipment_supported": equipment_supported
    }

    if request.user.is_authenticated:
        return render(request, "jobs/fsr_info.html", context)

def job_archive(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})

    archived_jobs=Job.objects.filter(archived=True)

    context = {
        "archived_jobs": archived_jobs
    }
    if request.user.is_authenticated:
        return render(request, "jobs/job_archive.html", context)

def job_trash(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})

    trashed_jobs=Job.objects.filter(trashed=True)

    context = {
        "trashed_jobs": trashed_jobs
    }
    if request.user.is_authenticated:
        return render(request, "jobs/job_trash.html", context)

def feedback(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    notes=FeedbackNote.objects.all()
    feedback_files=FeedbackFile.objects.all()
    # user = UserProperties.objects.get(user=request.user)
    # company = user.company
    # users = UserProperties.objects.filter(company = company)
    context={
        "notes": notes,
        "feedback_files": feedback_files,
        # "users": users
    }
    if request.user.is_authenticated:
        return render(request, "jobs/feedback.html", context)
        
def working_page(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})
    note=WorkingNote.objects.first()
    
    if note:
        note = note.note
    else:
        note = ""
    context={
        "note": note,
    }
    if request.user.is_authenticated:
        return render(request, "jobs/working_notes.html", context)
        
def agwells(request):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})        
    wells = None
    try:
        properties=UserProperties.objects.get(user=request.user)
        if properties.company:
            if properties.company.company_key == "agapp":
                wells = Well.objects.all().order_by("-pk")
        else:
            return render(request, "jobs/error.html", {"message": "aaaaaaaaaYour profile must be associated with the Agriculture portion of the App to view this information. If you don't have the company key for this, contact us.  Click Edit Profile above to add a key."})         
        
    except:
        properties=None
        pass
    context={
        "wells": wells,
    }    
    # try:
    if request.user.is_authenticated and properties.company:
        return render(request, "jobs/agwells.html", context)
    else:
        return render(request, "jobs/error.html", {"message": "bbbbbbbbbbbbbYour profile must be associated with the Agriculture portion of the App to view this information. If you don't have the company key for this, contact us.  Click Edit Profile above to add a key."})
    # except:
    #     # return render(request, "jobs/jobs.html", context)
    #     return render(request, "jobs/error.html", {"message": "cccccccccccccYour profile must be associated with the Agriculture portion of the App to view this information. If you don't have the company key for this, contact us.  Click Edit Profile above to add a key."})
   
def agwell(request, well_id):
    if not request.user.is_authenticated:
        return render(request, "jobs/login.html", {"message": None})        
    well = None
    maints = None
    try:
        properties=UserProperties.objects.get(user=request.user)
        if properties.company:
            if properties.company.company_key == "agapp":
                well = Well.objects.get(pk = well_id)
                maints = MaintEvent.objects.filter(well=well).order_by("-pk")
        else:
            return render(request, "jobs/error.html", {"message": "aaaaaaaaaaYour profile must be associated with the Agriculture portion of the App to view this information. If you don't have the company key for this, contact us.  Click Edit Profile above to add a key."})         
  
    except:
        properties=None
        pass
    context={
        "well": well,
        "maints": maints,
    }    
    # try:
    if request.user.is_authenticated and properties.company and well:
        return render(request, "jobs/agwell.html", context)
    else:
        return render(request, "jobs/error.html", {"message": "bbbbbbbbbbbYour profile must be associated with the Agriculture portion of the App to view this information. If you don't have the company key for this, contact us.  Click Edit Profile above to add a key."})
    # except:
    #     # return render(request, "jobs/jobs.html", context)
    #     return render(request, "jobs/error.html", {"message": "ccccccccccccccccYour profile must be associated with the Agriculture portion of the App to view this information. If you don't have the company key for this, contact us.  Click Edit Profile above to add a key."})
