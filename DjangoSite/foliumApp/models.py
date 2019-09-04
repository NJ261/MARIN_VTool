from django.contrib.gis.db import models

class Results(models.Model):

    ogc_fid = models.IntegerField(primary_key=True)
    sourcemmsi = models.CharField(max_length=50)
    targetmmsi = models.CharField(max_length=50)
    sourcedate = models.CharField(max_length=50)
    sourcetime = models.CharField(max_length=50)
    targetdate = models.CharField(max_length=50)
    targettime = models.CharField(max_length=50)
    sourcelat = models.FloatField()
    sourcelng = models.FloatField()
    targetlat = models.FloatField()
    targetlng = models.FloatField()
    sourcemstrid = models.CharField(max_length=50)
    targetmstrid = models.CharField(max_length=50)
    distance = models.FloatField()
    minimum = models.CharField(max_length=50)
    predictedpath = models.CharField(max_length=50)

    class Meta:
        db_table = 'processed_nwp_data'

    # Returns the string representation of the model.
    def __str__(self):
        return self.sourcemmsi

class UniqueMMSI(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    sourcemmsi = models.CharField(max_length=50)

    class Meta:
        db_table = 'unique_mmsi'

    def __str__(self):
        return self.sourcemmsi

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
