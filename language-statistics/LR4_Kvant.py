import sqlite3
import pandas as pd

def load_data(db_path, pos):
    conn = sqlite3.connect(db_path)
    query = f"SELECT підв_1, підв_2, підв_3, підв_4, підв_5, підв_6, підв_7, підв_8, підв_9, підв_10, підв_11, підв_12, підв_13, підв_14, підв_15, підв_16, підв_17, підв_18, підв_19, підв_20 FROM ЧС_частмови WHERE pos='{pos}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def create_and_save_results(db_path, dfs, pos):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS frequency_results_{pos} (
                sample_label TEXT,
                K1 INTEGER, K2 INTEGER, K3 INTEGER, K4 INTEGER, K5 INTEGER, 
                K6 INTEGER, K7 INTEGER, K8 INTEGER, K9 INTEGER, K10 INTEGER, 
                K11 INTEGER, K12 INTEGER, K13 INTEGER, K14 INTEGER, K15 INTEGER, 
                K16 INTEGER, K17 INTEGER, K18 INTEGER, K19 INTEGER, K20 INTEGER,
                Sum INTEGER
            );
        """)
        for df, label in dfs:
            df['Sum'] = df.sum(axis=1)
            df['sample_label'] = label
            df.to_sql(f'frequency_results_{pos}', conn, if_exists='append', index=False)
        
        sums = pd.concat([df.iloc[:, :-1] for df, _ in dfs]).sum().to_frame().T
        sums['Sum'] = sums.sum(axis=1)
        sums['sample_label'] = 'ΣK'
        sums.to_sql(f'frequency_results_{pos}', conn, if_exists='append', index=False)
    finally:
        conn.close()

def process_parts_of_speech(db_path1, db_path2, new_db_path, parts_of_speech):
    for pos in parts_of_speech:
        df1 = load_data(db_path1, pos)
        df2 = load_data(db_path2, pos)
        df1.columns = df2.columns = [f'K{i+1}' for i in range(20)]
        create_and_save_results(new_db_path, [(df1, 'M1'), (df2, 'M2')], pos)

# Шляхи до баз даних
db_path1 = 'text1.pdf.frequency_dict.db'
db_path2 = 'text2.txt.frequency_dict.db'
new_db_path = 'frequency_analysis.db'

# Частини мови, для яких будуть створені таблиці
parts_of_speech = ['noun', 'verb', 'conj']
process_parts_of_speech(db_path1, db_path2, new_db_path, parts_of_speech)

