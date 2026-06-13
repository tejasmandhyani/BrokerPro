from django import forms
from properties.models import Property

class PropertyForm(forms.ModelForm):

    class Meta:

        model = Property

        fields = [
            'title',
            'city',
            'location',
            'property_type',
            'status',
            'price',
            'bedrooms',
            'bathrooms',
            'area_sqft',
            'description',
            'featured'
        ]

        widgets = {

            'description': forms.Textarea(
                attrs={'rows':4}
            )

        }