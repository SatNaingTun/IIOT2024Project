from django.db import models

class S7InputAddress(models.Model):
    topic=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
