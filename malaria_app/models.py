from django.db import models

# Create your models here.
from django.db import models

class MalariaImage(models.Model):
    paatient_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    noteMedical = models.TextField(max_length=500, blank=True, null=True)
    