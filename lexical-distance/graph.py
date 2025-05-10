import sqlite3
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Підключаємося до бази даних SQLite
conn = sqlite3.connect('word_frequencies.db')

# Функції для обчислення метрик
def euclidean_distance(A, B):
    return np.sqrt(np.sum((A - B) ** 2))

def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    norm_a = np.linalg.norm(A)
    norm_b = np.linalg.norm(B)
    return dot_product / (norm_a * norm_b) if norm_a != 0 and norm_b != 0 else 0

def jaccard_similarity(A, B):
    intersection = np.minimum(A, B).sum()
    union = np.maximum(A, B).sum()
    return intersection / union if union != 0 else 0

def jaccard_distance(A, B):
    return 1 - jaccard_similarity(A, B)

# Функція для обчислення метрик для кожної пари текстів
def calculate_metrics(text_a, text_b):
    query_a = f"SELECT * FROM {text_a}"
    query_b = f"SELECT * FROM {text_b}"
    df_a = pd.read_sql(query_a, conn)
    df_b = pd.read_sql(query_b, conn)
    df_merged = pd.merge(df_a, df_b, on='word', how='outer', suffixes=(f'_{text_a}', f'_{text_b}')).fillna(0)
    A = df_merged[f'frequency_{text_a}'].values
    B = df_merged[f'frequency_{text_b}'].values
    return {
        'jaccard_dist': jaccard_distance(A, B),
        'euclidean_dist': euclidean_distance(A, B),
        'cosine_sim': cosine_similarity(A, B),
        'cosine_dist': 1 - cosine_similarity(A, B)
    }

# Тексти для обчислень
texts = ['text1', 'text2', 'text3', 'text4']
metrics = {'jaccard_dist': {}, 'euclidean_dist': {}, 'cosine_sim': {}, 'cosine_dist': {}}

# Обчислення метрик для всіх пар текстів і збереження результатів
for i, text_a in enumerate(texts):
    for text_b in texts[i+1:]:
        result = calculate_metrics(text_a, text_b)
        for key in metrics:
            metrics[key][(text_a, text_b)] = result[key]

# Функція для візуалізації графу з покращеним розташуванням підписів
def plot_graph(metric_name, data):
    G = nx.Graph()
    G.add_nodes_from(texts)
    for (text_a, text_b), value in data.items():
        G.add_edge(text_a, text_b, weight=value)
    pos = nx.spring_layout(G, seed=42)

    # Малюємо вузли та підписи до них
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightgreen')
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')

    # Малюємо ребра та підписи до них (ваги)
    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, edge_color='black')

    # Зміщуємо підписи на ребрах для кращої читабельності
    edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    plt.title(f'{metric_name} between Texts')
    plt.show()

# Побудова графіків для кожної метрики
for metric_name, data in metrics.items():
    plot_graph(metric_name, data)

# Закриваємо з'єднання з базою даних
conn.close()