import sqlite3
import os
import pandas as pd

path = os.getcwd()

def init_binary_db():
    conn = sqlite3.connect(path+'/DB/DataBase.db')
    c = conn.cursor()
    
    # 테이블이 이미 존재하는지 확인하고, 없다면 새로 생성
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS SK_API(
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Start Station CHAR,
                        End Station CHAR,
                        prevStationName CHAR,
                        Day of Week CHAR,
                        Time CHAR,
                        Congestion REAL
                        )
    '''

    c.execute(create_table_query)

    conn.commit()
    conn.close()
    
def db_insert_data_binary(date, result, data_list):
    # Connect to the database
    conn = sqlite3.connect(path+'/DB/binary_result.db')
    c = conn.cursor()

    # Define the INSERT statement
    insert_query = '''
        INSERT INTO binary_result (DATE, result, Mean_of_the_integrated_profile, 
                                 Standard_deviation_of_the_integrated_profile,
                                 Excess_kurtosis_of_the_integrated_profile,
                                 Skewness_of_the_integrated_profile, Mean_of_the_DM_SNR_curve,
                                 Standard_deviation_of_the_DM_SNR_curve,
                                 Excess_kurtosis_of_the_DM_SNR_curve,
                                 Skewness_of_the_DM_SNR_curve)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Prepend the date and result value to the data_list
    data_list = [date, result] + data_list

    # Execute the INSERT statement with the data
    c.execute(insert_query, data_list)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_binary_results():
    conn = sqlite3.connect(path+'/DB/binary_result.db')
    c = conn.cursor()

    # 데이터 조회
    c.execute('SELECT * FROM binary_result')

    results = c.fetchall()

    conn.close()

    return results

def binary_delete_result(ids):
    
    conn = sqlite3.connect(path+'/DB/binary_result.db')
    c = conn.cursor()

    for id in ids:
        c.execute('DELETE FROM binary_result WHERE Id = ?', (int(id),))

    conn.commit()
    
    c.execute('SELECT * FROM binary_result')
    results = c.fetchall()
    
    conn.close()
    
    return results


def log_to_csv():
    
    csv_file_path = path + '/dataset/log.csv'
    conn = sqlite3.connect(path + '/DB/binary_result.db')
    
    df = pd.read_sql_query('SELECT * FROM binary_result', conn)
    conn.close()

    df.to_csv(csv_file_path, index=False)  # CSV 파일로 저장

    return csv_file_path