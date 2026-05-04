#!/usr/bin/env python

import argparse
import sys
from pathlib import Path

import imgviz
import numpy as np
import labelme


def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("input_dir", help="Input annotated directory")
    parser.add_argument("output_dir", help="Output dataset directory")
    parser.add_argument("--labels", required=True,
                        help="Labels file or comma separated text")
    parser.add_argument("--noviz", action="store_true",
                        help="Disable visualization")

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not output_dir.exists():
        print("No data file exists")
        sys.exit(1)

    # Create folders
    masks_dir = output_dir / "masks"
    viz_dir = output_dir / "visualizations"

    masks_dir.mkdir(parents=True, exist_ok=True)
    if not args.noviz:
        viz_dir.mkdir(parents=True, exist_ok=True)

    print("Creating dataset:", output_dir)

    # Load labels
    if Path(args.labels).exists():
        with open(args.labels) as f:
            class_names = [line.strip() for line in f if line.strip()]
    else:
        class_names = [x.strip() for x in args.labels.split(",")]

    # Add background class
    class_names = ["_background_"] + class_names
    class_name_to_id = {name: i for i, name in enumerate(class_names)}

    # Process each JSON
    for json_path in sorted(input_dir.glob("*.json")):
        label_file = labelme.LabelFile(filename=str(json_path))

        base = json_path.stem

        out_mask_file = masks_dir / f"{base}.png"
        out_viz_file = viz_dir / f"{base}.jpg"

        # Load image
        img = labelme.utils.img_data_to_arr(label_file.imageData)

        # Convert shapes to label mask
        cls, _ = labelme.utils.shapes_to_label(
            img.shape,
            label_file.shapes,
            label_name_to_value=class_name_to_id,
        )

        # Save mask
        imgviz.io.lblsave(out_mask_file, cls.astype(np.uint8))

        # Save visualization
        if not args.noviz:
            viz = imgviz.label2rgb(
                cls,
                img,
                label_names=class_names,
                loc="rb",
            )
            imgviz.io.imsave(out_viz_file, viz)

    print("Completed generating masks.")


if __name__ == "__main__":
    main()
