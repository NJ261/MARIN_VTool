from django.shortcuts import render_to_response, render
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
    folium.LayerControl().add_to(map)

    context = {'my_map': map, 'defaultValue': 10, 'vesselList': [10,20,30]}
    map.save('foliumApp/static/mapIndex.html')
    return render(request, 'index.html', context)