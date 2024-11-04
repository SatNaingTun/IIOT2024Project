import uuid
from django.db import models

class InputAddress(models.Model):
    # id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    variable_name=models.CharField(max_length=24)
    address=models.CharField(max_length=24)
    # updated_time=models.DateTimeField(auto_now=True)

