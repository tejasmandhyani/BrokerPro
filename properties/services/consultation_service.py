from properties.models import CustomerProfile
from properties.serializers import ConsultationSerializer


class ConsultationService:

    @staticmethod
    def create(request, form):

        data = form.cleaned_data.copy()

        data["broker"] = request.POST.get("broker")

        if request.user.is_authenticated:

            data["user"] = request.user.id

        serializer = ConsultationSerializer(
            data=data,
            context={
            "request": request
        }
        )

        serializer.is_valid(
        raise_exception=True
        )

        return serializer.save()