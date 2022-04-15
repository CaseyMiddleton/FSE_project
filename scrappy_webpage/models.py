from django.db import models
from scrappy_webpage.choices import *

# Create your models here.
class Searches(models.Model):
    first_query = models.CharField(max_length=200)
    connector = models.CharField(choices = CONNECTOR_CHOICES, max_length = 100, default='and')
    second_query = models.CharField(max_length=200)