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


def expire_appointments():

    Appointment.objects.filter(
        appointment_date__lt=date.today(),
        status='Pending'
    ).update(
        status='Expired'
    )

def broker_login(request):

    print("BROKER LOGIN VIEW CALLED")

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

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user and user.is_staff:

            login(
                request,
                user
            )

            tokens = token_login(
                username,
                password
            )

            print("TOKENS:", tokens)

            if not tokens:

                messages.error(
                    request,
                    "Unable to generate API token."
                )

                logout(request)

                return redirect(
                    "broker_login"
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

    response = get(
        "/api/dashboard/dashboard/",
        request.user.username
    )

    if response.status_code != 200:

        messages.error(
            request,
            "Unable to load dashboard."
        )

        return redirect(
            "broker_login"
        )

    context = response.json()

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )
@staff_member_required
def property_list(request):

    response = get(
        "/api/dashboard/properties/",
        request.user.username
    )

    if response.status_code == 200:

        properties = response.json()

    else:

        properties = []

    return render(
        request,
        "dashboard/property_list.html",
        {
            "properties": properties
        }
    )

@staff_member_required
def property_create(request):

    if request.method == "POST":

        form = PropertyForm(request.POST)

        if form.is_valid():

            files = []

            for image in request.FILES.getlist("images"):

                files.append(
                    ("images", image)
                )

            for video in request.FILES.getlist("videos"):

                files.append(
                    ("videos", video)
                )

            response = post(
             "/api/dashboard/properties/create/",
            username=request.user.username,
            data=form.cleaned_data,
            files=files
            )

            if response.status_code == 201:

                messages.success(
                    request,
                    "Property added successfully."
                )

                return redirect("property_list")

            messages.error(
                request,
                response.text
            )

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

    if request.method == "POST":

        response = put(
            f"/api/dashboard/properties/{id}/",
            request.user.username,
            data=request.POST
        )

        if response.status_code == 200:

            return redirect(
                "property_list"
            )

    response = get(
        f"/api/dashboard/properties/{id}/",
        request.user.username
    )

    if response.status_code != 200:

        messages.error(
            request,
            "Property not found."
        )

        return redirect(
            "property_list"
        )

    property = response.json()

    form = PropertyForm(
        initial={
            "title": property["title"],
            "city": property["city"],
            "location": property["location"],
            "property_type": property["property_type"],
            "status": property["status"],
            "price": property["price"],
            "bedrooms": property["bedrooms"],
            "bathrooms": property["bathrooms"],
            "area_sqft": property["area_sqft"],
            "description": property["description"],
            "featured": property["featured"],
        }
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

    if request.method == "POST":

        response = delete(
            f"/api/dashboard/properties/delete/{id}/",
            request.user.username
        )

        if response.status_code == 200:

            return redirect("property_list")

    response = get(
        f"/api/dashboard/properties/{id}/",
        request.user.username
    )

    if response.status_code != 200:

        messages.error(
            request,
            "Property not found."
        )

        return redirect("property_list")

    property = response.json()

    return render(
        request,
        "dashboard/property_delete.html",
        {
            "property": property
        }
    )

from django.contrib import messages
@staff_member_required
def property_images(request, id):

    response = get(
        f"/api/dashboard/properties/{id}/",
        request.user.username
    )

    if response.status_code != 200:

        messages.error(
            request,
            "Property not found."
        )

        return redirect(
            "property_list"
        )

    property = response.json()

    if request.method == "POST":

        upload_type = request.POST.get(
            "upload_type"
        )

        if upload_type == "image":

            print(request.FILES)
            print(request.FILES.getlist("images"))
            print(len(request.FILES.getlist("images")))

            response = post(

                f"/api/dashboard/properties/images/{id}/",

                request.user.username,

                files=request.FILES
            )

            if response.status_code == 201:

                messages.success(
                    request,
                    "Images uploaded successfully."
                )

            else:

                messages.error(
                    request,
                    "Image upload failed."
                )

        elif upload_type == "video":

            response = post(

                f"/api/dashboard/properties/videos/{id}/",

                request.user.username,

                files=request.FILES
            )

            if response.status_code == 201:

                messages.success(
                    request,
                    "Video uploaded successfully."
                )

            else:

                messages.error(
                    request,
                    "Video upload failed."
                )

        return redirect(
            "property_images",
            id=id
        )

    return render(

        request,

        "dashboard/property_images.html",

        {
            "property": property
        }

    )
@staff_member_required
def delete_property_image(request, id):

    response = delete(

        f"/api/dashboard/properties/image/delete/{id}/",

        request.user.username

    )

    if response.status_code == 200:

        messages.success(
            request,
            "Image deleted successfully."
        )

    else:

        messages.error(
            request,
            "Unable to delete image."
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "property_list"
        )
    )
@staff_member_required
def delete_property_video(request, id):

    response = delete(

        f"/api/dashboard/properties/video/delete/{id}/",

        request.user.username

    )

    if response.status_code == 200:

        messages.success(
            request,
            "Video deleted successfully."
        )

    else:

        messages.error(
            request,
            "Unable to delete video."
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "property_list"
        )
    )

@staff_member_required
def appointment_list(request):

    response = get(
        "/api/dashboard/appointments/",
        request.user.username
    )

    if response.status_code != 200:

        messages.error(
            request,
            "Unable to load appointments."
        )

        return redirect(
            "dashboard_home"
        )

    appointments = response.json()

    return render(
        request,
        "dashboard/appointment_list.html",
        {
            "appointments": appointments
        }
    )

