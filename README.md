# parklet-vision

This is a collection of three notebooks used to perform the on-street parking mapping project with image segmentation. The first notebook, `1_data_collection.ipynb`, describes the data collection process used to form the training dataset supplied to the machine learning model. After collecting data, this is then labelled with LabelMe, and provided that the setup below has been completed, labelling is simplified by starting LabelMe locally using the script `open-labelme.sh` and then converting the produced LabelMe JSON files to trainable masks with `generate_masks.sh` (and this shell file essentially wraps around `labelme2masks.py`). Then, these masks are fed into `2_fine_tuning.ipynb` to train the model, ideally on a cloud computing service like Google Colaboratory, with the help of Weights and Biases to produce performance metrics graphs during the training process. Lastly, the produced model is then extracted from the training site and loaded into `3_crawler_classifier.ipynb` to be applied to the testing region to produce the final map (including performing a homographic transform across the image and GPS planes and post-processing the map to mitigate errors).

## Setup

The following setup assumes that you are using a linux environment. For those on Windows, it is highly recommended that you install the Windows Subsystem for Linux. Mac users may be able to just run these commands directly, provided that you install `git`, `python`, and `pip` first.

For local setup, first clone the repository:

```shell
git clone https://github.com/mufaro3/parklet-vision.git
```

AUTOMATIC SETUP: Use setup.sh to setup the virtual environment and
install all of the necessary packages in requirements.

```shell
sudo ./setup.sh
```

MANUAL SETUP: if setup.sh doesn't work, then manual setup for the
virtual environment is simple. You'll need Python and Pip (version 3).
First, create the virtual environment under 'venv/' with python3

```shell
python3 -m venv 'venv'
```

then activate the virtual environment with

```shell
source venv/bin/activate
```

upgrade pip before continuing

```shell
pip3 install --upgrade pip
```

install the necessary packages from requirements.txt with

```shell
pip3 install -r requirements.txt
```

then install the Jupyter Kernel to your machine with

```shell
python3 -m ipykernel install --user --name=parklet-vision --display-name='Python3 (ParkletVision)'
```

and each time you wish to edit the code, remember re-activate the virtual environment.