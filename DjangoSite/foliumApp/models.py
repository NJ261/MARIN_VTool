from django.contrib.gis.db import models

class Results(models.Model):

    ogc_fid = models.IntegerField(primary_key=True)
    vesselid = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)
    remoteindex = models.CharField(max_length=50)

    class Meta:
        db_table = 'sampleresults'

    # Returns the string representation of the model.
    def __str__(self):
        return self.vesselid

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
