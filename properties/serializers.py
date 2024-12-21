from rest_framework import serializers
from .models import Property, Favorite

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    property_id =serializers.CharField(write_only=True)
    property = PropertySerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = ['id', 'property', 'property_id']
        

class EnquirySerializer(serializers.Serializer):
    message = serializers.CharField(min_length=10, style={'base_template': 'textarea.html'})
    