import pandas as pd

leads = pd.read_csv('smb_leads.csv')
print('Leads shape:', leads.shape)
print('Total leads:', len(leads))
print('Activated leads:', len(leads[leads['stage_reached'] == 'Activated']))
print('Conversion rate:', len(leads[leads['stage_reached'] == 'Activated']) / len(leads) * 100)
print('Contacted:', len(leads[leads['stage_reached'].isin(['Contacted', 'Needs assessed', 'Quote accepted', 'KYC complete', 'Activated'])]))
print('Stage distribution:\n', leads['stage_reached'].value_counts())

sample = leads[leads['business_name'].str.contains('Vindhya|Harmony|Ganesh', na=False, case=False)]
print(sample[['lead_id', 'business_name', 'gstin', 'has_gstin', 'udyam_number', 'contact_name', 'city', 'state']])

