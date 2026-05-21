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

# +
"""
palette = [
  [0,   0,   0  ], # _background_
  [216, 82,  24 ], # sidewalk
  [255, 255, 0  ], # parking -> driveway
  [125, 46,  141], # roadway
  [118, 171, 47 ], # restricted_zone -> parking
  [161, 19,  46 ], # driveway -> restricted_zone
]
"""

palette = [
  [0,   0,   0  ], # _background_
  [216, 82,  24 ], # sidewalk
  [118, 171, 47 ], # parking
  [125, 46,  141], # roadway
  [161, 19,  46 ], # restricted_zone
  [255, 255, 0  ], # driveway
]
# -

legend_patches = [
    patches.Patch(color=np.array(color)/255, label=label) \
    for label, color \
    in zip(id2label.values(), palette)
]

def show_legend():
    fig, ax = plt.subplots(figsize=(5, 1))
    ax.legend(handles=legend_patches, ncol=3, fontsize=10)
    ax.axis('off')
    plt.show()


# +
from numpy.typing import NDArray

def append_mask_to_segmentation_map(segmentation_map: NDArray, mask, label):
    mask = np.asarray(mask)
    
    label_index = list(id2label.values()).index(label)
    color = palette[label_index]
    for c in range(3):
        segmentation_map[:, :, c] = np.where(mask, color[c], segmentation_map[:, :, c])
        
def plot_segmentation_map_over_image(image: NDArray, segmentation_map: NDArray, legend: bool = True):
    if type(image) is not NDArray:
        image = np.array(image)
        
    if legend:
        show_legend()
    plt.figure(figsize=(6, 6))
    plt.imshow(image)
    plt.imshow(segmentation_map, alpha=0.3)
    plt.axis('off')
    plt.show()
