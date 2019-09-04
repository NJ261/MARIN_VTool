from django.contrib.gis.db import models

# processed_nwp_data table, for result page
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

# unique_mmsi for main page
class UniqueMMSI(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    sourcemmsi = models.CharField(max_length=50)

    class Meta:
        db_table = 'unique_mmsi'

    def __str__(self):
        return self.sourcemmsi

# communities table for main page
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
