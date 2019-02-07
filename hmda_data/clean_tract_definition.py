import pandas as pd

df = pd.read_csv('Census_Tracts_2010.csv')

cleaned = df.drop(columns=['the_geom'])

cleaned.to_csv('geom_free_detroit_tracts.csv')
