class CLI:
    def read_user_message(self) -> str:
        return input("Faça sua pergunta: ")

    def is_valid_question(self, message: str, min_length: int = 5) -> bool:
        return bool(message and message.strip() and len(message.strip()) >= min_length)
    
    def clear_last_input_line(self) -> None:
        print("\033[A\033[2K", end="")
    
    def print_answer(self, question: str, answer: str) -> None:
        print(f"PERGUNTA: {question}")
        print(f"RESPOSTA: {answer}")
        print("\n---\n")