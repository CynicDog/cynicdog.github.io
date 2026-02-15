import os
import json
import glob
import logging
import time
import numpy as np
import yaml
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# 0. Setup Verbose Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("SemanticAnalyzer")

def process():
    start_time = time.time()

    # 1. Configuration
    POSTS_PATH = "src/data/blog/*.mdx"
    OUTPUT_PATH = "public/graph.json"
    MIN_SIMILARITY = 0.3
    NUM_CLUSTERS = 5
    now = datetime.now()

    logger.info("Initialization: Semantic Analysis & Meta-Metrics")

    # 2. Extract Data & Metadata
    files = glob.glob(POSTS_PATH)
    logger.info(f"Scanning directory: Found {len(files)} .mdx files")

    posts = []
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            raw_content = file.read()
            parts = raw_content.split('---')
            content = raw_content
            metadata = {}

            # Extract Frontmatter
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                    content = parts[2]
                except Exception as e:
                    logger.error(f"Failed to parse YAML in {f}: {e}")

            post_id = os.path.basename(f).replace('.mdx', '').replace('.md', '')

            # Date Score Calculation (Freshness Decay)
            pub_date = metadata.get('date', now)
            if isinstance(pub_date, str):
                try: pub_date = datetime.strptime(pub_date, '%Y-%m-%d')
                except: pub_date = now

            days_old = (now - pub_date).days
            date_score = max(0, 1 - (days_old / 365))

            posts.append({
                "id": post_id,
                "content": content,
                "word_count": len(content.split()),
                "date_score": round(date_score, 3),
                "title": metadata.get('title', post_id)
            })

    if not posts:
        logger.warning("No valid posts found to process.")
        return

    # 3. Embedding Generation
    logger.info(f"Loading Model... Encoding {len(posts)} posts into vector space")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([p['content'] for p in posts])

    # 4. Keyword Extraction (TF-IDF)
    logger.info("Calculating TF-IDF importance scores for keywords")
    vectorizer = TfidfVectorizer(stop_words='english', max_features=200)
    tfidf_matrix = vectorizer.fit_transform([p['content'] for p in posts])
    feature_names = vectorizer.get_feature_names_out()

    # 5. Clustering (Thematic Groups)
    actual_clusters = min(NUM_CLUSTERS, len(posts))
    logger.info(f"Grouping posts into {actual_clusters} clusters via KMeans")
    kmeans = KMeans(n_clusters=actual_clusters, n_init='auto', random_state=42)
    clusters = kmeans.fit_predict(embeddings)

    # 6. Relationship Mapping (Links)
    logger.info(f"Analyzing link density (Threshold: {MIN_SIMILARITY})")
    sim_matrix = cosine_similarity(embeddings)
    links = []
    for i in range(len(posts)):
        for j in range(i + 1, len(posts)):
            score = float(sim_matrix[i][j])
            if score > MIN_SIMILARITY:
                links.append({
                    "source": posts[i]['id'],
                    "target": posts[j]['id'],
                    "value": round(score, 3),
                    "rel_type": "semantic-match"
                })

    # 7. Final Assembly
    nodes = []
    for i, p in enumerate(posts):
        # Top 3 Keywords
        row = tfidf_matrix.getrow(i).toarray()[0]
        top_indices = row.argsort()[-3:][::-1]
        kws = [feature_names[idx] for idx in top_indices]

        nodes.append({
            "id": p['id'],
            "group": int(clusters[i]),
            "top_keywords": kws,
            "metrics": {
                "size": p['word_count'],
                "date_score": p['date_score'],
                "radius": 5 + (p['word_count'] // 400)
            }
        })
    # Write Result
    with open(OUTPUT_PATH, 'w') as f:
        json.dump({"nodes": nodes, "links": links}, f, indent=2)

if __name__ == "__main__":
    process()