from django.db import models

# Create your models here.

#observatories
"""
- name
- general location
- lat
- long

"""

class Observatory(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500, null=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    longitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)

    def __str__(self):
        return f"{self.name}"


#telescopes (could be many telescopes at the same observatory)
# could have same telescope at 2 different locations (new entry for each?)
"""
- name
- apature
- scale
"""

class Telescope(models.Model):
    name = models.CharField(max_length=500)
    aperature = models.CharField(max_length=500, null=True)
    scale = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    obs = models.ForeignKey(Observatory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, at {self.obs}"

class Emulsion(models.Model):
    emulsion = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.emulsion}"

class Filter(models.Model):
    filt = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.filt}"

class Band(models.Model):
    band = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.band}"

#plates
"""
- telescope (which connects to which observatory)
- plate id
- RA
- Dec
- JD (if specific date is available, JD2000.0)
- looser date (if nothing better)
- Exposure time (seconds)
- multi exposuers on the plate
- emulsion
- filter
- band

import allows for
- JD, HJD, Geocentric Date, Heliocentric Date
- RA/Dec degrees/hh:mm:sec
and will auto convert to a standard format, probably decimals all around


"""

class Plate(models.Model):
    series = models.CharField(max_length=3)
    number = models.IntegerField()
    # ra and dec, in decimal format
    ra = models.DecimalField(max_digits=8, decimal_places=5, null=True)
    dec = models.DecimalField(max_digits=8, decimal_places=5, null=True)
    # julian date
    jd = models.DecimalField(max_digits=13, decimal_places=5, null=True)
    # general date
    date = models.DateTimeField(null=True)
    # exposure time, seconds
    exptime = models.IntegerField(null=True)
    emulsion = models.ForeignKey(Emulsion, on_delete=models.CASCADE, null=True)
    filt = models.ForeignKey(Filter, on_delete=models.CASCADE, null=True)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.series}{self.number}"
