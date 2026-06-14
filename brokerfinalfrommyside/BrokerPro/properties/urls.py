from django.urls import path
from . import views
from .views import PropertyListAPIView,AppointmentAPIView,PropertyDetailAPIView,BrokerListAPIView,ConsultationAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.home, name='home'),
     path(
        'property/<int:id>/',
        views.property_detail,
        name='property_detail'
    ),
    path(
    'property/<int:id>/appointment/',
    views.book_appointment,
    name='book_appointment'
    ),
    path(
    'consultation/',
    views.consultation,
    name='consultation'
    ),
    path(
    'properties/',
    views.property_list,
    name='browse_properties'
    ),
    path(
    'register/',
    views.register,
    name='register'
    ),

    path(
    'login/',
    views.login_view,
    name='login'
    ),

    path(
    'logout/',
    views.logout_view,
    name='logout'
    ),

    path(
    'profile/',
    views.profile_view,
    name='profile'
    ),
    path(
    'about/',
    views.about,
    name='about'
    ),
    #api view url mapping 
    path(
        'api/properties/',
        PropertyListAPIView.as_view(),
        name='api-properties'
    ),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
    "api/properties/<int:pk>/",
    PropertyDetailAPIView.as_view(),
    name="api-property-detail",
    ),
    path(
    "api/brokers/",
    BrokerListAPIView.as_view(),
    name="api-brokers",
    ),
    path(
    "api/consultation/",
    ConsultationAPIView.as_view(),
    name="api-consultation",
    ),
    path(
    "api/appointments/",
    AppointmentAPIView.as_view(),
    name="appointment_api"
    ),
    
]