import pandas as pd
import sqlite3

def connect_database(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        
    return conn

def read_database(db_file,table):
    """
    Establish connect to db file and queries all rows in the tasks table.
    |db_file| (str) database file name
    |table| (str) table name
    """
    conn = connect_database(db_file)

    query = conn.execute("SELECT * FROM " + f"'{table}'")
    cols = [column[0] for column in query.description]
    results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
    
    conn.close()
    
    return results

def update_database(db_file,table,new_frame):
    """
    Updates table in db_file with data from new_frame. Only appends rows if it is not already in the database.
    
    :db_file: (str) database file name
    :table: (str) SQL table name
    :new_frame: (pd.DataFrame) frame containing new data
    """
    conn = connect_database(db_file)

    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"
    result = pd.read_sql_query(query, conn).shape[0]>0
    
    if not result:
        print(f"Table {table} not found in database {db_file}. Creating new table...")
        new_frame.to_sql(table, conn, if_exists='replace',index=False)
        conn.commit()
        conn.close()
        return
    
    
    print(f"Table {table} found in database {db_file}. Updating table...")
    
    new_frame.to_sql('temp_table', conn, if_exists='replace',index=False)
    
    #not working as expected
    conn.execute(f'''
        INSERT INTO {table} 
        SELECT * FROM temp_table 
        WHERE NOT EXISTS (
            SELECT * FROM {table} 
            WHERE {table}.teamAbbr = temp_table.teamAbbr 
            AND {table}.teamAbbr = temp_table.teamAbbr
        )
    ''')

    conn.execute('''
        DROP TABLE temp_table;
    ''')

    conn.commit()
    conn.close()

    
    