from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from services.env_config import EnvConfig
from enums.model_provider import ModelProvider

class Database:
    def __init__(self, env_config: EnvConfig):
        self.__env_config = env_config
        self.__vector_store = self.__init_vector_store()

    def add_documents(self, documents: list[Document], ids: list[str]):
        self.__vector_store.add_documents(documents, ids=ids)
    
    def similarity_search_with_score(self, user_message: str, k: int = 10):
        return self.__vector_store.similarity_search_with_score(user_message, k)
    
    def __init_vector_store(self):
        return PGVector(
            embeddings=self.__generate_embeddings(),
            collection_name=self.__env_config.get_pg_vector_collection_name(),
            connection=self.__env_config.get_database_url(),
            use_jsonb=True
        )

    def __generate_embeddings(self):
        AIEmbeddings = self.__get_class_ai_embeddings()
        
        return AIEmbeddings(
            model=self.__env_config.get_embedding_model()
        )

    def __get_class_ai_embeddings(self) -> (type[OpenAIEmbeddings] | type[GoogleGenerativeAIEmbeddings]):
        model_provider = self.__env_config.get_model_provider()
        
        if model_provider == ModelProvider.OPENAI:
            return OpenAIEmbeddings
        if model_provider == ModelProvider.GOOGLE:
            return GoogleGenerativeAIEmbeddings

        raise ValueError(f"Unsupported model provider: {model_provider}")
    