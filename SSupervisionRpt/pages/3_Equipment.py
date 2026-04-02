# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:36:57 2026

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
    page_title="Equipment",
    page_icon="D:/CPHL-MOH/pics/MoH_logo.png",
    layout="wide"
)

# %% Functions
# extract value from mixed cell, e.g. 45% (2/5)

def extract_percent(x):
    if pd.isna(x) or x == "":
        return np.nan
    return float(x.split("%")[0])

# Color coding
def col_rag(val):
    if pd.isna(val):
        return ""
    elif val < 50:
        return "color:green; font-weight: bold;"
    elif val < 80:
        return "color:#BA8E23; font-weight: bold;"
    else:
        return "color: red; font-weight: bold;"

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
st.markdown('<div class="sticky-header">Equipment Functionality<b> </div>', unsafe_allow_html=True)

# Content spacing
st.markdown('<div class="content">', unsafe_allow_html=True)


# %% Load the data frames
# -----------------------------------------------------
# Load the RRH-Hub Spokes Data
# -----------------------------------------------------

# Summary of proportions of sites with non-functional equipt, with long donwntime TAT

file_path7 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/EquipNonFntl_LongDowntime.xls"
equip = pd.read_excel(file_path7)

# %age of sites with Equipment not serviced as scheduled
file_path8 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/sites_Equip_nonServd_Scheduled.xls"
sche_ser = pd.read_excel(file_path8)

# list of equipment categories not serviced as scheduled
file_path9  =  "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/list_Equip_non_serviced.xls"
equipsche  = pd.read_excel(file_path9)

# List of equipment categories not sericed as scheduled by RRH
file_path10  = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/RRHlist_Equip_non_serviced.xls"
rrhEquipSer =  pd.read_excel(file_path10)

# Detailed equipment table
file_path11  = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/equipment_detail.xls"
equip_detail =  pd.read_excel(file_path11)

# list of equipment with prplonged downtime
file_path12  = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/equipment_wc_long_downtime.xls"
longdtime =  pd.read_excel(file_path12)


# %% Common filter
# -----------------------------------------------------
# Sidebar Filter for all tables
# -----------------------------------------------------
# Apply the filter for all table

# Define Hub Name
RRH_list = sorted(rrhEquipSer["RRH"].dropna().unique().tolist())


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
    "Equipt_serviced": rrhEquipSer,
    "DetailedEquip": equip_detail
        }

filtered_tables = {
    name: filter_by_rrh(table, selected_RRH)
    for name, table in tables.items()
}

# -----------------------------------------------------
# Access filtered tables
# -----------------------------------------------------
filter_Equipt_serviced = filtered_tables["Equipt_serviced"]
filter_DetailedEquip = filtered_tables["DetailedEquip"]


# %% List of equipment categories not serviced as scheduled
# rename columns
equipsche = equipsche.rename(columns = {
    "No.sites_withunserviced": "No_sites_unserviced"
    })   


# %% List of equipment with prolonged downtime
# rename columns
longdtime = longdtime.rename(columns = {
    "No.sites_withLongDT": "No_sites_withLongDT",
    "Equipment Category with >30 Day downtime": "Equipment Category"
    })   

# %% Combine the graphs, side by side
graph1, graph2 = st.columns(2)

with graph1:
    st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        Most Common Equipment Categories unserviced as scheduled (National)
    </h2>
    """, 
    unsafe_allow_html=True
)

    # sort values
    equipsche = equipsche.sort_values(
        by="No_sites_unserviced",
        ascending=False
    )

    # create the graph
    chart = alt.Chart(equipsche).mark_bar().encode(
        y=alt.Y(
            "Equipment Category:N",
            sort="-x",
            axis=alt.Axis(
                labelLimit=300,   # prevents truncation
                labelFontSize=11  # slightly smaller text
            )
        ),
        x=alt.X(
            "No_sites_unserviced:Q",
            axis=alt.Axis(
                format="d"  # ✅ removes decimals
            ),
            title="Number of Sites with Unserviced Equipment"
        ),
        tooltip=["Equipment Category", "No_sites_unserviced"]
    )

    # display
    st.altair_chart(chart, use_container_width=True)
    
with graph2:
 st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        Most Common Equipment Categories with long (>30day) equipment downtime (National)
    </h2>
    """, 
    unsafe_allow_html=True
)

