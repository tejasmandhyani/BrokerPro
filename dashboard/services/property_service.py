from properties.models import Property, PropertyImage, PropertyVideo


class DashboardPropertyService:

    @staticmethod
    def get_all():

        return (
            Property.objects
            .select_related("broker")
            .prefetch_related(
                "images",
                "videos"
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_by_id(property_id):

        return (
            Property.objects
            .select_related("broker")
            .prefetch_related(
                "images",
                "videos"
            )
            .get(id=property_id)
        )
    @staticmethod
    def create(
        *,
        form,
        images,
        videos,
        broker=None,
    ):

        property = form.save(commit=False)

        property.broker = broker

        property.save()

        for image in images:

            PropertyImage.objects.create(
                property=property,
                image=image
            )

        for video in videos:

            PropertyVideo.objects.create(
                property=property,
                video=video
            )

        return property
    
    @staticmethod
    def update(
    *,
    property,
    form,
    ):

        property.title = form.cleaned_data["title"]
        property.city = form.cleaned_data["city"]
        property.location = form.cleaned_data["location"]
        property.property_type = form.cleaned_data["property_type"]
        property.status = form.cleaned_data["status"]
        property.price = form.cleaned_data["price"]
        property.bedrooms = form.cleaned_data["bedrooms"]
        property.bathrooms = form.cleaned_data["bathrooms"]
        property.area_sqft = form.cleaned_data["area_sqft"]
        property.description = form.cleaned_data["description"]
        property.featured = form.cleaned_data["featured"]

        property.save()

        return property
    
    @staticmethod
    def delete(property):

        property.delete()

    
    @staticmethod
    def publish(property):

        property.publish_status = "Published"

        property.save()

    @staticmethod
    def unpublish(property):

        property.publish_status = "Draft"

        property.save()

    @staticmethod
    def get_versions(property):

        return property.versions.all().order_by("-created_at")
    
    @staticmethod
    def rollback(property, version):

        property.title = version.title
        property.city = version.city
        property.location = version.location
        property.property_type = version.property_type
        property.status = version.status
        property.price = version.price
        property.bedrooms = version.bedrooms
        property.bathrooms = version.bathrooms
        property.area_sqft = version.area_sqft
        property.description = version.description
        property.featured = version.featured
        property.publish_status = version.publish_status

        property.save()

        return property
    
    @staticmethod
    def get_featured():

        return (
            Property.objects
            .filter(featured=True)
            .select_related("broker")
            .prefetch_related(
            "images",
            "videos"
            )
        .order_by("-created_at")
        )


    @staticmethod
    def get_latest(limit=6):

        return (
            Property.objects
            .select_related("broker")
            .prefetch_related(
            "images",
            "videos"
            )
            .order_by("-created_at")[:limit]
        )
