from django.db.models import Q

from properties.models import Property
from properties.serializers import PropertySerializer


class PropertyService:

    @staticmethod
    def create(data, request):

        serializer = PropertySerializer(
            data=data,
            context={
            "request": request
            }
        )

        serializer.is_valid(
        raise_exception=True
        )

        return serializer.save()

    @staticmethod
    def get_all():
        return (
            Property.objects
            .filter(publish_status="Published")
            .select_related("broker")
        )

    @staticmethod
    def get_by_id(property_id):

        return (
        Property.objects
        .select_related("broker")
        .prefetch_related(
            "images",
            "videos",
        )
        .get(
            id=property_id,
            publish_status="Published",
        )
    )
    @staticmethod
    def search(search=None, city=None, property_type=None):

        queryset = PropertyService.get_all()

        if search:

            queryset = queryset.filter(

            Q(title__icontains=search) |

            Q(description__icontains=search) |

            Q(city__icontains=search) |

            Q(location__icontains=search) |

            Q(property_type__icontains=search)

            )

        if city:

            queryset = queryset.filter(
            city__icontains=city
            )

        if property_type:

            queryset = queryset.filter(
            property_type=property_type
            )

        return queryset
    @staticmethod
    def get_all_cities():

        return (
        Property.objects
        .filter(publish_status="Published")
        .values_list("city", flat=True)
        .distinct()
        .order_by("city")
        )