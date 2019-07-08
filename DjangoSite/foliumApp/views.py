from django.shortcuts import render_to_response
import folium

from foliumApp.Views.DataProjection import DataProjection
from foliumApp.Views.DataProcessing import DataProcessing

def index(request):
    lat, lon = DataProcessing().getLocation()
    map = folium.Map(location=[lat, lon], zoom_start=6, prefer_canvas=True)
    folium.Marker([lat, lon], tooltip='Your IP based location: {}, {}'.format(lat, lon), icon=folium.Icon(color='green')).add_to(map)

    # plotting communities data
    communitiesData = DataProcessing().getCommunitiesData()
    map = DataProjection().drawCommunitiesMarker(map, communitiesData)

    # plotting marine 2010 traffic data
    marineTrafficData = DataProcessing().getMarineTrafficData()
    map = DataProjection(weight=2, color='black').drawPolyLine(map, marineTrafficData, 'traffic')

    # plotting sample grids
    gridsData = DataProcessing().getGridsData()
    map = DataProjection().drawGrids(map, gridsData)

    folium.LayerControl().add_to(map)
    map.save('foliumApp/static/index.html')
    return render_to_response("index.html")
