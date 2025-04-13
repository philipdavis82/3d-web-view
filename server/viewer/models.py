from django.db import models

# Create your models here.
class DIRECTORY(models.Model):
    path = models.CharField(max_length=256)
    name = models.CharField(max_length=64)
    dir  = models.ForeignKey(
        "self", 
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )

class STL(models.Model):
    path = models.CharField(max_length=256)
    name = models.CharField(max_length=64)
    dir  = models.ForeignKey(DIRECTORY, on_delete=models.CASCADE)
    icon = models.CharField(max_length=16)
    prev = models.CharField(max_length=256) # Preview

