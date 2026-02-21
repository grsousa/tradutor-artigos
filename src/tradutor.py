# -*- coding: utf-8 -*-
"""Módulo principal do Tradutor de Artigos."""

import os
import argparse

import requests
from bs4 import BeautifulSoup
from langchain_openai.chat_models.azure import AzureChatOpenAI


def extract_text_from_url(url: str) -> str | None:
    """Extrai e limpa o texto de um artigo a partir de uma URL."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Falha ao acessar {url}. Código: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    texto = soup.get_text(separator=" ")
    lines = (line.strip() for line in texto.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return "\n".join(chunk for chunk in chunks if chunk)


def get_client() -> AzureChatOpenAI:
    """Cria o cliente Azure OpenAI a partir das variáveis de ambiente."""
    return AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
        deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
        max_retries=0,
    )


def translate_article(text: str, lang: str, client: AzureChatOpenAI | None = None) -> str:
    """Traduz o texto para o idioma especificado."""
    if client is None:
        client = get_client()

    messages = [
        {"role": "system", "content": "Você é um tradutor de artigos científicos. Mantenha a formatação e responda em markdown."},
        {"role": "user", "content": f"Traduza o seguinte texto para {lang}:\n\n{text}"},
    ]
    response = client.invoke(messages)
    return response.content


def main():
    """Interface de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Traduz artigos da web usando IA (Azure OpenAI)"
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="URL do artigo a ser traduzido",
    )
    parser.add_argument(
        "-l",
        "--lang",
        default="português",
        help="Idioma de destino (padrão: português)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Arquivo de saída para salvar a tradução",
    )
    args = parser.parse_args()

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    required = ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print("Erro: configure as variáveis de ambiente:", ", ".join(missing))
        print("Veja .env.example para referência.")
        return 1

    if args.url:
        text = extract_text_from_url(args.url)
        if text:
            print("Traduzindo...")
            result = translate_article(text, args.lang)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(result)
                print(f"Tradução salva em {args.output}")
            else:
                print(result)
    else:
        parser.print_help()
        print("\nExemplo:")
        print('  python main.py "https://dev.to/artigo" -l português -o artigo_pt.md')

    return 0


if __name__ == "__main__":
    exit(main())
