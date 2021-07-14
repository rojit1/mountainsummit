from django.db import models

class Place:
    name = models.CharField(max_length=200)
    
