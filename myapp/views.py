import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate,login
#new
from django.core.validators import MinValueValidator, MaxValueValidator
from django.views.decorators.csrf import csrf_exempt

def root_redirect(request):
    return redirect('login')


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
            return redirect('/myapp/login/')
    else:
        return redirect('/myapp/login/')

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
        pin=request.POST.get('pin', '')
        contact=request.POST.get('contact', '')
        total_members=request.POST.get('total-members', '')
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
        target_group, _ = Group.objects.get_or_create(name='emergency_rescue')
        user.groups.add(target_group)


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
    return render(request, 'admin/profile.html', {'admin': request.user})

@login_required
def news(request):
    if not request.user.groups.filter(name='admin').exists():
            logout(request)
            return redirect('/myapp/login/')
    obj=News.objects.all()
    return render(request, 'admin/news.html',{'obj':obj})

@login_required
def admin_view_news_reporter(request):
    a=News_reporter.objects.all()
    return render(request,"admin/view news reporter.html",{"data":a})

@login_required
def accept_news_reporter(request,id):
    a=News_reporter.objects.get(id=id)
    a.status="accepted"
    a.save()
    return redirect('/myapp/admin_view_news_reporter/')
@login_required
def reject_news_reporter(request,id):
    a=News_reporter.objects.get(id=id)
    a.status="rejected"
    a.save()
    return redirect('/myapp/admin_view_news_reporter/')




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
    coordinator = get_object_or_404(Coordinator, login_id=request.user)
    guid=Guideline.objects.filter(coordinator=coordinator)
    guid_count=guid.count()
    vol=Volunteer.objects.filter(coordinator=coordinator)
    vol_count = vol.count()
    stock=Stock.objects.filter(coordinator=coordinator)
    stock_count = stock.count()
    need = Needs.objects.filter(coordinator=coordinator, status="Pending")
    need_count = need.count()
    res = Medicine.objects.filter(coordinator=coordinator, status="Pending")
    res_count = res.count()
    rep=Notification.objects.all()
    rep_count=rep.count()
    return render(request, 'camp_cordinator/home_cord.html',
                    {'guid_count':guid_count,
                     'vol_count':vol_count,
                     'stock_count':stock_count,
                     'need_count':need_count,
                     'res_count':res_count,
                     'rep_count':rep_count,
                     })

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

        from datetime import datetime
        date = datetime.today()
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
    request.session['sid']=id
    if not request.user.groups.filter(name='cordinator').exists():
            logout(request)
            return redirect('/myapp/cordinator_home/')
    obj = Stock.objects.get(id=id)
    if request.method=='POST':
        type=request.POST['type']
        count=request.POST['count']
        date = datetime.today().date()
        coordinator = Coordinator.objects.get(login_id=request.user)

        obj=Stock.objects.get(id=request.session['sid'])
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


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


def delete_stock(request, id):
    # Security check
    if not request.user.groups.filter(name='cordinator').exists():
        return redirect('stock_management')

    stock = get_object_or_404(Stock, id=id)
    count = stock.count
    item_name = stock.type

    stock.delete()

    messages.success(request, f'Stock item "{item_name}" ({count} units) has been deleted.')
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
        date = datetime.datetime.today().date()
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


def guid_cord_view(request):
    # make sure the group name is correct in your project ('cordinator' vs 'coordinator')
    if not request.user.is_authenticated or not request.user.groups.filter(name='cordinator').exists():
        logout(request)
        return redirect('/myapp/cordinator_home/')

    coordinator = get_object_or_404(Coordinator, login_id=request.user)
    guidelines = Guideline.objects.filter(coordinator=coordinator).order_by('-date')
    return render(request, "camp_cordinator/guid_cord.html", {"guidelines": guidelines})














from django.views.decorators.csrf import csrf_exempt

# "==============================flutter==============================================="
@csrf_exempt
def logincode(request):
    print(request.POST)
    un = request.POST['username']
    pwd = request.POST['password']
    user=authenticate(username=un,password=pwd)
    print(user,"####################")
    if user is not None:
        if user.groups.filter(name='public').exists():
            print("in user function")
            data = {"task": "valid", "lid": user.id,"type":'public'}
            r = json.dumps(data)
            print(r)
            return JsonResponse(data)
        elif user.groups.filter(name='volunteer').exists():
            print("in volunteer function")
            data = {"task": "valid", "lid": user.id,"type":'volunteer'}
            r = json.dumps(data)
            print(r)
            return JsonResponse(data)
        elif user.groups.filter(name='emergency_rescue').exists():
            print("in emergency_response function")
            data = {"task": "valid", "lid": user.id,"type":'emergency_rescue'}
            r = json.dumps(data)
            print(r)
            return JsonResponse(data)
        elif user.groups.filter(name='news_reporter').exists():
            print("in news_reporter function")
            data = {"task": "valid", "lid": user.id, "type": 'news_reporter'}
            r = json.dumps(data)
            print(r)
            return JsonResponse(data)

        else:
            data = {"task": "invalid", "type": "none"}
            r = json.dumps(data)
            print(r)
            return JsonResponse(data)
    else:
        # Avoid ValueError: The view didn't return an HttpResponse object
        return JsonResponse({"task": "invalid", "error": "Invalid credentials", "type": "none"})



#==========vulenteer=============

@csrf_exempt
def volunteer_home(request):
    user = request.user

    try:
        data = {}

        volunteer = Volunteer.objects.get(login_id=user)
        data['name'] = volunteer.name
        data['camp'] = volunteer.Coordinator.Camp.name

        return JsonResponse({"task": "success", "data": data})
    except Volunteer.DoesNotExist:
        return JsonResponse({"task": "failed", "error": "invalid_id"})


@csrf_exempt
def view_needs_volunteer(request):

    volunteer = Volunteer.objects.get(login_id=request.user)

    needs = Needs.objects.filter(coordinator=volunteer.coordinator)

    data = [{
        "id": n.id,
        "type": n.type,
        "description": n.description,
        "count": n.count,
        "date": str(n.date) if n.date else None,
        "status": n.status
    } for n in needs]

    return JsonResponse({"task": "success", "data": data})

