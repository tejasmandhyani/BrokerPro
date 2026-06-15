from datetime import date

from properties.models import (
    Property,
    PropertyImage,
    PropertyVideo,
    Appointment,
    CustomerProfile,
    ConsultationLead,
)


class DashboardService:

    @staticmethod
    def get_dashboard_data():

        return {

            "property_count": Property.objects.count(),

            "customer_count": CustomerProfile.objects.count(),

            "appointment_count": Appointment.objects.count(),

            "consultation_count": ConsultationLead.objects.count(),

            "today_visits": Appointment.objects.filter(
                appointment_date=date.today()
            ).count(),

            "pending_appointments": Appointment.objects.filter(
                status="Pending"
            ).count(),

        }
    
    @staticmethod
    def add_images(property, images):

        for image in images:

            PropertyImage.objects.create(
            property=property,
            image=image
            )
    
    @staticmethod
    def add_videos(property, videos):

        for video in videos:

            PropertyVideo.objects.create(
            property=property,
            video=video
            )
    
    @staticmethod
    def delete_image(image):

        image.delete()
    
    @staticmethod
    def delete_video(video):

        video.delete()