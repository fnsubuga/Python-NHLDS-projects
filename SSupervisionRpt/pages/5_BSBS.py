# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:07:28 2026

@author: HP
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# -----------------------------------------------------
# Streamlit Page Config
# -----------------------------------------------------
st.set_page_config(
    page_title="BSBS",
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

# %% Fix the heading 
st.markdown("""
    <style>
    .sticky-header {
        position: fixed;
        top: 3.5rem;   /* pushes below Streamlit top bar */
        left: 0;
        right: 0;
        width: 100%;
        background-color: #f9f9f9;
        padding: 12px;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        z-index: 9999;
        border-bottom: 2px solid #ccc;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
   .content {
        margin-top: 90px;  /* prevents overlap */
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="sticky-header">Bio Safety Bio Security<b> </div>', unsafe_allow_html=True)

# Content spacing
st.markdown('<div class="content">', unsafe_allow_html=True)


# %% Load the data frames

# BSBS RRH KPIs
file_path16 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/rrh_KPI_Summary.xls"
bsbsKPI  =  pd.read_excel(file_path16)

# BSBS Health Facility Detail
file_path17 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/hFac_bsbs_detailsxls"
bsbsHfac  =  pd.read_excel(file_path17)

# %% Common filter
# -----------------------------------------------------
# Sidebar Filter for all tables
# -----------------------------------------------------
# Apply the filter for all table

# Define Hub Name
RRH_list = sorted(bsbsHfac["RRH"].dropna().unique().tolist())


with st.sidebar:
    st.header("Filter RRH Region", divider=True)

    selected_RRH = st.selectbox(
        "RRH:",
        options=["All"] + RRH_list,
        index=0,
        key="select_rrh"
    )

# -----------------------------------------------------
# Reusable filter function
# -----------------------------------------------------
def filter_by_rrh(dataframe, selected_RRH):
    # Check column exists to avoid crashing
    if "RRH" not in dataframe.columns:
        return dataframe.copy()
    
    if selected_RRH == "All":
        return dataframe.copy()
    else:
        return dataframe[dataframe["RRH"] == selected_RRH].copy()

# -----------------------------------------------------
# Apply filter to ALL tables
# -----------------------------------------------------
tables = {
    "BSBS_DetailedTbl": bsbsHfac 
        }

filtered_tables = {
    name: filter_by_rrh(table, selected_RRH)
    for name, table in tables.items()
}

# -----------------------------------------------------
# Access filtered tables
# -----------------------------------------------------
filter_BSBS_DetailedTbl = filtered_tables["BSBS_DetailedTbl"]


# %% BSBS RRH KPIs
# apply the styling
target_cols = ["Pct_performsBRM_audit", "Pct_perform_CrtWasteMgt", "Pct_fntlIncinerator_cntr"]

# create a helper columns
for col in target_cols:
    bsbsKPI[f"{col}_val"]  = bsbsKPI[col].apply(extract_percent)

# Apply styling
styled_bsbsKPI = bsbsKPI.style

for col in target_cols:
    styled_bsbsKPI = styled_bsbsKPI.apply(
        lambda x, c=col: [col_rag1(v) for v in bsbsKPI[f"{c}_val"]],
        subset=[col],
        axis=0
    )
    
# Clean up: Hide all helper columns and display
helper_cols = [f"{col}_val" for col in target_cols]
styled_bsbs = styled_bsbsKPI.hide(helper_cols, axis="columns")

# Diplay the table

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        BSBS Status by RRH Region
    </h2>
    """, 
    unsafe_allow_html=True
)


# Show all columns EXCEPT "percent_value"
visible_columns = ["RRH", "Pct_performsBRM_audit", "Pct_perform_CrtWasteMgt", "Pct_fntlIncinerator_cntr"]

st.dataframe(
    styled_bsbs,
    column_order=visible_columns, 
    use_container_width=True,
    hide_index=True
)

# %% The detailed table
filtered_bsbsDetail   =  filter_BSBS_DetailedTbl

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        Health Facility Line list with BSBS Detail
    </h2>
    """, 
    unsafe_allow_html=True
)


gb = GridOptionsBuilder().from_dataframe(filtered_bsbsDetail)

# Enable filtering
gb.configure_default_column(filter = True, sortable=True)

# Freeze RRH column
gb.configure_column("RRH", pinned="left")

# Wrap long column headers properly
gb.configure_column(
    "BRM_assessments",
    headerName="Lab performing BRM assessments",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

gb.configure_column(
    "Correct_wasteMgr",
    headerName="Lab performing correct waste management",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

gb.configure_column(
    "Functional_incinarator_contractor",
    headerName="Lab with functional incinerator",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

# Configure default column behavior
gb.configure_default_column(
    wrapText=True,              # Enable text wrapping
    autoHeight=True,            # Adjust row height to fit wrapped text
    cellStyle={
        'font-size': '12px',
        'line-height': '14px',  # Forces lines closer together (try 1.0 or 1.2 as well)
        'padding-top': '2px',   # Optional: reduces space at the top of the cell
        'padding-bottom': '2px' # Optional: reduces space at the bottom of the cell
          } 
)

grid_options = gb.build()

# Display the grid and capture the response
grid_response = AgGrid(
    filtered_bsbsDetail,
    gridOptions=grid_options,
    # for downloading
    data_return_mode="FILTERED_AND_SORTED", 
    update_mode=GridUpdateMode.MODEL_CHANGED,
    fit_columns_on_grid_load=True,
    theme='alpine'
)

# Add the Download Button
# Extract the data currently shown in the grid (post-filter/sort)
df_to_download = grid_response['data']

st.download_button(
    label="📥 Download Table",
    data=df_to_download.to_csv(index=False).encode('utf-8'),
    file_name='bsbs_report.csv',
    mime='text/csv'
)


