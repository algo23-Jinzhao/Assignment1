import os
import pandas as pd
import numpy as np

def test_orders(path_start, path_end, factor):
    files = os.listdir(path_start)
    for file in files:
        df2 = pd.read_csv(path_start + '/' + file, index_col=0)
        df2.index = pd.to_datetime(df2.index).values.astype('datetime64[D]')
        df2['return'] = np.log(df2['收盘'] / df2['收盘'].shift())
        print(df2[['return', factor]].corr())

test_orders('./factors', './orders', 'vnsp_llt')