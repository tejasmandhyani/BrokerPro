from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):

    PROPERTY_TYPES = [
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Plot', 'Plot'),
        ('Commercial', 'Commercial'),
    ]
    PUBLISH_STATUS = [
    ('Draft', 'Draft'),
    ('Published', 'Published'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold', 'Sold'),
        ('Booked', 'Booked'),
        ('Negotiation', 'Negotiation'),
    ]

    title = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    broker = models.ForeignKey(
    'Broker',
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available'
    )
    publish_status = models.CharField(
    max_length=20,
    choices=PUBLISH_STATUS,
    default='Draft'
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area_sqft = models.IntegerField()

    description = models.TextField()

    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='properties/'
    )

    def __str__(self):
        return self.property.title
    


class Broker(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    photo = models.ImageField(
        upload_to='brokers/'
    )
    

    experience = models.IntegerField()

    about = models.TextField()

    def __str__(self):
        return self.name
    


class PropertyVideo(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='videos'
    )

    video = models.URLField(
    max_length=500
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.property.title
    
class Appointment(models.Model):

    STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
    ('Expired', 'Expired'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )
    broker = models.ForeignKey(
    Broker,
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    customer_name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.customer_name} - {self.property.title}"
    

class PropertyVersion(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='versions'
    )

    title = models.CharField(max_length=200)

    city = models.CharField(max_length=100)

    location = models.CharField(max_length=200)

    property_type = models.CharField(
        max_length=20
    )

    status = models.CharField(
        max_length=20
    )

    publish_status = models.CharField(
        max_length=20
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    bedrooms = models.IntegerField()

    bathrooms = models.IntegerField()

    area_sqft = models.IntegerField()

    description = models.TextField()

    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.property.title} Version"
    
class ConsultationLead(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    broker = models.ForeignKey(
        Broker,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    customer_name = models.CharField(
    max_length=100,
    default=""
    )

    email = models.EmailField(
    default=""
    )

    phone = models.CharField(
    max_length=15,
    default=""
    )

    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    requirements = models.TextField()

    status = models.CharField(
        max_length=20,
        default="New Lead"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.customer_name} → {self.broker.name}"
class CustomerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    city = models.CharField(
        max_length=100
    )

    def __str__(self):

        return self.full_name