@csrf_exempt
def create_medical_request_volunteer(request):

    volunteer = Volunteer.objects.get(login_id=request.user)

    med_id = request.POST.get("medicine_id")

    medicine = Medicine.objects.get(id=med_id)

    mr = MedicalRequest.objects.create(
        volunteer=volunteer,
        medicine=medicine,
        status="Pending"
    )

    return JsonResponse({
        "task": "success",
        "medical_request_id": mr.id
    })

@csrf_exempt
def view_services_volunteer(request):

    volunteer = Volunteer.objects.get(login_id=request.user)

    services = Services.objects.filter(volunteer=volunteer)

    data = [{
        "id": s.id,
        "servicetype": s.servicetype,
        "details": s.details
    } for s in services]

    return JsonResponse({"task": "success", "data": data})

@csrf_exempt
def add_service_volunteer(request):

    volunteer = Volunteer.objects.get(login_id=request.user)

    servicetype = request.POST.get("servicetype")
    details = request.POST.get("details")

    s = Services.objects.create(
        volunteer=volunteer,
        servicetype=servicetype,
        details=details
    )

    return JsonResponse({
        "task": "success",
        "service_id": s.id
    })


@csrf_exempt
def chatbot_volunteer(request):

    return JsonResponse({
        "task": "success",
        "reply": ""
    })

@csrf_exempt
def view_donated_goods_volunteer(request):

    donations = DonateGoods.objects.all()

    data = [{
        "id": d.id,
        "item": d.item,
        "quantity": d.quantity,
        "status": d.status,
        "date": str(d.date) if d.date else None
    } for d in donations]

    return JsonResponse({"task": "success", "data": data})

@csrf_exempt
def collect_donation(request):
    volunteer = Volunteer.objects.get(login_id=request.user)

    donation_id = request.POST.get("donation_id")

    d = DonateGoods.objects.get(id=donation_id)
    d.volunteer = volunteer
    d.status = "Collected"
    d.save()

    return JsonResponse({"task": "success"})


@csrf_exempt
def news_reporter_registration(request):
    name=request.POST["name"]
    place=request.POST["place"]
    post=request.POST["post"]
    phone=request.POST["phone"]
    chanelname=request.POST["chanelname"]
    photo=request.FILES["photo"]
    username=request.POST["username"]
    password=request.POST["password"]
    user = User.objects.create(username=username, password=make_password(password))
    user.save()
    target_group, _ = Group.objects.get_or_create(name='news_reporter')
    user.groups.add(target_group)
    
    a=News_reporter()
    a.name=name
    a.place=place
    a.post=post
    a.phone=phone
    a.chanelname=chanelname
    a.photo=photo
    a.status='pending'
    a.LOGIN=user
    a.save()
    return JsonResponse({"task": "success"})


@csrf_exempt
def add_news(request):
    news=request.POST["news"]
    details = request.POST["details"]
    image = request.FILES["image"]
    date=request.POST["date"]
    lid=request.POST["lid"]

    a=News()
    a.news=news
    a.details=details
    a.image=image
    a.date=date
    a.NEWS_REPORTER=News_reporter.objects.get(LOGIN_id=lid)
    a.save()
    return JsonResponse({"task": "success"})


@csrf_exempt
def view_news(request):
    lid=request.POST["lid"]
    a=News.objects.filter(NEWS_REPORTER__LOGIN_id=lid)
    l=[]
    for i in a:
        l.append({"id":i.id,"news":i.news,"details":i.details,"date":i.date,"image":i.image.url})
    return JsonResponse({"task": "success", "data": l})


@csrf_exempt
def edit_news(request):
    # Pass the news ID from Flutter to identify which record to update
    nid = request.POST["nid"]
    news = request.POST["news"]
    details = request.POST["details"]
    date = request.POST["date"]

    a = News.objects.get(id=nid)
    a.news = news
    a.details = details
    a.date = date

    # Only update image if a new one is provided
    if 'image' in request.FILES:
        a.image = request.FILES["image"]

    a.save()
    return JsonResponse({"task": "success"})


@csrf_exempt
def delete_news(request):

    news_id = request.POST["nid"]

    try:
        a = News.objects.get(id=news_id)
        a.delete()
        return JsonResponse({"task": "success"})
    except News.DoesNotExist:
        return JsonResponse({"task": "failed", "error": "News not found"})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import News_reporter


@csrf_exempt  # Required if you are not sending a CSRF token from Flutter
def reporter_view_profile(request):
    if request.method == "POST":
        try:
            lid = request.POST.get("lid")


            a = News_reporter.objects.get(LOGIN_id=lid)

            photo_url = request.build_absolute_uri(a.photo.url) if a.photo else ""

            return JsonResponse({
                "status": "success",
                "name": a.name,
                "place": a.place,
                "post": a.post,
                "phone": a.phone,
                "chanelname": a.chanelname,
                "photo": photo_url
            })

        except News_reporter.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Reporter not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Replace 'User' with your actual model name if it's different (e.g., Login)
from .models import User


from django.contrib.auth.models import User # Or your custom model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def user_change_password(request):
    oldpassword = request.POST['oldpassword']
    newpassword = request.POST['newpassword']
    lid = request.POST['lid']

    auth_user = User.objects.get(id=lid)
    f = check_password(oldpassword, auth_user.password)
    if f:
        auth_user.set_password(newpassword)
        auth_user.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'failed'})

##################################################################



@csrf_exempt
def public_view_news(request):
    a=News.objects.all()
    l=[]
    for i in a:
        l.append({"id":i.id,
                  "news":i.news,
                  "details":i.details,
                  "date":i.date,
                  "image":i.image.url,
                  "news_reporter":i.NEWS_REPORTER.chanelname
                  })
    return JsonResponse({"status":"ok","data":l})

@csrf_exempt
def public_registration(request):
    name=request.POST["name"]
    phone=request.POST["phone"]
    email=request.POST["email"]
    photo=request.FILES["photo"]
    username=request.POST["username"]
    password=request.POST["password"]

    if User.objects.filter(username=username).exists():
        return JsonResponse({'msg':'username already exists'})


    user = User.objects.create(username=username, password=make_password(password))
    user.save()
    target_group, _ = Group.objects.get_or_create(name='public')
    user.groups.add(target_group)

    a=Public()
    a.name=name
    a.phone=phone
    a.email=email
    a.photo=photo
    a.login_id=user
    a.save()
    return JsonResponse({"status":"ok"})


