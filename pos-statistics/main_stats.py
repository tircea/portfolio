
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import math

conn = sqlite3.connect('/yourpath/text1.pdf.frequency_dict.db')
cursor = conn.cursor()

conn2 = sqlite3.connect('/yourpath/text2.txt.frequency_dict.db')
cursor2 = conn2.cursor()

print("Підключення до бази даних успішне")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'abs_%';")
tables_to_process = [table[0] for table in cursor.fetchall()]

print(f"Знайдено таблиці для обробки: {tables_to_process}")

cursor.execute(f"""
   CREATE TABLE IF NOT EXISTS value_l_t (
       pos TEXT,
       l INTEGER, t INTEGER
   );
""")

cursor2.execute(f"""
   CREATE TABLE IF NOT EXISTS value_l_t (
       pos TEXT,
       l INTEGER, t INTEGER
   );
""")

for table_name in tables_to_process:
   print(f"Обробка таблиці: {table_name}")
   cursor.execute(f"SELECT Xi, Ni, XiNi FROM {table_name} WHERE Xi IS NOT NULL")
   data = cursor.fetchall()
   if not data:
       print(f"В таблиці {table_name} після відкидання рядків з NULL не залишилось даних для обробки.")
       continue

   Xi, Ni, XiNi = zip(*data)
   Xi = [float(x) for x in Xi]
   Ni = [float(n) for n in Ni]
   XiNi = [float(n) for n in XiNi]

   x = sum(Xi[i] * Ni[i] for i in range(len(Xi))) / sum(Ni)

   differences_squared = [(xi - x)**2 * ni for xi, ni in zip(Xi, Ni)]
   sum_differences_squared = sum(differences_squared)
   sigma = np.sqrt(sum_differences_squared / sum(Ni))
   variation_measure = sigma / np.sqrt(sum(Ni))
  
   lower_bound_68 = x - variation_measure
   upper_bound_68 = x + variation_measure
   lower_bound_95 = x - 2 * variation_measure
   upper_bound_95 = x + 2 * variation_measure

   print(f"Сума (xi - x)^2 * ni: {sum_differences_squared:.4f}")
   print(f"Середнє квадратичне відхилення: {sigma:.2f}")
   print(f"Міра коливання середньої частоти: {variation_measure:.2f}")
   print(f"68% довірчий інтервал: від {lower_bound_68:.2f} до {upper_bound_68:.2f}")
   print(f"95% довірчий інтервал: від {lower_bound_95:.2f} до {upper_bound_95:.2f}")
   n = sum(Ni)
   v = sigma/x
   d = 1-(sigma/(x*math.sqrt(n-1)))
   e = (1.96/(math.sqrt(n)))*v
   print(f"Коефіцієнт варіації (V): {v:.2f}")
   print(f"Коефіцієнт стабільності (D): {d:.2f}")
   print(f"Відносна похибка: {e:.2f}\n")

   cursor.execute(f"UPDATE {table_name} SET squaredSum = {sum_differences_squared:.4f} WHERE Xi IS NULL")
   conn.commit()

   plt.figure(figsize=(10, 1))
   plt.hlines(1, lower_bound_68, upper_bound_68, color='blue', lw=5, label='68% довірчий інтервал')
   plt.hlines(1, lower_bound_95, upper_bound_95, color='red', lw=2, label='95% довірчий інтервал')
   plt.legend(loc='upper right')
   plt.title(f"Смуги коливань для {table_name}")
   plt.xlabel('Xi')
   plt.yticks([])
   plt.xlim(lower_bound_95 - variation_measure, upper_bound_95 + variation_measure)

conn.close()
conn2.close()
