
from django.db import models
 
class Data(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField()
    time = models.TimeField()
    check = models.IntegerField()
    amount = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    etype = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.day} Transaction'

