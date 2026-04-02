# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:13:54 2026

@author: HP
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

# -----------------------------------------------------
# Streamlit Page Config
# -----------------------------------------------------
st.set_page_config(
    page_title="NSRTN",
    page_icon="D:/CPHL-MOH/pics/MoH_logo.png",
    layout="wide"
)

# %% Functions
# Function:  extract value from mixed cell, e.g. 45% (2/5)
def extract_percent(x):
    if pd.isna(x) or x == "":
        return np.nan
    return float(x.split("%")[0])


# Fucntion:  Color coding - lowest to highest
def col_rag(val):
    if pd.isna(val):
        return ""
    elif val < 50:
        return "color:green; font-weight: bold;"
    elif val < 80:
        return "color:#BA8E23; font-weight: bold;"
    else:
        return "color: red; font-weight: bold;"
    
# Fucntion:  Color coding for normal highest to lowest
def col_rag1(val):
    if pd.isna(val):
        return ""
    elif val < 50:
        return "color:red; font-weight: bold;"
    elif val < 80:
        return "color:#BA8E23; font-weight: bold;"
    else:
        return "color: green; font-weight: bold;"
    

# Fucntion:  Color coding for Y or n
def col_rag2(val):
    if pd.isna(val):
        return ""
    elif val == "Y": # Use == for comparison
        return "color: green; font-weight: bold;"
    elif val == "Partial": # Use == for comparison
        return "color: #BA8E23; font-weight: bold;"
    else:
        return "color: red; font-weight: bold;"

# %% Load the data frames

# Reached as scheduled
file_path18 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/reached_as_scheduled.sxls"
scheduled  =  pd.read_excel(file_path18)

# Biker serviced, fueled
file_path17 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/bike_ser_fuled.xls"
biker  =  pd.read_excel(file_path17)

# Results TAT within TAT
file_path18 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/resultsTAT.xls"
resultsTAT  =  pd.read_excel(file_path18)

# Refer TAT within TAT
file_path19 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/referTAT.xls"
referdTAT  =  pd.read_excel(file_path19)

# Rejection Rate
file_path20 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/rejectn.xls"
rejtnRate  =  pd.read_excel(file_path20)

# NSRTN Details
file_path20 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/nsrtn_details.xls"
NSRTN_Details  =  pd.read_excel(file_path20)

# NSRTN Details
file_path21 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/nsrtn_KPIs.xls"
NSRTN_KPIs  =  pd.read_excel(file_path21)



# %% Common filter (RRH)
# Sidebar Filter for all tables

# Apply the filter for all table

# Define Hub Name
RRH_list = sorted(NSRTN_KPIs["RRH"].dropna().unique().tolist())
indicator_list  = sorted(NSRTN_KPIs["Indicator"].dropna().unique().tolist())

with st.sidebar:
    st.header("Filters", divider=True)
    
    selected_RRH = st.selectbox("RRH Region:", ["All"] + RRH_list, key="select_rrh")
    
    selected_Indicator = st.selectbox("Indicator:", ["All"] + indicator_list, key="select_ind")

  
# -----------------------------------------------------
# Reusable filter function
# -----------------------------------------------------
def apply_filters(df, rrh, indicator):
    df_filtered = df.copy()
    
    # Filter by RRH if column exists and not "All"
    if "RRH" in df_filtered.columns and rrh != "All":
        df_filtered = df_filtered[df_filtered["RRH"] == rrh]
        
    # Filter by Indicator if column exists and not "All"
    if "Indicator" in df_filtered.columns and indicator != "All":
        df_filtered = df_filtered[df_filtered["Indicator"] == indicator]
        
    return df_filtered

# -----------------------------------------------------
# Apply filter to ALL tables
# -----------------------------------------------------
# 1. Define the dictionary of original tables FIRST
tables = {
    "RRH_NSRTNKpis": NSRTN_KPIs,
    "NSRTN_Detail":  NSRTN_Details
}

# 2. Now apply the filter to that dictionary
filtered_tables = {
    name: apply_filters(table, selected_RRH, selected_Indicator)
    for name, table in tables.items()
}

# 3. Access the results
filter_NSRTN_KPIs = filtered_tables["RRH_NSRTNKpis"]
filter_NSRTN_Detail = filtered_tables["NSRTN_Detail"]


# %% NSRTN KPI list, by RRH Region
# apply the styling

col_name = "%age of sites with complete complaince"

