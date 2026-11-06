import glob
import os
import re
import pandas as pd

# Let's inspect the files in kyc_documents
for f in sorted(glob.glob('kyc_documents/*'))[:16]:
    print(f)

# Let's check mock_gstin_registry for 19EOGXH4115Y1ZL and 19E0GXH...
gstin_df = pd.read_csv('mock_gstin_registry.csv')
print("\nLook for 19EOGXH4115Y1ZL:")
print(gstin_df[gstin_df['gstin'].str.contains('19E.*XH4115', na=False)])

print("\nLook for 27XUIXG0767D1ZP (Ganesh Woodcraft):")
print(gstin_df[gstin_df['gstin'].str.contains('27XUIXG0767D1ZP|Ganesh', na=False, case=False)][['gstin', 'legal_name', 'trade_name', 'principal_place_of_business', 'status']])

print("\nLook for 37IHKXV5167L1ZS / Neha Kaur / Vindhya:")
print(gstin_df[gstin_df['legal_name'].str.contains('Neha Kaur', na=False, case=False)][['gstin', 'legal_name', 'trade_name', 'principal_place_of_business', 'status']])

