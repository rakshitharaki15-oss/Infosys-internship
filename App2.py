import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Title
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
# Custom Button Style
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
# File Upload
data = st.file_uploader("Upload your traffic dataset", type=["csv"])
if data:
    df = pd.read_csv(data)
    st.subheader("Data Preview")
    st.dataframe(df)
    # Calculate Severity Score
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
    # Sidebar Filters
    st.sidebar.title("Filters")
    violation_types = df['Violation_Type'].unique()
    chosen_type = st.sidebar.selectbox("Select Violation Type", violation_types)
    df_filtered = df[df['Violation_Type'] == chosen_type]

    # Location-wise violation count
    violations = df_filtered.groupby("Location").size().reset_index(name="Violation_Count")
    violations["Location"] = violations["Location"].str.strip().str.title()

    # Load India shapefile
    path = r"C:\\Users\\mruna\\Desktop\\InfosysInternship\\India-State-and-Country-Shapefile-Updated-Jan-2020-master\\India-State-and-Country-Shapefile-Updated-Jan-2020-master\\India_State_Boundary.shp"
    states = gpd.read_file(path)
    states["State_Name"] = states["State_Name"].str.strip().str.title()

    # Merge violation data with states
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
    # Map Plot: Numbered States
    st.subheader("Violation Count Map by State (Numbered)")

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
    sorted_states["Rank"] = range(1, len(sorted_states)+1)

    # Add rank numbers at state centroids
    for idx, row in sorted_states.iterrows():
        x, y = row["x"], row["y"]
        if row["State_Name"] == "Delhi":  # adjust Delhi label
            y += 60000
        ax.text(
            x, y,
            f"{row['Rank']}",
            fontsize=12,
            fontweight='bold',
            color='black',
            ha='center',
            va='center'
        )

    # legend mapping numbers to states

    legend_text = "\n".join([f"{row['Rank']}: {row['State_Name']}" for idx, row in sorted_states.iterrows()])

    plt.gcf().text(0.85, 0.3,  legend_text, fontsize=15, bbox=dict(facecolor='white', alpha=0.5))

    ax.set_axis_off()
    plt.title(f"Violations in India for '{chosen_type}'", fontsize=20)
    st.pyplot(fig)

    # Heatmap of Average Severity
    st.subheader("Average Severity Heatmap")

    location_heatmap = df.pivot_table(
        values='Violation_Severity_Score',
        index='Location',
        columns='Violation_Type',
        aggfunc=np.mean
    )
    fig2 = plt.figure(figsize=(14, 7))
    sns.heatmap(location_heatmap, cmap='coolwarm', annot=True)
    plt.title("Average Severity Score by Location and Violation Type")
    plt.tight_layout()
    st.pyplot(fig2)

    # Summary Stats Button
    if st.button("Get Summary Stats"):
        st.subheader("Summary Statistics")
        st.write(df.describe())
