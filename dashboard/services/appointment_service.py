from datetime import date
import urllib.parse

from properties.models import Appointment


class DashboardAppointmentService:

    @staticmethod
    def get_all():

        return (
            Appointment.objects
            .select_related(
                "property",
                "broker",
                "user"
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_by_id(appointment_id):

        return (
            Appointment.objects
            .select_related(
                "property",
                "broker",
                "user"
            )
            .get(id=appointment_id)
        )

    @staticmethod
    def get_today():

        return (
            Appointment.objects
            .filter(
                appointment_date=date.today()
            )
            .select_related(
                "property",
                "broker",
                "user"
            )
            .order_by("appointment_time")
        )

    @staticmethod
    def get_upcoming():

        return (
            Appointment.objects
            .filter(
                appointment_date__gt=date.today()
            )
            .select_related(
                "property",
                "broker",
                "user"
            )
            .order_by(
                "appointment_date",
                "appointment_time"
            )
        )

    @staticmethod
    def accept(appointment):

        appointment.status = "Accepted"

        appointment.save()

    @staticmethod
    def reject(appointment):

        appointment.status = "Rejected"

        appointment.save()

    @staticmethod
    def get_whatsapp_url(appointment):

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

        return (
        f"https://wa.me/91{appointment.phone}"
        f"?text={encoded_message}"
    )

    @staticmethod
    def expire_pending():

        Appointment.objects.filter(
        appointment_date__lt=date.today(),
        status="Pending"
        ).update(
        status="Expired"
        )