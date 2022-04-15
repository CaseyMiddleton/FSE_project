from django.db import models
from scrappy_webpage.choices import *

# Create your models here.
class Searches(models.Model):
    first_query = models.CharField(max_length=245)
    connector = models.CharField(choices = CONNECTOR_CHOICES, max_length = 5, default='and')
    second_query = models.CharField(max_length=245)