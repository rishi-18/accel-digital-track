import pandas as pd
gst = pd.read_csv('mock_gstin_registry.csv')
udyam = pd.read_csv('mock_udyam_registry.csv')

print("Row 33 GST:")
print(gst.iloc[33].to_dict())

print("\nRow 923 GST (Harmony Dental):")
print(gst.iloc[923].to_dict())

print("\nRow 2552 GST (Ganesh Woodcraft):")
print(gst.iloc[2552].to_dict())

print("\nUdyam matches for Vindhya, Harmony, Ganesh:")
print(udyam[udyam['enterprise_name'].str.contains('Vindhya|Harmony|Ganesh', case=False, na=False)][['udyam_number', 'enterprise_name', 'state', 'city']])

