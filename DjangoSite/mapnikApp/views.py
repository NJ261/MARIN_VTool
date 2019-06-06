from django.shortcuts import render
from django.http import HttpResponse
import mapnik

def index(request):
    m = mapnik.Map(1240, 720)
    m.background = mapnik.Color('steelblue')

    s = mapnik.Style()
    r = mapnik.Rule()

    polygon_symbolizer = mapnik.PolygonSymbolizer()
    polygon_symbolizer.fill = mapnik.Color('#f2eff9')
    r.symbols.append(polygon_symbolizer)
    s.rules.append(r)

    highlight = mapnik.PointSymbolizer()
    highlight.file='mapnikApp/static/images/point.png'
    highlight.allow_overlap="yes"

    countryList = ['India', 'United Kingdom', 'United States', 'Canada']

    for i in range(0, len(countryList)):
        countryName = mapnik.Rule()
        countryName.filter = mapnik.Expression("[name]='{}'".format(countryList[i]))
        countryName.symbols.append(highlight)
        s.rules.append(countryName)

    m.append_style('Borders', s)

    query = "(SELECT * FROM worldborders) AS data"
    ds = mapnik.PostGIS(dbname="temp", user="nirav", table=query)

    layer = mapnik.Layer("world")
    layer.datasource = ds
    layer.styles.append("Borders")
    m.layers.append(layer)

    m.zoom_all()
    mapnik.render_to_file(m, "mapnikApp/static/images/temp.png", "png")
    return render(request, "mapnikIndex.html")
