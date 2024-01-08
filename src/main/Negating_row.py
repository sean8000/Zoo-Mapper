import pandas as pd

df = pd.read_excel("some file", sheet_name=0)

df['Inverted'] = -1 * int(df['somename'])

df.to_excel("NewName.xlsx")