import pandas as pd

data_dict_df = pd.read_csv('2017_Dynamic_LAR_Spec.csv', header=1)

cleaned_cols = [s.strip() for s in data_dict_df[' Data Field Name'].tolist()]

data_df = pd.read_csv('2017_lar.txt', delimiter='|', names=cleaned_cols)

census_tract_df = pd.read_csv('Census_Tracts_2010.csv')

tract_codes = census_tract_df['NAME10'].tolist()

filtered_origination_df = data_df[(data_df['Census Tract'].isin(tract_codes)) & (data_df['Type of Action Taken'] == 1)]

filtered_origination_df.to_csv('detroit_mortgage_origination.csv')

