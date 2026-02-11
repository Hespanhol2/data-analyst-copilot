from db import get_database
from llm import get_llm
from sql_generator import generate_sql


def main():
    print("🤖 Data Analyst Copilot iniciado!")

    db = get_database()
    llm = get_llm()

    while True:
        question = input("\nPergunta: ")

        if question.lower() in ["sair", "exit", "quit"]:
            break

        # 1️⃣ Gera SQL
        sql_query = generate_sql(llm, db, question)

        print("\n📄 SQL Gerada:")
        print(sql_query)

        # 2️⃣ Executa SQL
        try:
            result = db.run(sql_query)

            print("\n📊 Resultado:")
            print(result)

        except Exception as e:
            print("\n❌ Erro ao executar SQL:")
            print(e)


if __name__ == "__main__":
    main()
