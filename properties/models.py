from django.db import models
from uuid import uuid4

# Create your models here.
class Property(models.Model):
    """
    This model will serve as the property listing
    """
    PROPERTY_TYPE_CHOICES = [('rental', 'Rental'), ('purchase', 'Purchase')]
    STATUS_CHOICES = [('available', 'Available'), ('unavailable', 'Unavailable'),('sold', 'Sold'), ('rented', 'Rented')]

    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    # title = models.CharField(max_length=255, db_index=True)
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
    
    def __str__(self):
        return f"{self.id} {self.title} {self.price} {self.status}"

    class Meta:
        ordering = ['-updated_on']
