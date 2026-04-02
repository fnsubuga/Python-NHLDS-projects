# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:22:28 2026

@author: HP
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder

# -----------------------------------------------------
# Streamlit Page Config
# -----------------------------------------------------
st.set_page_config(
    page_title="HR",
    page_icon="D:/CPHL-MOH/pics/MoH_logo.png",
    layout="wide"
)

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
st.markdown('<div class="sticky-header">Human Resources<b> </div>', unsafe_allow_html=True)

# Content spacing
st.markdown('<div class="content">', unsafe_allow_html=True)


# %% Load the data frames
# -----------------------------------------------------
# Load the RRH-Hub Spokes Data
# -----------------------------------------------------

# HR Available by Health Level

file_path2 = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/PctHRAvail_by_Level.xls"
HRLevel = pd.read_excel(file_path2)

# HR avaible by RRH Region

file_path3  =  "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/PctHRAvail_by_RRH.xls"
HRRgns  =  pd.read_excel(file_path3)

# Prop cadres unavailable by health level
file_path4  =  "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/Prop_cadres_unavailable.xls"
CadreAvail  =  pd.read_excel(file_path4)

# prop unvailable by RRH and health level
file_path5  =  "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/Prop_cadres_unavailable_RRH_lvl.xls"
CadreRRH_Lvl  =  pd.read_excel(file_path5)

# %% Common filter
# -----------------------------------------------------
# Sidebar Filter for all tables
# -----------------------------------------------------
# Apply the filter for all table

# Define Hub Name
RRH_list = sorted(CadreRRH_Lvl["RRH_Region"].dropna().unique().tolist())


with st.sidebar:
    st.header("Filter RRH Region", divider=True)

    selected_rrh = st.selectbox(
        "RRH_Region:",
        options=["All"] + RRH_list,
        index=0,
        key="select_hname_rrh"
    )

# -----------------------------------------------------
# Reusable filter function
# -----------------------------------------------------
def filter_by_rrh(dataframe, selected_rrh):
    # Check column exists to avoid crashing
    if "RRH_Region" not in dataframe.columns:
        return dataframe.copy()
    
    if selected_rrh == "All":
        return dataframe.copy()
    else:
        return dataframe[dataframe["RRH_Region"] == selected_rrh].copy()

# -----------------------------------------------------
# Apply filter to ALL tables
# -----------------------------------------------------
tables = {
    "Prop_CadresAvail_RRH": CadreRRH_Lvl
    
    }


filtered_tables = {
    name: filter_by_rrh(table, selected_rrh)
    for name, table in tables.items()
}

# -----------------------------------------------------
# Access filtered tables
# -----------------------------------------------------
filter_CadresAvail = filtered_tables["Prop_CadresAvail_RRH"]

# %% The HR Available

st.header("Proportion of health facilities with Recommended HR Available, by Level")

st.table(HRLevel)

# %% The HR by RRH (%age with cadres) % with inadequate cadres

st.header("%age of cadres available, Inadequate by RRH")

st.table(HRRgns)

# %% Proportion of cadres unavailable by health level

filtered_cadreAvail = filter_CadresAvail

# Apply color formatting 
styled_filtered_cadreAvail = (
    filtered_cadreAvail.style
        .format(precision=0, na_rep="")
)

st.header("Proportion of Cadres Unavailable by health level")


st.dataframe(
     styled_filtered_cadreAvail,
     use_container_width=False,
     hide_index=True,
     column_config={
         "Cadre": st.column_config.TextColumn("Cadre", width="medium"),
         "RRH": st.column_config.TextColumn("RRH", width="small"),
         "GH": st.column_config.TextColumn("GH", width="small"),
         "HCIV": st.column_config.TextColumn("HCIV", width="small"),
         "HCIII": st.column_config.TextColumn("HCIII", width="small")
         }
)






