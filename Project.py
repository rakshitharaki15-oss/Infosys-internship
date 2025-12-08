import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

df=pd.read_csv(r"C:\Users\mruna\Desktop\InfosysInternship\Indian_Traffic_Violations.csv")
print(df["Location"])
print(df.columns)
# print(df.info())
# print(df.describe())
# rows , cols = df.shape
# print("rows", rows)
# print("cols" , cols)

#WHY ONLY THIS DATASET?->TAKE MEDIUM TO LARGE RANGE OF DATASET...AS WHILE TESTING MODEL OR DURING TRAINING N MANIPULATING NOT TO COMPROMIZE WITH ACCURACY SCORE...1)TRAFFIC VIOLATION IS PROBLEM THAT AFFECT PUBLIC SAFTEY...IT HELP UNDERTAND MOST COMMON VIOLATION WEATER, SEATBELT, PAYMENT METHODS AS SEEN IN DATASET...IT CAN PREDICT WEATHER A FINE WILL BE PAYED OR NOT...FINE AMT IS TARGET VALUE...EG IF SUCH VIOLATIONS HAPPEN REGULARLY CHECKING...
#violation id, date ,time fine amt , violation type, payment method, weather condition , drivers age, helmet worn , seat belt worn , court appearance required , fine payed, ]
# print(df['Violation_Type].unique)
# print(df['freq'].count)
# speed_record = df[df['Recorded_Speed'] > df['Speed_Limit']]
# count = len(speed_record)
# total = len(df)
# percent = (count / total) * 100
# print( count)
# print(percent)

#Weather conditions impact on violations
# plt.figure(figsize=(12,6))
# sns.countplot(
#   y='Weather_Condition',
#   data=df,
#   order=df['Weather_Condition'].value_counts().index,
#   palette='magma'
# )
# plt.tight_layout()
# plt.show()

# hw
# rainy_df = df[df['Weather_Condition'].str.lower() == 'rainy']
# speeding_rainy = rainy_df[rainy_df['Recorded_Speed'] > rainy_df['Speed_Limit']]
# count_speeding_rainy = len(speeding_rainy)
# total_rainy = len(rainy_df)

# Compute proportion / percentage
# percent_speeding_rainy = (count_speeding_rainy / total_rainy) * 100

# print("Total violations on rainy days:", total_rainy)
# print("Speeding violations on rainy days:", count_speeding_rainy)
# print("Percentage of speeding violations on rainy days: {:.2f}%".format(percent_speeding_rainy))

#JOY PLOT-  SPEED difference distribution by weather

#create a new feature -> how much drivers exceeded speed limit
df['Speed_Diff'] = df['Recorded_Speed']-df['Speed_Limit']

#Sort weather conditions for a nice layered effect
order = df["Weather_Condition"].value_counts().index
# #inc plot size
# plt.figure(figsize=(12,8))
#draw ridge joy plot using seabord
# sns.violinplot(data=df, x="Speed_Diff" , y="Weather_Conditions" , order=order, scale="width" , inner="quartile")
# sns.title("Ridge Plot : speed difference by weather conditions")
# plt.xlabel("Speed difference")
# plt.ylabel("Weather condition")
# #plt.tight_layout() #prevents lavel cutoff
# plt.show()
#strip + swarm combo plot(Fine amount vs payment method)
plt.figure(figsize=(12,6))

sns.stripplot(data=df, x="Payment_Method" , y="Fine_Amount", jitter=True, color="gray", alpha= 0.4)
#jitter is variation in time delay 
#add a swarm plot on top for clarity
# sns.swarmplot(data=df ,x="Payment_Method", y="Fine_Amount", color="red" , size=4)
# plt.title("Fine Amount Distribution across Payment methods")
# plt.xlabel("Payment Method")
# plt.ylabel("Fine Amount")
# plt.show()

#horizontal boxing plot(advance boxplot)(Driver age vs fine)
# sns.boxenplot(data=df, x="Fine_Amount" ,y="Driver_Age")
# plt.title("Drivers age over fine amount payed")
# plt.ylabel("Drivers age")
# plt.xlabel("Fine amount")
# plt.show()
