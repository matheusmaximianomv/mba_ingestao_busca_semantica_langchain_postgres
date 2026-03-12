import os
from dotenv import load_dotenv
from enums.model_provider import ModelProvider

ENVS_REQUIRED = [
    'GEMINI_API_KEY',
    'OPENAI_API_KEY',
    'GOOGLE_MODEL',
    'OPENAI_MODEL',
    'GOOGLE_EMBEDDING_MODEL',
    'OPENAI_EMBEDDING_MODEL',
    'DATABASE_URL',
    'PG_VECTOR_COLLECTION_NAME',
    'PDF_PATH'
]

ENV_MODEL_PROVIDER = "MODEL_PROVIDER"

class EnvConfig:
    def __init__(self):
        load_dotenv()
        self.__validate_env()
    
    def get_model_provider(self) -> str:
        model_provider = os.getenv(ENV_MODEL_PROVIDER)
        
        if not model_provider:
            return ModelProvider.OPENAI

        if model_provider == ModelProvider.GOOGLE:
            return ModelProvider.GOOGLE
        elif model_provider == ModelProvider.OPENAI:
            return ModelProvider.OPENAI
        else:
            return ModelProvider.OPENAI
    
    def get_model(self) -> str:
        model_provider = self.get_model_provider()

        if model_provider == ModelProvider.GOOGLE:
            return self.GOOGLE_MODEL
        elif model_provider == ModelProvider.OPENAI:
            return self.OPENAI_MODEL
    
    def get_embedding_model(self) -> str:
        model_provider = self.get_model_provider()

        if model_provider == ModelProvider.GOOGLE:
            return self.GOOGLE_EMBEDDING_MODEL
        elif model_provider == ModelProvider.OPENAI:
            return self.OPENAI_EMBEDDING_MODEL
    
    def get_database_url(self) -> str:
        return self.DATABASE_URL
    
    def get_pg_vector_collection_name(self) -> str:
        return self.PG_VECTOR_COLLECTION_NAME
    
    def get_pdf_path(self) -> str:
        return self.PDF_PATH

    def __validate_env(self):   
        for keys in ENVS_REQUIRED:
            if not os.getenv(keys):
                raise ValueError(f"Environment variable {keys} is not set")
            else:
                setattr(self, keys, os.getenv(keys))
    