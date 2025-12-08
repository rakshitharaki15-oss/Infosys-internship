import pandas as pd
import numpy as np

df = pd.read_csv("data.csv")
print(df.shape)
# print(df.head())
# print(df.columns)
# print(df.isnull())
#1
# missing_val_sum = df.isnull().sum()
# print(missing_val_sum)
#2
df['Hours_Worked'] = df['Hours_Worked'].astype(int)
# print("dtype ",df['Hours_Worked'].dtype)
#3
df = df.drop_duplicates()
# print(df.shape)
#4
cols_to_strip = ['Name', 'Department', 'City']
for col in cols_to_strip:
    df[col] = df[col].astype(str).str.strip()

# print(df.head())
# print(df['Hours_Worked'].dtype)
#5
def productivity_score(row):
    return (row['Tasks_Completed'] / row['Hours_Worked']) * 100

df['Productivity_Score'] = df.apply(productivity_score, axis=1)
df['Productivity_Score'] = df['Productivity_Score'].round(2)

# print(df.head())
#6
high_prod = df[df['Productivity_Score'] > 18]
# print(high_prod)
indore_emp = df[df['City'] == 'Indore']
# print(indore_emp)
high_sal = df[df['Salary'] > 45000]
# print(high_sal)

report.to_csv("dept_report.csv", index=False)

#task 2 emergency : ->
# df['Hours_Worked'] = pd.to_numeric(df['Hours_Worked'], errors='coerce').astype('Int64')
# coerce - If a value cannot be converted, turn it into NaN instead of throwing an error.

