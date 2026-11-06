import pandas as pd
leads = pd.read_csv('smb_leads.csv')
for idx in [44, 1286, 3570]:
    row = leads.iloc[idx].dropna().to_dict()
    print(f"\n--- Lead {row.get('lead_id')} ---")
    for k, v in row.items():
        print(f"  {k}: {v}")

