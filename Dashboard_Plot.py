import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# This module handles plots for the Dashboard (Home Page)
# ---------------------------------------------------------
# UNIFORM STYLE CONFIGURATION
# ---------------------------------------------------------
# Define standard formatting constants
TITLE_SIZE = 22
LABEL_SIZE = 20
TICK_SIZE = 20
TITLE_WEIGHT = 'bold'
LABEL_WEIGHT = 'bold'
TICK_WEIGHT = 'bold'
FIG_SIZE = (16, 9)
# Define a standard color family (High intensity, distinct colors)
UNI_PALETTE = "deep" 

def apply_plot_style():
    """
    Applies the uniform style settings to matplotlib and seaborn.
    Call this at the start of plot functions or globally.
    """
    sns.set_theme(style="whitegrid", context="talk", palette=UNI_PALETTE)
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': TICK_SIZE,
        'axes.titlesize': TITLE_SIZE,
        'axes.titleweight': TITLE_WEIGHT,
        'axes.labelsize': LABEL_SIZE,
        'axes.labelweight': LABEL_WEIGHT,
        'xtick.labelsize': TICK_SIZE,
        'ytick.labelsize': TICK_SIZE,
        'figure.titlesize': TITLE_SIZE,
        'figure.figsize': FIG_SIZE,
        'axes.grid': True,
        'grid.alpha': 0.3
    })

# Apply global style on module load
apply_plot_style()

# =============================== Dashboard Overview Plots =============================================
# ----- Amit's Plots -----
def plot_violation_type_percentage_pie(df):
    """
    Plots the percentage of traffic violation types as a pie chart.
    """
    apply_plot_style()
    violation_counts = df['Violation_Type'].value_counts()
    
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    wedges, texts, autotexts = ax.pie(
        violation_counts,
        autopct='%1.1f%%',
        colors=sns.color_palette('tab10'), # Deep colors
        wedgeprops={'edgecolor': 'black'},
        pctdistance=0.85,
    )
    plt.setp(autotexts, size=TICK_SIZE, weight="bold") # standard size
    ax.legend(
        wedges, 
        violation_counts.index,
        title="Violation Types",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        title_fontsize=LABEL_SIZE,
        fontsize=TICK_SIZE,
    )
    ax.set_title("Percentage of Traffic Violation Types", fontsize=TITLE_SIZE)
    ax.axis('equal')
    plt.tight_layout()
    return fig

# =================================================================================
def plot_fines_based_on_violation_type(summary):
    """
    Plots the fines based on violation type (Paid vs Unpaid).
    """
    apply_plot_style()
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    summary.plot(
        kind='bar',
        stacked=True,
        color=['#FF6B6B', '#4ECDC4'],     # Paid, Unpaid
        edgecolor='black', 
        linewidth=1.5,
        fontsize=TICK_SIZE,
        ax=ax
    )
    ax.set_title('Fines Based on Violation Type', fontsize=TITLE_SIZE)
    ax.set_xlabel('Violation Type', fontsize=LABEL_SIZE)
    ax.set_ylabel('Total Fine Amount (₹)', fontsize=LABEL_SIZE)
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(rotation=25, fontweight=TICK_WEIGHT)

    # Format Color Bar values, Y-axis values
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    
    # Calculate totals for percentage calculation
    totals = summary.sum(axis=1)
    
    # Show Paid / Unpaid inside bars with Percentage
    for c in ax.containers:
        # Create custom labels with value and percentage
        labels = []
        for i, v in enumerate(c):
            height = v.get_height()
            # Avoid division by zero
            total_val = totals.iloc[i] if i < len(totals) else 0
            if height > 0 and total_val > 0:
                percentage = (height / total_val) * 100
                labels.append(f'{percentage:.1f}%')
            else:
                labels.append('')
        ax.bar_label(c, labels=labels, label_type='center', fontsize=12, color='black', rotation=0, fontweight='bold')

    totals = summary.sum(axis=1)
    for idx, total in enumerate(totals):
        ax.text(
            idx,
            summary.iloc[idx].sum() + (max(totals) * 0.02),
            f'{total:,.0f}',
            ha='center', va='bottom', fontsize=12, fontweight='bold', color='black'
        )
    
    plt.tight_layout()

    ax.legend(
        title="Status", 
        bbox_to_anchor=(1, 1.05), 
        loc="upper right", 
        ncol=2,
        title_fontsize=LABEL_SIZE,
        fontsize=TICK_SIZE,
    )
    return fig

# =================================================================================
def plot_violations_by_location(location_based_violations):
    apply_plot_style()
    
    # 1. Create subplots to have better control over the object
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    
    # 2. Plot the pie
    wedges, texts, autotexts = ax.pie(
        location_based_violations['No of Violations'],
        autopct='%1.1f%%',
        colors=sns.color_palette('bright'), # Deeper/Vibrant colors
        wedgeprops={'edgecolor': 'black'},
        pctdistance=0.85,
    )
    
    # 3. Handle Text Styling
    plt.setp(autotexts, size=TICK_SIZE, weight="bold")
    
    # 4. Create a legend on the side to utilize the 16:9 width
    ax.legend(
        wedges, 
        location_based_violations['Location'],
        title="Locations",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1), # This pushes the legend outside to the right
        title_fontsize=LABEL_SIZE,
        fontsize=TICK_SIZE,
    )
    
    ax.set_title("Violations by Location", fontsize=TITLE_SIZE)
    
    # 5. Enforce circular shape
    ax.axis('equal')
    # 6. Adjust layout to make room for the legend
    plt.tight_layout()
    return fig
