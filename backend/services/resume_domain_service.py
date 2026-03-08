import re

# Map resume keywords to REAL dataset categories
category_keywords = {
    "general programming": [
        "oop", "object oriented", "class", "inheritance",
        "polymorphism", "encapsulation"
    ],
    "data structures": [
        "stack", "queue", "linked list", "tree",
        "binary tree", "heap"
    ],
    "algorithms": [
        "algorithm", "sorting", "searching",
        "binary search", "dynamic programming",
        "greedy", "graph"
    ],
    "languages and frameworks": [
        "java", "python", "c++", "javascript",
        "spring", "django", "flask"
    ],
    "database and sql": [
        "sql", "mysql", "postgres",
        "database", "query", "joins"
    ],
    "database systems": [
        "database design", "indexing",
        "transaction", "sharding"
    ],
    "web development": [
        "html", "css", "web app"
    ],
    "front-end": [
        "react", "angular", "vue",
        "frontend", "ui"
    ],
    "back-end": [
        "node", "express", "api",
        "backend", "server"
    ],
    "full-stack": [
        "full stack", "mern", "mean"
    ],
    "system design": [
        "architecture", "scalable",
        "microservices", "distributed"
    ],
    "distributed systems": [
        "kafka", "distributed system",
        "consensus", "replication"
    ],
    "low-level systems": [
        "memory management",
        "operating system", "compiler"
    ],
    "devops": [
        "docker", "kubernetes",
        "ci/cd", "pipeline"
    ],
    "version control": [
        "git", "github", "gitlab"
    ],
    "networking": [
        "tcp", "udp", "network protocol"
    ],
    "security": [
        "authentication", "authorization",
        "jwt", "encryption", "cybersecurity"
    ],
    "software testing": [
        "unit testing", "integration testing",
        "test cases"
    ],
    "machine learning": [
        "machine learning", "tensorflow",
        "pytorch", "regression", "classification"
    ],
    "artificial intelligence": [
        "artificial intelligence",
        "neural network", "deep learning"
    ],
    "data engineering": [
        "spark", "data pipeline",
        "etl", "big data"
    ]
}


def detect_domain(resume_text: str):
    
    if not resume_text:
        return None
    
    resume_text = resume_text.lower()
    resume_text = resume_text.replace("-", " ")

    scores = {category: 0 for category in category_keywords}

    for category, keywords in category_keywords.items():
        for keyword in keywords:
            matches = re.findall(rf"\b{re.escape(keyword.lower())}\b", resume_text)
            scores[category] += len(matches)

    # 🔎 DEBUG PRINT
    print("Domain scores:", scores)

    # Remove zero-score categories
    non_zero_scores = {k: v for k, v in scores.items() if v > 0}

    if not non_zero_scores:
        print("No strong domain detected.")
        return None

    sorted_categories = sorted(non_zero_scores.items(), key=lambda x: x[1], reverse=True)

    best_category, best_score = sorted_categories[0]

    # If second best is too close → unclear signal
    if len(sorted_categories) > 1:
        second_score = sorted_categories[1][1]
        if best_score - second_score <= 1:
            print("Domain detection unclear (scores too close).")
            return None

    print("Detected domain:", best_category)

    return best_category