import os
import streamlit as st
import pandas as pd
from datetime import datetime
from snowflake_connector import fetch_data
from processor import *
from sidebar import sidebar

REMOTE_CSS_URL = "https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css"
# SQL query path
st.set_page_config(layout="wide")

def css():
    st.markdown(f'<link href="{REMOTE_CSS_URL}" rel="stylesheet">', unsafe_allow_html=True)
    try:
        with open("./app/style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        raise Exception("File not found", os.getcwd(), os.listdir())

def table_cards(df, view_details):

    table_scorecard = """
    <div class="ui five small statistics">
        <div class="grey statistic">
            <div class="value">"""+str(df[df['TABLE_TYPE'] == 'BASE TABLE']['TABLE_ID'].count())+"""
            </div>
            <div class="label">
                Tables
            </div>
        </div>
        <div class="grey statistic">
            <div class="value">"""+str(df[df['TABLE_TYPE'] == 'VIEW']['TABLE_ID'].count())+"""
            </div>
            <div class="label">
                Views
            </div>
        </div>
        <div class="grey statistic">
            <div class="value">"""+str(df[df['TABLE_TYPE'] == 'MATERIALIZED VIEW']['TABLE_ID'].count())+"""
            </div>
            <div class="label">
                Materialized Views
            </div>
        </div>
        <div class="grey statistic">
            <div class="value">
                """+human_format(df['ROW_COUNT'].sum())+"""
            </div>
            <div class="label">
                Rows
            </div>
        </div>
        <div class="grey statistic">
            <div class="value">
                """+human_bytes(df['BYTES'].sum())+" "+human_bytes_text(df['BYTES'].sum())+"""
            </div>
            <div class="label">
                Size
            </div>
        </div>
    </div>    
"""

    table_scorecard += """<br><br><br><div id="mydiv" class="ui centered cards">"""


    for index, row in df.iterrows():
        table_scorecard += """
<div class="card"">   
    <div class=" content """+header_bg(row['TABLE_TYPE'])+"""">
            <div class=" header smallheader">"""+row['TABLE_NAME']+"""</div>
<div class="meta smallheader">"""+row['TABLE_CATALOG']+"."+row['TABLE_SCHEMA']+"""</div>
</div>
<div class="content">
    <div class="description"><br>
        <div class="column kpi number">"""+human_format(row['ROW_COUNT'])+"""<br>
            <p class="kpi text">Rows</p>
        </div>
        <div class="column kpi number">"""+human_bytes(row['BYTES'])+"""<br>
            <p class="kpi text">"""+human_bytes_text(row['BYTES'])+"""</p>
        </div>
        <div class="column kpi number">"""+"{0:}".format(row['COLUMN_COUNT'])+"""<br>
            <p class="kpi text">Columns</b>
        </div>
    </div>
</div>
<div class="extra content">
    <div class="meta"><i class="table icon"></i> Table Type: """+(row['TABLE_TYPE'])+"""</div>
    <div class="meta"><i class="user icon"></i> Owner: """+str(row['TABLE_OWNER'])+""" </div>
    <div class="meta"><i class="calendar alternate outline icon"></i> Created On:
        """+str(pd.to_datetime(row['CREATED'], dayfirst=True, format='mixed').date())+"""</div>
</div>
<div class="extra content" """+view_details+""">
    <div class="meta"><i class="history icon"></i> Time Travel: """+str((row['RETENTION_TIME'])).strip(".0")+"""</div>
    <div class="meta"><i class="edit icon"></i> Last Altered: """+str(pd.to_datetime(row['LAST_ALTERED'], dayfirst=True, format='mixed').date())+"""</div>
    <div class="meta"><i class="calendar times outline icon"></i> Transient: """+str(row['IS_TRANSIENT'])+""" </div>
    <div class="meta"><i class="th icon"></i> Auto Clustering: """+str(row['AUTO_CLUSTERING_ON'])+""" </div>
    <div class="meta"><i class="key icon"></i> Clustering Key: """+str(row['IS_TRANSIENT'])+""" </div>
    <div class="meta"><i class="comment alternate outline icon"></i> Comment: """+str(row['IS_TRANSIENT'])+""" </div>
</div>
</div>
        """

    st.markdown(table_scorecard, unsafe_allow_html=True)

# using dayfirst is not efficient, build process to fix data at csv source
def main():
    # st.title("MetaFlake View")
    st.markdown("<h1 style='text-align: center; '>MetaFlake View</h1>", unsafe_allow_html=True)

    css()
    # Fetch data from Snowflake
    data = None
    try: 
        data = fetch_data()
    except:
        print('snowflake inaccessible')

    df = pd.read_csv('./app/data/metadata.csv') if not data else data

    df_final, view_details = sidebar(df)

    table_cards(df_final, view_details)
    

if __name__ == "__main__":
    main()
