import pandas as pd

data_dict_df = pd.read_csv('2017_Dynamic_LAR_Spec.csv', header=1)

cleaned_cols = [s.strip() for s in data_dict_df[' Data Field Name'].tolist()]

data_df = pd.read_csv('sample.txt', delimiter='|', names=cleaned_cols)

data_df.to_csv('merged.csv')
