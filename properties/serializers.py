from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        
class EnquirySerializer(serializers.Serializer):
    message = serializers.CharField(min_length=10, style={'base_template': 'textarea.html'})
    