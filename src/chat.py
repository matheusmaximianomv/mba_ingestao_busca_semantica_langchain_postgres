from langchain.chat_models import init_chat_model
from helpers.search import search_prompt
from services.env_config import EnvConfig
from services.cli import CLI
from database.database import Database
from helpers.build_context_from_results import build_context_from_results

def main():
    env_config = EnvConfig()
    database = Database(env_config)
    cli = CLI()

    llm = init_chat_model(
        model=env_config.get_model(),
        model_provider=env_config.get_model_provider(),
        temperature=0
    )

    while True:
        try:
            user_message = cli.read_user_message()
            cli.clear_last_input_line()

            if not cli.is_valid_question(user_message):
                cli.print_answer(user_message, "Pergunta fornecida inválida.")
                continue

            vector_response = database.similarity_search_with_score(user_message)
            context = build_context_from_results(vector_response)

            prompt = search_prompt(user_message, context)
            if not prompt:
                print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
                return

            response = llm.invoke(prompt)
            cli.print_answer(user_message, response.content)
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando...")
            break

if __name__ == "__main__":
    main()