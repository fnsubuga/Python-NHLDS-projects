# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:36:25 2026

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
    page_title="Support Supervision Report",
    page_icon="D:/CPHL-MOH/pics/MoH_logo.png",
    layout="wide"
)

st.title("Support Supervision Report")



st.markdown("""
            The suppport supervision report 
    
            """
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
st.markdown('<div class="sticky-header">The suppport supervision report<b> </div>', unsafe_allow_html=True)

# Content spacing
st.markdown('<div class="content">', unsafe_allow_html=True)

# %% Total sites visited, and by RRH
# Load data frame

file_path = "D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/RRH_TotalSites_Visited.xls"
visits  = pd.read_excel(file_path)

st.header("Number of health labs visited")

st.table(visits)

# %% Summary of key performance indicators
# Load data frame
file_path1 = ("D:/Python/dashboard/dashboard/SupportSupervisionRpt/Data/Jan_March/KPI_Summary.xls")
KPIs  = pd.read_excel(file_path1)

# -----------------------------------------------------
# Apply color formatting *after filtering*
# -----------------------------------------------------
styled_KPIs = (
    KPIs.style
        .format(precision=0, na_rep="")
        )


# -----------------------------------------------------
# Styling functions
# -----------------------------------------------------
# Hightlight sections
def highlight_sections(row):
    """highlight the section headers"""
    
    if row["Indicator"] in ["HR", "Equipment", "QMS", "BSBS", "NSRTN", "M&E", "ICT", "MicroBiology", "Radiology"]:
        return["background-color: #E8F0FE; font-weight: bold; color: #1a237e"] * len(row)
    return[""] * len(row)

# color the performance
def highlight_performance(val):
    """Color performance column"""
    if pd.isna(val):
        return ""
    if val >= 80:
        return "background-color: #C8E6C9; color: #1B5E20; font-weight: bold"
    elif val >= 50:
        return "background-color: #FFF3CD; color: #856404"
    else:
        return "background-color: #F8D7DA; color: #721C24"
    
   
# -----------------------------------------------------
# Apply styling
# -----------------------------------------------------
styled_KPIs = (
    KPIs.style
        .format({
            "No.sites": "{:.0f}",
            "ReportedSites": "{:.0f}",
            "%age of sites": "{:.0f}"
        }, na_rep="")
        
        # Section highlighting
        .apply(highlight_sections, axis=1)

        # Conditional formatting for performance
        .map(highlight_performance, subset=["%age of sites"])
        
 # Alignments
        .set_properties(subset=["No.sites", "ReportedSites", "%age of sites"],
                        **{"text-align": "center"})
        
        .set_properties(subset=["Indicator"],
                        **{"text-align": "left"})
        
        # Table styles
        .set_table_styles([
            {"selector": "th",
             "props": [("background-color", "#0B3D91"),
                       ("color", "white"),
                       ("font-weight", "bold"),
                       ("text-align", "center")]},
            {"selector": "td",
             "props": [("padding", "6px")]},

            {"selector": "tr:nth-child(even)",
             "props": [("background-color", "#f9f9f9")]},
        ])
)

# -----------------------------------------------------
# Display
# -----------------------------------------------------
st.header("📊 KPI Summary Table")

st.dataframe(
    styled_KPIs,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Indicator": st.column_config.TextColumn(width="large"),
        "No.sites": st.column_config.NumberColumn(width="small"),
        "ReportedSites": st.column_config.NumberColumn(width="small"),
        "%age of sites": st.column_config.NumberColumn(width="small"),
    },
)
