import folium
import geopandas as gpd

from constants import BOUNDARY_CENTER

def plot_to_map(parking_gdf, restricted_gdf, m=None):

    if m is None:
        m = folium.Map(location=BOUNDARY_CENTER, zoom_start=17)

    # ---- styling helpers ----
    def parking_style(feature):
        return {"color": "green", "fillOpacity": 0.4, "weight": 2}

    def restricted_style(feature):
        return {"color": "red", "fillOpacity": 0.4, "weight": 2}

    # ---- parking layer ----
    folium.GeoJson(
        parking_gdf,
        name="Parking",
        style_function=parking_style,
        tooltip=folium.GeoJsonTooltip(fields=["class"]),
        popup=folium.GeoJsonPopup(fields=["class"])
    ).add_to(m)

    # ---- restricted layer ----
    folium.GeoJson(
        restricted_gdf,
        name="Restricted Zones",
        style_function=restricted_style,
        tooltip=folium.GeoJsonTooltip(fields=["class"]),
        popup=folium.GeoJsonPopup(fields=["class"])
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m


def plot_bbox(bbox_gdf, m):
    folium.GeoJson(
        bbox_gdf, style_function=lambda x: {
            'fill': False,
            'color': 'red',
            'weight': 2
        }
    ).add_to(m)
