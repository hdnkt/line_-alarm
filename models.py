from django.db import models

class Members(models.Model):
    ID = models.CharField(max_length=50,primary_key=True)
    Active = models.BooleanField()
    when = models.DateTimeField(max_length=20)
