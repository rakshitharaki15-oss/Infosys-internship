import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyArrowPatch

st.markdown(
    """
    <h1 style="
        background: linear-gradient(to right, #ff512f, #dd2476);
        -webkit-background-clip: text;
        color: transparent;
        text-align: center;
        font-size: 48px;
        font-weight: bold;
    ">
    Smart Traffic Violation Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background: linear-gradient(to right, #ff512f, #dd2476);
        color: white;
        padding: 10px 22px;
        font-size: 16px;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


data = st.file_uploader("Upload your traffic dataset", type=["csv"])


if data:
    df = pd.read_csv(data)
    st.subheader("Data Preview")
    st.dataframe(df)

    # calculating severity scores
    def calc_severity_score(row):
        severity = 0
        if pd.notnull(row.get('Fine_Amount')):
            severity += row['Fine_Amount'] / 1000
        severity += row.get('Penalty_Points', 0)
        if pd.notnull(row.get('Recorded_Speed')) and pd.notnull(row.get('Speed_Limit')):
            overspeed = row['Recorded_Speed'] - row['Speed_Limit']
            if overspeed > 0:
                severity += overspeed / 10
        if pd.notnull(row.get('Alcohol_Level')):
            severity += row['Alcohol_Level'] * 10
        if row.get('Helmet_Worn') == 'No':
            severity += 10
        if row.get('Seatbelt_Worn') == 'No':
            severity += 10
        if row.get('Traffic_Light_Status') == 'Red':
            severity += 15
        severity += row.get('Previous_Violations', 0) * 1.5
        return severity

    df['Violation_Severity_Score'] = df.apply(calc_severity_score, axis=1)

    st.sidebar.title("Filters")
    violation_types = df['Violation_Type'].unique()
    chosen_type = st.sidebar.selectbox("Select Violation Type", violation_types)
    df_filtered = df[df['Violation_Type'] == chosen_type]

    #location wise violation count based on filter
    violations = df_filtered.groupby("Location").size().reset_index(name="Violation_Count")
    violations["Location"] = violations["Location"].str.strip().str.title()


    path = r"C:\\Users\\mruna\\Desktop\\InfosysInternship\\India-State-and-Country-Shapefile-Updated-Jan-2020-master\\India-State-and-Country-Shapefile-Updated-Jan-2020-master\\India_State_Boundary.shp"

    states = gpd.read_file(path)

    states["State_Name"] = states["State_Name"].str.strip().str.title()

    merged = states.merge(
        violations,
        left_on="State_Name",
        right_on="Location",
        how="left"
    )

    merged_proj = merged.to_crs(epsg=3857)
    merged_proj["centroid"] = merged_proj.geometry.centroid
    merged_proj["x"] = merged_proj.centroid.x
    merged_proj["y"] = merged_proj.centroid.y

    #mapping plot with arrows
    st.subheader("Violation Count Map by State")

    fig, ax = plt.subplots(1, 1, figsize=(17, 7))
    
    merged_proj.plot(
        column="Violation_Count",
        cmap="Reds",
        legend=True,
        edgecolor="black",
        linewidth=0.5,
        missing_kwds={"color": "lightgrey", "label": "No Data"},
        ax=ax
    )

    sorted_states = merged_proj.dropna(subset=["Violation_Count"]).sort_values(by="Violation_Count", ascending=False)
    
    for i in range(len(sorted_states)-1):
        row_source = sorted_states.iloc[i]
        row_target = sorted_states.iloc[i+1]
        diff = row_source["Violation_Count"] - row_target["Violation_Count"]
        linewidth = 0.5 
        arrow = FancyArrowPatch(
            (row_source["x"], row_source["y"]),
            (row_target["x"], row_target["y"]),
            connectionstyle="arc3,rad=0.3",
            color="black",
            alpha=0.8,
            linewidth=linewidth,
            arrowstyle="Simple,head_length=10,head_width=5,tail_width=1"
        )
        ax.add_patch(arrow)

    #adding number ranking
    ranked_states = sorted_states.copy()
    ranked_states["Rank"] = range(1, len(ranked_states)+1)
    for idx, row in ranked_states.iterrows():
        x, y = row["x"], row["y"]
        if row["State_Name"] == "Delhi":
            y += 60000
        ax.text(
            x, y,
            str(row["Rank"]),
            fontsize=10,
            fontweight='bold',
            color='black',
            ha='center',
            va='center',
            zorder=5
        )
    ax.set_axis_off()
    plt.title(f"Violations in India for '{chosen_type}'", fontsize=20)
    st.pyplot(fig)

    # if st.button("View Filtered data"):
    #     st.subheader(f"Filtered Data for: {chosen_type}")
    #     st.dataframe(violations)

    #HeatMap
    st.subheader("Average Severity Heatmap")

    #pivot table
    location_heatmap = df.pivot_table(
        values='Violation_Severity_Score',
        index='Location',
        columns='Violation_Type',
        aggfunc=np.mean
    )
    fig2 = plt.figure(figsize=(14, 7))
    sns.heatmap(location_heatmap, cmap='coolwarm', annot=True)
    # sns.barplot(location_heatmap)
    plt.title("Average Severity Score by Location and Violation Type")
    plt.tight_layout()
    st.pyplot(fig2)

    st.subheader("Average Severity Grouped Bar Chart")

    agg_df = df.groupby(['Location', 'Violation_Type'])['Violation_Severity_Score'].mean().reset_index()

    # Plotting
    fig3, ax3 = plt.subplots(figsize=(15, 7))

    # grouped bar 
    sns.barplot(
        data=agg_df,
        x='Location',
        y='Violation_Severity_Score',
        hue='Violation_Type',
        palette='Set2',
        ax=ax3
    )

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Average Violation Severity Score")
    plt.xlabel("Location")
    plt.title("Average Violation Severity by Location and Violation Type")
    plt.legend(title='Violation Type')
    plt.tight_layout()

    st.pyplot(fig3)

    if st.button("Get Summary Stats"):
        st.subheader("Summary Statistics")
        st.write(df.describe())
