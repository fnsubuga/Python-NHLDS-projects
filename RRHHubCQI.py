# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 10:33:46 2025

@author: HP
"""
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder

# -----------------------------------------------------
# Streamlit Page Config
# -----------------------------------------------------
st.set_page_config(
    page_title="RRH Sample Movement Dashboard",
    page_icon="D:/CPHL-MOH/pics/MoH_logo.png",
    layout="wide"
)

# %% Inject the stick dashboard 
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
st.markdown('<div class="sticky-header">NHLDS M&E CQI support to RRH Hubs </div>', unsafe_allow_html=True)

# Content spacing
st.markdown('<div class="content">', unsafe_allow_html=True)

# %% Load the data frames
# -----------------------------------------------------
# Load the RRH-Hub Spokes Data
# -----------------------------------------------------
file_path = "D:/CPHL-MOH/Running Grants/coag/CoAg2025_26/CQI/CQI/Regionalization/NSRTN/Datasets/sample tracking/dashboard data/HubTAT_Quarterly.xls"
df = pd.read_excel(file_path)

#  RRH Hub TAT by Month

file_path7 = "D:/CPHL-MOH/Running Grants/coag/CoAg2025_26/CQI/CQI/Regionalization/NSRTN/Datasets/sample tracking/dashboard data/TATbyHub_monthly.xls"
df7 = pd.read_excel(file_path7)

# Health Faciilty line list
file_path1 = "D:/CPHL-MOH/Running Grants/coag/CoAg2025_26/CQI/CQI/Regionalization/NSRTN/Datasets/sample tracking/dashboard data/TATbyHFac_Quarterly.xls"
df1 = pd.read_excel(file_path1)


# %% Functions
# -----------------------------------------------------
# Define color function
# -----------------------------------------------------
def color_scale(val):
    if pd.isna(val):
        return "background-color: #E0E0E0; color: #555555;"  # grey NDA
    # Convert anything else to number safely
    num = pd.to_numeric(val, errors="coerce")
    if pd.isna(num):
        return ""  # no style if still not numeric
    
    elif 0 <= val <= 2:
        return "background-color: #2E8B57; color: white;"
    elif val == 3:
        return "background-color: #66CC66; color: white;"
    elif val == 4:
        return "background-color: #FFFF00; color: black;"
    elif val > 4:
        return "background-color: #8B0000; color: red;"
    else:
        return ""



# %% Common filter
# -----------------------------------------------------
# Sidebar Filter for all tables
# -----------------------------------------------------
# Apply the filter for all table

# Define Hub Name
HName_list = sorted(df["HName"].dropna().unique().tolist())


with st.sidebar:
    st.header("Filter Hub", divider=True)

    selected_HName = st.selectbox(
        "HName:",
        options=["All"] + HName_list,
        index=0,
        key="select_hname_rrh"
    )

# -----------------------------------------------------
# Reusable filter function (SAFE)
# -----------------------------------------------------
def filter_by_hub(dataframe, selected_hub):
    # Check column exists to avoid crashing
    if "HName" not in dataframe.columns:
        return dataframe.copy()
    
    if selected_hub == "All":
        return dataframe.copy()
    else:
        return dataframe[dataframe["HName"] == selected_hub].copy()

# -----------------------------------------------------
# Apply filter to ALL tables
# -----------------------------------------------------
tables = {
    "HubQtrlyTAT": df,
    "HubMonthlyTAT": df7,
    "HFacMonthlyTAT": df1
}

filtered_tables = {
    name: filter_by_hub(table, selected_HName)
    for name, table in tables.items()
}

# -----------------------------------------------------
# Access filtered tables
# -----------------------------------------------------
filter_HubQtrlyTAT = filtered_tables["HubQtrlyTAT"]
filter_HubMonthlyTAT = filtered_tables["HubMonthlyTAT"]
filter_HFacMonthlyTAT = filtered_tables["HFacMonthlyTAT"]



# %% RRH Hub Quarterly TAT Analysis

# -----------------------------------------------------
# Load the RRH-Hub Spokes Data
# -----------------------------------------------------
file_path = "D:/CPHL-MOH/Running Grants/coag/CoAg2025_26/CQI/CQI/Regionalization/NSRTN/Datasets/sample tracking/dashboard data/HubTAT_Quarterly.xls"
df = pd.read_excel(file_path)

# -----------------------------------------------------
# Sidebar Filters — RRH Level
# -----------------------------------------------------
# List the RRH / Hub names
HName_list = df["HName"].dropna().unique().tolist()

with st.sidebar:
    st.header("Filter Hub (TAT)", divider=True)

    selected_HName = st.selectbox(
        "HName:",
        options=["All"] + HName_list,
        index=0,
        key="select_hname_rrh"   
    )

# Apply filter
if selected_HName == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["HName"] == selected_HName].copy()

# -----------------------------------------------------
# Apply color formatting 
# -----------------------------------------------------

# -----------------------------------------------------
# Columns to color
# -----------------------------------------------------
cols_to_color = ["Oct-Dec", "Jan-Mar"]

styled_filtered_df = (
    filtered_df.style
        .format(precision=0, na_rep="")
        .map(color_scale, subset=cols_to_color)
)

# %% RRH Hub TAT by Month

file_path7 = "D:/CPHL-MOH/Running Grants/coag/CoAg2025_26/CQI/CQI/Regionalization/NSRTN/Datasets/sample tracking/dashboard data/TATbyHub_monthly.xls"
df7 = pd.read_excel(file_path7)

# -----------------------------------------------------
# Columns to color
# -----------------------------------------------------
month_cols_to_color = ["Oct","Nov", "Dec", "Jan", "Feb"]

# -----------------------------------------------------
# Sidebar Filters — RRH Level
# -----------------------------------------------------
# List the RRH / Hub names
HName_list7 = df7["HName"].dropna().unique().tolist()

with st.sidebar:
    st.header("Filter Hub (Monthly TAT)", divider=True)

    selected_HName7 = st.selectbox(
        "HName:",
        options=["All"] + HName_list7,
        index=0,
        key="select_hname_rrh11"   
    )

# Apply filter
if selected_HName7 == "All":
    filtered_df7 = df7.copy()
else:
    filtered_df7 = df7[df7["HName"] == selected_HName7].copy()

# -----------------------------------------------------
# Apply color formatting *after filtering*
# -----------------------------------------------------
styled_filtered_df7 = (
    filtered_df7.style
        .format(precision=0, na_rep="")
        .map(color_scale, subset=month_cols_to_color)
)

   
# %% Combine the table, side by side
col1, col2 = st.columns(2)


styled_filtered_df
with col1:
    st.subheader("Sample Delivery TAT")
    st.dataframe(
        styled_filtered_df,
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("RRH Hub Monthly TAT")
    st.dataframe(
        styled_filtered_df7,
        use_container_width=True,
        hide_index=True,
        column_config={
            "HName": st.column_config.TextColumn(width="small"),
            "Oct": st.column_config.NumberColumn(width="small"),
            "Nov": st.column_config.NumberColumn(width="small"),
            "Dec": st.column_config.NumberColumn(width="small"),
            "Jan": st.column_config.NumberColumn(width="small"),
            "Feb": st.column_config.NumberColumn(width="small")
        },
    )

# %% Percentage sample tracked informing TAT (Regional Hub) 
# ------------------------------------------------------------------------------------
# %age of samples informing the TAT analysis 
# ------------------------------------------------------------------------------------
file_path2 = "D:/CPHL-MOH/Running Grants/coag/CoAg2025_26/CQI/CQI/Regionalization/NSRTN/Datasets/sample tracking/dashboard data/PCtinformingTAT_Hub_Quarterly.xls"
df3 = pd.read_excel(file_path2)


# -----------------------------------------------------
# Side Bar
# -----------------------------------------------------
HName_options = ["All"] + sorted(df3["HName"].dropna().unique().tolist())

with st.sidebar:
    st.header("Filter Hub (%age Samples with TAT)", divider=True)

    selected_HName3 = st.selectbox(
        "HName:",
        options=HName_options,
        index=0,
        key="select_hname_rrh2"
    )

# -----------------------------------------------------
# Filter
# -----------------------------------------------------
if selected_HName3 == "All":
    filtered_df3 = df3.copy()
else:
    filtered_df3 = df3.loc[df3["HName"] == selected_HName3].copy()

# -----------------------------------------------------
# Rename the columns
# -----------------------------------------------------
df3_ordered = filtered_df3[["HName", "Oct-Dec.x", "Jan-Mar.x", "PctOctDec", "PctJanMar"]].copy()

# rename
df3_named = df3_ordered.rename(columns={
    "HName": "RRH Hub",
    "Oct-Dec.x": "No.SamplesOct_Dec",
    "Jan-Mar.x": "No.SamplesJan_Mar"
})


# -----------------------------------------------------
# Display table
# -----------------------------------------------------
st.header("%age Samples with TAT")

st.data_editor(
    df3_named,
    use_container_width=False,
    hide_index=True,
    column_config={
        "RRH Hub": st.column_config.TextColumn(width="small"),
        "Oct–Dec": st.column_config.NumberColumn(width="small"),
        "Jan–Mar": st.column_config.NumberColumn(width="small"),
        
        "PctOctDec":  st.column_config.NumberColumn(width="small"),
        "PctJanMar":  st.column_config.NumberColumn(width="small") 
    },
)


# %% HFacility Quarterly TAT
# ---------------------------------------------------------------------
# Health Faciilty line list
# -------------------------------------------------------------------------
file_path1 = "D:/CPHL-MOH/Running Grants/coag/CoAg2025_26/CQI/CQI/Regionalization/NSRTN/Datasets/sample tracking/dashboard data/TATbyHFac_Quarterly.xls"
df1 = pd.read_excel(file_path1)

# ----------------------------------------------------------------------------------------------
# Side bar for facility level 
# ----------------------------------------------------------------------------------------------
HName_fac  =  ["All"] + sorted(df1["HName"].dropna().unique().tolist())

with st.sidebar:
    st.header("Hub Filter(Facility TAT)", divider = True)
    
    selected_HName1  = st.selectbox(
        "HName:",
        options= HName_fac,
        index=0,
        key="select_hname_facilities1"   # ✅ unique key fixes DuplicateElementId
        )
    
# Apply filter 
if selected_HName1 == "All":
    filtered_df1 = df1.copy()
else:
    filtered_df1 = df1.loc[df1["HName"] == selected_HName1].copy()
# -----------------------------------------------------
# Apply color formatting *after filtering*
# -----------------------------------------------------
def format_tbl(df1):
    styled = (
        df1.style
          .map(color_scale, subset=cols_to_color)   # colors handle NA
          .format(na_rep="")                     # display NA as NDA
    )
    return styled

# -----------------------------------------------------
# Display RRH-Level Table
# -----------------------------------------------------
st.header("Health Facility Quarterly TAT")
styled_filtered_df1 = format_tbl(filtered_df1)


styled_filtered_df1 = (
    filtered_df1.style
        .format(precision=0, na_rep="")
        .map(color_scale, subset=cols_to_color)
)

st.data_editor(
    styled_filtered_df1,
    use_container_width=True,
    disabled=True,
    key="tbl_health_facility_tat",
    column_config={
        "HName": st.column_config.TextColumn(width="small"),
        "HFacility": st.column_config.TextColumn(width="small"),
        "Oct-Dec": st.column_config.NumberColumn(width="small"),
        "Jan-Mar": st.column_config.NumberColumn(width="small"),
    },
)

# %% Health facility monthly TAT

file_path8 = "D:/CPHL-MOH/Running Grants/coag/CoAg2025_26/CQI/CQI/Regionalization/NSRTN/Datasets/sample tracking/dashboard data/TATbyHFac_Monthly.xls"
df8 = pd.read_excel(file_path8)

# ----------------------------------------------------------------------------------------------
# Side bar for facility level 
# ----------------------------------------------------------------------------------------------
HName_fac8  =  ["All"] + sorted(df8["HName"].dropna().unique().tolist())

with st.sidebar:
    st.header("Hub Filter(Facility Monthly TAT)", divider = True)
    
    selected_HName8  = st.selectbox(
        "HName:",
        options= HName_fac8,
        index=0,
        key="select_hname_facilities8"   # ✅ unique key fixes DuplicateElementId
        )
    
# Apply filter 
if selected_HName8 == "All":
    filtered_df8 = df8.copy()
else:
    filtered_df8 = df8.loc[df8["HName"] == selected_HName8].copy()
# -----------------------------------------------------
# Apply color formatting *after filtering*
# -----------------------------------------------------
def format_tbl(df8):
    styled = (
        df8.style
          .map(color_scale, subset=month_cols_to_color)   # colors handle NA
          .format(na_rep="")                     # display NA as NDA
    )
    return styled

# -----------------------------------------------------
# Display RRH-Level Table
# -----------------------------------------------------
st.header("Health Facility Monthly TAT")
styled_filtered_df8 = format_tbl(filtered_df8)


styled_filtered_df8 = (
    filtered_df8.style
        .format(precision=0, na_rep="")
        .map(color_scale, subset=month_cols_to_color)
)

st.data_editor(
    styled_filtered_df8,
    use_container_width=True,
    disabled=True,
    key="tbl_health_facility_tat8",
    column_config={
        "HName": st.column_config.TextColumn(width="small"),
        "HFacility": st.column_config.TextColumn(width="small"),
        
        "Oct": st.column_config.NumberColumn(width="small"),
        "Nov": st.column_config.NumberColumn(width="small"),
        "Dec": st.column_config.NumberColumn(width="small"),
        "Jan": st.column_config.NumberColumn(width="small"),
        "Feb": st.column_config.NumberColumn(width="small")
    },
)

# %% HFacility Samples informing TAT by facility by month

file_path9 = "D:/CPHL-MOH/Running Grants/coag/CoAg2025_26/CQI/CQI/Regionalization/NSRTN/Datasets/sample tracking/dashboard data/HFac_SampleInformingTAT_Monthy.xls"
df9 = pd.read_excel(file_path9)


# -----------------------------------------------------
# Side Bar
# -----------------------------------------------------
HName_options = ["All"] + sorted(df9["HName"].dropna().unique().tolist())

with st.sidebar:
    st.header("Filter Facility (HFacility Sample Vols and Samples Tracked)", divider=True)

    selected_HName9 = st.selectbox(
        "HName:",
        options=HName_options,
        index=0,
        key="select_hname_rrh9"
    )

# -----------------------------------------------------
# Filter
# -----------------------------------------------------
if selected_HName9 == "All":
    filtered_df9 = df9.copy()
else:
    filtered_df9 = df9.loc[df9["HName"] == selected_HName9].copy()

# -----------------------------------------------------
# Rename the columns
# -----------------------------------------------------
df9_ordered = filtered_df9[["HName", "HFacility", "N_Oct", "N_Nov", "N_Dec", "N_Jan", "N_Feb",
                            "PctTracked_Oct", "PctTracked_Nov", "PctTracked_Dec",
                            "PctTracked_Jan", "PctTracked_Feb" ]].copy()



# -----------------------------------------------------
# Display table
# -----------------------------------------------------
st.header("HFacility Linelist: Sample Vols and Pct e-tracked by Month")

# the lists 
vol_cols = ["N_Oct", "N_Nov", "N_Dec", "N_Jan", "N_Feb"] 
pct_cols = ["PctTracked_Oct", "PctTracked_Nov", "PctTracked_Dec", "PctTracked_Jan", "PctTracked_Feb"] 


# create the table
vol_children = [ {"field": col, 
                  "width": 90, 
                  "type": ["numericColumn"]
                  } 
                for col in vol_cols ] 
pct_children = [ {
                "field": col, 
                "width": 90, 
                "type": ["numericColumn"]
                } 
                for col in pct_cols ] 

grid_options = { 
    "columnDefs": [ 
    { "headerName": "RRH Hub", 
     "field": "HName", 
     "pinned": "left", 
     "width": 130 
   }, 
    { 
     "headerName": "Health Facility", 
     "field": "HFacility", 
     "pinned": "left", 
     "width": 220 
     }, 
    { 
     "headerName": "Sample Volumes Collected", 
     "children": vol_children }, 
    
    { "headerName": "%age samples e-tracked", 
     "children": pct_children 
     }
    ], 
    
    "defaultColDef": { 
        "sortable": True, 
        "filter": True, 
        "resizable": True 
        } 
 } 
AgGrid( 
       df9_ordered, 
       gridOptions=grid_options, 
       height=450, 
       theme="streamlit" )

# %% %age picked, delivered and with date delivered
file_path5 = "D:/CPHL-MOH/Running Grants/coag/CoAg2025_26/CQI/NSRTN/data for python/Pctpikd.xls"
df5 = pd.read_excel(file_path5)

# ----------------------------------------------------------------------------------------------
# Side bar for facility level 
# ----------------------------------------------------------------------------------------------
HName_options2 = ["All"] + sorted(df5["HName"].dropna().unique().tolist())

with st.sidebar:
    st.header("Hub Filter (%age Samples picked,delivered, with collection date)", divider=True)

    selected_HName5 = st.selectbox(
        "HName:",
        options=HName_options2, 
        index=0,
        key="select_rrh_tracked"   # unique key fixes DuplicateElementId
        )

# Apply filter
filtered_df5 = df5.copy() if selected_HName5 == "All" else df5.loc[df5["HName"] == selected_HName5].copy()

#-------------------------------------------------------------------------------
# --- 1) Reorder using ORIGINAL column names (done BEFORE renaming) ---
desired_order_df5  = [
    "HName",
    "PctPickedOctDec", "PctPickedJanMar",
    "PctDeliveredOctDec", "PctDeliveredJanMar",
    "PctwDateColltedOctDec", "PctwDateColltedJanMar"
]
# Order the dataframe in the exact order
df5_ordered = filtered_df5[desired_order_df5].copy()

# - Column naming (R version of set column names)
rename_map2 = {
    "HName": "RRH Hub",
    
   "PctPickedOctDec": "Oct–Dec",
   "PctPickedJanMar": "Jan–Mar",

   "PctDeliveredOctDec": "Oct–Dec",
   "PctDeliveredJanMar": "Jan–Mar",

   "PctwDateColltedOctDec": "Oct–Dec",
   "PctwDateColltedJanMar": "Jan–Mar"
        }
# obtain updated data frame
df5_named = df5_ordered.rename(columns = rename_map2)

# - Create grouped headings
grouped_cols2 = pd.MultiIndex.from_tuples([
    ("RRH Hub","RRH Hub"),
   
    ("%Pick", "Oct–Dec"),
    ("%Pick", "Jan–Mar"),

    ("%Del", "Oct–Dec"),
    ("%Del", "Jan–Mar"),

    ("%DateColl", "Oct–Dec"),
    ("%DateColl", "Jan–Mar"),
])

# Ensure columns count mataches
if df5_named.shape[1] == len(grouped_cols2):
    df5_named.columns = grouped_cols2
else:
    st.warning(
        f"Column mismatch: data has {df5_named.shape[1]} cols but grouped header expects {len(grouped_cols2)}. "
        "Showing without grouped headers."
    )

# format the table
styler2 = (
    df5_named.style
        .format(precision=0, na_rep="")
        .set_properties(**{
            "text-align": "center"
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("text-align", "center"),
                    ("font-weight", "bold"),
                    ("white-space", "normal"),   # ✅ allow wrapping
                    ("word-wrap", "break-word"),
                ],
            },
            {
                "selector": "td",
                "props": [
                    ("text-align", "center"),
                    ("white-space", "normal"),
                ],
            },
        ])
)

# -----------------------------------------------------
# Display hFacility sample collected and proportions Table
# -----------------------------------------------------
st.header("%age of samples e-tracked at 1) Picking, 2) Delivery to Hub, and with Sample Collection Date")
st.caption(f"Filtered: {selected_HName5}")

st.data_editor(styler2, use_container_width=True, disabled=True)


# %% health facilty %age picked, deliverd and with date collected

file_path6 = "D:/CPHL-MOH/Running Grants/coag/CoAg2025_26/CQI/NSRTN/data for python/hfPropsPicked.xlsx"
df6 = pd.read_excel(file_path6)

# ----------------------------------------------------------------------------------------------
# Side bar for facility level 
# ----------------------------------------------------------------------------------------------
HName_options3 = ["All"] + sorted(df6["HName"].dropna().unique().tolist())

with st.sidebar:
    st.header("Hub Filter (%age Site Samples picked,delivered, with collection date)", divider=True)

    selected_HName6 = st.selectbox(
        "HName:",
        options=HName_options3, 
        index=0,
        key="select_hfacity_tracked"   # unique key fixes DuplicateElementId
        )

# Apply filter
filtered_df6 = df6.copy() if selected_HName6 == "All" else df6.loc[df6["HName"] == selected_HName6].copy()

#-------------------------------------------------------------------------------
# --- 1) Reorder using ORIGINAL column names (done BEFORE renaming) ---
desired_order_df6  = [
    "HName", "HFacility",
    "PctPickedOctDec", "PctPickedJanMar",
    "PctDeliveredOctDec", "PctDeliveredJanMar",
    "PctwDateColltedOctDec", "PctwDateColltedJanMar"
]
# Order the dataframe in the exact order
df6_ordered = filtered_df6[desired_order_df6].copy()

# - Column naming (R version of set column names)
rename_map3 = {
    "HName": "RRH Hub",
    "HFacility": "Health Facility",
    
   "PctPickedOctDec": "Oct–Dec",
   "PctPickedJanMar": "Jan–Mar",

   "PctDeliveredOctDec": "Oct–Dec",
   "PctDeliveredJanMar": "Jan–Mar",

   "PctwDateColltedOctDec": "Oct–Dec",
   "PctwDateColltedJanMar": "Jan–Mar"
        }
# obtain updated data frame
df6_named = df6_ordered.rename(columns = rename_map3)

# - Create grouped headings
grouped_cols3 = pd.MultiIndex.from_tuples([
    ("RRH Hub","RRH Hub"),
    ("Health Facility", "Health Facility"),
    
    ("%Pick", "Oct–Dec"),
    ("%Pick", "Jan–Mar"),

    ("%Del", "Oct–Dec"),
    ("%Del", "Jan–Mar"),

    ("%DateColl", "Oct–Dec"),
    ("%DateColl", "Jan–Mar"),
])

# Ensure columns count mataches
if df6_named.shape[1] == len(grouped_cols3):
    df6_named.columns = grouped_cols3
else:
    st.warning(
        f"Column mismatch: data has {df6_named.shape[1]} cols but grouped header expects {len(grouped_cols3)}. "
        "Showing without grouped headers."
    )

# format the table
styler3 = (
    df6_named.style
        .format(precision=0, na_rep="")
        .set_properties(**{
            "text-align": "center"
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("text-align", "center"),
                    ("font-weight", "bold"),
                    ("white-space", "normal"),   # ✅ allow wrapping
                    ("word-wrap", "break-word"),
                ],
            },
            {
                "selector": "td",
                "props": [
                    ("text-align", "center"),
                    ("white-space", "normal"),
                ],
            },
        ])
)

# -----------------------------------------------------
# Display hFacility sample collected and proportions Table
# -----------------------------------------------------
st.header("Site %age of samples e-tracked at 1) Picking, 2) Delivery to Hub, and with Sample Collection Date")
st.caption(f"Filtered: {selected_HName5}")

st.data_editor(styler3, use_container_width=True, disabled=True)
