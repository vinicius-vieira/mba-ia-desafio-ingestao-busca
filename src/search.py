from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt():
    prompt = ChatPromptTemplate.from_messages([
          ("system", ''' 
              CONTEXTO:
              {contexto}    
        
              REGRAS:            
              - Responda somente com base no CONTEXTO.
              - Se a informação não estiver explicitamente no CONTEXTO, responda:
                  "Não tenho informações necessárias para responder sua pergunta."
              - Nunca invente ou use conhecimento externo.
              - Nunca produza opiniões ou interpretações além do que está escrito.

              EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
              Pergunta: "Qual é a capital da França?"
              Resposta: "Não tenho informações necessárias para responder sua pergunta."

              Pergunta: "Quantos clientes temos em 2024?"
              Resposta: "Não tenho informações necessárias para responder sua pergunta."

              Pergunta: "Você acha isso bom ou ruim?"
              Resposta: "Não tenho informações necessárias para responder sua pergunta."
          
              PERGUNTA DO USUÁRIO:
              {pergunta}
          
              RESPONDA A "PERGUNTA DO USUÁRIO"
          '''),
          ("human", "{pergunta}"),
      ])
    return prompt
