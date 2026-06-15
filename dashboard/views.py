from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import urllib.parse
from django.contrib.admin.views.decorators import staff_member_required
from .services.api_client import get,put,delete,get_dashboard_property,get_preview_properties,get_dashboard_properties
from properties.services.api_client import get as property_get

from properties.models import Property
from properties.models import PropertyImage
from properties.models import PropertyVideo,Appointment,PropertyVersion,Broker
from datetime import date
from properties.models import ConsultationLead
from .forms import PropertyForm
from dashboard.services.api_client import post
from properties.services.api_client import get_property
from django.contrib import messages
from dashboard.services.token_manager import login as token_login

#new imports 
from dashboard.services.dashboard_service import DashboardService
from dashboard.services.property_service import DashboardPropertyService
from dashboard.services.appointment_service import DashboardAppointmentService
from dashboard.services.customer_service import DashboardCustomerService
from dashboard.services.consultation_service import DashboardConsultationService
from dashboard.services.broker_service import DashboardBrokerService



def expire_appointments():

    Appointment.objects.filter(
        appointment_date__lt=date.today(),
        status='Pending'
    ).update(
        status='Expired'
    )

@login_required(login_url="login")
def broker_login(request):

    if request.user.is_authenticated:

        return redirect(
            "dashboard_home"
        )

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = DashboardBrokerService.authenticate_broker(
            username,
            password
        )

        if DashboardBrokerService.is_staff(user):

            login(
                request,
                user
            )

            return redirect(
                "dashboard_home"
            )

        elif user:

            messages.error(
                request,
                "Only staff users can access the dashboard."
            )

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "dashboard/login.html"
    )
def broker_logout(request):

    logout(request)

    return redirect("broker_login")

@login_required(login_url="broker_login")
@staff_member_required
def dashboard_home(request):

    DashboardAppointmentService.expire_pending()

    context = DashboardService.get_dashboard_data()

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )
@staff_member_required
def property_list(request):

    properties = DashboardPropertyService.get_all()

    return render(
        request,
        "dashboard/property_list.html",
        {
            "properties": properties
        }
    )

@login_required(login_url="broker_login")
@staff_member_required
def property_create(request):

    if request.method == "POST":

        form = PropertyForm(request.POST)

        if form.is_valid():

            broker = DashboardBrokerService.get_by_user(
                request.user
            )

            DashboardPropertyService.create(

                form=form,

                images=request.FILES.getlist("images"),

                videos=request.FILES.getlist("videos"),

                broker=broker,

            )

            messages.success(
                request,
                "Property created successfully."
            )

            return redirect("property_list")

    else:

        form = PropertyForm()

    return render(
        request,
        "dashboard/property_create.html",
        {
            "form": form
        }
    )

@staff_member_required
def property_update(request, id):

    property = DashboardPropertyService.get_by_id(id)

    if request.method == "POST":

        form = PropertyForm(
            request.POST,
            instance=property
        )

        if form.is_valid():

            DashboardPropertyService.update(

                property=property,

                form=form,

            )

            messages.success(
                request,
                "Property updated successfully."
            )

            return redirect(
                "property_list"
            )

    else:

        form = PropertyForm(
            instance=property
        )

    return render(
        request,
        "dashboard/property_update.html",
        {
            "form": form,
            "property": property
        }
    )
@staff_member_required
def property_delete(request, id):

    property = DashboardPropertyService.get_by_id(id)

    if request.method == "POST":

        DashboardPropertyService.delete(property)

        messages.success(
            request,
            "Property deleted successfully."
        )

        return redirect(
            "property_list"
        )

    return render(
        request,
        "dashboard/property_delete.html",
        {
            "property": property
        }
    )
from django.contrib import messages
@login_required(login_url="broker_login")
@staff_member_required
def property_images(request, id):

    property = DashboardPropertyService.get_by_id(id)

    if request.method == "POST":

        DashboardPropertyService.add_images(

            property,

            request.FILES.getlist("images")

        )

        DashboardPropertyService.add_videos(

            property,

            request.FILES.getlist("videos")

        )

        messages.success(
            request,
            "Media uploaded successfully."
        )

        return redirect(
            "property_images",
            id=property.id
        )

    return render(
        request,
        "dashboard/property_images.html",
        {
            "property": property
        }
    )
@login_required(login_url="broker_login")
@staff_member_required
def delete_property_image(request, id):

    image = get_object_or_404(
        PropertyImage,
        id=id
    )

    property_id = image.property.id

    DashboardPropertyService.delete_image(image)

    messages.success(
        request,
        "Image deleted successfully."
    )

    return redirect(
        "property_images",
        id=property_id
    )
@login_required(login_url="broker_login")
@staff_member_required
def delete_property_video(request, id):

    video = get_object_or_404(
        PropertyVideo,
        id=id
    )

    property_id = video.property.id

    DashboardPropertyService.delete_video(video)

    messages.success(
        request,
        "Video deleted successfully."
    )

    return redirect(
        "property_images",
        id=property_id
    )
