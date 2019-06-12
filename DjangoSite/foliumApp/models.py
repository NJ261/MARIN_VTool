from django.contrib.gis.db import models

class WorldBorder(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.MultiPolygonField()

    class Meta:
        db_table = 'worldborders'

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

class Communities(models.Model):
    wkb_geometry = models.MultiPolygonField()
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(default='NA')

    # ToDo: add relevent info here.
    '''
    timestamp = models.DateTimeField()
    begin = models.DateTimeField()
    end = models.DateTimeField()
    altitudemode = models.TextField(default='')
    tessellate = models.IntegerField()
    extrude = models.IntegerField()
    visibility = models.IntegerField()
    draworder = models.IntegerField()
    icon = models.TextField()
    snippet = models.TextField()'''

    class Meta:
        db_table = 'communities'

    def __str__(self):
        return self.name
