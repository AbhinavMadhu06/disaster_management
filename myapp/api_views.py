from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User, Group
from .models import *
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class PublicViewSet(viewsets.ModelViewSet):
    queryset = Public.objects.all()
    serializer_class = PublicSerializer
    permission_classes = [AllowAny]

class CoordinatorViewSet(viewsets.ModelViewSet):
    queryset = Coordinator.objects.all()
    serializer_class = CoordinatorSerializer
    permission_classes = [IsAuthenticated]

class CampViewSet(viewsets.ModelViewSet):
    queryset = Camp.objects.all()
    serializer_class = CampSerializer
    permission_classes = [AllowAny]

class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

class GuidelineViewSet(viewsets.ModelViewSet):
    queryset = Guideline.objects.all()
    serializer_class = GuidelineSerializer
    permission_classes = [AllowAny]

class News_reporterViewSet(viewsets.ModelViewSet):
    queryset = News_reporter.objects.all()
    serializer_class = News_reporterSerializer
    permission_classes = [AllowAny]

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

class EmergencyRescueViewSet(viewsets.ModelViewSet):
    queryset = EmergencyRescue.objects.all()
    serializer_class = EmergencyRescueSerializer
    permission_classes = [AllowAny]

class EmergencyAlertViewSet(viewsets.ModelViewSet):
    queryset = EmergencyAlert.objects.all()
    serializer_class = EmergencyAlertSerializer
    permission_classes = [AllowAny]

class NeedsViewSet(viewsets.ModelViewSet):
    queryset = Needs.objects.all()
    serializer_class = NeedsSerializer
    permission_classes = [AllowAny]

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]

class MedicalRequestViewSet(viewsets.ModelViewSet):
    queryset = MedicalRequest.objects.all()
    serializer_class = MedicalRequestSerializer
    permission_classes = [IsAuthenticated]

class DonateGoodsViewSet(viewsets.ModelViewSet):
    queryset = DonateGoods.objects.all()
    serializer_class = DonateGoodsSerializer
    permission_classes = [IsAuthenticated]

class ChatbotViewSet(viewsets.ModelViewSet):
    queryset = Chatbot.objects.all()
    serializer_class = ChatbotSerializer
    permission_classes = [IsAuthenticated]
