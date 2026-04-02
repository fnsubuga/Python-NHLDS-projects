# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:13:23 2026

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
    page_title="ICT",
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
st.markdown('<div class="sticky-header">ICT<b> </div>', unsafe_allow_html=True)

# Content spacing
st.markdown('<div class="content">', unsafe_allow_html=True)


# %% Load the data frames

# ICT RRH KPIs
file_path30 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/all_ict_status.xls"
ictkpis  =  pd.read_excel(file_path30)

# ICT Health Facility Detail
file_path31 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/ict_detail.xls"
ictDetails  =  pd.read_excel(file_path31)

# %% Common filter
# -----------------------------------------------------
# Sidebar Filter for all tables
# -----------------------------------------------------
# Apply the filter for all table

# Define Hub Name
RRH_list = sorted(ictkpis["RRH"].dropna().unique().tolist())


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
    "ict_KPIs": ictkpis,
    "ictdetails": ictDetails
        }

filtered_tables = {
    name: filter_by_rrh(table, selected_RRH)
    for name, table in tables.items()
}

# -----------------------------------------------------
# Access filtered tables
# -----------------------------------------------------
filter_ict_KPIs = filtered_tables["ict_KPIs"]
filter_ictdetails = filtered_tables["ictdetails"]

# %% ICT RRH KPIs

filter_ict_KPIs  =  filter_ict_KPIs.rename(columns = {
    "% Functional": "Pct_functional",
    "% non-functional": "Pct_nonFunctional",
    "% partially funtional": "Pct_partial"
        })

filtered_ict_KPIs  =  filter_ict_KPIs

# apply the styling
target_cols = ["Pct_functional"]

# create a helper columns
for col in target_cols:
    filtered_ict_KPIs[f"{col}_val"]  = filtered_ict_KPIs[col].apply(extract_percent)

# Apply styling
styled_filtered_ict_KPIs = filtered_ict_KPIs.style

for col in target_cols:
    styled_filtered_ict_KPIs = styled_filtered_ict_KPIs.apply(
        lambda x, c=col: [col_rag1(v) for v in filter_ict_KPIs[f"{c}_val"]],
        subset=[col],
        axis=0
    )
    
# Clean up: Hide all helper columns and display
helper_cols = [f"{col}_val" for col in target_cols]
styled_filtered_ict_KPIs = styled_filtered_ict_KPIs.hide(helper_cols, axis="columns")

# Diplay the table

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        ICT Status by RRH Region
    </h2>
    """, 
    unsafe_allow_html=True
)


# Show all columns EXCEPT "percent_value"
visible_columns = ["RRH", "Pct_functional", "Pct_nonFunctional", "Pct_partial"]

st.dataframe(
    styled_filtered_ict_KPIs,
    column_order=visible_columns, 
    use_container_width=True,
    hide_index=True
)

# %% The detailed table
filtered_ictdetails   =  filter_ictdetails

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        Health Facility Line list with ICT Detail
    </h2>
    """, 
    unsafe_allow_html=True
)

# Making a copy of the data frame
df_for_grid = filtered_ictdetails.copy()

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
target_cols = ["The facility possesses a functional lab e-LIMS (ALIS) - with the required infrastructure, computer, internet bundles, Power Back up", 
               "The facility has fully transferred to electronic data management, using e-LIMS for among others, monthly, and quarterly HMIS reporting", 
               "If the facility is an EMR site, the facility is implementing Health Information Exchange (HIE) - VL request and results made and returned to EMR sites, respectively", 
               "Timely (at least once a week if not automated), automated data connectivity implemented" 
               ]
for col in target_cols:
    gb.configure_column(col, cellStyle=color_jscode)

# Column Headers & Pining
gb.configure_column("RRH", pinned="left")

gb.configure_column("The facility possesses a functional lab e-LIMS (ALIS) - with the required infrastructure, computer, internet bundles, Power Back up", headerName="The facility possesses a functional lab e-LIMS (ALIS)", wrapHeaderText=True, autoHeaderHeight=True)
gb.configure_column("The facility has fully transferred to electronic data management, using e-LIMS for among others, monthly, and quarterly HMIS reporting", headerName="The facility has fully transferred to electronic data management", wrapHeaderText=True, autoHeaderHeight=True)
gb.configure_column("If the facility is an EMR site, the facility is implementing Health Information Exchange (HIE) - VL request and results made and returned to EMR sites, respectively", headerName="The facility has functional EMRs", wrapHeaderText=True, autoHeaderHeight=True)
gb.configure_column("Timely (at least once a week if not automated), automated data connectivity implemented", headerName="The facility has automated connectivity", wrapHeaderText=True, autoHeaderHeight=True)

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
    file_name='ict_report.csv',
    mime='text/csv'
)




