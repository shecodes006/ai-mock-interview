import os
import matplotlib
matplotlib.use("Agg")   # Added: use non-GUI backend for server environments

import matplotlib.pyplot as plt


GRAPH_DIR = "graphs"

os.makedirs(GRAPH_DIR, exist_ok=True)


def save_graph(session_id, name):
    path = f"{GRAPH_DIR}/session_{session_id}_{name}.png"
    plt.tight_layout(pad=2.0)
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    return path


def generate_all_graphs(session_id, score_progression, category_breakdown):

    for file in os.listdir(GRAPH_DIR):
        if file.startswith(f"session_{session_id}_"):
            os.remove(os.path.join(GRAPH_DIR, file))

    graphs = {}

    categories = list(category_breakdown.keys())
    scores = list(category_breakdown.values())

    # 1️ Score Progression (Line Graph)
    plt.figure(figsize=(8,5))

    x = list(range(1, len(score_progression) + 1))

    plt.plot(x, score_progression, marker="o", linewidth=2, color="#1f77b4")

    plt.title("Score Progression During Interview", fontsize=14)
    plt.xlabel("Question Number")
    plt.ylabel("Score")
    plt.xticks(x)
    plt.grid(True)

    graphs["score_progression"] = save_graph(session_id, "score_progression")


    # 2️ Category Performance (Bar Graph)
    plt.figure(figsize=(8,5))

    plt.bar(categories, scores, color="#2ca02c")

    plt.title("Category Performance", fontsize=14)
    plt.xlabel("Category")
    plt.ylabel("Average Score")
    plt.xticks(rotation=30)

    graphs["category_performance"] = save_graph(session_id, "category_performance")


    # 3️ Skill Strength (Horizontal Bar)
    plt.figure(figsize=(8,5))

    plt.barh(categories, scores, color="#9467bd")

    plt.title("Skill Strength Comparison", fontsize=14)
    plt.xlabel("Score")
    plt.ylabel("Skill Area")

    graphs["skill_strength"] = save_graph(session_id, "skill_strength")


    # 4️ Interview Score Distribution (Pie Chart)
    plt.figure(figsize=(6,6))

    plt.pie(
        scores,
        labels=categories,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Interview Score Distribution", fontsize=14)

    graphs["score_pie"] = save_graph(session_id, "score_pie")


    # 5️ Score Distribution (Histogram)
    plt.figure(figsize=(8,5))

    plt.hist(score_progression, bins=5, color="#17becf")

    plt.title("Score Distribution", fontsize=14)
    plt.xlabel("Score Range")
    plt.ylabel("Frequency")

    graphs["score_histogram"] = save_graph(session_id, "score_histogram")
  
    return graphs


    