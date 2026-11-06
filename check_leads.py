import pandas as pd
leads = pd.read_csv('smb_leads.csv')
print("Find leads with 37IHKXV5167L1ZS or 19EOGXH4115Y1ZL or 27XUIXG0767D1ZP:")
print(leads[leads['gstin'].isin(['37IHKXV5167L1ZS', '19EOGXH4115Y1ZL', '27XUIXG0767D1ZP'])][['lead_id', 'business_name', 'contact_name', 'gstin', 'udyam_number', 'stage_reached', 'drop_reason']])

