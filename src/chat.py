import os
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
from langchain_postgres import PGVector
from dotenv import load_dotenv
from search import search_prompt
from validate_env import validate_env

load_dotenv()

validate_env([
    "PG_VECTOR_COLLECTION_NAME",
    "DATABASE_URL",
    "OPENAI_EMBEDDING_MODEL",
])

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

def main():

    while True:
        try:
            user_message = input("Faça sua pergunta: ")
            
            print("\033[A\033[2K", end="")

            print("PERGUNTA: ", user_message)

            if not user_message or user_message.strip() == "" or len(user_message.strip()) < 5:
                print("RESPOSTA: Pergunta fornecida inválida.")
                print("\n---\n")
                continue

            embeddings = OpenAIEmbeddings(
                model=str(OPENAI_EMBEDDING_MODEL)
            )

            db_vector_store = PGVector(
                embeddings=embeddings,
                collection_name=str(PG_VECTOR_COLLECTION_NAME),
                connection=str(DATABASE_URL),
                use_jsonb=True
            )

            vector_response = db_vector_store.similarity_search_with_score(user_message, k=10)
            parsed_docs = ""
            for (doc, _score) in vector_response:
                parsed_docs += f"{doc.page_content}\n"

            prompt = search_prompt(user_message, parsed_docs)

            if not prompt:
                print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
                return

            llm = init_chat_model(model=str(OPENAI_MODEL), model_provider="openai", temperature=0)
            
            main_chain = llm.invoke(prompt)

            print("RESPOSTA: ", main_chain.content)
            print("\n---\n")

        except EOFError:
            print("\nEncerrando...")
            break

if __name__ == "__main__":
    main()