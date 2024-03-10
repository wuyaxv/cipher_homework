import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# plt.style.use('seaborn-whitegrid')

def isKAnonymized(df, k):
    for index, row in df.iterrows():
        query = '&'.join([f'{col}=={row[col]}' for col in df.columns])
        rows = df.query(query)
        if rows.shape[0] < k:
            return False
        return True

raw_data = {
    'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'], 
    'last_name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze'], 
    'age': [42, 52, 36, 24, 73], 
    'preTestScore': [4, 24, 31, 2, 3],
    'postTestScore': [25, 94, 57, 62, 70]}
#df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
df = pd.DataFrame(raw_data, columns = ['age', 'preTestScore', 'postTestScore'])

print(df)
k = 1
print(f"k={k}, is k anonymized?", isKAnonymized(df, k))
k = 2
print(f"k={k}, is k anonymized?", isKAnonymized(df, k))

