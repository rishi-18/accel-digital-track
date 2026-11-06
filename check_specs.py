import os
import glob
import pandas as pd

files = glob.glob('kyc_documents/*')
print('Total files in kyc_documents:', len(files))

# Let's inspect mock_gstin_registry and mock_udyam_registry
gstin_df = pd.read_csv('mock_gstin_registry.csv')
udyam_df = pd.read_csv('mock_udyam_registry.csv')
print('GSTIN records:', len(gstin_df), gstin_df.columns.tolist())
print('Udyam records:', len(udyam_df), udyam_df.columns.tolist())

# Check K01-K03 in prompt:
# Neha Kaur / Vindhya Tours
# Joseph Shah / Harmony Dental
# Joseph Singh / Ganesh Woodcraft
for kw in ['Vindhya', 'Harmony Dental', 'Ganesh Woodcraft', 'Neha Kaur', 'Joseph']:
    matches = gstin_df[gstin_df['legal_name'].str.contains(kw, case=False, na=False) | gstin_df['trade_name'].str.contains(kw, case=False, na=False)]
    print(f"Match for {kw}:")
    print(matches[['gstin', 'legal_name', 'trade_name', 'status', 'state', 'pincode'] if 'pincode' in gstin_df.columns else matches.columns])

