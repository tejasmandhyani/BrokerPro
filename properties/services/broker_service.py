from django.shortcuts import get_object_or_404

from properties.models import Broker


class BrokerService:

    @staticmethod
    def get_all():

        return Broker.objects.all()

    @staticmethod
    def get_by_id(broker_id):

        return get_object_or_404(
            Broker,
            id=broker_id
        )

    @staticmethod
    def get_first():

        return Broker.objects.first()

    @staticmethod
    def exists():

        return Broker.objects.exists()

    @staticmethod
    def count():

        return Broker.objects.count()
    
    @staticmethod
    def get_all_with_first():

        brokers = Broker.objects.all()

        broker = brokers.first()

        return brokers, broker