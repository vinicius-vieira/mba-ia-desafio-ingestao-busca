# Desafio MBA Engenharia de Software com IA - Full Cycle

## Geral

Essa aplicação faz a Ingestão e Busca Semântica com LangChain e Postgres.

## Configuração do Ambiente

Para configurar o ambiente e instalar as dependências do projeto, siga os passos abaixo:

1. **Criar e ativar um ambiente virtual (`venv`):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. **Instalar as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar as variáveis de ambiente:**

   - Duplique o arquivo `.env.example` e renomeie para `.env`
   - Abra o arquivo `.env` e substitua os valores pelas suas chaves de API reais.   

4. **Suba as imagens docker:**

   ```bash
   docker compose up -d
   ```

## Ingestão dos Dados

1. **Executar ingestão do PDF:**

   ```bash
   python src/ingest.py
   ```

## Executar a aplicação

1. **Rodar o chat:**

   ```bash
   python src/chat.py
   ```

Após a inicialização a aplicação irá permitir que o usuário faça perguntas via linha de comando (CLI) e receba respostas baseadas apenas no conteúdo do PDF.

**Exemplo no CLI**
```bash
Faça uma pergunta (ou 'sair' para encerrar):
Qual o faturamento da Empresa SuperTechIABrazil?

RESPOSTA: O faturamento da SuperTechIABrazil é de R$ 10.000.000,00.

Faça uma pergunta (ou 'sair' para encerrar):
Quantos clientes temos em 2024?

RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

Faça uma pergunta (ou 'sair' para encerrar):
sair
Encerrando a conversa. Até mais!
```