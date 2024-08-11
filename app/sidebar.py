import pandas as pd
import streamlit as st

def sidebar(df):

    df_reset = df
    
    cb_view_details = st.sidebar.checkbox('View Details')

    view_details = "" if cb_view_details else """style="display: none;" """
    

    selectbox_orderby = st.sidebar.selectbox("Order By", ('A → Z', 'Z → A', 'Data Size ↓', 'Data Size ↑',
                                            'Rows ↓', 'Rows ↑', 'Date Created ↓', 'Date Created ↑', 'Date Altered ↓', 'Date Altered ↑'))
    

    all_option = pd.Series(['All'], index=[9999999])

    #TABLE_SCHEMA=TABLE_SCHEMA._append({'TABLE_SCHEMA':'All'},ignore_index = True)

    if 'selectbox_database_key' not in st.session_state:
        st.session_state.selectbox_database_key = 10
        st.session_state.selectbox_schema_key = 20
        st.session_state.selectbox_owner_key = 30
        st.session_state.selectbox_table_type_key = 40
        st.session_state.selectbox_max_rows_key = 50
        st.session_state.selectbox_data_size_key = 60

    # Table Catalog/Database
    fv_database = df['TABLE_CATALOG'].drop_duplicates()
    fv_database = fv_database._append(all_option, ignore_index=False)

    selectbox_database = st.sidebar.selectbox(
        'Database', fv_database, index=len(fv_database)-1, key=st.session_state.selectbox_database_key)

    if selectbox_database != 'All':
        df = df.loc[df['TABLE_CATALOG'] == selectbox_database]
    else:
        df = df.loc[df['TABLE_CATALOG'].isin(fv_database)]

    # Table Schema
    fv_table_schema = df['TABLE_SCHEMA'].drop_duplicates()
    fv_table_schema = fv_table_schema._append(all_option)

    selectbox_schema = st.sidebar.selectbox(
        "Table Schema", fv_table_schema, len(fv_table_schema)-1, key=st.session_state.selectbox_schema_key)

    if selectbox_schema != 'All':
        df = df.loc[df['TABLE_SCHEMA'] == selectbox_schema]
    else:
        df = df.loc[df['TABLE_SCHEMA'].isin(fv_table_schema)]

    # Table Owner
    fv_owner = df['TABLE_OWNER'].drop_duplicates()
    fv_owner = fv_owner._append(all_option)
    selectbox_owner = st.sidebar.selectbox(
        "Table Owner", fv_owner, len(fv_owner)-1, key=st.session_state.selectbox_owner_key)

    if selectbox_owner != 'All':
        df = df.loc[df['TABLE_OWNER'] == selectbox_owner]
    else:
        df = df.loc[df['TABLE_OWNER'].isin(fv_owner)]

    # Table Type
    fv_table_type = df['TABLE_TYPE'].drop_duplicates()
    selectbox_table_type = st.sidebar.multiselect(
        'Table Type', fv_table_type, fv_table_type, key=st.session_state.selectbox_table_type_key)

    if len(selectbox_table_type) > 0:
        df = df.loc[df['TABLE_TYPE'].isin(selectbox_table_type)]
    else:
        df = df.loc[df['TABLE_TYPE'].isin(fv_table_type)]

    # #!!! This part is disabled since sliders are causing performance issues with large datasets.!!!
    # # data size selection
    max_data_mb = int(df['BYTES'].max()/1048576)
    step_size = 1

    if max_data_mb>1000:
        step_size=10
    elif max_data_mb>1000000:
        step_size=100
    elif max_data_mb>1000000000:
        step_size=1000
    elif max_data_mb>1000000000000:
        step_size=10000      

    data_size = st.sidebar.slider(
        'Data Size (MB)', 0, max_data_mb+1, (0, max_data_mb+1), key=st.session_state.selectbox_data_size_key, step=step_size)
    df = df.loc[(df['BYTES'] >= data_size[0]*1048576) &
                (df['BYTES'] <= data_size[1]*1048576)]

    # rows selection
    max_rows = int(df['ROW_COUNT'].max())
    step_size = 10

    if max_rows>1000000:
        step_size=100
    elif max_rows>1000000000:
        step_size=1000
    elif max_rows>1000000000000:
        step_size=10000    

    data_rows = st.sidebar.slider('Number of Rows', 0, max_rows+1,
                                (0, max_rows+1), key=st.session_state.selectbox_max_rows_key, step=step_size)
    df = df.loc[(df['ROW_COUNT'] >= data_rows[0]) &
                (df['ROW_COUNT'] <= data_rows[1])]


    def reset_button():
        st.session_state.selectbox_database_key = st.session_state.selectbox_database_key+1
        st.session_state.selectbox_schema_key = st.session_state.selectbox_schema_key+1
        st.session_state.selectbox_owner_key = st.session_state.selectbox_owner_key+1
        st.session_state.selectbox_table_type_key = st.session_state.selectbox_table_type_key+1
        st.session_state.selectbox_max_rows_key = st.session_state.selectbox_max_rows_key+1
        st.session_state.selectbox_data_size_key = st.session_state.selectbox_data_size_key+1


    clear_button = st.sidebar.button(
        label='Clear Selections', on_click=reset_button)

    if clear_button:
        df = df_reset

    # Card order
    orderby_column = ''
    orderby_asc = True


    if selectbox_orderby == 'A → Z':
        orderby_column = 'TABLE_NAME'
        orderby_asc = True
    elif selectbox_orderby == 'Z → A':
        orderby_column = 'TABLE_NAME'
        orderby_asc = False
    elif selectbox_orderby == 'Data Size ↓':
        orderby_column = 'BYTES'
        orderby_asc = False
    elif selectbox_orderby == 'Data Size ↑':
        orderby_column = 'BYTES'
        orderby_asc = True
    elif selectbox_orderby == 'Rows ↓':
        orderby_column = 'ROW_COUNT'
        orderby_asc = False
    elif selectbox_orderby == 'Rows ↑':
        orderby_column = 'ROW_COUNT'
        orderby_asc = True
    elif selectbox_orderby == 'Date Created ↓':
        orderby_column = 'CREATED'
        orderby_asc = False
    elif selectbox_orderby == 'Date Created ↑':
        orderby_column = 'CREATED'
        orderby_asc = True
    elif selectbox_orderby == 'Date Altered ↓':
        orderby_column = 'LAST_ALTERED'
        orderby_asc = False
    elif selectbox_orderby == 'Date Altered ↑':
        orderby_column = 'LAST_ALTERED'
        orderby_asc = True


    df.sort_values(by=[orderby_column], inplace=True, ascending=orderby_asc)

    return df, view_details

def main():
    sidebar()

if __name__ == "__main__":
    main()