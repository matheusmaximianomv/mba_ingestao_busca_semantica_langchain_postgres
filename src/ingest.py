import os
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from validate_env import validate_env

load_dotenv()

validate_env([
    "PDF_PATH",
    "PG_VECTOR_COLLECTION_NAME",
    "DATABASE_URL",
    "OPENAI_MODEL",
    "GOOGLE_MODEL",
    "OPENAI_EMBEDDING_MODEL",
    "GOOGLE_EMBEDDING_MODEL"
])

PDF_PATH = os.getenv("PDF_PATH")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")

def ingest_pdf():
    doc = PyPDFLoader(str(PDF_PATH)).load()
    
    splitters = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=True,
    ).split_documents(doc)

    if not splitters:
        raise SystemExit(0)
    
    enriched = [
        Document(
            page_content=document.page_content,
            metadata={key: value for key, value in document.metadata.items() if value not in ("", None)}
        )
        for document in splitters
    ]

    embeddings = OpenAIEmbeddings(
        model=str(OPENAI_EMBEDDING_MODEL)
    )

    db_vector_store = PGVector(
        embeddings=embeddings,
        collection_name=str(PG_VECTOR_COLLECTION_NAME),
        connection=str(DATABASE_URL),
        use_jsonb=True
    )

    ids = [f"document-{i}" for i in range(len(enriched))]

    db_vector_store.add_documents(enriched, ids=ids)

if __name__ == "__main__":
    ingest_pdf()