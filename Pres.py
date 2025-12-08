import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
df = pd.read_csv("Indian_Traffic_Violations.csv")
# print(df.head())
# print(df.columns)
# dup_ids = (df[df['Violation_ID'].duplicated()]['Violation_ID'])
# print(dup_ids)
#creating severity scores
# def calc_severity_score(row):
    # severity = 0
    # Fine Amount
    # if pd.notnull(row['Fine_Amount']):
    #     severity += row['Fine_Amount'] / 100
    # # 2. Penalty Points
    # severity += row['Penalty_Points'] * 2
    # # 3. Speed Violation
    # if pd.notnull(row['Recorded_Speed']) and pd.notnull(row['Speed_Limit']):
    #     overspeed = row['Recorded_Speed'] - row['Speed_Limit']
    #     if overspeed > 0:
    #         severity += overspeed * 0.2
    # # 4. Alcohol Level
    # if pd.notnull(row['Alcohol_Level']):
    #     severity += row['Alcohol_Level'] * 5

    # # 5. Helmet / Seatbelt Violation
    # if row['Helmet_Worn'] == 'No':
    #     severity += 10
    # if row['Seatbelt_Worn'] == 'No':
    #     severity += 10

    # # 6. Traffic Light Status
    # if row['Traffic_Light_Status'] == 'Red':
    #     severity += 15

    # # 7. Previous Violations
    # severity += row['Previous_Violations'] * 1.5

    # return severity


# df['Violation_Severity_Score'] = df.apply(calc_severity_score, axis=1)
# print(df[['Violation_Type', 'Fine_Amount', 'Penalty_Points', 'Violation_Severity_Score']].head())

# plt.figure(figsize=(14,6))
# sns.boxplot(data=df, x='Violation_Type', y='Violation_Severity_Score', color="skyblue")
# plt.xticks(rotation=90)
# plt.title("Severity Score by Violation Type (Boxplot)")
# plt.tight_layout()
# plt.show()

# location_heatmap = df.pivot_table(
#     values='Violation_Severity_Score',
#     index='Location',
#     columns='Violation_Type',
#     aggfunc=np.mean
# )

# plt.figure(figsize=(14,7))
# sns.heatmap(location_heatmap, cmap='coolwarm', annot=True)
# plt.title("Average Severity Score by Location and Violation Type")
# plt.tight_layout()
# plt.show()

print(df["Location"])
state_counts = df['Location'].value_counts().reset_index()
state_counts.columns = ['State', 'Count']
fig = px.choropleth(
    state_counts,
    geojson="https://raw.githubusercontent.com/pravj/india-maps/master/india-states.json",
    featureidkey="properties.state",
    locations="State",
    color="Count",
    color_continuous_scale="Blues",
    title="Traffic Violations by State"
)

fig.update_geos(fitbounds="locations", visible=False)
fig.show()
