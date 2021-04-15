import glob

import numpy as np
import pandas as pd
import rasterio

from json_to_jp2 import read_raster, write_output, DATA_DIR


def prediction_csv_to_jp2(fname, reference_raster):
    print(fname)
    df = pd.read_csv(fname)
    df.columns = ['C', 'i']
    df['i'] = df.i.astype(np.uint)
    df['C'] = df['C'].astype(np.uint) + 1
    df = df.set_index(['i'])
    _, pr = read_raster(DATA_DIR / reference_raster)
    n = np.zeros((pr['width'], pr['height'])).flatten()
    np.put(n, df[df.C == 1].index, 1)
    np.put(n, df[df.C == 2].index, 2)
    n2 = np.reshape(n, (pr['width'], pr['height']), 'F')
    write_output(n2.astype(rasterio.uint8), pr, fname.replace('.txt', '.jp2'))


def main():
    dname = 'predictions'
    reference_raster = 'PNM_A027474_20200925T082711_cloud_mask.jp2'
    for fname in glob.glob(str(DATA_DIR / dname / '*.txt')):
        prediction_csv_to_jp2(fname, reference_raster)


if __name__ == '__main__':
    main()
