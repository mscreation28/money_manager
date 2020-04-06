
from django.db import models
 
class Date(models.Model):
    day = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
 
    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'
