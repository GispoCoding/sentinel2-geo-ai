import json
from pathlib import Path
from typing import Tuple, Dict

import numpy as np
import rasterio

DATA_DIR = (Path(__file__).parent / '../../data').resolve()


def json_to_arr(fil: Path, width: int, height: int):
    with open(fil) as f:
        data = json.load(f)
    coordinates = data[1:]
    arr = np.ones((width, height)).astype(rasterio.uint8)
    for coord in coordinates:
        arr[coord[1] - 1][coord[0] - 1] = 2
    return arr


def read_raster(raster_file: Path) -> Tuple[np.ndarray, Dict]:
    with rasterio.Env():
        with rasterio.open(raster_file) as ds:
            return ds.read(1), ds.profile


def mask_no_data(raster_arr: np.ndarray, arr: np.ndarray) -> np.ndarray:
    raster_arr[raster_arr > 0] = 1
    return arr * raster_arr.astype(rasterio.uint8)


def write_output(arr: np.ndarray, profile: Dict, output_file: Path):
    with rasterio.Env():
        profile.update(
            dtype=rasterio.uint8,
            count=1)

        with rasterio.open(output_file, 'w', **profile) as dst:
            dst.write(arr, 1)


def main():
    files = {
        'T35PNM_20200925T082711_B01.jp2': 'PNM_A027474_20200925T082711.json',
        'T35PPM_20200902T081611_B01.jp2': 'PPM_A027145_20200902T081611_1.json',
        'T35PNL_20201010T082759_B01.jp2': 'clouds_PNL_A018780_20201010.json',
        'T35PPM_20200922T081641_B01.jp2': 'clouds_PPM_A027431.json',
        'T35PQM_20200917T081609_B01.jp2': 'clouds_PQM_A018451.json',
        'T35PQM_20201017T081839_B01.jp2': 'clouds_PQM_A018880_20201017.json'
    }
    for raster_file, json_file in files.items():
        try:
            output_file = json_file.replace('clouds_', '').replace('.json', '_cloud_mask.jp2')
            raster_arr, profile = read_raster(DATA_DIR / raster_file)
            arr = json_to_arr(DATA_DIR / json_file, profile['width'], profile['height'])
            arr = mask_no_data(raster_arr, arr)
            write_output(arr, profile, DATA_DIR / output_file)
        except Exception:
            print(f"Error occurred with {raster_file}")
            raise


if __name__ == '__main__':
    main()
