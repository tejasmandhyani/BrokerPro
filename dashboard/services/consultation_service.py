from properties.models import ConsultationLead


class DashboardConsultationService:

    @staticmethod
    def get_all():

        return (
            ConsultationLead.objects
            .select_related(
                "broker",
                "user"
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_by_id(consultation_id):

        return (
            ConsultationLead.objects
            .select_related(
                "broker",
                "user"
            )
            .get(id=consultation_id)
        )

    @staticmethod
    def count():

        return ConsultationLead.objects.count()