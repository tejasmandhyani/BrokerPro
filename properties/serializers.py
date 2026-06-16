from rest_framework import serializers
from .models import Property,Broker,PropertyImage,PropertyVideo,ConsultationLead,Appointment



class PropertySerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = '__all__'

    def get_image_url(self, obj):

        image = obj.images.first()

        if image:

            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(image.image.url)

            return image.image.url

        return None
    
class BrokerSerializer(serializers.ModelSerializer):

    photo = serializers.SerializerMethodField()

    class Meta:
        model = Broker
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "about",
            "experience",
            "photo"
        ]

    def get_photo(self, obj):

        request = self.context.get("request")

        if obj.photo:
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url

        return None
    
class PropertyImageSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:

        model = PropertyImage

        fields = [
            "id",
            "image"
        ]

    def get_image(self, obj):

        request = self.context.get("request")

        if request:

            return request.build_absolute_uri(
                obj.image.url
            )

        return obj.image.url
    
class PropertyVideoSerializer(serializers.ModelSerializer):

    video = serializers.SerializerMethodField()

    class Meta:

        model = PropertyVideo

        fields = [
            "id",
            "video"
        ]

    def get_video(self, obj):

        request = self.context.get("request")

        if request:

            return request.build_absolute_uri(
                obj.video.url
            )

        return obj.video.url
    
class PropertyDetailSerializer(serializers.ModelSerializer):

    broker = BrokerSerializer(read_only=True)

    images = PropertyImageSerializer(
        many=True,
        read_only=True
    )

    videos = PropertyVideoSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Property

        fields = "__all__"





class ConsultationSerializer(serializers.ModelSerializer):

    class Meta:

        model = ConsultationLead

        fields = [
            "customer_name",
            "email",
            "phone",
            "broker",
            "budget",
            "requirements",
            "user",
        ]

        extra_kwargs = {
            "user": {
                "required": False
            }
        }

    def create(self, validated_data):

        return ConsultationLead.objects.create(
            **validated_data
        )
class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Appointment

        fields = [
            "property",
            "customer_name",
            "email",
            "phone",
            "appointment_date",
            "appointment_time",
            "message"
        ]
    
