from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 150):
        self.__pdf_path = pdf_path
        self.__chunk_size = chunk_size
        self.__chunk_overlap = chunk_overlap
    
    def process(self):
        docs = self._load_document()

        split_docs = self._split_documents(docs)

        if not split_docs:
            raise SystemExit(0)

        enriched = self._enrich_documents(split_docs)

        ids = self._generate_ids(enriched)

        return enriched, ids

    def _load_document(self):
        loader = PyPDFLoader(str(self._pdf_path))
        return loader.load()

    def _split_documents(self, documents: list[Document]):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=self._chunk_overlap,
            add_start_index=True,
        )

        return splitter.split_documents(documents)

    def _enrich_documents(self, documents: list[Document]):
        return [
            Document(
                page_content=document.page_content,
                metadata={
                    key: value
                    for key, value in document.metadata.items()
                    if value not in ("", None)
                },
            )
            for document in documents
        ]

    def _generate_ids(self, documents: list[Document]):
        return [f"document-{i}" for i in range(len(documents))]