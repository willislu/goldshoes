import os
import pandas as pd

folder_path = r'C:\Users\luwil\Documents\NFL-Data\NFL-data-Players'  # update this path

csv_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.csv'):
            full_path = os.path.join(root, file)
            csv_files.append(full_path)

print(f"Found {len(csv_files)} CSV files in total (including subfolders).")

# Read and concatenate all CSVs
df_list = []
for file_path in csv_files:
    print(f"Reading {file_path}")
    df = pd.read_csv(file_path)
    df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)

output_path = os.path.join(folder_path, 'combined_nfl_player_stats_all_years.csv')
combined_df.to_csv(output_path, index=False)
print(f"Combined CSV saved to {output_path}")
