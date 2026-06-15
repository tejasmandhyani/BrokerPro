from properties.models import Property, Broker


class HomeService:

    @staticmethod
    def get_home_page_data():

        return {
            "featured_properties": (
                Property.objects
                .filter(
                    publish_status="Published",
                    featured=True
                )
                .select_related("broker")
            ),

            "latest_properties": (
                Property.objects
                .filter(
                    publish_status="Published"
                )
                .select_related("broker")
                .order_by("-created_at")[:6]
            ),

            "brokers": Broker.objects.all(),

            "total_properties": Property.objects.filter(
                publish_status="Published"
            ).count(),

            "total_brokers": Broker.objects.count(),
        }