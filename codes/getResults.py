import os
import pandas as pd
import matplotlib.pyplot as plt

def get_results(path_start, path_end, factor):
    files = os.listdir(path_start)
    for file in files:
        df3 = pd.read_csv(path_start + '/' + file[:-12] + factor + '.csv', index_col=0)
        df3.index = pd.to_datetime(df3.index).values.astype('datetime64[D]')

        # long_only
        net_value = 1
        unit = 0 # 持有份额
        for i in range(len(df3.index)):
            if df3.loc[df3.index[i], 'delta_position_long_only'] == 1:
                unit = net_value/df3.loc[df3.index[i], '收盘']
            elif df3.loc[df3.index[i], 'delta_position_long_only'] == -1:
                net_value = df3.loc[df3.index[i], '收盘'] * unit
                unit = 0

            df3.loc[df3.index[i], 'net_value_long_only'] = net_value
        
        # long_short
        net_value = 1
        unit = 0 # 持有份额
        for i in range(len(df3.index)):
            # 开多仓
            if df3.loc[df3.index[i], 'position_long_short'] == 0 and df3.loc[df3.index[i], 'delta_position_long_short'] == 1:
                open_price = df3.loc[df3.index[i], '收盘']
                unit = net_value/df3.loc[df3.index[i], '收盘']
            # 开空仓
            elif df3.loc[df3.index[i], 'position_long_short'] == 0 and df3.loc[df3.index[i], 'delta_position_long_short'] == -1:
                open_price = df3.loc[df3.index[i], '收盘']
                unit = -net_value/df3.loc[df3.index[i], '收盘']
            # 平多仓
            elif df3.loc[df3.index[i], 'position_long_short'] == 1 and df3.loc[df3.index[i], 'delta_position_long_short'] == -1:
                net_value += (df3.loc[df3.index[i], '收盘'] - open_price) * unit
                unit = 0
            # 平空仓
            elif df3.loc[df3.index[i], 'position_long_short'] == -1 and df3.loc[df3.index[i], 'delta_position_long_short'] == 1:
                net_value += (df3.loc[df3.index[i], '收盘'] - open_price) * unit
                unit = 0

            df3.loc[df3.index[i], 'net_value_long_short'] = net_value


        #绘制第一个Y轴
        fig = plt.figure(figsize=(20,8), dpi=80)
        ax = fig.add_subplot(111)
        lin1 = ax.plot(df3.index, df3['收盘'], label='close price')
        ax.set_ylabel('close price')
        
        #绘制另一Y轴    
        ax1 = ax.twinx()
        lin2 = ax1.plot(df3.index, df3['net_value_long_only'], color='blue', label="long only")
        lin3 = ax1.plot(df3.index, df3['net_value_long_short'], color="red", label="long short")
        ax1.set_ylabel('net value')
        
        #合并图例
        lins = lin1 + lin2 + lin3
        labs = [l.get_label() for l in lins]
        ax.legend(lins, labs, loc="upper left", fontsize=15)
        plt.savefig(path_end + '/' + file[:-12] + factor[:4] + '.png')