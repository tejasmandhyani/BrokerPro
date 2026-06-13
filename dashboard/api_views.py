from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.shortcuts import get_object_or_404
from properties.models import (
    Property,
    Broker,
    PropertyImage,
    PropertyVideo,PropertyVersion,ConsultationLead,Appointment
)

from properties.serializers import PropertyDetailSerializer,PropertySerializer
from dashboard.serializers import PropertyVersionSerializer,DashboardConsultationSerializer,DashboardCustomerSerializer,DashboardAppointmentSerializer
from .serializers import DashboardPropertySerializer


class DashboardPropertyAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        print("=" * 50)
        print("Authenticated User:", request.user)
        print("Username:", request.user.username)
        print("=" * 50)

        serializer = DashboardPropertySerializer(
            data=request.data
        )

        if serializer.is_valid():

            broker = Broker.objects.get(
                user=request.user
            )

            property = serializer.save(
                broker=broker
            )

            images = request.FILES.getlist("images")

            if images:

                for image in images:

                    PropertyImage.objects.create(
                    property=property,
                    image=image
                    )

            else:

                PropertyImage.objects.create(
                property=property,
                image="defaults/property_default.jpg"
                )

            videos = request.FILES.getlist("videos")

            for video in videos:

                PropertyVideo.objects.create(
                    property=property,
                    video=video
                )

            return Response(
                PropertyDetailSerializer(
                    property,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class DashboardPropertyListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        broker = Broker.objects.get(
            user=request.user
        )

        properties = Property.objects.filter(
            broker=broker
        ).order_by("-created_at")

        serializer = PropertySerializer(
            properties,
            many=True
        )

        return Response(serializer.data)
    
class DashboardPropertyUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        broker = Broker.objects.get(
            user=request.user
        )

        property = get_object_or_404(
            Property,
            id=id,
            broker=broker
        )

        serializer = PropertyDetailSerializer(
            property,
            context={"request": request}
        )

        return Response(serializer.data)


    def put(self, request, id):

        broker = Broker.objects.get(
            user=request.user
        )

        property = get_object_or_404(
            Property,
            id=id,
            broker=broker
        )

        serializer = DashboardPropertySerializer(
            property,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            PropertyVersion.objects.create(

            property=property,

            title=property.title,

            city=property.city,

            location=property.location,

            property_type=property.property_type,

            status=property.status,

            publish_status=property.publish_status,

            price=property.price,

            bedrooms=property.bedrooms,

            bathrooms=property.bathrooms,

            area_sqft=property.area_sqft,

            description=property.description

            )

            serializer.save()

            return Response(
                PropertyDetailSerializer(
                    property,
                    context={"request": request}
                ).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class DashboardPropertyDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        broker = Broker.objects.get(
            user=request.user
        )

        property = get_object_or_404(
            Property,
            id=id,
            broker=broker
        )

        property.delete()

        return Response(
            {
                "message": "Property deleted successfully."
            },
            status=status.HTTP_200_OK
        )

class DashboardPropertyImageAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        broker = Broker.objects.get(
            user=request.user
        )

        property = get_object_or_404(
            Property,
            id=id,
            broker=broker
        )
        print(request.FILES)
        print(request.FILES.getlist("images"))
        print("API TOTAL:", len(request.FILES.getlist("images")))

        images = request.FILES.getlist(
            "images"
        )

        for image in images:

            PropertyImage.objects.create(
                property=property,
                image=image
            )

        return Response(
            {
                "message": "Images uploaded successfully."
            },
            status=status.HTTP_201_CREATED
        )
    
class DashboardDeletePropertyImageAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        image = get_object_or_404(
            PropertyImage,
            id=id,
            property__broker__user=request.user
        )

        image.delete()

        return Response(
            {
                "message": "Image deleted successfully."
            },
            status=status.HTTP_200_OK
        )

class DashboardPropertyVideoAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        broker = Broker.objects.get(
            user=request.user
        )

        property = get_object_or_404(
            Property,
            id=id,
            broker=broker
        )

        videos = request.FILES.getlist(
            "videos"
        )

        for video in videos:

            PropertyVideo.objects.create(
                property=property,
                video=video
            )

        return Response(
            {
                "message": "Videos uploaded successfully."
            },
            status=status.HTTP_201_CREATED
        )
class DashboardDeletePropertyVideoAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        video = get_object_or_404(
            PropertyVideo,
            id=id,
            property__broker__user=request.user
        )

        video.delete()

        return Response(
            {
                "message": "Video deleted successfully."
            },
            status=status.HTTP_200_OK
        )

class DashboardPublishPropertyAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        broker = Broker.objects.get(
            user=request.user
        )

        property = get_object_or_404(
            Property,
            id=id,
            broker=broker
        )

        property.publish_status = "Published"

        property.save()

        return Response(
            {
                "message": "Property published successfully."
            },
            status=status.HTTP_200_OK
        )
    
class DashboardUnpublishPropertyAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        broker = Broker.objects.get(
            user=request.user
        )

        property = get_object_or_404(
            Property,
            id=id,
            broker=broker
        )

        property.publish_status = "Draft"

        property.save()

        return Response(
            {
                "message": "Property unpublished successfully."
            },
            status=status.HTTP_200_OK
        )
class DashboardPropertyVersionsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        broker = Broker.objects.get(
            user=request.user
        )

        property = get_object_or_404(
            Property,
            id=id,
            broker=broker
        )

        versions = PropertyVersion.objects.filter(
            property=property
        ).order_by("-created_at")

        serializer = PropertyVersionSerializer(
            versions,
            many=True
        )

        return Response(serializer.data)
    
class DashboardRollbackPropertyAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, version_id):

        version = get_object_or_404(
            PropertyVersion,
            id=version_id,
            property__broker__user=request.user
        )

        property = version.property

        property.title = version.title
        property.city = version.city
        property.location = version.location
        property.property_type = version.property_type
        property.status = version.status
        property.publish_status = version.publish_status
        property.price = version.price
        property.bedrooms = version.bedrooms
        property.bathrooms = version.bathrooms
        property.area_sqft = version.area_sqft
        property.description = version.description

        property.save()

        return Response(
            {
                "message": "Property restored successfully."
            },
            status=status.HTTP_200_OK
        )
    
class DashboardHomeAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        broker = Broker.objects.get(
            user=request.user
        )

        total_properties = Property.objects.filter(
            broker=broker
        ).count()

        pending_appointments = Appointment.objects.filter(
            broker=broker,
            status="Pending"
        ).count()

        customer_count = Appointment.objects.filter(
            broker=broker
        ).values(
            "customer_name",
            "email",
            "phone"
        ).distinct().count()

        lead_count = ConsultationLead.objects.filter(
            broker=broker
        ).count()

        return Response(
            {
                "total_properties": total_properties,
                "pending_appointments": pending_appointments,
                "customer_count": customer_count,
                "lead_count": lead_count
            }
        )
    
class DashboardAppointmentListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        broker = Broker.objects.get(
            user=request.user
        )

        appointments = Appointment.objects.filter(
            broker=broker
        ).order_by("-created_at")

        serializer = DashboardAppointmentSerializer(
            appointments,
            many=True
        )

        return Response(
            serializer.data
        )
    
class DashboardAcceptAppointmentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        broker = Broker.objects.get(
            user=request.user
        )

        appointment = get_object_or_404(
            Appointment,
            id=id,
            broker=broker
        )

        appointment.status = "Accepted"

        appointment.save()

        return Response(
            {
                "message": "Appointment accepted successfully."
            },
            status=status.HTTP_200_OK
        )

class DashboardRejectAppointmentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        broker = Broker.objects.get(
            user=request.user
        )

        appointment = get_object_or_404(
            Appointment,
            id=id,
            broker=broker
        )

        appointment.status = "Rejected"

        appointment.save()

        return Response(
            {
                "message": "Appointment rejected successfully."
            },
            status=status.HTTP_200_OK
        )
    
from django.utils.timezone import localdate

class DashboardTodayAppointmentsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        broker = Broker.objects.get(
            user=request.user
        )

        appointments = Appointment.objects.filter(
            broker=broker,
            appointment_date=localdate(),
            status="Accepted"
        ).order_by("appointment_time")

        serializer = DashboardAppointmentSerializer(
            appointments,
            many=True
        )

        return Response(serializer.data)
    
class DashboardUpcomingAppointmentsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        broker = Broker.objects.get(
            user=request.user
        )

        appointments = Appointment.objects.filter(
            broker=broker,
            appointment_date__gt=localdate(),
            status="Accepted"
        ).order_by(
            "appointment_date",
            "appointment_time"
        )

        serializer = DashboardAppointmentSerializer(
            appointments,
            many=True
        )

        return Response(serializer.data)
    
from django.db.models import Count


class DashboardCustomerListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        broker = Broker.objects.get(
            user=request.user
        )

        customers = Appointment.objects.filter(
            broker=broker
        ).values(
            "customer_name",
            "email",
            "phone"
        ).annotate(
            appointments=Count("id")
        ).order_by(
            "customer_name"
        )

        serializer = DashboardCustomerSerializer(
            customers,
            many=True
        )

        return Response(
            serializer.data
        )
    
class DashboardConsultationListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        broker = Broker.objects.get(
            user=request.user
        )

        leads = ConsultationLead.objects.filter(
            broker=broker
        ).order_by(
            "-created_at"
        )

        serializer = DashboardConsultationSerializer(
            leads,
            many=True
        )

        return Response(
            serializer.data
        )
    
class DashboardPropertyPreviewAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        property = get_object_or_404(
            Property,
            id=id
        )

        serializer = PropertyDetailSerializer(
            property,
            context={"request": request}
        )

        return Response(serializer.data)
    
