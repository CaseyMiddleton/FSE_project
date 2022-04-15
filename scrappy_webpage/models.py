from django.db import models

# Create your models here.
class Searches(models.Model):
    first_query = models.CharField(max_length=245)