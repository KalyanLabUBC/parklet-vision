import requests, json, os
import numpy as np

# +
from dotenv import load_dotenv
from constants import PITCH, SIZE

load_dotenv()
API_KEY=os.getenv('GOOGLE_API_KEY')

def streetview_query_url(lat: float, lon: float, direction: int) -> str:
    """
    Queries Google StreetView with the given parameters,
    i.e. a direct interface for the API
    """
    params = dict()
    
    params['location'] = '&location=%.7f,%.7f' % (lat,lon)
    params['size'    ] = '&size=%dx%d' % (SIZE,SIZE)
    params['heading' ] = '&heading=%d' % direction
    params['pitch'   ] = '&pitch=%d' % PITCH
    params['key'     ] = '&key=%s' % API_KEY
    
    url = 'https://maps.googleapis.com/maps/api/streetview?' +\
        params['location'] + params['size'] + params['heading'] +\
        params['pitch'] + params['key']
    
    return url


# +
from io import BytesIO
from PIL import Image
from shapely import Point

def get_streetview_image(lat: float, lon: float, direction: int = 0) -> Image:
    """
    Simplified wrapper around the query method.
    """
    url = streetview_query_url(lat, lon, direction)
    r = requests.get(url)
    r.raise_for_status()
    
    return Image.open(BytesIO(r.content))

def query_streetview_point(p: Point, direction: int = 0) -> Image:
    return get_streetview_image(lat=p.y, lon=p.x, direction = direction)
    
def has_imagery(lat: float, lon: float) -> bool:
    """
    Checks if imagery exists at a coordinate.
    """
    meta_url = (
        "https://maps.googleapis.com/maps/api/streetview/metadata"
        f"?location={lat},{lon}&key={API_KEY}"
    )
    meta = requests.get(meta_url).json()
    return meta.get("status") == "OK"


# -

from shapely import Point
point_to_array=lambda p: np.array([p.y, p.x])


def make_intersection_checker(roads_projected_gdf, buffer_range=10):
    """
    Generates a function to check if a point is on an intersection 
    by checking the number of connecting roads to this point (3 or 
    more is an intersection, 2 is a road, and 1 is a road's end).
    
    Assumes that the GeoDataFrame is already in UTM CRS.
    
    Within buffer_range meters (default 20 meters)
    """
    sindex = roads_projected_gdf.sindex
    
    def is_intersection(point):
        buffer = point.buffer(buffer_range)
        
        possible_idx = list(sindex.intersection(buffer.bounds))
        nearby = roads_projected_gdf.iloc[possible_idx]
        nearby = nearby[nearby.intersects(buffer)]
        
        return len(nearby) >= 3 and nearby.geometry.length.sum() > 20
    
    return is_intersection


# The following code also computes the tangent angles in StreetView format. It does this with the following process: First, it obtains the points for nearby the original point ($p_1,p_2$) on the road (1). Then, it computes one of the two perpendicular directions based on the following formula:
# $$\theta = \text{arctan2}\left(\frac{p_{2x} - p_{1x}}{p_{2y} - p_{1y}}\right)$$
# where $y$ is latitude and $x$ is longitude. This is inverted because StreetView headings are inverted, increasing clockwise rather than counterclockwise. Then, we compute the other three principal directions (the other perpendicular direction and the two parallel directions) by adding by 90 then modding 360.

def compute_tangent_angles(road, point, delta):
    """
    Compute tangent-based Street View headings at a point along a road.
    
    Assumes that the road is in UTM crs
    
    Returns:
        directions: array of 4 headings (forward, right, back, left)
        ref_points: (ref_point_1, ref_point_2)
    """
    distance = road.project(point)
    if point.distance(road) > 1e-6:
        raise ValueError(f"Point {point} is not on the road")
    
    ref_point_1 = road.interpolate(max(0, distance - delta))
    ref_point_2 = road.interpolate(min(road.length, distance + delta))
    
    dx = ref_point_2.x - ref_point_1.x
    dy = ref_point_2.y - ref_point_1.y
    
    # 0 = north, clockwise (Google Street View convention)
    theta = int((np.degrees(np.arctan2(dx, dy)) + 360)) % 360
    
    directions = np.array([
        theta,
        theta + 90,
        theta + 180,
        theta + 270
    ]) % 360
    
    return directions, (ref_point_1, ref_point_2)