@staff_member_required
def accept_appointment(request, id):

    response = post(

        f"/api/dashboard/appointments/accept/{id}/",

        request.user.username

    )

    if response.status_code == 200:

        messages.success(
            request,
            "Appointment accepted successfully."
        )

    else:

        messages.error(
            request,
            "Unable to accept appointment."
        )

    return redirect(
        "appointment_list"
    )


@staff_member_required
def reject_appointment(request, id):

    response = post(
        f"/api/dashboard/appointments/reject/{id}/",
        request.user.username
    )

    if response.status_code == 200:

        messages.success(
            request,
            "Appointment rejected successfully."
        )

    else:

        messages.error(
            request,
            "Unable to reject appointment."
        )

    return redirect(
        "appointment_list"
    )
#customer functionn
@staff_member_required
def customer_list(request):

    response = get(
        "/api/dashboard/customers/",
        request.user.username
    )

    if response.status_code != 200:

        messages.error(
            request,
            "Unable to load customers."
        )

        return redirect(
            "dashboard_home"
        )

    customers = response.json()

    return render(
        request,
        "dashboard/customer_list.html",
        {
            "customers": customers
        }
    )
#whatsapp view 
@staff_member_required
def whatsapp_customer(request, id):

    appointment = get_object_or_404(
        Appointment,
        id=id
    )

    message = f"""
Hello {appointment.customer_name},

Your appointment request for
{appointment.property.title}

Status: {appointment.status}

Date: {appointment.appointment_date}
Time: {appointment.appointment_time}

For any questions, please contact us.

Thank you,
BrokerPro
"""

    encoded_message = urllib.parse.quote(
        message
    )

    whatsapp_url = (
        f"https://wa.me/91{appointment.phone}"
        f"?text={encoded_message}"
    )

    return redirect(
        whatsapp_url
    )

#dashboard todays and upcoming visits 
@staff_member_required
def today_visits(request):

    response = get(
        "/api/dashboard/appointments/today/",
        request.user.username
    )

    if response.status_code != 200:

        messages.error(
            request,
            "Unable to load today's visits."
        )

        return redirect("appointment_list")

    appointments = response.json()

    return render(
        request,
        "dashboard/today_visits.html",
        {
            "appointments": appointments
        }
    )
@staff_member_required
def upcoming_visits(request):

    response = get(
        "/api/dashboard/appointments/upcoming/",
        request.user.username
    )

    if response.status_code != 200:

        messages.error(
            request,
            "Unable to load upcoming visits."
        )

        return redirect("appointment_list")

    appointments = response.json()

    return render(
        request,
        "dashboard/upcoming_visits.html",
        {
            "appointments": appointments
        }
    )

#consultation List 
@staff_member_required
def consultation_list(request):

    response = get(
        "/api/dashboard/consultations/",
        request.user.username
    )

    if response.status_code != 200:

        messages.error(
            request,
            "Unable to load consultation leads."
        )

        return redirect(
            "dashboard_home"
        )

    leads = response.json()

    return render(
        request,
        "dashboard/consultation_list.html",
        {
            "leads": leads
        }
    )
#publish and unpublish views
@staff_member_required
def publish_property(request, id):

    response = post(
        f"/api/dashboard/properties/publish/{id}/",
        request.user.username
    )

    if response.status_code == 200:

        messages.success(
            request,
            "Property published successfully."
        )

    else:

        messages.error(
            request,
            "Unable to publish property."
        )

    return redirect(
        "property_list"
    )


@staff_member_required
def unpublish_property(request, id):

    response = post(
        f"/api/dashboard/properties/unpublish/{id}/",
        request.user.username
    )

    if response.status_code == 200:

        messages.success(
            request,
            "Property unpublished successfully."
        )

    else:

        messages.error(
            request,
            "Unable to unpublish property."
        )

    return redirect(
        "property_list"
    )
#rollback and versions 
@staff_member_required
def property_versions(request, id):

    response = get(
        f"/api/dashboard/property/{id}/versions/",
        request.user.username
    )

    if response.status_code != 200:

        messages.error(
            request,
            "Unable to load property versions."
        )

        return redirect(
            "property_list"
        )

    versions = response.json()

    return render(
        request,
        "dashboard/property_versions.html",
        {
            "versions": versions
        }
    )
@staff_member_required
def rollback_property(request, version_id):

    response = post(
        f"/api/dashboard/rollback/{version_id}/",
        request.user.username
    )

    if response.status_code == 200:

        messages.success(
            request,
            "Property restored successfully."
        )

    else:

        messages.error(
            request,
            "Unable to restore property."
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "property_list"
        )
    )
#preview
@staff_member_required
def preview_home(request):

    properties = get_dashboard_properties(
        request.user.username
    )

    print("=" * 80)
    print(properties)
    print("=" * 80)

    featured_properties = [
        p for p in properties
        if p["featured"]
    ]

    latest_properties = sorted(
        properties,
        key=lambda x: x["created_at"],
        reverse=True
    )[:6]

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

    properties = get_dashboard_properties(
        request.user.username
    )

    search = request.GET.get("search", "").lower()
    city = request.GET.get("city", "").lower()
    property_type = request.GET.get("property_type", "").lower()

    if search:

        properties = [
            p for p in properties
            if search in p["title"].lower()
        ]

    if city:

        properties = [
            p for p in properties
            if city in p["city"].lower()
        ]

    if property_type:

        properties = [
            p for p in properties
            if property_type in p["property_type"].lower()
        ]

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

    property = get_dashboard_property(
        id,
        request.user.username
    )

    print("=" * 80)
    print(property)
    print("=" * 80)

    return render(
        request,
        "property/property_detail.html",
        {
            "property": property,
            "preview_mode": True
        }
    )