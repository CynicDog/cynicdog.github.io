import os
import json
import glob
import logging
import time
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

# Setup clean, readable logging
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
    MIN_SIMILARITY = 0.45
    NUM_CLUSTERS = 5

    logger.info("--- 🏁 Starting Semantic Analysis Pipeline ---")

    # 2. Extract Data
    files = glob.glob(POSTS_PATH)
    logger.info(f"📂 Found {len(files)} blog posts in {POSTS_PATH}")

    posts = []
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            # Clean ID: remove extension and path
            post_id = os.path.basename(f).replace('.mdx', '').replace('.md', '')
            posts.append({"id": post_id, "content": content})

    if not posts:
        logger.warning("⚠️ No posts found. Exiting.")
        return

    # 3. Vectorization
    logger.info(f"🧠 Loading Transformer Model: all-MiniLM-L6-v2...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    logger.info("🧪 Generating embeddings (Semantic DNA)...")
    embeddings = model.encode([p['content'] for p in posts])
    logger.info(f"✅ Generated {len(embeddings)} vectors ({embeddings.shape[1]} dimensions each)")

    # 4. Clustering (Themes)
    actual_clusters = min(NUM_CLUSTERS, len(posts))
    logger.info(f"🌈 Grouping posts into {actual_clusters} thematic clusters...")
    kmeans = KMeans(n_clusters=actual_clusters, n_init='auto', random_state=42)
    clusters = kmeans.fit_predict(embeddings)

    # 5. Relationship Calculation
    logger.info(f"🔗 Calculating cosine similarity (Threshold > {MIN_SIMILARITY})...")
    sim_matrix = cosine_similarity(embeddings)
    links = []
    for i in range(len(posts)):
        for j in range(i + 1, len(posts)):
            score = float(sim_matrix[i][j])
            if score > MIN_SIMILARITY:
                links.append({
                    "source": posts[i]['id'],
                    "target": posts[j]['id'],
                    "value": round(score, 3)
                })

    logger.info(f"✅ Found {len(links)} semantic connections.")

    # 6. Assemble Nodes
    nodes = []
    for i, p in enumerate(posts):
        nodes.append({
            "id": p['id'],
            "group": int(clusters[i]),
            "radius": 5
        })

    # 7. Write to File & Final Summary
    with open(OUTPUT_PATH, 'w') as f:
        json.dump({"nodes": nodes, "links": links}, f, indent=2)

    duration = round(time.time() - start_time, 2)

    print("\n" + "="*50)
    print("📊 SEMANTIC BUSINESS SUMMARY")
    print("="*50)
    print(f"Total Posts Processed: {len(nodes)}")
    print(f"Thematic Clusters:     {actual_clusters}")
    print(f"Strong Relationships:  {len(links)}")
    print(f"Output File:           {OUTPUT_PATH}")
    print(f"Pipeline Runtime:      {duration}s")
    print("="*50 + "\n")

if __name__ == "__main__":
    process()