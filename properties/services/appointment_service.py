from properties.models import Appointment


class AppointmentService:

    @staticmethod
    def create(
        *,
        user,
        property,
        customer_name,
        email,
        phone,
        appointment_date,
        appointment_time,
        message,
    ):

        appointment = Appointment.objects.create(
            user=user,
            broker=property.broker,
            property=property,
            customer_name=customer_name,
            email=email,
            phone=phone,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            message=message,
            status="Pending",
        )

        return appointment

    @staticmethod
    def get_user_appointments(user):

        return (
            Appointment.objects
            .filter(user=user)
            .select_related(
                "property",
                "broker"
            )
            .order_by("-created_at")
        )