from django.shortcuts import render_to_response, render
import folium

from foliumApp.Views.DataProjection import DataProjection
from foliumApp.Views.DataProcessing import DataProcessing

# index: select vessel
def index(request):
    lat, lon = DataProcessing().getLocation()
    map = folium.Map(location=[lat, lon], zoom_start=6, prefer_canvas=True)
    folium.Marker([lat, lon], tooltip='Your IP based location: {}, {}'.format(lat, lon), icon=folium.Icon(color='cadetblue')).add_to(map)

    # plotting communities data
    communitiesData = DataProcessing().getCommunitiesData()
    map = DataProjection().drawCommunitiesMarker(map, communitiesData)
    folium.LayerControl().add_to(map)

    vesselNamesList = DataProcessing().getVesselNamesList()
    context = {'my_map': map, 'vesselList': vesselNamesList}
    map.save('foliumApp/static/mapIndex.html')
    return render(request, 'index.html', context)

# result: vessel data
def results(request, vesselID):
    timeData = DataProcessing().getTimeDuration(vesselID)
    tempData = [index for index, value in enumerate(timeData)]
    context = {'vesselID': vesselID, 'timeDurationList': timeData, 'tempData': tempData, 'stepsValue': 1, 'value':tempData[0]}
    try:
        context['value'] = tempData[int(timeData.index(request.POST['hiddenValue']))]
    except:
        pass
    finally:
        locationIndex = tempData.index(context['value'])
        communityData, trafficData = DataProcessing().getTrafficData(vesselID, timeData[locationIndex])
        locationData = DataProcessing().getLocationData(vesselID, timeData[:locationIndex+1])
        remoteIndexColor, targetmmsi, distance = DataProcessing().getRemoteIndexColor(vesselID, timeData[locationIndex])

        map = folium.Map(location=locationData[-1], zoom_start=4, prefer_canvas=True)
        DataProjection(color='black', weight=4).drawPolyLine(map, locationData, vesselID)

        map = DataProjection().drawCommunitiesMarker(map, communityData)
        map = DataProjection().drawCommunitiesMarker(map, trafficData, color='orange', layername='Vessels')

        folium.Marker(locationData[-1], tooltip="<b>You are here:</b> {:.4f}, {:.4f} <br><b>TargetMMSI</b>: {} <br><b>Distance</b>: {} km".
                      format(locationData[-1][0], locationData[-1][1], targetmmsi, distance),
                      icon=folium.Icon(color=remoteIndexColor)).add_to(map)

        folium.LayerControl().add_to(map)

        map.save('foliumApp/static/mapResults.html')
    return render(request, 'result.html', context)