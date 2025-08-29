import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

for k in ("LLM_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")
    
os.environ["OPENAI_API_KEY"] = os.getenv("LLM_API_KEY")    
PDF_PATH = os.getenv("PDF_PATH")

def store_doc(enriched, ids):
    """Store documents in the vector database."""
    embeddings = OpenAIEmbeddings(model=os.getenv("AI_MODEL","text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)

def split_docs(docs):
    """Split documents into smaller chunks."""
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150, 
        add_start_index=False).split_documents(docs)

    if not splits:
        raise SystemExit(0)
    return splits


def enrich_docs(splits):
    """Enrich document splits with metadata."""
    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]   

    ids = [f"doc-{i}" for i in range(len(enriched))]

    return enriched, ids

def ingest_pdf():
    """Ingest a PDF document."""
    docs = PyPDFLoader(str(PDF_PATH)).load()

    if not docs:
        raise ValueError(f"Document Not Found: {str(PDF_PATH)}")

    splits = split_docs(docs)

    enriched_doc, ids = enrich_docs(splits)
    
    store_doc(enriched_doc, ids)


if __name__ == "__main__":
    ingest_pdf()