from django.http import JsonResponse
from .models import Public


@csrf_exempt
def public_view_profile(request):
    if request.method == "POST":
        try:
            lid = request.POST.get("lid")
            # Using get() is better to avoid MultiValueDictKeyError
            if not lid:
                return JsonResponse({"status": "error", "message": "LID is missing"})

            a = Public.objects.get(login_id_id=lid)


            photo_url = request.build_absolute_uri(a.photo.url) if a.photo else ""

            return JsonResponse({
                "status": "ok",
                "name": a.name,
                "phone": a.phone,
                "email": a.email,
                "photo": photo_url
            })

        except Public.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User profile not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})
##########################################################################
@csrf_exempt
def volunteer_view_medicines(request):
    a=Medicine.objects.all()
    l=[]
    for i in a:
        l.append({"id":str(i.id),"medicine":i.medicine})
    return JsonResponse({"status":"ok","data":l})







@csrf_exempt
def volunteer_view_needs(request):
    if request.method == 'POST':
        data = Needs.objects.all().order_by('-date')
        l = []
        for i in data:
            l.append({
                "id": str(i.id),
                "type": i.type,
                "description": i.description,
                "count": i.count,
                "date": str(i.date) if i.date else "",
                "status": i.status,
                "coordnator": i.coordinator.name if i.coordinator else "No Coordinator"
            })
        return JsonResponse({"status": "ok", "data": l})
    return JsonResponse({"status": "error", "message": "Invalid request"})


from django.http import JsonResponse

@csrf_exempt
def volunteer_view_donations(request):
    try:
        # Get volunteer login ID from the Flutter app
        volunteer_lid = request.POST.get('lid')

        # Filter donations assigned to this specific volunteer
        donations = DonateGoods.objects.filter(volunteer__login_id=volunteer_lid).order_by('-date')

        data_list = []
        for d in donations:
            # Default values if Public is missing
            donor_data = {
                "id": d.id,
                "item": d.item,
                "quantity": d.quantity,
                "status": d.status,
                "date": d.date.strftime("%d %b %Y"),
                "camp_name": d.camp.name,
                "donor_name": "Anonymous",
                "donor_phone": "N/A",
                "donor_email": "N/A",
                "donor_photo": "",
            }

            # If Public relation exists, populate full details
            if d.Public:
                donor_data["donor_name"] = d.Public.name
                donor_data["donor_phone"] = str(d.Public.phone)
                donor_data["donor_email"] = d.Public.email
                if d.Public.photo:
                    # build_absolute_uri ensures the Flutter app gets the full URL (http://ip/media/...)
                    donor_data["donor_photo"] = request.build_absolute_uri(d.Public.photo.url)

            data_list.append(donor_data)

        return JsonResponse({"status": "ok", "data": data_list})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt
def volunteer_view_profile(request):
    lid=request.POST["lid"]
    a=Volunteer.objects.get(login_id=lid)
    return JsonResponse({"status":"ok","name":a.name,"email":a.email,"phone":a.phone,"place":a.place,"post":a.post,"pin":a.pin,"district":a.district,"age":a.age,"gender":a.gender,"coordinator":a.coordinator.name})

@csrf_exempt
def add_medical_support_vol(request):
    lid=request.POST["lid"]
    mid=request.POST["mid"]
    a=MedicalRequest()
    a.volunteer=Volunteer.objects.get(login_id=lid)
    a.medicine_id=mid
    a.status="pending"
    a.save()
    return JsonResponse({"status":"ok"})

@csrf_exempt
def view_medical_support_vol(request):
    lid=request.POST["lid"]
    a=MedicalRequest.objects.filter(volunteer__login_id=lid)
    l=[]
    for i in a:
        l.append({"id":str(i.id),"medicine":i.medicine.medicine,"status":i.status})

    return JsonResponse({"status":"ok","data":l})

@csrf_exempt
def add_services(request):
    lid=request.POST["lid"]
    servicetype=request.POST["servicetype"]
    details=request.POST["details"]
    a=Services()
    a.servicetype=servicetype
    a.details=details
    a.volunteer=Volunteer.objects.get(login_id=lid)
    a.save()
    return JsonResponse({"status":"ok"})

@csrf_exempt
def volunteer_view_services(request):
    lid=request.POST["lid"]
    a=Services.objects.filter(volunteer__login_id=lid)
    l=[]
    for i in a:
        l.append({"id":i.id,"servicetype":i.servicetype,"details":i.details})
    return JsonResponse({"status":"ok","data":l})

@csrf_exempt
def volunteer_change_password(request):
    oldpassword = request.POST['oldpassword']
    newpassword = request.POST['newpassword']
    lid = request.POST['lid']

    auth_user = User.objects.get(id=lid)
    f = check_password(oldpassword, auth_user.password)
    if f:
        auth_user.set_password(newpassword)
        auth_user.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'failed'})

@csrf_exempt
def view_donation_vol(request):
    lid=request.POST["lid"]
    a=DonateGoods.objects.filter(volunteer__login_id_id=lid)
    l=[]
    for i in a:
        l.append({"id":i.id,"public":i.Public.name,"camp":i.camp.name,"quantity":i.quantity,"status":i.status})

import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os

# Configure Google Gemini API
GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY', '')  # Set this in your Render Environment Variables
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini Model
model = genai.GenerativeModel('gemini-2.5-flash')


