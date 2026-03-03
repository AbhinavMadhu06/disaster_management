from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from myapp import api_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'api/users', api_views.UserViewSet)
router.register(r'api/admins', api_views.AdminViewSet)
router.register(r'api/coordinators', api_views.CoordinatorViewSet)
router.register(r'api/camps', api_views.CampViewSet)
router.register(r'api/volunteers', api_views.VolunteerViewSet)
router.register(r'api/notifications', api_views.NotificationViewSet)
router.register(r'api/complaints', api_views.ComplaintViewSet)
router.register(r'api/guidelines', api_views.GuidelineViewSet)
router.register(r'api/news', api_views.NewsViewSet)
router.register(r'api/stocks', api_views.StockViewSet)
router.register(r'api/collections', api_views.CollectionViewSet)
router.register(r'api/emergency-rescues', api_views.EmergencyRescueViewSet)
router.register(r'api/emergency-alerts', api_views.EmergencyAlertViewSet)
router.register(r'api/needs', api_views.NeedsViewSet)
router.register(r'api/medicines', api_views.MedicineViewSet)
router.register(r'api/medical-requests', api_views.MedicalRequestViewSet)
router.register(r'api/services', api_views.ServicesViewSet)

urlpatterns = [
    path('', lambda request: redirect('/myapp/')),  # root redirect
    path('admin/', admin.site.urls),               # keep admin here
    path('myapp/', include('myapp.urls')),         # your app URLs
    path('', include(router.urls)),                # API endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)