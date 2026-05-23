from pathlib import Path
from typing import Any

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.document import Document
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings

from services.config import settings


class LocalEmbeddings(Embeddings):
    def __init__(self) -> None:
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode([text], normalize_embeddings=True)[0].tolist()


embeddings = LocalEmbeddings()


def _index_path() -> Path:
    settings.vectorstore_path.mkdir(parents=True, exist_ok=True)
    return settings.vectorstore_path


def _load() -> FAISS | None:
    path = _index_path()
    if not (path / "index.faiss").exists():
        return None
    return FAISS.load_local(str(path), embeddings, allow_dangerous_deserialization=True)


def index_text(filename: str, text: str) -> int:
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)
    chunks = splitter.split_text(text)
    docs = [Document(page_content=chunk, metadata={"source": filename, "chunk": idx + 1}) for idx, chunk in enumerate(chunks)]
    existing = _load()
    if existing:
        existing.add_documents(docs)
        existing.save_local(str(_index_path()))
    else:
        FAISS.from_documents(docs, embeddings).save_local(str(_index_path()))
    return len(chunks)


def retrieve(query: str, k: int = 4) -> list[dict[str, Any]]:
    try:
        store = _load()
        if not store:
            return []
        docs = store.similarity_search_with_score(query, k=k)
    except Exception:
        return []
    return [
        {
            "text": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "chunk": doc.metadata.get("chunk", 0),
            "score": float(score),
        }
        for doc, score in docs
    ]
