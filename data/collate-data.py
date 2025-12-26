import pandas as pd
import json
import os
import sys
from pathlib import Path

df = pd.read_csv('metadata.csv')
label_files = list(filter(lambda filename : filename.endswith('.json'),
                     os.listdir('images')))
json_data = list(map(lambda filename : Path('./images/' + filename)
                     .read_text(), label_files))
objects = list(map(lambda raw : json.loads(raw), json_data))

for label in objects:
    image_name = Path(label['imagePath']).name
    
    mask = df['LABEL'].apply(lambda p: Path(p).name == image_name)
    row = df[mask]
    lon, lat, direction = float(row['LON']), \
        float(row['LAT']), int(row['DIR']) 

    label['lon'] = lon
    label['lat'] = lat
    label['dir'] = direction

# write to the master json file
with open("dataset.json", "w", encoding="utf-8") as f:
    json.dump(objects, f, indent=2)
