import sqlite3
import pandas as pd
import numpy as np



def ensure_table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    exists = cursor.fetchone() is not None
    cursor.close()
    return exists

def calculate_chi_square(db_path, pos):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Завантаження даних для вказаної частини мови
    cur.execute(f"SELECT * FROM frequency_results_{pos}")
    rows = cur.fetchall()
    conn.close()


    fullMathStr = ""
    calculated = 0
    N = 0

    for row in rows:
        rowName = row[0]
        sumData = row[-1]
        data = row[1:][:-1]
        if rowName == "ΣK":
            N = sumData

        i = 0

        sumStr = ""
        for col in data:
            if(rowName != "ΣK"):
                KiMi = col
                sumKi = sumData
                sumMi = rows[-1][i+1]
                calculatedResult = ((KiMi**2)/(sumKi * sumMi))
                calculated = calculated + calculatedResult
                sumStr = sumStr + f"({KiMi}^2/{sumKi} * {sumMi})" + " + "
                i = i + 1

    finalResult = N*(calculated-1)
    return finalResult

def main():
    db_path = 'frequency_analysis.db'
    parts_of_speech = ['noun', 'conj', 'verb']

    for pos in parts_of_speech:
        final = calculate_chi_square(db_path, pos)
        print(f"pos: {pos}, result: {final}")

if __name__ == "__main__":
    main()
