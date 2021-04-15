# Sentinel-2 GEO AI

Demo project for cloud recognition from Sentinel-2 satellite imagery using machine learning.

All Copernicus Sentinel-2 data [2020] used in this demo project is acquired from [AWS S3](https://registry.opendata.aws/sentinel-2/) and provided by the European Commission and the European Space Agency - ESA.

Premade demo data is made available by Gispo Ltd. for testing purposes.
The data is available to download [here](https://drive.google.com/file/d/1yuElFSXVSwLy1DNx5lTFacy8pouq9A2S/view?usp=sharing).

The demo presentation slides are also available in [geoai-presentation.pdf](geoai-presentation.pdf).

## Demo

The main Jupyter notebook ([Classifiers.ipynb](Classifiers.ipynb)) contains code for 9 different classifiers.
Running the main demo notebook requires the .csv files from the demo dataset.

Extract the downloaded zip file (or generate the csv files with the processing scripts) and place the main notebook in the same directory as the .csv files before running.

## Data

Cloud masks, used as training data, are contained in the [data](data/) directory.
The masks were created manually for 6 Sentinel-2 images in the Abyei region in South Sudan in 60m resolution using the [mpl-pixel-picker](https://github.com/joonalai/mpl-pixel-picker) tool.

The .csv files in the zip archive can be reproduced without setting up [OpenDataCube](https://opendatacube.org) by using the processing scripts in [S2GeoAi/processing](S2GeoAi/processing).
More specifically, the [images_to_csv](S2GeoAi/processing/images_to_csv.py) script can be used to recreate the .csv files from the .jp2 cloud masks in [data](data/) and downloaded Sentinel-2 data.

S2 data can be downloaded to .SAFE format from the Sentinel-2 AWS S3 bucket using e.g. [sentinelhub-py](https://github.com/sentinel-hub/sentinelhub-py).
For examples on indexing Sentinel-2 data from AWS S3 to OpenDataCube, see [here](https://github.com/GispoCoding/CFSI/tree/master/cfsi/scripts/index).
