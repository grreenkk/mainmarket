from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now=True)