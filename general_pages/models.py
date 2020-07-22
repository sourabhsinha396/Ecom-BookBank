from django.db import models


class contactus(models.Model):
    name        = models.CharField(max_length=100)
    email       = models.EmailField(max_length=100)
    subject     = models.CharField(max_length=150)
    message     = models.TextField(max_length=400)
