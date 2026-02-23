from sqlalchemy import select
from models import Chunk
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")

def retrieve_chunks(session, query: str, top_k: int = 5):
    q_emb = embedder.encode(query).tolist()

    stmt = (
        select(Chunk)
        .order_by(Chunk.embedding.cosine_distance(q_emb))
        .limit(top_k)
    )

    results = session.execute(stmt).scalars().all()
    return results