@login_required(login_url="broker_login")
@staff_member_required
def appointment_list(request):

    appointments = DashboardAppointmentService.get_all()

    return render(
        request,
        "dashboard/appointment_list.html",
        {
            "appointments": appointments
        }
    )
@login_required(login_url="broker_login")
@staff_member_required
def accept_appointment(request, id):

    appointment = DashboardAppointmentService.get_by_id(id)

    DashboardAppointmentService.accept(
        appointment
    )

    messages.success(
        request,
        "Appointment accepted."
    )

    return redirect(
        "appointment_list"
    )

@login_required(login_url="broker_login")
@staff_member_required
def reject_appointment(request, id):

    appointment = DashboardAppointmentService.get_by_id(id)

    DashboardAppointmentService.reject(
        appointment
    )

    messages.success(
        request,
        "Appointment rejected."
    )

    return redirect(
        "appointment_list"
    )
#customer functionn
@login_required(login_url="broker_login")
@staff_member_required
def customer_list(request):

    customers = DashboardCustomerService.get_all()

    return render(
        request,
        "dashboard/customer_list.html",
        {
            "customers": customers
        }
    )
#whatsapp view 
@login_required(login_url="broker_login")
@staff_member_required
def whatsapp_customer(request, id):

    appointment = DashboardAppointmentService.get_by_id(id)

    whatsapp_url = (
        DashboardAppointmentService
        .get_whatsapp_url(
            appointment
        )
    )

    return redirect(
        whatsapp_url
    )
#dashboard todays and upcoming visits 
@login_required(login_url="broker_login")
@staff_member_required
def today_visits(request):

    appointments = DashboardAppointmentService.get_today()

    return render(
        request,
        "dashboard/today_visits.html",
        {
            "appointments": appointments
        }
    )
@login_required(login_url="broker_login")
@staff_member_required
def upcoming_visits(request):

    appointments = DashboardAppointmentService.get_upcoming()

    return render(
        request,
        "dashboard/upcoming_visits.html",
        {
            "appointments": appointments
        }
    )
#consultation List 
@login_required(login_url="broker_login")
@staff_member_required
def consultation_list(request):

    consultations = DashboardConsultationService.get_all()

    return render(
        request,
        "dashboard/consultation_list.html",
        {
            "consultations": consultations
        }
    )
#publish and unpublish views
@staff_member_required
def publish_property(request, id):

    property = DashboardPropertyService.get_by_id(id)

    DashboardPropertyService.publish(property)

    messages.success(
        request,
        "Property published successfully."
    )

    return redirect("property_list")
@staff_member_required
def unpublish_property(request, id):

    property = DashboardPropertyService.get_by_id(id)

    DashboardPropertyService.unpublish(property)

    messages.success(
        request,
        "Property moved to draft."
    )

    return redirect("property_list")


#rollback and versions 
@login_required(login_url="broker_login")
@staff_member_required
def property_versions(request, id):

    property = DashboardPropertyService.get_by_id(id)

    versions = DashboardPropertyService.get_versions(
        property
    )

    return render(
        request,
        "dashboard/property_versions.html",
        {
            "property": property,
            "versions": versions,
        }
    )
@login_required(login_url="broker_login")
@staff_member_required
def rollback_property(request, property_id, version_id):

    property = DashboardPropertyService.get_by_id(
        property_id
    )

    version = get_object_or_404(
        PropertyVersion,
        id=version_id,
        property=property
    )

    DashboardPropertyService.rollback(
        property,
        version
    )

    messages.success(
        request,
        "Property rolled back successfully."
    )

    return redirect(
        "property_versions",
        id=property.id
    )
#preview
@staff_member_required
def preview_home(request):

    featured_properties = (
        DashboardPropertyService
        .get_featured()
    )

    latest_properties = (
        DashboardPropertyService
        .get_latest(6)
    )

    return render(
        request,
        "home.html",
        {
            "featured_properties": featured_properties,
            "latest_properties": latest_properties,
            "preview_mode": True
        }
    )
@staff_member_required
def preview_property_list(request):

    properties = DashboardPropertyService.get_all()

    search = request.GET.get("search")

    city = request.GET.get("city")

    property_type = request.GET.get(
        "property_type"
    )

    if search:

        properties = properties.filter(
            title__icontains=search
        )

    if city:

        properties = properties.filter(
            city__icontains=city
        )

    if property_type:

        properties = properties.filter(
            property_type=property_type
        )

    return render(
        request,
        "property/browse_properties.html",
        {
            "properties": properties,
            "preview_mode": True
        }
    )
@staff_member_required
def preview_property_detail(request, id):

    property = DashboardPropertyService.get_by_id(id)

    return render(
        request,
        "property/property_detail.html",
        {
            "property": property,
            "preview_mode": True
        }
    )