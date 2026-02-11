from langchain_core.prompts import ChatPromptTemplate


def generate_sql(llm, db, question: str):

    schema = db.get_table_info()

    prompt = ChatPromptTemplate.from_template(
        """
Você é um especialista em SQL PostgreSQL.

Baseado no schema abaixo:

{schema}

Gere apenas a query SQL que responde a pergunta do usuário.
Não explique nada.
Retorne somente a SQL.

Pergunta:
{question}
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "schema": schema,
        "question": question
    })

    return response.content.strip()
