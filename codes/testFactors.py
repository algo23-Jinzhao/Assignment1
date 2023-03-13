import os
import pandas as pd
import numpy as np

def test_factors(path_start, factor):
    files = os.listdir(path_start)
    for file in files:
        df2 = pd.read_csv(path_start + '/' + file, index_col=0)
        df2.index = pd.to_datetime(df2.index).values.astype('datetime64[D]')
        df2['return'] = np.log(df2['收盘'].shift(-1) / df2['收盘'])
        for i in range(1, len(df2.index)):
            df2.loc[df2.index[i], 'factor_slope'] = 1 if df2.loc[df2.index[i], factor] - df2.loc[df2.index[i-1], factor] >= 0\
                else -1
        print(df2[['return', 'factor_slope']].corr())

test_factors('./factors', 'vnsp_llt')