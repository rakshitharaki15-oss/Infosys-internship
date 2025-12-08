import pandas as pd
import numpy as np

df = pd.read_csv("Indian_Traffic_Violations.csv")

#1. Data quality report
# report = pd.DataFrame()

# report["Data_Type"] = df.dtypes

# report["Missing_%"] = df.isnull().mean() * 100

# report["Unique_Values"] = df.nunique()

# duplicate_percent = (df.duplicated().sum() / len(df)) * 100


# print("\n------------DATA QUALITY REPORT-----------")
# print(report)

# #2. Summary report

# print("-----------SUMMARY REPORT----------")

# print("Total Violations:", len(df))

# if "Violation_Type" in df.columns:
#     print("Most Common Violation:", df["Violation_Type"].mode()[0])

# if "Fine_Amount" in df.columns:
#     print("Average Fine Amount:", df["Fine_Amount"].mean())
#     print("Max Fine:", df["Fine_Amount"].max())
#     print("Min Fine:", df["Fine_Amount"].min())

# if "Issuing_Agency" in df.columns:
#     print("Most Active Issuing Agency:", df["Issuing_Agency"].mode()[0])


# #3. Rule based flagging
# print("-----------Rule based flags---------")

# if "Recorded_Speed" in df.columns and "Speed_Limit" in df.columns:
#     df["Over_Speeding_Flag"] = df["Recorded_Speed"] > df["Speed_Limit"]

# if "Fine_Amount" in df.columns:
#     p90 = df["Fine_Amount"].quantile(0.90)
#     df["High_Fine_Flag"] = df["Fine_Amount"] > p90

# if "Weather" in df.columns:
#     bad_weather = ["Fog", "Rain", "Snow", "Storm"]
#     df["Bad_Weather_Risk"] = df["Weather"].isin(bad_weather)

# print(df.head())

# GENERATE INSIGHTS BY GROUPING EXT OUTPUTS AND USE GROUP BY AND PRINT INSIGHTS LIK VIOLATION PER CITY, AVG FINE BY VIOLATION TYPE, AVG AGE OF VIOLATERS, HEIGHEST FINE COLLECTED BY WEATHER CONIDTION, PAYMENT METHOD IN PERCT...ALL IN TABLES

# TOP 10 MOST FREQUEST VIOLATIONS IN OUTPUT TABLE- SORTED FREQUENCY TABLE, VIOLATIION TYPE FRE, PERCENT 3 COLS

#TIME BEASED ANALYSIS NO VISUALIZATION - FROM DATE N TIME EXTRACT DAY OF WEEK MONTH HR OF DAY, REPORT DAY WITH HEIGHTS VIOLATION, MONTH WITH HEIGHTS FINES COLLECTED, WHAT TIEM OF DAY VIOLATION PEAk


#violation per city
if "Location" in df.columns:
    city_counts = df.groupby("Location").size().reset_index(name="Violation_Count")
    city_counts = city_counts.sort_values(by="Violation_Count", ascending=False)
    print(city_counts)
else:
    print("City column not found.")

#avg fine by violation type
if "Violation_Type" in df.columns and "Fine_Amount" in df.columns:
    fine_violation = df.groupby("Violation_Type")["Fine_Amount"].mean().reset_index()
    fine_violation = fine_violation.sort_values(by="Fine_Amount", ascending=False)
    print(fine_violation)
else:
    print("Required columns not found.")

#avg age of violator
if "Driver_Age" in df.columns:
    print("Average Age of Violators:", df["Driver_Age"].mean())
else:
    print("Age column not found.")

#total fine by weather condition
if "Weather_Condition" in df.columns and "Fine_Amount" in df.columns:
    fine_weather = df.groupby("Weather_Condition")["Fine_Amount"].sum().reset_index()
    fine_weather = fine_weather.sort_values(by="Fine_Amount", ascending=False)
    print(fine_weather)
else:
    print("Required columns not found.")

#paymemnt method percent
if "Payment_Method" in df.columns:
    payment_percent = (df["Payment_Method"].value_counts(normalize=True) * 100).reset_index()

    payment_percent.columns = ["Payment_Method", "Percent"]

    print(payment_percent)
else:
    print("Payment_Method column not found.")

print("\n TOP 10 MOST FREQUENT VIOLATIONS \n")

if "Violation_Type" in df.columns:
    violation_freq = df["Violation_Type"].value_counts().reset_index()
    violation_freq.columns = ["Violation_Type", "Frequency"]

    violation_freq["Percent"] = (violation_freq["Frequency"] / len(df)) * 100
    print(violation_freq.head(10))
else:
    print("Violation_Type column not found.")
