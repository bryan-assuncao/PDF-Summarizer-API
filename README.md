# PDF Summarizer API

Esta é uma API Flask que resume o conteúdo de arquivos PDF. A aplicação recebe um arquivo PDF, extrai seu texto, utiliza a API do Google Gemini para gerar um resumo executivo e, em seguida, cria um novo arquivo PDF com esse resumo, disponibilizando-o para download.

## Funcionalidades

* **Upload de PDF:** Envie arquivos PDF para a API.
* **Extração de Texto:** Extrai automaticamente o texto de documentos PDF.
* **Resumo com IA:** Utiliza o modelo `gemini-1.5-flash-latest` do Google para criar resumos concisos e de alta qualidade.
* **Geração de PDF:** Cria um novo arquivo PDF contendo o resumo gerado.
* **Endpoint de Download:** Fornece uma URL para baixar o PDF resumido.
* **Tratamento de Erros:** Valida os uploads de arquivos e a extração de texto, além de fornecer feedback claro em caso de falhas na API.

## Tecnologias Utilizadas

* **Flask:** Um microframework para Python usado para construir a API web.
* **PyMuPDF (fitz):** Uma biblioteca para extrair texto e dados de arquivos PDF.
* **fpdf2:** Uma biblioteca para a criação e geração de arquivos PDF.
* **google-generativeai:** A biblioteca cliente oficial do Python para a API do Google Gemini.
* **python-dotenv:** Para gerenciar variáveis de ambiente, como a chave da API.

## Configuração e Instalação

### Pré-requisitos

* Python 3.7+
* Uma chave de API do Google Gemini

### Passos

1. **Clone o repositório:**
   **Bash**

   ```
   git clone https://github.com/bryan-assuncao/PDF-Summarizer-API.git
   ```
2. **Crie e ative um ambiente virtual:**
   **Bash**

   ```
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```
3. **Instale as dependências:**
   **Bash**

   ```
   pip install -r requirements.txt
   ```
4. **Configure as variáveis de ambiente:**

   * Crie um arquivo chamado `.env` na raiz do projeto.
   * Adicione sua chave da API do Google Gemini ao arquivo `.env`:
     ```
     GOOGLE_API_KEY="SUA_CHAVE_DE_API_AQUI"
     ```
5. **Execute a aplicação:**
   **Bash**

   ```
   python main.py
   ```

   A aplicação estará disponível em `http://127.0.0.1:5006`.

## Endpoints da API

### `/summarize`

* **Método:** `POST`
* **Descrição:** Recebe um arquivo PDF, gera um resumo e retorna um link para download.
* **Formato do Corpo (form-data):**

  * `file`: O arquivo PDF a ser resumido.
* **Resposta de Sucesso (200 OK):**
  **JSON**

  ```
  {
      "original_filename": "nome_do_arquivo.pdf",
      "page_count": 5,
      "summary_text": "Este é o resumo gerado do documento...",
      "summary_pdf_url": "http://127.0.0.1:5006/download/resumo_uuid.pdf"
  }
  ```
* **Respostas de Erro:**

  * `400 Bad Request`: Se nenhum arquivo for enviado ou se o arquivo não for um PDF.
  * `500 Internal Server Error`: Se ocorrer um erro durante o processamento do arquivo ou se a chave da API do Gemini não estiver configurada.
  * `503 Service Unavailable`: Se a resposta da API do Gemini for bloqueada.

### `/download/<filename>`

* **Método:** `GET`
* **Descrição:** Permite o download do arquivo PDF resumido.
* **Parâmetros da URL:**
  * `filename`: O nome do arquivo PDF gerado (retornado pela rota `/summarize`).
* **Resposta de Sucesso (200 OK):**
  * O arquivo PDF para download.

## Como Usar

Você pode usar uma ferramenta como o `curl` ou o Postman para interagir com a API.

**Exemplo com `curl`:**

**Bash**

```
curl -X POST -F "file=@/caminho/para/seu/documento.pdf" http://127.0.0.1:5006/summarize
```
