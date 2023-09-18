from django.db import models

class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length= 300, blank = False)
    slide_url = models.URLField(blank = False)
