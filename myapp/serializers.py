from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class PublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Public
        fields = '__all__'

class CoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinator
        fields = '__all__'

class CampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camp
        fields = '__all__'

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'

class GuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guideline
        fields = '__all__'

class News_reporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = News_reporter
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class EmergencyRescueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyRescue
        fields = '__all__'

class EmergencyAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyAlert
        fields = '__all__'

class NeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Needs
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class MedicalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRequest
        fields = '__all__'

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class DonateGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonateGoods
        fields = '__all__'

class ChatbotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatbot
        fields = '__all__'
