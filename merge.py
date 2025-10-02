import pandas as pd
import glob

csv_files = glob.glob("Medicare_Hospital_Spending_by_Claim_Q*.csv")

combined_df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

combined_df.drop_duplicates(inplace=True)

combined_df.to_csv("Medicare_Hospital_Spending_by_Claim.csv", index=False)

print("Combined CSVs successfully into 'Medicare_Hospital_Spending_by_Claim.csv'")
print(f"Total rows: {len(combined_df)}")
print("Columns:", combined_df.columns.tolist())
