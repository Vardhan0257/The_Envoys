import fitz  # PyMuPDF
import uuid
from sentence_transformers import SentenceTransformer
from models import Document, Chunk

CHUNK_SIZE = 800
OVERLAP = 150

embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")

def extract_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

def chunk_text(text: str):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + CHUNK_SIZE
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start += CHUNK_SIZE - OVERLAP

    return chunks

def ingest_pdf(session, pdf_path: str):
    text = extract_text(pdf_path)
    chunks = chunk_text(text)

    doc = Document(filename=pdf_path)
    session.add(doc)
    session.commit()

    embeddings = embedder.encode(chunks)

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        c = Chunk(
            document_id=doc.id,
            chunk_id=f"chunk_{i}",
            text=chunk,
            embedding=emb.tolist()
        )
        session.add(c)

    session.commit()