# =====================================================================================
# ---- Anshu's Plots ----
def plot_license_validity_by_gender(df):

    """
    Anshu: License Validity by Gender.
    """
    apply_plot_style()
    validity_gender = df.groupby(['License_Validity', 'Driver_Gender']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    validity_gender.plot(
        kind='bar', 
        ax=ax,
        edgecolor='black', 
        linewidth=1.5,
        fontsize=TICK_SIZE,
    )

    ax.set_title("Number of License Validities by Gender", fontsize=TITLE_SIZE)
    ax.set_xlabel("License Status", fontsize=LABEL_SIZE)
    ax.set_ylabel("Count", fontsize=LABEL_SIZE)
    ax.legend(title="Driver Gender", fontsize=TICK_SIZE)
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.tight_layout()
    return fig

# ============================== Additional Plots ===================================================
# 1. Gender Distribution
def plot_gender_distribution(gender_distribution):
    """
    Plots the gender distribution of drivers.
    """
    apply_plot_style()
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(
        x=gender_distribution.index, 
        y=gender_distribution.values, 
        hue=gender_distribution.index,
        legend=False,
        palette='viridis', 
        edgecolor='black', 
        linewidth=1.5,
        ax=ax
    )
    ax.set_title('Gender Distribution', fontsize=TITLE_SIZE)
    ax.set_xlabel('Gender', fontsize=LABEL_SIZE)
    ax.set_ylabel('Count', fontsize=LABEL_SIZE)
   
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(rotation=25, fontweight=TICK_WEIGHT)
    return fig

# 2. Vehicle Type vs Violation Type (Mounika's Contribution)
def plot_vehicle_type_vs_violation_type(df):
    """
    Mounika: Vehicle type vs Violation Type.
    """
    apply_plot_style()
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.countplot(
        data=df, 
        x='Violation_Type',
        hue='Vehicle_Type',
        ax=ax,
        palette='Set1',
        edgecolor='black'
    )
    ax.set_title('Vehicle Type vs Violation Type', fontsize=TITLE_SIZE)
    ax.set_xlabel('Violation Type', fontsize=LABEL_SIZE)
    ax.set_ylabel('Number of Violations', fontsize=LABEL_SIZE)
    ax.legend(title='Vehicle Type', fontsize=TICK_SIZE, title_fontsize=LABEL_SIZE, bbox_to_anchor=(1, 1), loc='upper left')
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.tight_layout()
    return fig

# 3. Severity Heatmap by Location (Mrunalini's Contribution)
def plot_severity_heatmap_by_location(df):
    """
    Mrunalini: Average Severity Score by Location and Violation Type.
    """
    apply_plot_style()
    # Helper to calculate severity (Internal logic kept same)
    def calc_severity_score(row):
        severity = 0
        if pd.notnull(row.get('Fine_Amount')): severity += row['Fine_Amount'] / 1000
        if pd.notnull(row.get('Penalty_Points')): severity += row['Penalty_Points'] 
        if pd.notnull(row.get('Recorded_Speed')) and pd.notnull(row.get('Speed_Limit')):
            if row['Recorded_Speed'] > row['Speed_Limit']:
                severity += (row['Recorded_Speed'] - row['Speed_Limit']) / 10
        if pd.notnull(row.get('Alcohol_Level')): severity += row['Alcohol_Level'] * 10
        if row.get('Helmet_Worn') == 'No': severity += 10
        if row.get('Seatbelt_Worn') == 'No': severity += 10
        if row.get('Traffic_Light_Status') == 'Red': severity += 15
        if pd.notnull(row.get('Previous_Violations')): severity += row['Previous_Violations'] * 1.5
        return severity

    # We need a copy to avoid SettingWithCopyWarning on the original df if modifying
    # But for dashboard summary df is passed, better to just apply
    # Optimizing: Calculate on the fly might be slow for full df, but for dashboard summary (last n days) should be fine.
    
    # We'll use a local copy to be safe
    local_df = df.copy()
    local_df['Violation_Severity_Score'] = local_df.apply(calc_severity_score, axis=1)
    
    location_heatmap = local_df.pivot_table(
        values='Violation_Severity_Score',
        index='Location',
        columns='Violation_Type',
        aggfunc='mean'
    )

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.heatmap(
        location_heatmap, 
        cmap='magma_r', 
        annot=True, 
        fmt=".1f", 
        ax=ax,
        annot_kws={"size": 12, "weight": "bold"},
        linewidths=1,
        linecolor='black',
    )
    ax.set_title("Average Severity Score by Location and Violation Type", fontsize=TITLE_SIZE)
    ax.set_xlabel('Violation Type', fontsize=LABEL_SIZE)
    ax.set_ylabel('Location', fontsize=LABEL_SIZE)
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.tight_layout()
    return fig
