from django.db import models

# Create your models here.
class data(models.Model):
    file_name=models.TextField(default=None, null=True)
    objects_detected=models.TextField(default=None, null=True)
    time_stamp=models.DateField(default=None, null=True)