# image parameters
PITCH=0
SIZE=640

import numpy as np
# coordinates for oakland
OAKLAND_COORDS = np.array([37.8786, -122.2241])

# bounding markers for where to randomly sample points from
BOTTOM_LEFT = np.array([37.810752, -122.291342]) # 14th St and Mandela Parkway 
TOP_RIGHT   = np.array([37.814505, -122.278666]) # West Grand Ave and Market St

BOUNDARY_CENTER=(BOTTOM_LEFT + TOP_RIGHT) / 2

# files
ROAD_GEOMETRY_FILENAME='OaklandStreetOSM.geojson'
DATASET_OUTPUT_DIR='data'
IMAGE_FILE_OUTPUT=f'{DATASET_OUTPUT_DIR}/images'
METADATA_FILE_OUTPUT=f'{DATASET_OUTPUT_DIR}/metadata.csv'
METADATA_HEADER = [ 'LABEL', 'LAT', 'LON', 'DIR' ]
