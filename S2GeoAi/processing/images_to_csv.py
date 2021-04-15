import os
import subprocess
import tempfile
from pathlib import Path
from typing import List

import rasterio
import numpy as np
import pandas as pd

DATA_DIR = (Path(__file__).parent / '../../data').resolve()
RESOLUTION = 60
COLUMNS = ["C", "B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B10", "B11", "B12"]


def build_vrt(raster_files: List[Path], resolution: int, prefix: str) -> Path:
    output = Path(tempfile.NamedTemporaryFile(dir=DATA_DIR, prefix=prefix, suffix=".vrt").name)
    resolution = str(resolution)
    command = ["gdalbuildvrt", "-resolution", "user", "-tr",
               resolution, resolution, "-separate", output] + raster_files
    subprocess.run(command)
    return output


def convert_data_to_csv(raster_dir: Path, mask_file: Path):
    raster_files = sorted(filter(lambda f: f.name.endswith('jp2'), list(raster_dir.iterdir())))
    raster = build_vrt(raster_files, RESOLUTION, raster_dir.name)
    mask = build_vrt([mask_file], RESOLUTION, raster_dir.name + '_mask_')
    try:
        df = rasters_to_df(mask, raster)
        df.to_csv(DATA_DIR / mask_file.name.replace('_cloud_mask.jp2', f'_{RESOLUTION}m.csv'), index=True,
                  compression='gzip')
    finally:
        os.remove(raster)
        os.remove(mask)


def rasters_to_df(mask: Path, raster: Path) -> pd.DataFrame:
    with rasterio.Env():
        with rasterio.open(raster) as ds:
            ds: rasterio.DatasetReader
            with rasterio.open(mask) as mask_ds:
                mask_ds: rasterio.DatasetReader
                ds_arr = ds.read()
                mask_arr = mask_ds.read()
    print("Data read successfully")
    arr = np.concatenate((mask_arr, ds_arr), axis=0)
    arr = np.reshape(arr, (-1, 1), 'F').reshape(-1, 14)  # (x*y,14)

    df = pd.DataFrame(arr, columns=COLUMNS)
    # Drop no-data pixels
    df = df[df['C'] > 0]
    return df


def main():
    data = {
        'PNM_A027474': 'PNM_A027474_20200925T082711_cloud_mask.jp2',
        'PPM_A027145': 'PPM_A027145_20200902T081611_1_cloud_mask.jp2',
        'PNL_A018780': 'PNL_A018780_20201010_cloud_mask.jp2',
        'PPM_A027431': 'PPM_A027431_cloud_mask.jp2',
        'PQM_A018451': 'PQM_A018451_cloud_mask.jp2',
        'PQM_A018880': 'PQM_A018880_20201017_cloud_mask.jp2'

    }
    for dir, mask_name in data.items():
        try:
            print(f"Processing {dir}")
            convert_data_to_csv(DATA_DIR / dir, DATA_DIR / mask_name)
        except Exception:
            print(f"Error orrcurred with {dir}")
            raise


if __name__ == '__main__':
    main()
