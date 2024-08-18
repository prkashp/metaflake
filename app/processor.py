import pandas as pd

def human_bytes(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B, '')
    elif KB <= B < MB:
        return '{0:.2f}'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f}'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f}'.format(B / GB)
    elif TB <= B:
        return '{0:.2f}'.format(B / TB)

def human_bytes_text(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return 'Bytes'
    elif KB <= B < MB:
        return 'KB'
    elif MB <= B < GB:
        return 'MB'
    elif GB <= B < TB:
        return 'GB'
    elif TB <= B:
        return 'TB'

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return ('%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])).replace('.00', '')

def header_bg(table_type):
    if table_type == "BASE TABLE":
        return "tablebackground"
    elif table_type == "VIEW":
        return "viewbackground"
    else:
        return "mvbackground"

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function returns different series after appending an element "All"
    """
    # adding Select all option 
    select_all = pd.Series(["All"], index=[9999999]) # Why 9.9 Mil? as it way beyoud number of tables exists across db

    # Database filter view
    col_db = df["TABLE_CATALOG"].drop_duplicates()
    col_db = col_db._append(select_all, ignore_index=False)
    #return col_db

    col_schema = df["TABLE_SCHEMA"].drop_duplicates()
    col_schema = col_schema._append(select_all, ignore_index=False)

    col_owner = df["TABLE_OWNER"].drop_duplicates()
    col_owner = col_owner._append(select_all, ignore_index=False)

    col_table_type = df["TABLE_TYPE"].drop_duplicates()

    return col_db, col_schema, col_owner, col_table_type
