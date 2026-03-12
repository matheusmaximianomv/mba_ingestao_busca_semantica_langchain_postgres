from langchain_core.documents import Document

def build_context_from_results(results: list[tuple[Document, float]]) -> str:
    return "\n".join(document.page_content for document, _score in results)
