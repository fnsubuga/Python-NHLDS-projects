# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 10:12:30 2026

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
    page_title="QMS",
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
st.markdown('<div class="sticky-header">Quality Management Systems (QMS)<b> </div>', unsafe_allow_html=True)

# Content spacing
st.markdown('<div class="content">', unsafe_allow_html=True)


# %% Load the data frames
# -----------------------------------------------------
# Load the RRH-Hub Spokes Data
# -----------------------------------------------------

# Summary of KPI indicators

file_path13 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/QMS_KPIs_RRH.xls"
qms = pd.read_excel(file_path13)

# QMS Detailed Table
file_path14 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/QMS_details_RRH.xls"
QMSDetail = pd.read_excel(file_path14)

# %age of sites with major tests enrolled onto EQA scheme
file_path15 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/MajorTests_onEQA.xls"
TestsEQA  =  pd.read_excel(file_path15)

# Tests without EQA Schemes
file_path15 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/testNotonEQA.xls"
NotestEQA  =  pd.read_excel(file_path15)

# Tests without EQA Schemes by RRH
file_path15 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/testNotonEQA_RRH.xls"
NotestEQArrh  =  pd.read_excel(file_path15)


# %% Common filter

# Sidebar Filter for all tables

# Apply the filter for all table

# Define Hub Name
RRH_list = sorted(QMSDetail["RRH"].dropna().unique().tolist())


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
    "QMS_DetailedTbl": QMSDetail,
    "RRH_EQAScheme":  NotestEQArrh 
        }

filtered_tables = {
    name: filter_by_rrh(table, selected_RRH)
    for name, table in tables.items()
}

# -----------------------------------------------------
# Access filtered tables
# -----------------------------------------------------
filter_QMS_DetailedTbl = filtered_tables["QMS_DetailedTbl"]
filter_RRH_EQAScheme = filtered_tables["RRH_EQAScheme"]


# %% QMS status by RRH
# apply the styling
target_cols = ["Pct_enrolled", "Pct_QMSAudited", "Pct_ImproveScore"]

# create a helper columns
for col in target_cols:
    qms[f"{col}_val"]  = qms[col].apply(extract_percent)

# Apply styling
styled_qms = qms.style

for col in target_cols:
    styled_qms = styled_qms.apply(
        lambda x, c=col: [col_rag1(v) for v in qms[f"{c}_val"]],
        subset=[col],
        axis=0
    )
    
# Clean up: Hide all helper columns and display
helper_cols = [f"{col}_val" for col in target_cols]
styled_qms = styled_qms.hide(helper_cols, axis="columns")

# Diplay the table

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        Proportion of non - accredited labs enrolled into QMS program, by RRH Region
    </h2>
    """, 
    unsafe_allow_html=True
)


# Show all columns EXCEPT "percent_value"
visible_columns = ["RRH", "Pct_enrolled", "Pct_QMSAudited", "Pct_ImproveScore"]

st.dataframe(
    styled_qms,
    column_order=visible_columns, 
    use_container_width=True,
    hide_index=True
)

# %% The detailed table
filtered_QMSDetail   =  filter_QMS_DetailedTbl

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        Health Facility Line list with QMS Detail
    </h2>
    """, 
    unsafe_allow_html=True
)


gb = GridOptionsBuilder().from_dataframe(filtered_QMSDetail)

# Enable filtering
gb.configure_default_column(filter = True, sortable=True)

# Freeze RRH column
gb.configure_column("RRH", pinned="left")

# Wrap long column headers properly
gb.configure_column(
    "Lab is enrolled onto a QMS Program",
    headerName="Lab is enrolled onto a QMS Program",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

gb.configure_column(
    "Lab is audited at least one in the 12 months preceding this Supervision Visit",
    headerName="Lab is audited at least one in the last 12 months",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

gb.configure_column(
    "Lab registered improving audit scores between succesive QMS Audits",
    headerName="Lab registered improving audit scores between succesive QMS Audits",
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
    filtered_QMSDetail,
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
    file_name='QMS_report.csv',
    mime='text/csv'
)


# %% %age of sites with major tests enrolled onto EQA scheme

st.header("External Quality Assessment", divider="rainbow")

# apply the styling

col_name = "Pct_EQASites"

# create a helper column
TestsEQA["percent_value"]  = TestsEQA[col_name].apply(extract_percent)

# Apply styling
styled_TestsEQA = (
    TestsEQA.style
    .apply(
        lambda x: [col_rag1(v) for v in TestsEQA["percent_value"]],
        subset=[col_name],
        axis=0  # Explicitly apply along the index (rows)
    )
    .hide(["percent_value"], axis="columns")
)

 # Diplay the table

st.markdown(
     """
     <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
         Proportion of sites whose major tests are enrolled onto EQA Scheme, by RRH Region
     </h2>
     """, 
     unsafe_allow_html=True
 )



# Show all columns EXCEPT "percent_value"
visible_columns = [col for col in TestsEQA.columns if col != "percent_value"]

st.dataframe(
     styled_TestsEQA,
     column_order=visible_columns,
     use_container_width=True,
     hide_index=True
 )

# %% National: Tests not on EQA schemes

# rename columns
NotestEQA  =  NotestEQA.rename(columns = {
    "Tests Not enrolled onto an EQA Scheme": "NotEnrolled",
    "No.sites_withoutEQA":  "No_sites_withoutEQA"
    })

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        Major tests not enrolled onto National EQA Schemes (National)
    </h2>
    """, 
    unsafe_allow_html=True
)

# sort values
NotestEQA = NotestEQA.sort_values(
        by="No_sites_withoutEQA",
        ascending=False
    )

# create the graph
chart = alt.Chart(NotestEQA).mark_bar().encode(
    y=alt.Y(
    "NotEnrolled:N",
    sort="-x",
    axis=alt.Axis(
    labelLimit=300,   # prevents truncation
    labelFontSize=11  # slightly smaller text
            )
        ),
    x=alt.X(
    "No_sites_withoutEQA:Q",
    axis=alt.Axis(
    format="d"  # removes decimals
    ),
    title="Sites with Tests not enrolled onto an EQA Scheme"
        ),
        tooltip=["NotEnrolled", "No_sites_withoutEQA"]
    )

# display
st.altair_chart(chart, use_container_width=True)

# %% Tests not enrolled onto EQA by RRH

filtered_NotestEQArrh   =  filter_RRH_EQAScheme

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        Health Facility Line list whose major tests are not enrolled onto an EQA Scheme
    </h2>
    """, 
    unsafe_allow_html=True
)


gb = GridOptionsBuilder().from_dataframe(filtered_NotestEQArrh)

# Enable filtering
gb.configure_default_column(filter = True, sortable=True)

# Freeze RRH column
gb.configure_column("RRH", pinned="left")

# Wrap long column headers properly
gb.configure_column(
    "If not, indicate the number and list the tests not enrolled EQA",
    headerName="Major Test Without EQA Scheme",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

gb.configure_column(
    "No.sites_withoutEQA",
    headerName="No.sites_withoutEQA",
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
    filtered_NotestEQArrh,
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
    file_name='EQA_report.csv',
    mime='text/csv'
)