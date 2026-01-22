import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/1/Desktop/ABC-XYZ analyz/abc_xyz_dataset.csv')
df['date'] = pd.to_datetime(df['date'])

#ABC
def ABC(arg):
    if arg <= 80:
        return 'A'
    elif arg <= 95:
        return 'B'
    else:
        return 'C'

df_abc = df.groupby('sku')['revenue'].sum().reset_index().sort_values(by='revenue', ascending=False)
df_abc['cumsum'] = df_abc['revenue'].cumsum()
df_abc['Percentage_rev'] = (df_abc['cumsum']/df_abc['revenue'].sum())*100
df_abc['Classification_ABC'] = df_abc['Percentage_rev'].apply(ABC)

#XYZ analyz
def XYZ(cv):
    if cv <= 10:
        return 'X'
    elif cv <= 25:
        return 'Y'
    else:
        return 'Z'

df['month'] = df['date'].dt.to_period('M')
monthly_demand = df.groupby(['month', 'sku'])['qty'].sum().reset_index()

xyz = monthly_demand.groupby('sku')['qty'].agg(['mean', 'std']).reset_index()
xyz['CV'] = (xyz['std']/xyz['mean'])*100
xyz = xyz.sort_values(by='CV', ascending=True)

xyz['Classification_XYZ'] = xyz['CV'].apply(XYZ)

#Combination

abc_for_comb = df_abc[['sku', 'Classification_ABC']]
xyz_for_comb = xyz[['sku', 'Classification_XYZ']]

complex_ABC_XYZ = abc_for_comb.merge(xyz_for_comb, on='sku', how='inner')
complex_ABC_XYZ['ABC+XYZ'] = complex_ABC_XYZ['Classification_ABC']+complex_ABC_XYZ['Classification_XYZ']

count = complex_ABC_XYZ.groupby('ABC+XYZ')['ABC+XYZ'].count()
count.plot(kind='bar', figsize=(10, 4))
plt.ylabel('Count')
plt.title('Count per ABC+XYZ')
plt.show()