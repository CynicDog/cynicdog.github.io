import os
import json
import glob
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

def process():
    # 1. Configuration
    POSTS_PATH = "src/data/blog/*.mdx" # Adjust to your Astro path
    OUTPUT_PATH = "public/graph.json"
    MIN_SIMILARITY = 0.4  # Threshold for drawing a link
    NUM_CLUSTERS = 5      # Number of color groups (themes)

    # 2. Extract Data
    files = glob.glob(POSTS_PATH)
    posts = []
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            posts.append({
                "id": os.path.basename(f).replace('.md', ''),
                "content": content
            })

    if not posts:
        return

    # 3. Vectorization (Semantic DNA)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([p['content'] for p in posts])

    # 4. Clustering (Themes/Colors)
    kmeans = KMeans(n_clusters=min(NUM_CLUSTERS, len(posts)), n_init='auto')
    clusters = kmeans.fit_predict(embeddings)

    # 5. Relationship Calculation (Links)
    sim_matrix = cosine_similarity(embeddings)
    links = []
    for i in range(len(posts)):
        for j in range(i + 1, len(posts)):
            score = float(sim_matrix[i][j])
            if score > MIN_SIMILARITY:
                links.append({
                    "source": posts[i]['id'],
                    "target": posts[j]['id'],
                    "value": score * 10 # Scale for D3 stroke-width
                })

    # 6. Assemble Nodes
    nodes = []
    for i, p in enumerate(posts):
        nodes.append({
            "id": p['id'],
            "group": int(clusters[i]),
            "radius": 5 # You could scale this by post length!
        })

    # 7. Write to File
    with open(OUTPUT_PATH, 'w') as f:
        json.dump({"nodes": nodes, "links": links}, f, indent=2)

if __name__ == "__main__":
    process()