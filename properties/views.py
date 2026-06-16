from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import ConsultationForm
from django.contrib.auth import login

from .forms import CustomerRegistrationForm
from django.contrib.auth.decorators import login_required
#property add using restapiframework 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import PropertySerializer,PropertyDetailSerializer,AppointmentSerializer,BrokerSerializer,ConsultationSerializer

#main imports after updating architecture
from properties.services.property_service import PropertyService
from properties.services.broker_service import BrokerService
from properties.services.appointment_service import AppointmentService
from properties.services.consultation_service import ConsultationService
from properties.services.home_service import HomeService
from properties.services.auth_service import AuthService


#updated with new service 
def home(request):

    context = HomeService.get_home_page_data()

    return render(
        request,
        "home.html",
        context
    )

#changed property_detail with new service
def property_detail(request, id):

    property = PropertyService.get_by_id(id)

    return render(
        request,
        "property/property_detail.html",
        {
            "property": property
        }
    )
#updated with new service
@login_required(login_url="login")
def book_appointment(request, id):

    property = PropertyService.get_by_id(id)

    if request.method == "POST":

        try:

            AppointmentService.create(

                user=request.user,

                property=property,

                customer_name=request.POST.get("customer_name"),

                email=request.POST.get("email"),

                phone=request.POST.get("phone"),

                appointment_date=request.POST.get("appointment_date"),

                appointment_time=request.POST.get("appointment_time"),

                message=request.POST.get("message"),

            )

            messages.success(
                request,
                "Appointment request submitted successfully."
            )

            return redirect(
                "property_detail",
                id=property.id
            )

        except Exception as e:

            print(e)   # <-- Keep this temporarily for debugging

            messages.error(
                request,
                "Unable to submit appointment request."
            )

    return render(
        request,
        "book_appointment.html",
        {
            "property": property
        }
    )
from .models import Broker

from properties.models import CustomerProfile

#updated with new service 

def consultation(request):

    brokers, broker = BrokerService.get_all_with_first()

    form = ConsultationForm()

    if request.method == "POST":

        form = ConsultationForm(request.POST)

        if form.is_valid():

            try:

                ConsultationService.create(
                    request=request,
                    form=form
                )

                messages.success(
                    request,
                    "Consultation request submitted successfully."
                )

                return redirect("consultation")

            except Exception:

                messages.error(
                    request,
                    "Unable to submit consultation request."
                )

    return render(
        request,
        "property/consultation.html",
        {
            "form": form,
            "brokers": brokers,
            "broker": broker,
        },
    )
#updated with new service 
from .models import Property

def property_list(request):

    properties = PropertyService.search(

        search=request.GET.get("search"),

        city=request.GET.get("city"),

        property_type=request.GET.get("property_type"),

    )

    cities = (
        Property.objects
        .values_list("city", flat=True)
        .distinct()
        .order_by("city")
    )

    return render(

        request,

        "property/browse_properties.html",

        {

            "properties": properties,

            "cities": cities,

        }

    )
#register - view
def register(request):

    if request.method == "POST":

        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():

            user = AuthService.register(form)

            login(
                request,
                user
            )

            return redirect("home")

    else:

        form = CustomerRegistrationForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form
        }
    )
#login - view 
def login_view(request):

    if request.user.is_authenticated:

        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = AuthService.login(
        request,
        username,
        password
        )

        if user is not None:

            login(
                request,
                user
            )

            messages.success(
                request,
                f'Welcome {user.username}'
            )

            return redirect(
                'home'
            )

        else:

            messages.error(
                request,
                'Invalid username or password'
            )

    return render(
        request,
        'accounts/login.html'
    )

#logout view 
@login_required(login_url='login')
def logout_view(request):

    AuthService.logout(request)

    messages.success(
        request,
        'Logged out successfully.'
    )

    return redirect(
        'home'
    )

@login_required(login_url="login")
def profile_view(request):

    appointments = AppointmentService.get_user_appointments(
        request.user
    )

    context = {
        "appointments": appointments,
        "appointment_count": appointments.count(),
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )
#updated
def about(request):

    brokers = BrokerService.get_all()

    return render(
        request,
        "property/about.html",
        {
            "brokers": brokers
        }
    )
# property list Api View
class PropertyListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        properties = PropertyService.search(

            search=request.GET.get("search"),

            city=request.GET.get("city"),

            property_type=request.GET.get("property_type"),

        )

        serializer = PropertySerializer(

            properties,

            many=True,

            context={
                "request": request
            }

        )

        return Response(serializer.data)

    def post(self, request):

        try:

            property = PropertyService.create(

                request.data,

                request

            )

            return Response(

                PropertySerializer(

                    property,

                    context={
                        "request": request
                    }

                ).data,

                status=status.HTTP_201_CREATED,

            )

        except Exception as e:

            return Response(

                {

                    "error": str(e)

                },

                status=status.HTTP_400_BAD_REQUEST,

            )
class PropertyDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        property = PropertyService.get_by_id(pk)

        serializer = PropertyDetailSerializer(
            property,
            context={"request": request}
        )

        return Response(serializer.data)

class BrokerListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        brokers = BrokerService.get_all()

        serializer = BrokerSerializer(
            brokers,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

class ConsultationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ConsultationSerializer(

        data=request.data,

        context={
            "request": request
        }

        )

        serializer.is_valid(
        raise_exception=True
        )

        consultation = serializer.save()

        return Response(

        ConsultationSerializer(

            consultation,

            context={
                "request": request
            }

        ).data,

        status=status.HTTP_201_CREATED,

    )
class AppointmentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = AppointmentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            property = serializer.validated_data["property"]

            appointment = serializer.save(

                user=request.user,

                broker=property.broker,

                status="Pending"

            )

            return Response(

                AppointmentSerializer(
                    appointment
                ).data,

                status=status.HTTP_201_CREATED

            )

        return Response(

            serializer.errors,

            status=status.HTTP_400_BAD_REQUEST

        )