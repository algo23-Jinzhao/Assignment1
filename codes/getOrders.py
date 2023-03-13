import os
import pandas as pd

def get_orders(path_start, path_end, factor):
    files = os.listdir(path_start)
    for file in files:
        df2 = pd.read_csv(path_start + '/' + file, index_col=0)
        df2.index = pd.to_datetime(df2.index).values.astype('datetime64[D]')
        # 产生信号
        for i in range(1, len(df2.index)):
            if df2.loc[df2.index[i], factor] > df2.loc[df2.index[i-1], factor]:
                df2.loc[df2.index[i], 'signal'] = '看多'
            elif df2.loc[df2.index[i], factor] < df2.loc[df2.index[i-1], factor]:
                df2.loc[df2.index[i], 'signal'] = '看空'
            else:
                df2.loc[df2.index[i], 'signal'] = '不变'
        df2.dropna(axis=0, inplace=True)

        # 信号转换为order，只做多
        position = 0
        for i in range(len(df2.index)):
            delta_position = 0
            if position == 0 and df2.loc[df2.index[i], 'signal'] == '看多':
                delta_position = 1
            elif position == 1 and df2.loc[df2.index[i], 'signal'] == '看空':
                delta_position = -position
            position += delta_position
            df2.loc[df2.index[i], 'delta_position_long_only'] = delta_position

        # 信号转换为order，多空
        position = 0
        for i in range(len(df2.index)):
            delta_position = 0
            df2.loc[df2.index[i], 'position_long_short'] = position # 每日初始仓位
            if position <= 0 and df2.loc[df2.index[i], 'signal'] == '看多':
                delta_position = 1
            elif position >= 0 and df2.loc[df2.index[i], 'signal'] == '看空':
                delta_position = -1
            position += delta_position
            df2.loc[df2.index[i], 'delta_position_long_short'] = delta_position

        df2[['收盘', 'delta_position_long_only', 'position_long_short', 'delta_position_long_short']].to_csv(\
            path_end + '/' + file[:-4] + '_' + factor + '.csv')
