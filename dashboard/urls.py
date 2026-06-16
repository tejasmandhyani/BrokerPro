from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.dashboard_home,
        name='dashboard_home'
    ),

    path(
        'properties/',
        views.property_list,
        name='property_list'
    ),

    path(
        'properties/add/',
        views.property_create,
        name='property_create'
    ),

    path(
        'properties/edit/<int:id>/',
        views.property_update,
        name='property_update'
    ),

    path(
        'properties/delete/<int:id>/',
        views.property_delete,
        name='property_delete'
    ),
    path(
    'properties/images/<int:id>/',
    views.property_images,
    name='property_images'
    ),

    path(
    'properties/image/delete/<int:id>/',
    views.delete_property_image,
    name='delete_property_image'
    ),
    path(
    'properties/video/delete/<int:id>/',
    views.delete_property_video,
    name='delete_property_video'
    ),
    path(
    'login/',
    views.broker_login,
    name='broker_login'
    ),

    path(
    'logout/',
    views.broker_logout,
    name='broker_logout'
    ),

    #appointment links 
    path(
    'appointments/',
    views.appointment_list,
    name='appointment_list'
    ),

    path(
    'appointments/accept/<int:id>/',
    views.accept_appointment,
    name='accept_appointment'
    ),

    path(
    'appointments/reject/<int:id>/',
    views.reject_appointment,
    name='reject_appointment'
    ),

    #customers url 
    path(
    'customers/',
    views.customer_list,
    name='customer_list'
    ),
    #whatsapp url 
    path(
    'appointments/whatsapp/<int:id>/',
    views.whatsapp_customer,
    name='whatsapp_customer'
    ),
    #todays and upcoming 
    path(
    'appointments/today/',
    views.today_visits,
    name='today_visits'
    ),

    path(
    'appointments/upcoming/',
    views.upcoming_visits,
    name='upcoming_visits'
    ),
    #consultation 
    path(
    'consultations/',
    views.consultation_list,
    name='consultation_list'
    ),

    #publish and unpublish urls 
    path(
    'properties/publish/<int:id>/',
    views.publish_property,
    name='publish_property'
    ),

    path(
    'properties/unpublish/<int:id>/',
    views.unpublish_property,
    name='unpublish_property'
    ),
    #version and rollback 
    path(
    'property/<int:id>/versions/',
    views.property_versions,
    name='property_versions'
    ),
    path(
    "properties/versions/<int:id>/details/",
    views.property_version_detail,
    name="property_version_detail",
    ),
    path(
    'rollback/<int:version_id>/',
    views.rollback_property,
    name='rollback_property'
    ),
    #preview
    path(
    'preview/',
    views.preview_home,
    name='preview_home'
    ),
    path(
    'preview/properties/',
    views.preview_property_list,
    name='preview_property_list'
    ),
    path(
    'preview/property/<int:id>/',
    views.preview_property_detail,
    name='preview_property_detail'
    ),

]
