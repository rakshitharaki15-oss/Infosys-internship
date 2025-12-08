import pandas as pd
df=pd.read_csv(r"C:\Users\Desktop\InfosysInternship\grades.csv")
# print(df.head())
df.columns = df.columns.str.replace('"','').str.strip()
# print(df.columns())
# print(df.info())
# print(df.describe())
# print(df.iloc[3])
# cols=['test1','test2','test3','test4']
# df[cols]=df[cols].apply(pd.to_numeric,errors='coerce')
# df['Average']=df[cols].mean(axis=1)
print(df.head())

df = df.dropna()
df['Final'] = pd.to_numeric(df['Final'], errors='coerce')
df['Performance'] = df['Final'].apply(
  lambda x : 'Excellent' if x>85
  else 'Good' if x>=70 and x<=84
  else 'Average' if x>=60 and x<=69
  else 'Poor'
)
print(df)
