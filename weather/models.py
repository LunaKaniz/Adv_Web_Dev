from django.db import models

class ClimateRecord(models.Model):
    station_id = models.CharField(max_length=50)
    date = models.DateField()
    tmax = models.FloatField(null=True, blank=True)
    tmin = models.FloatField(null=True, blank=True)
    precipitation = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('station_id', 'date')

    def __str__(self):
        return f"{self.station_id} - {self.date}"