# sort values
 longdtime = longdtime.sort_values(
        by="No_sites_withLongDT",
        ascending=False
    )

    # create the graph
 chart2 = alt.Chart(longdtime).mark_bar().encode(
        y=alt.Y(
            "Equipment Category:N",
            sort="-x",
            axis=alt.Axis(
                labelLimit=300,   # prevents truncation
                labelFontSize=11  # slightly smaller text
            )
        ),
        x=alt.X(
            "No_sites_withLongDT:Q",
            axis=alt.Axis(
                format="d"  # ✅ removes decimals
            ),
            title="Number of Sites with Equipment with long Downtime"
        ),
        tooltip=["Equipment Category", "No_sites_withLongDT"]
    )

    # display
 st.altair_chart(chart2, use_container_width=True)




# %% Summary of equipment status, %age sites with non functinal. or with long downtime

# Apply formatting 
styled_equip = (
    equip.style
        .format(precision=0, na_rep="")
)

# %% %age of facilities with equipment not serviced as scheduled RRH
# apply the styling

col_name = "Proportion of sites with equipment not serviced as scheduled"

# create a helper column
sche_ser["percent_value"]  = sche_ser[col_name].apply(extract_percent)

# Apply styling
styled_sche_ser = (
    sche_ser.style
    .apply(
        lambda x: [col_rag(v) for v in sche_ser["percent_value"]],
        subset=[col_name],
        axis=0  # Explicitly apply along the index (rows)
    )
    .hide(["percent_value"], axis="columns")
)

# %% Combine the table, side by side:  RRH Service and long downtime
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
            Proportion of sites with non-functional equipment, and equipment with long downtime, by RRH Region
        </h2>
        """, 
        unsafe_allow_html=True
    )

    st.dataframe(
         styled_equip,
         use_container_width=False,
         hide_index=True,
         column_config={
             "RRH": st.column_config.TextColumn("Cadre", width="medium"),
             "Prop_NonFnlEquip": st.column_config.TextColumn("Non Functional", width="medium"),
             "Prop_NoLongBDwn": st.column_config.TextColumn("Long Downtime", width="medium")
             }
    )

with col2:
    # Diplay the table

    st.markdown(
        """
        <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
            Proportion of labs with equipment not serviced as scheduled, by RRH Region
        </h2>
        """, 
        unsafe_allow_html=True
    )



    # Show all columns EXCEPT "percent_value"
    visible_columns = [col for col in sche_ser.columns if col != "percent_value"]

    st.dataframe(
        styled_sche_ser,
        column_order=visible_columns,
        use_container_width=True,
        hide_index=True
    )
   
# %% Most common equipment not serviced as scheduled by RRH
filtered_rrhEquipSer  =  filter_Equipt_serviced

# Apply formatting 
styled_rrhEquipSer = (
    filtered_rrhEquipSer.style
        .format(precision=0, na_rep="")
)

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        Most common equipment not serviced as scheduled by RRH Region
    </h2>
    """, 
    unsafe_allow_html=True
)

st.dataframe(
     styled_rrhEquipSer,
     use_container_width=False,
     hide_index=True,
     column_config={
         "RRH": st.column_config.TextColumn("RRH", width="medium"),
         
         }
)

# %% Equipment detailed table

filtered_equip_detail   =  filter_DetailedEquip

st.markdown(
    """
    <h2 style='font-size: 14px; font-family: sans-serif; font-weight: bold;'>
        Health Facility Line list with Equipment Detail
    </h2>
    """, 
    unsafe_allow_html=True
)


gb = GridOptionsBuilder().from_dataframe(filtered_equip_detail)

# Enable filtering
gb.configure_default_column(filter = True, sortable=True)

# Freeze RRH column
gb.configure_column("RRH", pinned="left")

# Wrap long column headers properly
gb.configure_column(
    "The facility has non-functional equipment",
    headerName="The facility has non-functional equipment",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

gb.configure_column(
    "If Yes, the Number and List of Non-functional equipment",
    headerName="The Number and List of Non-functional equipment",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

gb.configure_column(
    "Facility has equipment not serviced as scheduled",
    headerName="Facility has equipment not serviced as scheduled",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

gb.configure_column(
    "If Yes, No. and List of equipment not be serviced as scheduled",
    headerName="No. and List of equipment not be serviced as scheduled",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

gb.configure_column(
    "Facility experienced prolonged equipment downtime (more than 30 days) in the 6 months preceding this visit",
    headerName="Equipment with long downtime",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

gb.configure_column(
    "Facility experienced prolonged equipment downtime (more than 30 days) in the 6 months preceding this visit",
    headerName="Facility has Equipment with long (>6 months) downtime",
    wrapHeaderText=True,
    autoHeaderHeight=True
)

gb.configure_column(
    "If Yes, no and List of equipment indicated to have prolonged equipment downtime",
    headerName="Equipment with long downtime (>6 Month)",
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
    filtered_equip_detail,
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
    file_name='equipment_report.csv',
    mime='text/csv'
)
