from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np

id2label = {
    0: '_background_',
    1: 'sidewalk',
    2: 'parking',
    3: 'roadway',
    4: 'restricted_zone',
    5: 'driveway'
}

label2id = { v: k for k, v in id2label.items() }

palette = [
  [0,   0,   0  ], # _background_
  [216, 82,  24 ], # sidewalk
  [255, 255, 0  ], # parking
  [125, 46,  141], # roadway
  [118, 171, 47 ], # restricted_zone
  [161, 19,  46 ], # driveway
]

legend_patches = [
    patches.Patch(color=np.array(color)/255, label=label) \
    for label, color \
    in zip(id2label.values(), palette)
]

def show_legend():
    fig, ax = plt.subplots(figsize=(18, 2))

    ax.legend(
        handles=legend_patches, 
        loc='center', 
        bbox_to_anchor=(0.5, 0.5), 
        ncol=5, 
        fontsize=20
    )

    ax.axis('off')
    plt.show()