from properties.models import CustomerProfile
from django.db.models import Count


class DashboardCustomerService:

    from django.db.models import Count
from properties.models import CustomerProfile


class DashboardCustomerService:

    @staticmethod
    def get_all():

        return (
            CustomerProfile.objects
            .select_related("user")
            .annotate(
                appointment_count=Count("user__appointment")
            )
            .order_by("-id")
        )
    @staticmethod
    def get_by_id(customer_id):

        return (
            CustomerProfile.objects
            .select_related("user")
            .get(id=customer_id)
            
        )

    @staticmethod
    def count():

        return CustomerProfile.objects.count()