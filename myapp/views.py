import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login
#new
from django.core.validators import MinValueValidator, MaxValueValidator
from django.views.decorators.csrf import csrf_exempt

def root_redirect(request):
    return redirect('login')  # redirects to /myapp/login/


def login_get(request):
    return render(request, 'login_page.html')
@csrf_exempt
def loginpost(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username,password=password)
    if user is not None:
        if user.groups.filter(name='admin').exists():
            login(request,user)
            return redirect('/myapp/admin_home/')
        elif user.groups.filter(name='cordinator').exists():
            login(request,user)
            return redirect('/myapp/cordinator_home/')
        else:
            return redirect('/myapp/')
    else:
        return redirect('/myapp/')

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    """
    Logs the user out. Only accept POST requests for the actual logout action.
    If GET, redirect to home (prevent CSRF risks and accidental logouts).
    """
    if request.method == "POST":
        logout(request)
        # Redirect where you want after logout (login page or public home)
        return redirect('/myapp/login/')    # <-- change this if you want /myapp/login/ etc.
    # For GET requests, just redirect (no logout on GET)
    return redirect('/myapp/')

@login_required
def index_page(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    cordinator= Coordinator.objects.all()
    camp = Camp.objects.filter(status='open')
    last_camp = Camp.objects.order_by('-id').first()
    guid= Guideline.objects.all()
    notification= Notification.objects.all()
    rescue=EmergencyRescue.objects.all()
    last_news = News.objects.order_by('-date').first()
    stock=Stock.objects.all()
    stock_count = stock.count()
    camp_count = camp.count()
    cor_count = cordinator.count()
    guid_count = guid.count()
    noti_count = notification.count()
    rescue_count = rescue.count()
    unreplied = Complaint.objects.filter(reply__isnull=True) | Complaint.objects.filter(reply='')
    unreplied_count=unreplied.count()

    return render(request, 'admin/home.html',
                  {'cor_count':cor_count,
                   'camp_count':camp_count,
                   'guid_count':guid_count,
                   'noti_count':noti_count,
                   'rescue_count':rescue_count,
                   'unreplied_count':unreplied_count,
                   'stock_count':stock_count,
                   'last_camp': last_camp,
                   'last_news':last_news})

@login_required
def view_camp(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    camps = Camp.objects.all()
    return render(request, 'admin/view_camp.html', {'camps': camps})
#def view_camp_post(request):
    #district=request.POST['district']
    #type=request.POST['type']

@login_required
def add_camp(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    coordinators = Coordinator.objects.all()
    return render(request, 'admin/add_camp.html',{'coordinators': coordinators})

@login_required
def ad_camp_post(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    if request.method == 'POST':
        camp_name=request.POST['camp_name']
        coordinator_id = request.POST['coordinator']

        coordinator_id = request.POST.get('coordinator')
        
        if not coordinator_id:
            messages.error(request, "Please select a coordinator.")
            return redirect('ad_camp_post')

        coordinator = Coordinator.objects.get(id=coordinator_id)

        district=request.POST['district']
        address=request.POST['address']
        pin=request.POST['pin']
        total_members=request.POST['total-members']
        latitude=request.POST['latitude']
        longitude=request.POST['longitude']
        status=request.POST['status']
        contact = coordinator.phone 

        obj= Camp()
        obj.name=camp_name
        obj.coordinator=coordinator
        obj.district=district
        obj.total_member=total_members
        obj.place=address
        obj.phone=contact
        obj.pin=pin
        obj.status=status
        obj.latitude = float(latitude) if latitude else None
        obj.longitude = float(longitude) if longitude else None
        obj.save()
        messages.success(request,"Camp added successfully!")
        return redirect('view_camp')
    return render(request, 'admin/add_camp.html')

from django.shortcuts import get_object_or_404

@login_required
def edit_camp(request, id):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    obj = get_object_or_404(Camp, id=id)
    coordinators = Coordinator.objects.all()
    if request.method=='POST':
        camp_name=request.POST['camp_name']
        coordinator_id = request.POST['coordinator']

        coordinator_id = request.POST.get('coordinator')
        
        if not coordinator_id:
            messages.error(request, "Please select a coordinator.")
            return redirect('ad_camp_post')

        coordinator = Coordinator.objects.get(id=coordinator_id)

        district=request.POST['district']
        address=request.POST['address']
        pin=request.POST['pin']
        contact=request.POST['contact']
        total_members=request.POST['total-members']
        latitude=request.POST['latitude']
        longitude=request.POST['longitude']
        status=request.POST['status']

        obj.name=camp_name
        obj.coordinator=coordinator
        obj.district=district
        obj.total_member=total_members
        obj.place=address
        obj.phone=contact
        obj.pin=pin
        obj.status=status
        obj.latitude = float(latitude) if latitude else None
        obj.longitude = float(longitude) if longitude else None

        kk = obj.name

        obj.save()
        messages.success(request,f'Camp "{kk}" edited successfully!')
        return redirect('view_camp')
    return render(request, 'admin/edit_camp.html',{'coordinators': coordinators,'obj':obj})


@login_required
def camp_codinator(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    coordinator = Coordinator.objects.all()
    return render(request, 'admin/camp_codinators.html',{'coordinator': coordinator})

#def camp_codinator_post(request):
#   coordinator=request.POST['coordinator']
#   district=request.POST['district']
#   status=request.POST['status']


@login_required
def add_codinator(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    coordinators = Coordinator.objects.all()
    return render(request, 'admin/add_codinators.html', {'coordinators': coordinators})

@login_required
def add_codinator_post(request):
   if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
   if request.method == 'POST':
        

        #login id creator
        

        full_name=request.POST['full_name']
        email=request.POST['email']
        phone=request.POST['phone']
        district=request.POST['district']
        address=request.POST['address']
        pin=request.POST['pin']
        post_office=request.POST['post_office']
        photo_upload = request.FILES.get('photo_upload')  # Use request.FILES instead of request.POST
        username=request.POST['username']
        password=request.POST['password']
        user=User.objects.create(username=username,password=make_password(password))
        user.save()
        user.groups.add(Group.objects.get(name='cordinator'))
        status = request.POST.get('status', 'Active') 

       

        obj=Coordinator()
        obj.login_id=user
        obj.name=full_name
        obj.email = email
        obj.phone = phone
        obj.district = district
        obj.place = address 
        obj.post = post_office
        obj.pin = pin
        obj.photo = photo_upload 
        obj.username =username
        obj.status = status
        kk = obj.name
        obj.save()

        messages.success(request, f'Coordinator "{kk}" added successfully!')
        return redirect("cordinators")
   
@login_required
def edit_coordinator(request, id):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    obj = get_object_or_404(Coordinator, id=id)
    if request.method == 'POST':
        #login id creator

        full_name=request.POST['full_name']
        email=request.POST['email']
        phone=request.POST['phone']
        district=request.POST['district']
        address=request.POST['address']
        pin=request.POST['pin']
        post_office=request.POST['post_office']
        photo_upload = request.FILES.get('photo_upload')  # New file if uploaded
        username=request.POST['username']
        password=request.POST['password']
        status = request.POST.get('status', 'Active') 

                
        obj.name=full_name
        obj.email = email
        obj.phone = phone
        obj.place = address 
        obj.post = post_office
        obj.pin = pin
        obj.username =username

        kk=obj.name
        

        if district:
            obj.district = district

        if status:
            obj.status = status

        if photo_upload:
            obj.photo = photo_upload

        if password.strip():  # only update if password field not empty
            user = obj.login_id  # linked Django User
            user.set_password(password)  # hashes automatically
            user.save()    

        obj.save()

        messages.success(request, f'Coordinator "{kk}" edited successfully!')
        return redirect("cordinators")  
     
    return render(request,'admin/edit_coordinators.html',{'obj':obj})

@login_required
def delete_coordinator(request, id):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    coordinator = get_object_or_404(Coordinator, id=id)
    name = coordinator.name
    try:
        # Delete associated User
        if coordinator.login_id:
            coordinator.login_id.delete()
        coordinator.delete()
        messages.success(request, f'Coordinator "{name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting coordinator: {e}')
    return redirect('cordinators')

@login_required
def guid_codinator(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    coordinator = Coordinator.objects.all()
    guidlines = Guideline.objects.all()
    return render(request, 'admin/guid_cordinator.html',
                  {'coordinator':coordinator,
                   'guidlines':guidlines})

@login_required
def guid_codinator_post(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    
    coordinator_id = request.POST['coordinator']

    coordinator_id = request.POST.get('coordinator')
        
    if not coordinator_id:
            messages.error(request, "Please select a coordinator.")
            return redirect('ad_camp_post')

    coordinator = Coordinator.objects.get(id=coordinator_id)

    guidlines_title=request.POST['guideline_title']
    guidline=request.POST['guideline_content']
    priority=request.POST['priority']
    date=request.POST['date']

    obj=Guideline()
    obj.coordinator=coordinator
    obj.title=guidlines_title 
    obj.guideline =guidline
    obj.date=date
    obj.priority=priority

    kk = coordinator.name

    obj.save()

    messages.success(request,f'guidline to "{kk}" added successfully')

    return redirect('guidlines')


@login_required
def complaint_manage(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    obj=Complaint.objects.all()
    return render(request, 'admin/complaint_mange.html',{"obj":obj})

@login_required
def complaint_manage_replay(request, id):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    if request.method == 'POST':
        obj = get_object_or_404(Complaint, id=id)
        replay = request.POST.get('replay', '').strip()
        obj.reply = replay
        obj.save()
        messages.success(request, 'Reply provided successfully.')
        return redirect('complaint_manage')  # redirect back to list page
    else:
        return redirect('complaint_manage')
    
@login_required    
def map(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    return render(request, 'admin/map.html')
          

@login_required
def emergency_res(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    teams = EmergencyRescue.objects.all()
    return render(request, 'admin/emergency_responce.html',{'teams':teams})


@login_required
def add_rescue(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')

    if request.method=='POST':
        person_name = request.POST['name']     
        phone = request.POST['phone']               
        district = request.POST['district']              
        place = request.POST['place']       
        role = request.POST['role']            
        p_lat = request.POST['latitude' ]           
        p_lng = request.POST['longitude']             
        p_notes = request.POST['notes'] 
        email = request.POST['email'] 
        post = request.POST['post'] 
        pin = request.POST['pin'] 
        status = request.POST['status'] 


        
        username=request.POST['username']
        password=request.POST['password']
        user=User.objects.create(username=username,password=make_password(password))
        user.save()
        user.groups.add(Group.objects.get(name='emergency_rescue'))


        obj=EmergencyRescue()
        obj.post = post
        obj.name = person_name
        obj.login_id=user
        obj.phone = phone
        obj.place = place
        obj.district = district  
        obj.role = role    
        obj.latitude = p_lat
        obj.longitude = p_lng
        obj.notes = p_notes 
        obj.email = email
        obj.pin  =pin
        obj.status=status

        obj.save()
        messages.success(request,"Rescue team added successfully")
        return redirect('emergency_res')      
    return render(request,'admin/add_rescue.html')    

@login_required
def edit_rescue(request, id):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    obj = get_object_or_404(EmergencyRescue, id=id)
    if request.method == 'POST':
        person_name = request.POST['name']     
        phone = request.POST['phone']               
        district = request.POST['district']              
        place = request.POST['place']       
        role = request.POST['role']            
        p_lat = request.POST['latitude' ]           
        p_lng = request.POST['longitude']             
        p_notes = request.POST['notes'] 
        email = request.POST['email'] 
        post = request.POST['post'] 
        pin = request.POST['pin'] 
        status = request.POST['status'] 
        username = request.POST['username']
        password = request.POST['password']

        obj.post = post
        obj.name = person_name
        obj.phone = phone
        obj.place = place
        obj.role = role    
        obj.latitude = p_lat
        obj.longitude = p_lng
        obj.notes = p_notes 
        obj.email = email
        obj.pin  =pin
        obj.username =username

        if district:
            obj.district = district

        if status:
            obj.status = status

        
        if password.strip():  # only update if password field not empty
            user = obj.login_id  # linked Django User
            user.set_password(password)  # hashes automatically
            user.save()    

        obj.save()

        messages.success(request,"Rescue team edited successfully")
        return redirect('emergency_res') 
        
    return render(request, 'admin/edit_rescue.html',{'obj':obj})

@login_required
def delete_rescue(request, id):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    rescue = get_object_or_404(EmergencyRescue, id=id)
    name = rescue.name
    try:
        # Delete associated User
        if rescue.login_id:
            rescue.login_id.delete()
        rescue.delete()
        messages.success(request, f'rescue "{name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting rescue: {e}')
    return redirect('emergency_res')


@login_required
def password_change(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    return render(request, 'admin/password.html')

from django.contrib.auth import update_session_auth_hash

@login_required
def admin_password_post(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    old_password=request.POST['curpass']
    new_password=request.POST['newpass']
    confirm_password=request.POST['confirmpass']
    user=request.user
    if not user.check_password(old_password):
        
        return redirect('/myapp/change_pass/')
    if new_password != confirm_password:
        return redirect('/myapp/change_pass/')
    user.set_password(confirm_password)
    user.save()
    update_session_auth_hash(request,user)
    return redirect('/myapp/')





@login_required
def notification(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    notification = Notification.objects.all()
    return render(request, 'admin/notification.html',{'notification': notification})

from datetime import datetime

@login_required
def notification_post(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    title=request.POST['title']
    role=request.POST['role']
    district=request.POST['district']
    phone=request.POST['phone']
    address=request.POST['address']

    def to_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
            
    latitude = to_float(request.POST.get('latitude'))
    longitude = to_float(request.POST.get('longitude'))
    details=request.POST['details']

    datetime_value = request.POST.get('datetime')  # matches input name="datetime"

        
    if datetime_value:
            dt_object = datetime.strptime(datetime_value, "%Y-%m-%dT%H:%M")
    else:
            dt_object = None

    obj=Notification()
    obj.roll=role
    obj.district=district
    obj.title=title
    obj.phone=phone
    obj.date=dt_object
    obj.address=address
    obj.latitude=latitude
    obj.longitude=longitude
    obj.description=details
    obj.save()

    return redirect('notifications')


@login_required
def inventories(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    camp=Camp.objects.all()
    return render(request, 'admin/inventories.html',{'camp':camp})

@login_required
def inventories_post(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    camp=request.POST['camp']

@login_required
def admin_profile(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    admin = Admin.objects.all()
    return render(request, 'admin/profile.html',{'admin':admin})

@login_required
def news(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    obj=News.objects.all()
    return render(request, 'admin/news.html',{'obj':obj})








def my_coordinator_profile(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    coordinator = Coordinator.objects.get(login_id=request.user)
    return render(request, 'camp_cordinator/cordinator_profile.html', {'coordinator': coordinator})

def cordinator_home(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    return render(request, 'camp_cordinator/home_cord.html')

def medical_support(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    cordinator= get_object_or_404(Coordinator, login_id = request.user)
    obj= Medicine.objects.filter(coordinator=cordinator)
    return render(request, 'camp_cordinator/medical_support.html',{'obj':obj})

def medical_support_post(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    if request.method=='POST':
        coordinator = Coordinator.objects.get(login_id=request.user)
        medicine=request.POST['medicine']
        qnty=request.POST['quantity']

        obj=Medicine()
        obj.coordinator=coordinator
        obj.medicine=medicine
        obj.quantity=qnty
        obj.save()
        messages.success(request,"New Medicine Request added succesfully")
        return redirect('medical_support')
    return render(request,'camp_cordinator/add_medicine.html')

def delete_medicine_request(request,id):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    obj= get_object_or_404(Medicine, id=id)
    item= obj.medicine
    qt=obj.quantity
    obj.delete()
    messages.success(request,f'Request for "{qt}"  "{item}" is deleted ')
    return redirect('medical_support')

def member_register(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    co= get_object_or_404(Coordinator, login_id=request.user)
    obj=Volunteer.objects.filter(coordinator=co)
    return render(request, 'camp_cordinator/member register.html',{'obj':obj,'co':co})

def add_member(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    if request.method=='POST':
        coordinator = Coordinator.objects.get(login_id=request.user)
        name=request.POST['name']
        email=request.POST['email']
        place=request.POST['place']
        post=request.POST['post']
        pin=request.POST['pin']
        phone=request.POST['phone']
        district=request.POST['district']
        age=request.POST['age']
        gender=request.POST['gender']

        username=request.POST['username']
        password=request.POST['password']
        user=User.objects.create(username=username,password=make_password(password))
        user.save()
        user.groups.add(Group.objects.get(name='volunteer'))
        

        obj=Volunteer()
        obj.name=name
        obj.login_id=user
        obj.email=email
        obj.place=place
        obj.post=post
        obj.pin=pin
        obj.coordinator=coordinator
        obj.phone=phone
        obj.district=district
        obj.age=age
        obj.username=username
        obj.gender=gender
        obj.save()
        messages.success(request,"New volunteer added succesfully")
        return redirect('member_register')
    return render(request,'camp_cordinator/add_member.html')

def edit_member(request, id):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    volunteer = get_object_or_404(Volunteer, id=id)

    if request.method == 'POST':
        coordinator = Coordinator.objects.get(login_id=request.user)

        volunteer.name = request.POST['name']
        volunteer.email = request.POST['email']
        volunteer.place = request.POST['place']
        volunteer.post = request.POST['post']
        volunteer.pin = request.POST['pin']
        volunteer.phone = request.POST['phone']
        volunteer.district = request.POST['district']
        volunteer.age = request.POST['age']
        volunteer.gender = request.POST['gender']
        volunteer.coordinator = coordinator

        # Update linked user details
        user = volunteer.login_id
        user.username = request.POST['username']

        password = request.POST.get('password')
        if password:  # only update password if provided
            user.password = make_password(password)
        user.save()

        volunteer.save()
        messages.success(request, "Volunteer updated successfully")
        return redirect('member_register')

    return render(request, 'camp_cordinator/edit_member.html', {'obj': volunteer})


def delete_member(request, id):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    volunteer = get_object_or_404(Volunteer, id=id)
    
    user = volunteer.login_id
    volunteer.delete()
    user.delete()
    
    messages.success(request, "Volunteer deleted successfully.")
    return redirect('member_register')

def stock_management(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    coordinator = get_object_or_404(Coordinator, login_id=request.user)
    obj = Stock.objects.filter(coordinator=coordinator).order_by('-date', '-id')
    return render(request, 'camp_cordinator/stock_management.html', {'obj': obj})

from django.contrib.auth.decorators import login_required

def stock_management_post(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    if request.method=='POST':
        type=request.POST['type']
        count=request.POST['count']
        date = datetime.today().date()
        coordinator = Coordinator.objects.get(login_id=request.user)

        obj=Stock()
        obj.type=type
        obj.count=count
        obj.date=date
        obj.coordinator=coordinator
        no=obj.count
        item=obj.type
        obj.save()
        messages.success(request, f'"{no}" "{item}" added successfully')

        return redirect('stock_management')
    return render(request,'camp_cordinator/add_stock.html')

def edit_stock(request, id):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    obj = Stock.objects.get(id=id)
    if request.method=='POST':
        type=request.POST['type']
        count=request.POST['count']
        date = datetime.today().date()
        coordinator = Coordinator.objects.get(login_id=request.user)

        obj=Stock()
        obj.type=type
        obj.count=count
        obj.date=date
        obj.coordinator=coordinator
        no=obj.count
        item=obj.type
        obj.save()
        messages.success(request, f'"{item}" updated successfully')

        return redirect('stock_management')
    return render(request,'camp_cordinator/edit_stock.html',{'obj':obj})

def delete_stock(request, id):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    stock = get_object_or_404 (Stock ,id=id)
    no=stock.count
    item=stock.type
    stock.delete()
    messages.success(request, f'"{no}" "{item}" added successfully')
    return redirect('stock_management')


def manage_needs(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    cordinator= get_object_or_404(Coordinator, login_id = request.user)
    obj= Needs.objects.filter(coordinator=cordinator)
    return render(request, 'camp_cordinator/manage_needs.html',{'obj':obj})

def manage_needs_post(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')

    if request.method=='POST':
        type=request.POST['type']
        description=request.POST['description']
        count=request.POST['count']
        date = datetime.today().date()
        coordinator = Coordinator.objects.get(login_id=request.user)

        obj=Needs()
        obj.type=type
        obj.description=description
        obj.coordinator=coordinator
        obj.date=date
        obj.count=count
        obj.save()
        return redirect('manage_needs')
    return render(request,'camp_cordinator/add_needs.html')

def edit_needs(request, id):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    obj = get_object_or_404(Needs, id=id)
    if request.method=='POST':
        type=request.POST['type']
        description=request.POST['description']
        count=request.POST['count']
        status = request.POST['status']
        date = datetime.today().date()
        coordinator = Coordinator.objects.get(login_id=request.user)

        obj.type=type
        obj.description=description
        obj.coordinator=coordinator
        obj.date=date
        obj.count=count
        item=obj.type
        obj.status=status
        obj.save()
        messages.success(request, f' "{item}" edited successfully')
        return redirect('manage_needs')
    return render(request,'camp_cordinator/edit_needs.html',{'obj':obj})

def delete_needs(request, id):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    obj =get_object_or_404(Needs,id=id)
    item=obj.type
    obj.delete()
    messages.success(request, f' "{item}" deleted successfully')
    return redirect('manage_needs')

def view_user_report(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    alerts=EmergencyAlert.objects.all()
    return render(request, 'camp_cordinator/view_user_report.html',{'alerts':alerts})

def change_password(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    return render(request, 'camp_cordinator/change_password.html')


from django.contrib.auth import update_session_auth_hash

def coordinator_password_post(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    old_password=request.POST['currpass']
    new_password=request.POST['newpass']
    confirm_password=request.POST['conpass']
    user=request.user
    if not user.check_password(old_password):
        messages.error(request,"Incurrect old Password")
        return redirect('co_pass_change')
    if new_password != confirm_password:
        return redirect('co_pass_change')
    user.set_password(confirm_password)
    user.save()
    update_session_auth_hash(request,user)
    return redirect('/myapp/')




def news_report(request):
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    obj=News.objects.all()
    return render(request, 'camp_cordinator/news_report.html',{'obj':obj})





















# "==============================flutter==============================================="
def logincode(request):
    print(request.POST)
    un = request.POST['username']
    pwd = request.POST['password']
    user=authenticate(username=un,password=pwd)
    if user is not None:
        if user.groups.filter(name='user').exists():
            print("in user function")
            data = {"task": "valid", "lid": user.id,"type":'user'}
            r = json.dumps(data)
            print(r)
            return HttpResponse(r)
        elif user.groups.filter(name='volunteer').exists():
            print("in volunteer function")
            data = {"task": "valid", "lid": user.id,"type":'volunteer'}
            r = json.dumps(data)
            print(r)
            return HttpResponse(r)
        elif user.groups.filter(name='emergency_response').exists():
            print("in emergency_response function")
            data = {"task": "valid", "lid": user.id,"type":'emergency_response'}
            r = json.dumps(data)
            print(r)
            return HttpResponse(r)

        else:
            data = {"task": "invalid"}
            r = json.dumps(data)
            print(r)
            return HttpResponse(r)
        




def viewnews_flutter(request):
    ob=News.objects.all()
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'news':i.news,'details':i.details,'phone':i.phone,'regno':i.regno,'email':i.email,'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})
