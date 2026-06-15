from properties.models import Broker
from django.contrib.auth import authenticate


class DashboardBrokerService:

    @staticmethod
    def get_all():

        return Broker.objects.all()

    @staticmethod
    def get_by_user(user):

        return Broker.objects.filter(
            user=user
        ).first()

    @staticmethod
    def get_by_id(broker_id):

        return Broker.objects.get(
            id=broker_id
        )

    @staticmethod
    def count():

        return Broker.objects.count()
    
    @staticmethod
    def authenticate_broker(
        username,
        password
        ):

        return authenticate(
        username=username,
        password=password
        )
    
    @staticmethod
    def is_staff(user):

        return user and user.is_staff
    
    