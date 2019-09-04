import folium

class DataProjection:
    '''
    Description:
    ------------
    Generate GeoJson layers, draw polylines within layer control so that one can modify it.

    Parameters:
    -----------
    self,
    **kwargs :
             color : boundry of polygon e.g 'red' or hex (#fff000) value (default: blue)
             fillColor : color inside polygon e.g 'red' or hex (#fff000) value (default: blue)
             weight : line weight (default = 2)
             opacity : opacity (default = 1)

    '''

    def __init__(self, **kwargs):
        self.color = kwargs.get('color','blue')
        self.fillColor = kwargs.get('fillColor','blue')
        self.weight = kwargs.get('weight', 2)
        self.opacity = kwargs.get('opacity', 1)

    # Redundant - for reference
    def addGeoJsonLayer(self, map, data, layerName):
        '''
        Description:
        ------------
        Generate a layer with input json data

        Parameters:
        -----------
        self,
        map : Folium map object as input
        data : Input json data to generate a layer
        layerName : layer name so that one can enable/disable it in real-time

        Returns:
        --------
        Folium map object with updated layer
        '''

        featureGroup = folium.FeatureGroup(name=layerName)
        folium.GeoJson(data, style_function=lambda feature: {
                                'fillColor': self.fillColor,
                                'color': self.color,
                                'weight': self.weight}).add_to(featureGroup)
        featureGroup.add_to(map)
        return map

    def drawPolyLine(self, map, data, lineName):
        '''
        Description:
        ------------
        Generate a PolyLine with input data as list

        Parameters:
        -----------
        self,
        map : Folium map object as input
        data : Input json data to generate a polyline
        layerName : line name so that one can enable/disable it in real-time

        Returns:
        --------
        Folium map object with updated line
        '''

        featureGroup = folium.FeatureGroup(name=lineName, show=True)
        folium.PolyLine(data, color=self.color, weight=self.weight, opacity=self.opacity).add_to(featureGroup)
        featureGroup.add_to(map)

        return map

    # draw marker for community and vessels traffic
    def drawCommunitiesMarker(self, map, data, **kwargs):
        # TODO: need to work here on icon: type, shape, size and color
        self.color = kwargs.get('color', 'blue')
        self.layerName = kwargs.get('layername', 'Community')
        featureGroup = folium.FeatureGroup(name=self.layerName)
        for i in range(0, len(data)):
            folium.Marker(location=data[i][1], tooltip='{} Name: {}'.format(self.layerName, data[i][0]), icon=folium.Icon(color=self.color)).add_to(featureGroup)
        featureGroup.add_to(map)
        return map

    # Redundant - for reference
    def drawGrids(self, map, data):
        featureGroup = folium.FeatureGroup(name='Grids')
        folium.Polygon(data, color=self.color).add_to(featureGroup)
        featureGroup.add_to(map)
        return map