@csrf_exempt
# def chatbot_response(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#
#             user_message = data.get('message', '').strip()
#             lid = data.get('lid')
#
#             if not user_message:
#                 return JsonResponse({'response': 'Please enter a valid question.'})
#
#             if not lid:
#                 return JsonResponse({'response': 'User ID missing in request'}, status=400)
#
#             usertable = User.objects.get(id=lid)
#
#             bot_response = model.generate_content(user_message).text.strip()
#
#             Chatbot.objects.create(
#                 LOGIN=usertable,
#                 date=datetime.now().today(),
#                 question=user_message,
#                 answer=bot_response
#             )
#
#             return JsonResponse({'response': bot_response})
#
#         except User.DoesNotExist:
#             return JsonResponse({'response': 'User not found'}, status=404)
#
#         except Exception as e:
#             print(e)
#             return JsonResponse({'response': str(e)}, status=500)
#
#     return JsonResponse({'response': 'Invalid method'}, status=405)
#
#
# @csrf_exempt
def chat_history(request):
    try:
        lid = request.GET.get('lid')

        if not lid:
            return JsonResponse({'response': 'User ID missing'}, status=400)

        usertable = User.objects.get(id=lid)

        chats = Chatbot.objects.filter(LOGIN=usertable).order_by('id')

        history = [{"question": c.question, "answer": c.answer} for c in chats]

        return JsonResponse(history, safe=False)

    except User.DoesNotExist:
        return JsonResponse({'response': 'User not found'}, status=404)
#


# Helper to fetch weather
import json
import requests
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Chatbot  # Ensure these are imported correctly

import json
import requests
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Chatbot
import json
import requests
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Chatbot


import json
from django.http import JsonResponse
from datetime import datetime
from .models import User, Chatbot






@csrf_exempt
def public_send_complaint(request):
    complaint=request.POST['complaint']
    lid=request.POST['lid']
    a=Complaint()
    a.complaint=complaint
    a.date=datetime.datetime.now().today()
    a.reply='pending'
    a.login_id=User.objects.get(id=lid)
    a.save()
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def public_view_reply(request):
    lid=request.POST['lid']
    a=Complaint.objects.filter(login_id=lid)
    l=[]
    for i in a:
        l.append({"id":str(i.id),"complaint":i.complaint,"reply":i.reply,"date":str(i.date)})
    return JsonResponse({"status":"ok","data":l})


@csrf_exempt
def er_view_profile(request):
    lid=request.POST['lid']
    a=EmergencyRescue.objects.get(login_id=lid)
    return JsonResponse({"status":"ok",
                         "name":a.name,
                         "email":a.email,
                         "phone":a.phone,
                         "place":a.place,
                         "district":a.district,
                         "post":a.post,
                         "pin":a.pin,
                         "role":a.role,
                         "notes":a.notes
                         })

@csrf_exempt
def er_change_password(request):
    oldpassword = request.POST['oldpassword']
    newpassword = request.POST['newpassword']
    lid = request.POST['lid']

    auth_user = User.objects.get(id=lid)
    f = check_password(oldpassword, auth_user.password)
    if f:
        auth_user.set_password(newpassword)
        auth_user.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'failed'})


from django.http import JsonResponse
from .models import EmergencyAlert


@csrf_exempt
def view_user_reports(request):
    alerts = EmergencyAlert.objects.all()
    report_list = []
    for item in alerts:
        report_list.append({
            "id": str(item.id),
            "public": item.PUBLIC.name,
            "alert": item.alert,
            "latitude": item.latitude,
            "longitude": item.longitude,
        })
    return JsonResponse({'status':'ok', "data":report_list})
@csrf_exempt
def emergency_request(request):
    return JsonResponse({'status':'ok'})

import json

from django.views.decorators.csrf import csrf_exempt
from .models import DonateGoods, Public, Volunteer, Camp
import datetime

