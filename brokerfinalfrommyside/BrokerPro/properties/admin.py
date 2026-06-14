from django.contrib import admin
from .models import Property, PropertyImage, Broker,Appointment


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'city',
        'price',
        'status',
        'featured'
    )

    list_filter = (
        'city',
        'status',
        'property_type'
    )

    search_fields = (
        'title',
        'city',
        'location'
    )


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):

    list_display = (
        'property',
    )


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'phone',
        'experience'
    )

admin.site.register(Appointment)