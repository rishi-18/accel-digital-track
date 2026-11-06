import pandas as pd
gst = pd.read_csv('mock_gstin_registry.csv')
print(gst[gst['trade_name'].str.contains('Vindhya', na=False, case=False)])

