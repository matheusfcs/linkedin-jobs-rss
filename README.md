# LinkedIn RSS Feed Generator

Este projeto gera um feed RSS consolidado a partir de múltiplas buscas de vagas no LinkedIn.

## Como funciona

- Você define os links das buscas no arquivo `urls.txt`.
- O script `linkedin_rss.py` faz scraping das vagas.
- Um arquivo `feed.xml` é gerado com os dados.
- GitHub Actions atualiza isso automaticamente diariamente.
- RSS hospedado via GitHub Pages.

## Setup

1. Faça fork deste repositório.
2. Vá em **Settings > Pages** e ative GitHub Pages no branch `main`, pasta `/ (root)`.
3. Use o link `https://<seu-usuário>.github.io/linkedin-rss/feed.xml` no seu leitor RSS.

## Exemplo de uso

Edite o arquivo `urls.txt` com suas buscas personalizadas do LinkedIn.

```
https://www.linkedin.com/jobs/search/?keywords=python&location=remote
https://www.linkedin.com/jobs/search/?keywords=flutter&location=brazil
```
