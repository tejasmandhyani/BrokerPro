from properties.models import CustomerProfile
from properties.serializers import ConsultationSerializer


class ConsultationService:

    @staticmethod
    def create(request, form):

        customer = CustomerProfile.objects.get(
            user=request.user
        )

        data = form.cleaned_data.copy()

        data["broker"] = request.POST.get("broker")
        data["customer_name"] = customer.full_name
        data["email"] = request.user.email
        data["phone"] = customer.phone

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