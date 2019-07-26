from django.contrib.gis.db import models

class WorldBorder(models.Model):
    # TODO: DB description needed here.

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
    # TODO: DB description needed here.

    geom = models.MultiPolygonField()
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(default='NA')

    # ToDo: add relevent fields from DB here.
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


class MarineTrafficData(models.Model):
    # TODO: DB description needed here.

    name = models.CharField(max_length=50, primary_key=True)
    geom = models.MultiPolygonField()

    class Meta:
        db_table = 'marine_traffic_2010_data'

    def __str__(self):
        return self.name


class AllPorts(models.Model):
    # TODO: DB description needed here.

    country = models.CharField(max_length=100, primary_key=True)
    port = models.CharField(max_length=100)
    latitude  = models.FloatField()
    longitude = models.FloatField()
    population = models.FloatField()
    notes = models.CharField(max_length=200)
    source = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    date_creat = models.DateTimeField()
    owner = models.CharField(max_length=100)
    geom = models.MultiPolygonField()

    class Meta:
        db_table = 'all_ports'

    def __str__(self):
        return self.name

class Grids(models.Model):
    # TODO: DB description needed here.

    id = models.IntegerField(primary_key=True)
    mstrid = models.FloatField()
    f_p = models.FloatField()
    f1_p = models.FloatField()
    f2_p = models.FloatField()
    f3_p = models.FloatField()
    f4_p = models.FloatField()
    grid0_1 = models.FloatField()
    geom = models.MultiPolygonField()

    class Meta:
        db_table = 'amtgrids'

    def __str__(self):
        return self.id
