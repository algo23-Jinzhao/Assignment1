import akshare as ak

index_stock_info_df = ak.index_stock_info()
index_stock_info_df.to_csv('./IndexInfo.csv', index=0)