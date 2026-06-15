from properties.models import CustomerProfile


class DashboardCustomerService:

    @staticmethod
    def get_all():

        return (
            CustomerProfile.objects
            .select_related("user")
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