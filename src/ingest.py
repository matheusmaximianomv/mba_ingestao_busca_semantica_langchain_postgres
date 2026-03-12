from database.database import Database
from services.env_config import EnvConfig
from services.document_processor import DocumentProcessor

def ingest_pdf():
    env_config = EnvConfig()
    document_processor = DocumentProcessor(env_config.get_pdf_path())

    documents, ids = document_processor.process()

    database = Database(env_config)
    database.add_documents(documents, ids)

if __name__ == "__main__":
    ingest_pdf()