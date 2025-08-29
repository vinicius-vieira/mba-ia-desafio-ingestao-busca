import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

from search import search_prompt

load_dotenv()

for k in ("LLM_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "PDF_PATH"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")
    
os.environ["OPENAI_API_KEY"] = os.getenv("LLM_API_KEY")   


def get_store_doc():
    """Get the document store."""
    embeddings = OpenAIEmbeddings(model=os.getenv("AI_MODEL","text-embedding-3-small"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    return store

def create_llm_model():
    """Create the LLM model instance."""
    llm = ChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL", "gpt-5-nano"), temperature=0.2)
    return llm

def build_context_from_store(question: str) -> str:
    """Build context from the document store."""
    store = get_store_doc()

    TOP_K = 10
    docs = store.similarity_search(question, k=TOP_K)
    
    if not docs:
        return ""
    
    parts = []
    for i, d in enumerate(docs, 1):
        meta = ", ".join(f"{k}: {v}" for k, v in (d.metadata or {}).items())
        parts.append(f"Trecho {i}:\n{d.page_content.strip()}\nMetadados: {meta}\n")

    return "\n\n".join(parts)

def prepare_inputs(payload: dict) -> dict:
    """
    Prepare inputs for the LLM model.
    """   
    question = payload.get("question", "")
    context = build_context_from_store(question)
    return {"pergunta": question, "contexto": context}

def main():

    prepare = RunnableLambda(prepare_inputs)
    chain = prepare | search_prompt() | create_llm_model()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    while True:
        try:
            user_q = input("Faça uma pergunta (ou 'sair' para encerrar):\n").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando a conversa. Até mais!")
            break

        if not user_q:
            continue
        if user_q.lower() in {"sair", "exit", "quit"}:
            print("Encerrando a conversa. Até mais!")
            break

        resp = chain.invoke({"question": user_q})
        print(f"\nRESPOSTA: {resp.content}\n")


if __name__ == "__main__":
    main()