@csrf_exempt
def add_donation_api(request):
    if request.method == "POST":
        try:

            user_login_id = request.POST.get('public_id')
            camp_id = request.POST.get('camp_id')
            volunteer_id = request.POST.get('volunteer_id')
            item = request.POST.get('item')
            quantity = request.POST.get('quantity')
            date_str = request.POST.get('date')

            try:
                public_obj = Public.objects.get(login_id=user_login_id)
            except Public.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Public Profile not found for this user"})

            camp_obj = Camp.objects.get(id=camp_id)
            vol_obj = Volunteer.objects.get(id=volunteer_id)

            DonateGoods.objects.create(
                Public=public_obj,
                volunteer=vol_obj,
                camp=camp_obj,
                item=item,
                quantity=int(quantity),
                date=date_str,
                status='Not Collected'
            )

            return JsonResponse({"status": "ok", "message": "Donation added successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})


from django.http import JsonResponse
from .models import DonateGoods


@csrf_exempt
def public_view_donations(request):
    try:

        user_login_id = request.GET.get('login_id')
        donations = DonateGoods.objects.filter(
            Public__login_id=user_login_id
        ).select_related('camp', 'volunteer', 'Public').order_by('-date')

        data_list = []
        for d in donations:
            data_list.append({
                "id": d.id,
                "item": d.item,
                "quantity": d.quantity,
                "status": d.status,
                "date": d.date.strftime("%d %b %Y"),
                "camp_name": d.camp.name,
                "volunteer_name": d.volunteer.name,
                "public_name": d.Public.name if d.Public else "Anonymous"
            })

        return JsonResponse({"status": "ok", "data": data_list})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

from django.http import JsonResponse
from .models import Camp, Volunteer

@csrf_exempt
def get_donation_metadata(request):
    try:
        camps = Camp.objects.all().values('id', 'name')
        volunteers = Volunteer.objects.all().values('id', 'name')

        return JsonResponse({
            "status": "ok",
            "camps": list(camps),
            "volunteers": list(volunteers)
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import DonateGoods


@csrf_exempt
def volunteer_update_donation_status(request):
    if request.method == 'POST':
        try:
            donation_id = request.POST.get('donation_id')

            # Retrieve the specific donation record
            donation = DonateGoods.objects.get(id=donation_id)

            # Update the status
            donation.status = 'Collected'
            donation.save()

            return JsonResponse({"status": "ok", "message": "Status updated to Collected"})
        except DonateGoods.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Donation record not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

#
# def get_predicttt(request):
#     if request.method == 'POST':
#         try:
#
#             lat = float(request.POST['lat'])
#             lon = float(request.POST['lon'])
#             distance_str = "1000"
#
#             # Get river data
#             river_data = get_rivers_near_location(lat, lon)
#             if "error" in river_data:
#                 print(river_data["error"])
#             else:
#                 print(f"Rivers near location ({lat}, {lon}):")
#                 for river in river_data:
#                     if isinstance(river["distance_km"], (float, int)):
#                         distance_str = float(river['distance_km'])
#                         break
#                     else:
#                         distance_str = "Distance not available"
#                         break
#
#             # Fetch elevation, soil type, and slope angle data
#             elevation, soil_type, slope_angle = getmaindata(float(lat), float(lon))
#             print(elevation, soil_type, slope_angle, distance_str)
#
#             if lat is None or lon is None:
#                 return render(request,"camp_cordinator/result.html",{"val":"invalid"})
#             # Fetch weather data
#             api_url = f'https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={API_KEY}'
#             response = requests.get(api_url)
#             weather_data = response.json()
#             print(weather_data)
#
#         except json.JSONDecodeError as e:
#             print(e)
#             return render(request, "camp_cordinator/result.html", {"val": "invalid"})
#
#             # return JsonResponse({'error': 'Invalid JSON'}, status=400)
#
#     # Load the KNN model
#     # knn = joblib.load(r"C:\Users\USER\Downloads\landslide (1)\landslide\app\knn-model.joblib")
#
#     # Ensure the input data matches the expected dimensions
#     try:
#         # Adjust the row to have the correct number of features
#         st = [
#             'Fluvisols',
#             'Andosols',
#             'Arenosols',
#             'Chernozem',
#             'Gleysols',
#             'Histosols',
#             'Kastanozems',
#             'Luvisols',
#             'Nitisols',
#             'Regosols',
#             'Vertisols',
#             'Solonchaks',
#             'Podzols',
#             'Alisols',
#             'Cambisols',
#             'Calcisols',
#             'Phaeozems',
#             'Acrisols',
#             'Plinthosols'
#         ]
#         # try:
#         #     row = [float(lat), float(lon), float(elevation), float(distance_str), float(slope_angle),weather_data['data'][0]['precip'],st.index(soil_type),weather_data['data'][0]['rh'],weather_data['data'][0]['rh']]  # Adjust as necessary
#         # except:
#         #     row = [float(lat), float(lon), float(elevation), float(distance_str), float(slope_angle),1,st.index(soil_type),1,1]  # Adjust as necessary
#         # if len(row) != knn.n_features_in_:
#         #     raise ValueError(f"Expected {knn.n_features_in_} features, but got {len(row)}")
#
#
#
#         from  myapp.Randomforest import random_forest
#
#         # Make the prediction
#         # res = knn.predict([row])
#
#         try:
#
#             res=random_forest(float(lat), float(lon), float(elevation), float(distance_str), float(slope_angle),weather_data['data'][0]['precip'],st.index(soil_type),weather_data['data'][0]['rh'],weather_data['data'][0]['rh'])
#             print(res, "++++++++++++++++++")
#         except:
#             res=random_forest(float(lat), float(lon), float(elevation), float(distance_str), float(slope_angle),1,st.index(soil_type),1,1)
#
#
#
#
#         print(res,"jjjjjjj")
#         if res[0] == "0":
#             try:
#                 return render(request,"camp_cordinator/result.html",{'status': 'ok', 'val': 'Non-landslide','weather_data':weather_data,'st':soil_type,'river':distance_str,'altitude':elevation,'rainfall':weather_data['data'][0]['precip'],'city_name':weather_data['data'][0]['city_name']})
#             except:
#                 return render(request,"camp_cordinator/result.html",{'status': 'ok', 'val': 'Non-landslide','weather_data':weather_data,'st':soil_type,'river':distance_str,'altitude':elevation,'rainfall':5,'city_name':""})
#         else:
#             try:
#                 return HttpResponse({'status': 'not ok', 'val': 'Landslide','weather_data':weather_data,'st':soil_type,'river':distance_str,'altitude':elevation,'rainfall':weather_data['data'][0]['precip'],'city_name':weather_data['data'][0]['city_name']})
#             except:
#                 return HttpResponse({'status': 'not ok', 'val': 'Landslide','weather_data':weather_data,'st':soil_type,'river':distance_str,'altitude':elevation,'rainfall':5,'city_name':""})
#
#     except ValueError as e:
#         print("Error in prediction:", str(e))
#         return JsonResponse({'error': 'Prediction failed', 'details': str(e)}, status=500)

from django.http import JsonResponse
import requests
from myapp.Randomforest import random_forest

API_KEY = 'YOUR_WEATHERBIT_API_KEY'


@csrf_exempt
def api_get_predict(request):
    """
    API for Automated Prediction via Lat/Lon
    URL Example: /api_get_predict/?lat=11.25&lon=75.3
    """
    try:
        # 1. Capture Inputs
        lat_val = request.GET.get('lat')
        lon_val = request.GET.get('lon')

        if not lat_val or not lon_val:
            return JsonResponse({'status': 'error', 'message': 'Missing coordinates'}, status=400)

        lat = float(lat_val)
        lon = float(lon_val)
        distance_str = 1000.0

        # 2. Get River Data
        try:
            river_data = get_rivers_near_location(lat, lon)
            if isinstance(river_data, list):
                for river in river_data:
                    if isinstance(river.get("distance_km"), (float, int)):
                        distance_str = float(river['distance_km'])
                        break
        except Exception as e:
            print(f"River Data Logic Error: {e}")

        # 3. Fetch Elevation, Soil, and Slope
        # NOTE: Ensure getmaindata always returns 3 values to avoid unpacking errors
        elevation, soil_type, slope_angle = getmaindata(lat, lon)

        # 4. Fetch Weather Data
        precip, rh, city_name = 5.0, 1.0, "Unknown"
        try:
            api_url = f'https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={API_KEY}'
            response = requests.get(api_url, timeout=5)
            w_data = response.json()
            if 'data' in w_data:
                precip = w_data['data'][0].get('precip', 5.0)
                rh = w_data['data'][0].get('rh', 1.0)
                city_name = w_data['data'][0].get('city_name', "Unknown")
        except Exception as e:
            print(f"Weather API Error: {e}")

        # 5. Soil Mapping
        st_list = ['Fluvisols', 'Andosols', 'Arenosols', 'Chernozem', 'Gleysols', 'Histosols',
                   'Kastanozems', 'Luvisols', 'Nitisols', 'Regosols', 'Vertisols',
                   'Solonchaks', 'Podzols', 'Alisols', 'Cambisols', 'Calcisols',
                   'Phaeozems', 'Acrisols', 'Plinthosols']

        soil_idx = st_list.index(soil_type) if soil_type in st_list else 0

        # 6. ML Prediction
        try:
            res = random_forest(lat, lon, elevation, distance_str, slope_angle, precip, soil_idx, rh, rh)
        except:
            res = random_forest(lat, lon, elevation, distance_str, slope_angle, 1, soil_idx, 1, 1)

        # 7. Final Response
        is_landslide = str(res[0]) != "0"
        return JsonResponse({
            'status': 'success',
            'val': 'Landslide' if is_landslide else 'No-landslide',
            'is_danger': is_landslide,
            'details': {
                'city': city_name,
                'rainfall': precip,
                'altitude': elevation,
                'river_dist': distance_str,
                'soil': soil_type
            }
        })

    except Exception as e:
        print(traceback.format_exc())  # Prints exact error line in your terminal
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

#
# def predict(request):
#     v1=request.form['textfield']
#     v2=request.form['textfield2']
#     v3=request.form['textfield3']
#     v4=request.form['textfield4']
#     v5=request.form['textfield5']
#     v6=request.form['textfield6']
#     v7=request.form['textfield7']
#     v8=request.form['select']
#     v9=request.form['textfield8']
#     row=[float(v1),
#          float(v2),
#          float(v3),
#          float(v4),
#          float(v5),
#          float(v6),
#          float(v7),
#          float(v8),
#          float(v9)]
#
#
#     from myapp.Randomforest import random_forest
#
#
#     res=random_forest(float(v1),
#          float(v2),
#          float(v3),
#          float(v4),
#          float(v5),
#          float(v6),
#          float(v7),
#          float(v8),
#          float(v9))
#
#     # clf = RandomForestClassifier(n_estimators = 100)
#     # clf.fit(X_train,y_train)
#     # y_pred = clf.predict(X_test)
#
#
#
#
#     # knn=joblib.load("knn-model.joblib")
#     # res=knn.predict([row])
#     # print(res,"++++++++++++++++++")
#     if res[0]==0:
#         return  render(request,"camp_cordinator/result.html",val="No-landslide")
#     else:
#         return render(request,"camp_cordinator/result.html", val="Landslide")


from django.http import JsonResponse
from myapp.Randomforest import random_forest

@csrf_exempt
def api_manual_predict(request):

    try:

        data = {
            'elevation': request.GET.get('v1'), # v1
            'slope':     request.GET.get('v2'), # v2
            'aspect':    request.GET.get('v3'), # v3
            'placurv':   request.GET.get('v4'), # v4
            'procurv':   request.GET.get('v5'), # v5
            'lsfactor':  request.GET.get('v6'), # v6
            'twi':       request.GET.get('v7'), # v7
            'geology':   request.GET.get('v8'), # v8
            'sdoif':     request.GET.get('v9'), # v9
        }

        # 2. Validation: Ensure no parameter is missing or empty
        for key, value in data.items():
            if value is None or value.strip() == "":
                return JsonResponse({
                    'status': 'error',
                    'message': f'Missing parameter: {key} (v{list(data.keys()).index(key) + 1})'
                }, status=400)


        prediction = random_forest(
            float(data['elevation']),
            float(data['slope']),
            float(data['aspect']),
            float(data['placurv']),
            float(data['procurv']),
            float(data['lsfactor']),
            float(data['twi']),
            float(data['geology']),
            float(data['sdoif'])
        )


        val_code = int(prediction[0])
        prediction_text = "No-landslide" if val_code == 0 else "Landslide"

        return JsonResponse({
            'status': 'success',
            'val': prediction_text,
            'code': val_code
        })

    except ValueError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid input: All parameters must be numeric.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@csrf_exempt
def api_view_requests(request):
    lid=request.POST['lid']
    a=EmergencyAlert.objects.filter(emergency_rescue__login_id_id=lid).order_by('-id')
    l=[]
    for i in a:
        # Determine alert type based on the text
        alert_text = i.alert.lower()
        alert_type = 'SOS' if 'sos' in alert_text else 'Normal'
        
        # Get user details safely
        user_name = "Unknown"
        user_phone = "Not Available"
        if i.PUBLIC:
            user_name = i.PUBLIC.name
            user_phone = str(i.PUBLIC.phone)

        l.append({"id":str(i.id),
                  "alert":i.alert,
                  "status":i.status,
                  "latitude":i.latitude,
                  "longitude":i.longitude,
                  "type": alert_type,
                  "user_name": user_name,
                  "phone": user_phone
                  })
    return JsonResponse({"status":"ok","data":l})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EmergencyAlert


@csrf_exempt
def api_update_alert_status(request):

    if request.method == 'POST':
        try:
            alert_id = request.POST.get('alert_id')
            new_status = request.POST.get('status')  # 'Accepted' or 'Rejected'

            alert = EmergencyAlert.objects.get(id=alert_id)
            alert.status = new_status
            alert.save()

            return JsonResponse({
                "status": "ok",
                "message": f"Alert has been {new_status.lower()}"
            })
        except EmergencyAlert.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Alert not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid Request"}, status=400)


from django.http import JsonResponse
from .models import EmergencyRescue, Public, EmergencyAlert, User


@csrf_exempt
def public_view_rescue_teams(request):
    try:
        teams = EmergencyRescue.objects.filter(status='Varified')
        data = []
        for team in teams:
            data.append({
                'id': team.id,
                'name': team.name,
                'district': team.district,
                'role': team.role,
                'phone': team.phone,
                'place': team.place,
            })
        return JsonResponse({"status": "ok", "data": data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def public_send_emergency_request(request):
    try:
        lid = request.POST.get('lid')

        alert_text = request.POST.get('alert', 'Automatic SOS Signal')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        eid = request.POST.get('eid')


        if not lid or not lat or not lon or not eid:
            return JsonResponse({"status": "error", "message": "Incomplete location or user data"})

        a = EmergencyAlert()

        a.PUBLIC = Public.objects.get(login_id_id=lid)
        a.alert = alert_text
        a.latitude = lat
        a.longitude = lon
        a.status = 'pending'


        a.emergency_rescue = EmergencyRescue.objects.get(id=eid)
        a.save()

        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt
def public_view_needs(request):
    a = Needs.objects.all()
    l = []
    for i in a:
        
        camp = Camp.objects.filter(coordinator=i.coordinator).first()
        l.append({
            "id": i.id,
            "coordinator": i.coordinator.name,
            "camp_name": camp.name if camp else "General", # Added for Flutter auto-select
            "type": i.type,
            "description": i.description,
            "count": i.count,
            "date": i.date,
            "status": i.status
        })
    return JsonResponse({"status": "ok", "data": l})


@csrf_exempt
def public_add_donation_from_need(request):
    if request.method == "POST":
        need_id = request.POST.get("need_id")
        login_id = request.POST.get("login_id")  # Get current user
        quantity = request.POST.get("quantity")

        try:
            need = Needs.objects.get(id=need_id)
            public_user = Public.objects.get(login_id=login_id)

            # Find the camp associated with the coordinator who requested the need
            camp = Camp.objects.get(coordinator=need.coordinator)

            # Since the model requires a Volunteer, we can either:
            # 1. Assign a default volunteer from that camp
            # 2. Or modify your model to allow null volunteer until collected
            volunteer = Volunteer.objects.filter(coordinator=need.coordinator).first()

            DonateGoods.objects.create(
                Public=public_user,
                volunteer=volunteer,
                camp=camp,
                item=need.type,
                quantity=quantity,
                status='Not Collected',
                date=datetime.date.today()
            )
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def public_accept_need(request):
    if request.method == "POST":
        need_id = request.POST.get("need_id")
        try:
            need = Needs.objects.get(id=need_id)
            need.status = "Resolved" # Or "Accepted" based on your preference
            need.save()
            return JsonResponse({"status": "ok", "message": "Need accepted successfully"})
        except Needs.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Need not found"})

@csrf_exempt
def public_reject_need(request):
    if request.method == "POST":
        need_id = request.POST.get("need_id")
        try:
            need = Needs.objects.get(id=need_id)
            need.status = "Rejected"
            need.save()
            return JsonResponse({"status": "ok", "message": "Need rejected successfully"})
        except Needs.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Need not found"})

@csrf_exempt
def api_poll_alerts(request):
    try:
        lid = request.POST.get('lid')
        
        # Determine the emergency rescue team associated with this lid
        team = EmergencyRescue.objects.get(login_id_id=lid)
        
        # Get pending SOS alerts
        query = EmergencyAlert.objects.filter(emergency_rescue=team, status='pending', alert__icontains='SOS')
        
        # Return only the count and a snippet of the latest one to trigger the local notification
        count = query.count()
        if count > 0:
            latest = query.order_by('-id').first()
            return JsonResponse({
                'status': 'ok',
                'count': count,
                'latest_alert': latest.alert,
                'id': latest.id
            })
        else:
            return JsonResponse({'status': 'empty'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)})

@csrf_exempt
def api_poll_donations(request):
    try:
        lid = request.POST.get('lid')
        
        # Get the volunteer associated with this lid
        volunteer = Volunteer.objects.get(login_id_id=lid)
        
        # Get uncollected donations assigned to this volunteer
        query = DonateGoods.objects.filter(volunteer=volunteer, status='Not Collected')
        
        count = query.count()
        if count > 0:
            latest = query.order_by('-id').first()
            return JsonResponse({
                'status': 'ok',
                'count': count,
                'item': latest.item,
                'quantity': latest.quantity,
                'id': latest.id
            })
        else:
            return JsonResponse({'status': 'empty'})
    except Exception as e:
         return JsonResponse({'status': 'error', 'msg': str(e)})

@csrf_exempt
def api_unified_poll(request):
    try:
        lid = request.POST.get('lid')
        user_type = request.POST.get('type') # public, volunteer, news_reporter, emergency_rescue
        
        results = []

        # 1. General Notifications
        roll_map = {
            'public': 'Public',
            'volunteer': 'Volunteer',
            'emergency_rescue': 'Emergency Team',
        }
        roll = roll_map.get(user_type)
        if roll:
            latest_notif = Notification.objects.filter(roll=roll).order_by('-id').first()
            if latest_notif:
                results.append({
                    'type': 'broadcast',
                    'id': latest_notif.id,
                    'title': latest_notif.title,
                    'body': latest_notif.description
                })

        # 2. News (For everyone)
        latest_news = News.objects.order_by('-id').first()
        if latest_news:
             results.append({
                'type': 'news',
                'id': latest_news.id,
                'title': 'Latest News',
                'body': latest_news.news
            })

        # 3. Guidelines
        latest_guide = Guideline.objects.order_by('-id').first()
        if latest_guide:
             results.append({
                'type': 'guideline',
                'id': latest_guide.id,
                'title': 'New Guideline: ' + latest_guide.title,
                'body': latest_guide.guideline[:100]
            })

        # 4. Complaint Replies
        latest_reply = Complaint.objects.filter(login_id=lid).exclude(reply='').exclude(reply__isnull=True).order_by('-id').first()
        if latest_reply:
             results.append({
                'type': 'complaint_reply',
                'id': latest_reply.id,
                'title': 'Complaint Replied',
                'body': 'Your complaint has been answered: ' + latest_reply.reply[:50]
            })

        # 5. Role Specific
        if user_type == 'emergency_rescue':
            team = EmergencyRescue.objects.get(login_id_id=lid)
            alert = EmergencyAlert.objects.filter(emergency_rescue=team, status='pending', alert__icontains='SOS').order_by('-id').first()
            if alert:
                results.append({
                    'type': 'sos_alert',
                    'id': alert.id,
                    'title': 'SOS Emergency!',
                    'body': alert.alert
                })
        
        elif user_type == 'volunteer':
            volunteer = Volunteer.objects.get(login_id_id=lid)
            # Donations
            donation = DonateGoods.objects.filter(volunteer=volunteer, status='Not Collected').order_by('-id').first()
            if donation:
                results.append({
                    'type': 'donation',
                    'id': donation.id,
                    'title': 'New Donation to Collect',
                    'body': f"{donation.item} ({donation.quantity})"
                })
            # Medical Requests
            med = MedicalRequest.objects.filter(volunteer=volunteer, status='pending').order_by('-id').first()
            if med:
                results.append({
                    'type': 'medical_request',
                    'id': med.id,
                    'title': 'New Medical Request',
                    'body': f"Medicine: {med.medicine.medicine}"
                })
        
        elif user_type == 'public':
            # Check for SOS updates
            public_user = Public.objects.get(login_id=lid)
            alert_update = EmergencyAlert.objects.filter(PUBLIC=public_user).exclude(status='pending').order_by('-id').first()
            if alert_update:
                results.append({
                    'type': 'sos_update',
                    'id': alert_update.id,
                    'title': f"SOS Status: {alert_update.status}",
                    'body': f"Your alert '{alert_update.alert[:30]}...' is now {alert_update.status}",
                    'status': alert_update.status # Include status for change detection
                })
        
        elif user_type == 'news_reporter':
            reporter = News_reporter.objects.get(LOGIN_id=lid)
            results.append({
                'type': 'reporter_status',
                'id': reporter.id,
                'title': 'Account Status Update',
                'body': f"Your reporter account is currently: {reporter.status}",
                'status': reporter.status
            })

        return JsonResponse({'status': 'ok', 'notifications': results})

    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)})


@csrf_exempt
def public_chat_history(request):
    try:
        lid = request.GET.get('lid')
        if not lid:
            return JsonResponse({'response': 'User ID missing'}, status=400)

        # Ensure we filter history ONLY for the logged-in User ID
        usertable = User.objects.get(id=lid)
        chats = Chatbot.objects.filter(LOGIN=usertable).order_by('id')

        history = [{"question": c.question, "answer": c.answer} for c in chats]
        return JsonResponse(history, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'response': 'User not found'}, status=404)
@csrf_exempt
def public_chatbot_response(request):
    if request.method != 'POST':
        return JsonResponse({'response': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message', '').strip()
        lid = data.get('lid')
        lat = data.get('lat')
        lon = data.get('lon')
        weather = data.get('weather')

        # 🔹 Extracting details for Prediction
        temp = weather.get('temperature_2m') if weather else "N/A"
        wind = weather.get('wind_speed_10m') if weather else "N/A"
        code = weather.get('weather_code') if weather else "N/A"

        # 🔹 Enhanced AI Prompt for Prediction
        system_prompt = f"""
        You are a Disaster Management AI. 
        Current Location: Latitude {lat}, Longitude {lon}
        Current Weather Data:
        - Temperature: {temp}°C
        - Wind Speed: {wind} m/s
        - Weather Code: {code} (WMO Standard)

        User Question: {user_message}

        TASK:
        1. Answer the user's question.
        2. Based on the weather data provided, predict any potential disaster risks 
           (e.g., Heatwave if temp > 40°C, Storm if wind > 20m/s, Flood if heavy rain code).
        3. Provide safety recommendations if a risk is detected.
        """

        # 🔹 Generate response from Gemini
        try:
            bot_response = model.generate_content(system_prompt).text.strip()
        except Exception as ai_error:
            print("GEMINI API ERROR (Public Chatbot):", str(ai_error))
            bot_response = f"I can't predict right now. Error: {str(ai_error)}"

        # 🔹 Save to DB
        user_obj = User.objects.get(id=lid)
        Chatbot.objects.create(
            LOGIN=user_obj,
            date=datetime.date.today(),
            question=user_message,
            answer=bot_response,
            latitude=str(lat),
            longitude=str(lon)
        )

        return JsonResponse({'response': bot_response})

    except Exception as e:
        return JsonResponse({'response': 'Server Error'}, status=500)
        
        
        

@csrf_exempt
def chatbot_response(request):
    if request.method != 'POST':
        return JsonResponse({'response': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message', '').strip()
        lid = data.get('lid')
        lat = data.get('lat')
        lon = data.get('lon')
        weather = data.get('weather')

        if not user_message or not lid:
            return JsonResponse({'response': 'Message or user ID missing'}, status=400)

        # 🔹 Prediction Parameters
        temp = weather.get('temperature_2m') if weather else "Unknown"
        wind = weather.get('wind_speed_10m') if weather else "Unknown"
        code = weather.get('weather_code') if weather else "Unknown"

        system_prompt = f"""
        You are a Disaster Management AI. 
        Target Location: {lat}, {lon}
        Current Weather: {temp}°C, Wind: {wind} m/s, WMO Code: {code}.

        TASK:
        1. Answer: "{user_message}"
        2. PREDICT DISASTERS: Analyze these numbers. If temp > 40C (Heatwave), 
           if wind > 20m/s (Storm/Cyclone), if code is 65, 82, 95+ (Flood/Thunderstorm).
        3. SAFETY: Give a brief warning if risk is high.
        """

        try:
            bot_response = model.generate_content(system_prompt).text.strip()
        except Exception as ai_error:
            print("GEMINI API ERROR (Chatbot Response):", str(ai_error))
            bot_response = f"Unable to predict at the moment. Error: {str(ai_error)}"

        # 🔹 Save chat (Filters by lid to ensure privacy)
        user_obj = User.objects.get(id=lid)
        Chatbot.objects.create(
            LOGIN=user_obj,
            date=datetime.date.today(),
            question=user_message,
            answer=bot_response,
            latitude=str(lat),
            longitude=str(lon)
        )

        return JsonResponse({'response': bot_response})
    except Exception as e:
        return JsonResponse({'response': 'Server Error'}, status=500)

@csrf_exempt
def chat_history(request):
    try:
        lid = request.GET.get('lid')
        usertable = User.objects.get(id=lid)
        # Strictly filter by the user currently logged in
        chats = Chatbot.objects.filter(LOGIN=usertable).order_by('id')
        history = [{"question": c.question, "answer": c.answer} for c in chats]
        return JsonResponse(history, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'response': 'User not found'}, status=404)
