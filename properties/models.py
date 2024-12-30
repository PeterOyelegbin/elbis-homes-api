from django.db import models
from uuid import uuid4
from users.models import UserModel

# Create your models here.
class Property(models.Model):
    """
    This model will serve as the property listing
    """
    PROPERTY_TYPE_CHOICES = [('Rental', 'Rental'), ('Purchase', 'Purchase')]
    STATUS_CHOICES = [('Available', 'Available'), ('Unavailable', 'Unavailable')]

    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    bedroom = models.PositiveSmallIntegerField(default=1)
    bathroom = models.PositiveSmallIntegerField(default=1)
    electricity = models.PositiveSmallIntegerField(default=100)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    price = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    cover_image = models.ImageField(upload_to='elbis/cover_images/')
    bedroom_image = models.ImageField(upload_to='elbis/bedroom_images/')
    bathroom_image = models.ImageField(upload_to='elbis/bathroom_images/')
    video_url = models.URLField()
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        return f"{self.id} {self.title} {self.price} {self.status}"
    

class Favorite(models.Model):
    """
    This model will serve as the property favorite listing
    """
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.user} - {self.property}"
    