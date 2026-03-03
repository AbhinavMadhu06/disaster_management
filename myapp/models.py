from django.db import models
from django.contrib.auth.models import User

class Public(models.Model):
    login_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.BigIntegerField()
    email=models.CharField(max_length=255)
    photo=models.FileField()

class Coordinator(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    login_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255)
    place = models.CharField(max_length=200)
    post = models.CharField(max_length=100)
    pin = models.CharField(max_length=50)
    district = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    photo = models.FileField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=10, default='Active')



class Camp(models.Model):
    CAMP_STATUS=[
        ('open','open'),
        ('closed','closed')
    ]
    name = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    total_member = models.IntegerField()
    place = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,default='open')


class Volunteer(models.Model):
    login_id = models.ForeignKey(User,on_delete=models.CASCADE)
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    place= models.CharField(max_length=200)
    post = models.CharField(max_length=100)
    pin = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    district = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)



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
    date = models.DateTimeField()
    roll = models.CharField(max_length=50, choices=ROLL_CHOICES, default='Public')
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    district = models.CharField(max_length=200)
   

class Complaint(models.Model):
    login_id = models.ForeignKey(User,on_delete=models.CASCADE)
    complaint = models.TextField()
    date = models.DateField()
    reply = models.TextField()



class Guideline(models.Model):
    PRIORITY_CHOICES = [
        ('Normal', 'Normal'),
        ('High', 'High'),
        ('Critical','Critical'),
    ]
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    guideline = models.TextField()
    date = models.DateField()
    priority = models.CharField(max_length=10)

class News_reporter(models.Model):
    name=models.CharField(max_length=200)
    place=models.CharField(max_length=200)
    post=models.CharField(max_length=200)
    phone=models.CharField(max_length=50)
    chanelname=models.CharField(max_length=200)
    status=models.CharField(max_length=200,default='pending')
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    photo=models.FileField()


class News(models.Model):
    NEWS_REPORTER = models.ForeignKey(News_reporter, on_delete=models.CASCADE, null=True, blank=True)
    news = models.CharField(max_length=255)
    details = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    date = models.DateField() 

    
class Stock(models.Model):
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    count = models.IntegerField()
    date = models.DateField()



class Collection(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    PUBLIC = models.ForeignKey(Public,on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=200)
    details = models.TextField()
    quantity = models.IntegerField()
    date = models.DateField()



class EmergencyRescue(models.Model):
    STATUS_CHOICES = [
        ('Varified', 'Varified'),
        ('Not Varified', 'Not Varified'),
    ]
    login_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    place = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    post = models.CharField(max_length=100)
    pin = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=100)  
    notes = models.TextField()  
    status = models.CharField(max_length=16, default='Not Varified')


class EmergencyAlert(models.Model):
    PUBLIC = models.ForeignKey(Public,on_delete=models.CASCADE, null=True, blank=True)
    emergency_rescue = models.ForeignKey(EmergencyRescue, on_delete=models.CASCADE)
    alert = models.TextField()
    status = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()



class Needs(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    description = models.TextField()
    count = models.IntegerField()
    date = models.DateField()
    status = models.CharField(max_length=100, default='Pending')

class Medicine(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=200)
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, default='Pending')

class MedicalRequest(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)


class Services(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    servicetype = models.CharField(max_length=200)
    details = models.TextField()

class DonateGoods(models.Model):
    STATUS_CHOICES = [
        ('Not Collected', 'Not Collected'),
        ('Collected', 'Collected'),
    ]

    Public = models.ForeignKey(Public, on_delete=models.CASCADE, null=True, blank=True)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default='Not Collected')
    date = models.DateField()
class Chatbot(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    date=models.DateField()
    question=models.TextField()
    answer=models.TextField()
    latitude=models.CharField(max_length=100,default=0)
    longitude=models.CharField(max_length=100,default=0)
