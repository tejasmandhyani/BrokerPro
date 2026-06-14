from django.shortcuts import render, get_object_or_404,redirect
from .models import Property,Appointment,CustomerProfile,Broker
from django.contrib import messages
from .forms import ConsultationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from .forms import CustomerRegistrationForm
from django.contrib.auth.decorators import login_required
#property add using restapiframework 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import PropertySerializer,PropertyDetailSerializer,AppointmentSerializer,BrokerSerializer,ConsultationSerializer
from properties.services.api_client import get,get_property,post


#home page 
def home(request):
    return render(request, "home.html")


def property_detail(request, id):

    property = get_property(id)

    return render(
        request,
        "property/property_detail.html",
        {
            "property": property
        }
    )
@login_required(login_url="login")
def book_appointment(request, id):

    property = get_object_or_404(
        Property,
        id=id
    )

    if request.method == "POST":

        status_code = post(

            "/api/appointments/",

            {

                "property": property.id,

                "customer_name": request.POST.get(
                    "customer_name"
                ),

                "email": request.POST.get(
                    "email"
                ),

                "phone": request.POST.get(
                    "phone"
                ),

                "appointment_date": request.POST.get(
                    "appointment_date"
                ),

                "appointment_time": request.POST.get(
                    "appointment_time"
                ),

                "message": request.POST.get(
                    "message"
                )

            }

        )

        if status_code == 201:

            messages.success(
                request,
                "Appointment request submitted successfully."
            )

            return redirect(
                "property_detail",
                id=property.id
            )

        else:

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

@login_required(login_url="login")
def consultation(request):

    brokers = get(
        "/api/brokers/",
        auth=False
    )

    broker = brokers[0] if brokers else None

    form = ConsultationForm()

    if request.method == "POST":

        form = ConsultationForm(request.POST)

        if form.is_valid():

            customer = CustomerProfile.objects.get(
                user=request.user
            )

            data = form.cleaned_data.copy()

            data["broker"] = request.POST.get("broker")
            data["customer_name"] = customer.full_name
            data["email"] = request.user.email
            data["phone"] = customer.phone

            status_code = post(
                "/api/consultation/",
                data
            )

            if status_code == 201:

                messages.success(
                    request,
                    "Consultation request submitted successfully."
                )

                return redirect("consultation")

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
            "broker": broker
        }
    )
    
def property_list(request):

    params = {}

    if request.GET.get("search"):
        params["search"] = request.GET.get("search")

    if request.GET.get("city"):
        params["city"] = request.GET.get("city")

    if request.GET.get("property_type"):
        params["property_type"] = request.GET.get("property_type")

    properties = get(
    "/api/properties/",
    params=params,
    auth=False
    )

    properties = [
        p for p in properties
        if p["publish_status"] == "Published"
    ]

    return render(
        request,
        "property/browse_properties.html",
        {
            "properties": properties
        }
    )

#register - view
def register(request):

    if request.method == 'POST':

        form = CustomerRegistrationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()
            CustomerProfile.objects.create(

             user=user,

            full_name=form.cleaned_data[
              'full_name'
             ],

            phone=form.cleaned_data[
             'phone'
              ],

             city=form.cleaned_data[
             'city'
             ]
            )
            

            login(
                request,
                user
            )

            return redirect(
                'home'
            )

    else:

        form = CustomerRegistrationForm()

    return render(
        request,
        'registration/register.html',
        {
            'form': form
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

        user = authenticate(
            request,
            username=username,
            password=password
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

    logout(request)

    messages.success(
        request,
        'Logged out successfully.'
    )

    return redirect(
        'home'
    )

@login_required(login_url='login')
def profile_view(request):

    appointments = Appointment.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )

    context = {

        'appointments': appointments,

        'appointment_count':
        appointments.count()

    }

    return render(
        request,
        'accounts/profile.html',
        context
    )

def about(request):

    brokers = get(
    "/api/brokers/",
    auth=False
    )

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

        properties = Property.objects.filter(
            publish_status="Published"
        )

        search = request.GET.get("search")
        city = request.GET.get("city")
        property_type = request.GET.get("property_type")

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

        serializer = PropertySerializer(
            properties,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)
    def post(self, request):

        serializer = PropertySerializer(
        data=request.data,
        context={"request": request}
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
            serializer.data,
            status=201
            )

        return Response(
        serializer.errors,
        status=400
         )
    
class PropertyDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        property = get_object_or_404(
            Property,
            pk=pk,
            publish_status="Published"
        )

        serializer = PropertyDetailSerializer(
            property,
            context={"request": request}
        )

        return Response(serializer.data)

class BrokerListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        brokers = Broker.objects.all()

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
            context={"request": request}
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
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