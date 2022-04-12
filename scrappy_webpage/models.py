from django.db import models

# Create your models here.
class Searches(models.Model):
    your_name = models.CharField(max_length=30)