# create a helper column
filter_NSRTN_KPIs["percent_value"]  = filter_NSRTN_KPIs[col_name].apply(extract_percent)

# Apply styling
styled_filter_NSRTN_KPIs = (
    filter_NSRTN_KPIs.style
    .apply(
        lambda x: [col_rag1(v) for v in filter_NSRTN_KPIs["percent_value"]],
        subset=[col_name],
        axis=0  # Explicitly apply along the index (rows)
    )
    .hide(["percent_value"], axis="columns")
)

# Diplay the table

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        NSRTN KPI Status by Region
    </h2>
    """, 
    unsafe_allow_html=True
)



# Show all columns EXCEPT "percent_value"
visible_columns = [col for col in filter_NSRTN_KPIs.columns if col != "percent_value"]

# Dispay the data frame
st.dataframe(
    styled_filter_NSRTN_KPIs,
    column_order=visible_columns,
    use_container_width=True,
    hide_index=True,
    column_config={
        "%age of sites with complete complaince": st.column_config.TextColumn(
           "Compliance %", 
           help="%age of sites with complete compliance",
           width="small"
       ),
       "Partial_Status_Observed": st.column_config.TextColumn(
           "Audited (%)", 
           help="Labs QMS Audited (%)",
           width="small"
       ),
       "Status resulting from observed partial performance": st.column_config.TextColumn(
           "Partial", 
           help="Status resulting from observed partial performance",
           width="small"
        )
    }
)

# %% NSRTN Detailed table

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        Health Facility NSRTN Line list Detail
    </h2>
    """, 
    unsafe_allow_html=True
)


# Making a copy of the data frame
df_for_grid = filter_NSRTN_Detail.copy()

# Define the JavaScript for color coding (Equivalent to the function)

color_jscode = JsCode("""
function(params) {
    if (params.value === 'Y') {
        return {'color': 'green', 'font-weight': 'bold', 'font-size': '12px'};
    } else if (params.value === 'Partial') {
        return {'color': '#BA8E23', 'font-weight': 'bold', 'font-size': '12px'};
    } else if (params.value === 'N') {
        return {'color': 'red', 'font-weight': 'bold', 'font-size': '12px'};
    } else {
        return {'font-size': '12px'};
    }
};
""")

# Build Grid Options from the data frame
gb = GridOptionsBuilder.from_dataframe(df_for_grid)

# Default column behavior
gb.configure_default_column(
    filter=True, 
    sortable=True,
    wrapText=True,
    autoHeight=True,
    cellStyle={'font-size': '12px', 'line-height': '14px', 'padding-top': '2px'}
)

# Apply the color logic to the target columns
target_cols = ["scheduledVst", "bike_service_fueled", "TAT_withinTarget", "Refer_timely", "RejtRate"]
for col in target_cols:
    gb.configure_column(col, cellStyle=color_jscode)

# Column Headers & Pining
gb.configure_column("RRH", pinned="left")

gb.configure_column("scheduledVst", headerName="Site visited by sample transporter as scheduled", wrapHeaderText=True, autoHeaderHeight=True)
gb.configure_column("bike_service_fueled", headerName="The hubs have bikes timely serviced, and fueled", wrapHeaderText=True, autoHeaderHeight=True)
gb.configure_column("TAT_withinTarget", headerName="The facility receives samples results within targeted TAT", wrapHeaderText=True, autoHeaderHeight=True)
gb.configure_column("Refer_timely", headerName="The facility refers samples within the targeted TAT", wrapHeaderText=True, autoHeaderHeight=True)
gb.configure_column("RejtRate", headerName="The facility rejection rate is within acceptable Rejection Rates", wrapHeaderText=True, autoHeaderHeight=True)

grid_options = gb.build()

# Display the grid using the DATAFRAME 
grid_response = AgGrid(
    df_for_grid,
    gridOptions=grid_options,
    allow_unsafe_jscode=True,  # REQUIRED to use JsCode for colors
    data_return_mode="FILTERED_AND_SORTED", 
    update_mode=GridUpdateMode.MODEL_CHANGED,
    fit_columns_on_grid_load=True,
    theme='alpine'
)

# Download Button
df_to_download = grid_response['data']
st.download_button(
    label="📥 Download Table",
    data=df_to_download.to_csv(index=False).encode('utf-8'),
    file_name='NSRTN_report.csv',
    mime='text/csv'
)


