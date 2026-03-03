from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
#new
from django.core.validators import MinValueValidator, MaxValueValidator


class Admin(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.username
    
class Coordinator(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    login_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    place = models.CharField(max_length=200, blank=True)
    post = models.CharField(max_length=100, blank=True)
    pin = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True, unique=True)
    photo = models.ImageField(upload_to='coordinator_photos/', blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255, validators=[MinLengthValidator(8)])

     # New field
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.username



# Define the Camp class
class Camp(models.Model):
    CAMP_STATUS=[
        ('open','open'),
        ('closed','closed')
    ]
    name = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    total_member = models.IntegerField(null=True, blank=True)
    place = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)], null=True)
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)], null=True)
    coordinator = models.ForeignKey(Coordinator, on_delete=models.SET_NULL, null=True, blank=True, related_name='camps')
    status = models.CharField(max_length=20, choices=CAMP_STATUS,default='open')

    def __str__(self):
        return self.name

#new
class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100, validators=[MinLengthValidator(8)])





class Volunteer(models.Model):
    login_id = models.ForeignKey(User,on_delete=models.CASCADE)
    coordinator = models.ForeignKey(Coordinator, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=255, blank=True)
    place = models.CharField(max_length=200, blank=True)
    post = models.CharField(max_length=100, blank=True)
    pin = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=200, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255, validators=[MinLengthValidator(8)])



class Notification(models.Model):
    ROLL_CHOICES = [
        ('Admin','Admin'),
        ('Camp_Coordinator','Camp Coordinator'),
        ('Volunteer','Volunteer'),
        ('Public','Public'),
        ('Emergency Team','Emergency Team'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=200)
    date = models.DateTimeField(null=True, blank=True)
    roll = models.CharField(max_length=50, choices=ROLL_CHOICES, default='Public')
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)], null=True,)
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)], null=True,)
    address = models.CharField(max_length=200, blank=True, default='None')
    phone = models.CharField(max_length=50, blank=True, default='None')
    district = models.CharField(max_length=200, default='None')
   

class Complaint(models.Model):
    
    login_id = models.ForeignKey(User,on_delete=models.CASCADE)
    complaint = models.TextField(blank=True)
    date = models.DateTimeField(null=True, blank=True)
    reply = models.TextField(blank=True)



class Guideline(models.Model):
    PRIORITY_CHOICES = [
        ('Normal', 'Normal'),
        ('High', 'High'),
        ('Critical','Critical'),
    ]
    coordinator = models.ForeignKey(Coordinator, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200,default='Emergency')
    guideline = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Normal')

class News(models.Model):
    login_id = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.CharField(max_length=255, blank=True)
    details = models.TextField(blank=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    date = models.DateField(null=True, blank=True) 

    
class Stock(models.Model):
    coordinator = models.ForeignKey(Coordinator, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=200, blank=True)
    count = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)



class Collection(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=200, blank=True)
    details = models.TextField(blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)



class EmergencyRescue(models.Model):
    STATUS_CHOICES = [
        ('Varified', 'Varified'),
        ('Not Varified', 'Not Varified'),
    ]
    login_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    place = models.CharField(max_length=200, blank=True)
    district = models.CharField(max_length=200,blank=True)
    post = models.CharField(max_length=100, blank=True)
    pin = models.CharField(max_length=50, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    #new
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255, validators=[MinLengthValidator(8)])
    role = models.CharField(max_length=100, blank=True)  # For the person's role (e.g., Volunteer, Coordinator, etc.)
    notes = models.TextField(blank=True)  # Notes related to the emergency rescue
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='Not Varified')


class EmergencyAlert(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    emergency_rescue = models.ForeignKey(EmergencyRescue, on_delete=models.SET_NULL, null=True, blank=True)
    alert = models.TextField(blank=True)
    status = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)



class Needs(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    count = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')



class Medicine(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]
    coordinator = models.ForeignKey(Coordinator, on_delete=models.SET_NULL, null=True, blank=True)
    medicine = models.CharField(max_length=200, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')


class MedicalRequest(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, null=True, blank=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=100, blank=True)



class Services(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, null=True, blank=True)
    servicetype = models.CharField(max_length=200, blank=True)
    details = models.TextField(blank=True)

