from rest_framework import serializers
from properties.models import Property,PropertyVersion,Appointment,ConsultationLead


class DashboardPropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        exclude = [
            "broker",
            "created_at",
        ]

class PropertyVersionSerializer(serializers.ModelSerializer):

    class Meta:

        model = PropertyVersion

        fields = "__all__"

class DashboardAppointmentSerializer(serializers.ModelSerializer):

    property_title = serializers.CharField(
        source="property.title",
        read_only=True
    )

    class Meta:

        model = Appointment

        fields = [
            "id",
            "customer_name",
            "email",
            "phone",
            "appointment_date",
            "appointment_time",
            "status",
            "property_title",
            "created_at"
        ]

class DashboardCustomerSerializer(serializers.Serializer):

    customer_name = serializers.CharField()

    email = serializers.EmailField()

    phone = serializers.CharField()

    appointments = serializers.IntegerField()

class DashboardConsultationSerializer(serializers.ModelSerializer):

    class Meta:

        model = ConsultationLead

        fields = [
            "id",
            "customer_name",
            "email",
            "phone",
            "budget",
            "requirements",
            "status",
            "created_at"
        ]