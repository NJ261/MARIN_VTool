from django.shortcuts import render_to_response, render
import folium

from foliumApp.Views.DataProjection import DataProjection
from foliumApp.Views.DataProcessing import DataProcessing

# index: select vessel
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

# result: vessel data
def results(request, vesselID):
    timeData = DataProcessing().getTimeDuration(vesselID)
    tempData = list(range(0,101, int(100/len(timeData))))
    context = {'vesselID': vesselID, 'timeDurationList': timeData, 'tempData': tempData[1:], 'stepsValue': int(100/len(timeData)), 'value':tempData[1]}
    try:
        context['value'] = tempData[int(timeData.index(request.POST['hiddenValue'])+1)]
    except:
        pass
    finally:
        locationIndex = tempData.index(context['value'])
        locationData = DataProcessing().getLocationData(vesselID, locationIndex)
        remoteIndexColor = DataProcessing().getRemoteIndexColor(vesselID, locationIndex)
        map = folium.Map(location=locationData[-1], zoom_start=8, prefer_canvas=True)
        DataProjection(color='black', weight=4).drawPolyLine(map, locationData, vesselID)
        folium.Marker(locationData[-1], tooltip='You are here: {}, {}'.format(locationData[-1][0], locationData[-1][1]), icon=folium.Icon(color=remoteIndexColor)).add_to(map)
        map.save('foliumApp/static/mapResults.html')
    return render(request, 'result.html', context)