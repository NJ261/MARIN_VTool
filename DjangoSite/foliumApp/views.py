from django.shortcuts import render
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
    timeData = DataProcessing().getTimeDuration(vesselID) # fetching date and time values for sourcemmsi
    tempData = [index for index, value in enumerate(timeData)] # index range for sliders
    context = {'vesselID': vesselID, 'timeDurationList': timeData, 'tempData': tempData, 'stepsValue': 1, 'value':tempData[0]} # data for template
    try:
        context['value'] = tempData[int(timeData.index(request.POST['hiddenValue']))] # fetching user's input i.e. dateTime index here
    except:
        pass
    finally:
        locationIndex = tempData.index(context['value'])

        # getting community, traffic data for a single time period
        communityData, trafficData = DataProcessing().getTrafficData(vesselID, timeData[locationIndex])

        # getting previous locations (lat, lng) for a sourcemmsi till current time period
        locationData = DataProcessing().getLocationData(vesselID, timeData[:locationIndex+1])

        # getting remoteIndexColor (i.e. green, lightred, red), min distance, targetmmsi for the min distance
        remoteIndexColor, targetmmsi, distance = DataProcessing().getRemoteIndexColor(vesselID, timeData[locationIndex])
        map = folium.Map(location=locationData[-1], zoom_start=4, prefer_canvas=True)
        map = DataProjection().drawCommunitiesMarker(map, communityData) # plotting communities data
        map = DataProjection().drawCommunitiesMarker(map, trafficData, color='orange', layername='Vessels') # plotting other vessels
        DataProjection(color='black', weight=4).drawPolyLine(map, locationData, vesselID) #drawing vessel's path

        # drawing source mmsi's current location marker
        folium.Marker(locationData[-1], tooltip="<b>You are here:</b> {:.4f}, {:.4f} <br><b>TargetMMSI</b>: {} <br><b>Distance</b>: {} km".
                      format(locationData[-1][0], locationData[-1][1], targetmmsi, distance),
                      icon=folium.Icon(color=remoteIndexColor)).add_to(map)
        folium.LayerControl().add_to(map)
        map.save('foliumApp/static/mapResults.html')
    return render(request, 'result.html', context)