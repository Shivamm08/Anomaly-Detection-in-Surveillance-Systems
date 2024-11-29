from django.db import models

# Create your models here.
class ViolenceImage(models.Model):
    image = models.ImageField(upload_to='violence_images/')
    confidence = models.FloatField()