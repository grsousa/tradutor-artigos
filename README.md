# 📖 Tradutor de Artigos

Traduza artigos da web para qualquer idioma usando IA. Extrai o conteúdo de URLs e traduz com Azure OpenAI (GPT-4o-mini ou similar), preservando formatação em Markdown.

## Funcionalidades

- **Extração de texto** — Remove scripts, estilos e formatação HTML
- **Tradução com IA** — Usa Azure OpenAI para traduções contextuais
- **CLI** — Uso simples pela linha de comando
- **Módulo Python** — Importável para uso em seus projetos

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/article-translator.git
cd article-translator

# Crie um ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt
```

## Configuração

1. Copie o arquivo de exemplo e edite com suas credenciais:

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/Mac
```

2. Preencha as variáveis no `.env`:

| Variável | Descrição |
|----------|-----------|
| `AZURE_OPENAI_ENDPOINT` | URL do seu recurso Azure OpenAI |
| `AZURE_OPENAI_API_KEY` | Chave de API |
| `AZURE_OPENAI_API_VERSION` | Versão da API (opcional) |
| `AZURE_OPENAI_DEPLOYMENT` | Nome do deployment (opcional, padrão: gpt-4o-mini) |


## Uso

### Linha de comando

```bash
# Traduzir um artigo (exibe no terminal)
python main.py "https://dev.to/artigo-sobre-ia"
# ou: python -m src.tradutor "https://dev.to/artigo-sobre-ia"

# Salvar tradução em arquivo
python main.py "https://exemplo.com/artigo" -o artigo_traduzido.md

# Especificar idioma de destino
python main.py "https://exemplo.com/artigo" -l "inglês" -o artigo_en.md
```

### Como módulo Python

```python
from src.tradutor import extract_text_from_url, translate_article

# Extrair texto de uma URL
texto = extract_text_from_url("https://dev.to/artigo")
if texto:
    # Traduzir
    traducao = translate_article(texto, "português")
    print(traducao)
```

## Estrutura do projeto

```
article-translator/
├── src/
│   ├── __init__.py
│   └── tradutor.py      # Módulo principal
├── main.py              # Ponto de entrada
├── .env.example         # Template de configuração
├── .gitignore
├── requirements.txt
└── README.md
```

