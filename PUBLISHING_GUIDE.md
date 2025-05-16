# Guia para Publicar sua Biblioteca Python no PyPI

Este guia explica como empacotar e publicar a biblioteca `muffins-ai` no PyPI (Python Package Index), tornando-a disponível para instalação com pip.

## Pré-requisitos

1. Criar uma conta no PyPI (https://pypi.org/account/register/)
2. Instalar ferramentas de empacotamento:
   ```bash
   pip install build twine
   ```

## Estrutura do Projeto

A estrutura do projeto deve ser como a seguir:

```
muffins-ai/
├── pyproject.toml
├── README.md
├── LICENSE
└── muffinscorp/
    ├── __init__.py
    ├── client.py
    ├── exceptions.py
    └── utils.py
```

## Passo a Passo para Publicação

### 1. Preparar o projeto

Certifique-se de que todos os arquivos estão organizados conforme a estrutura acima e que o `pyproject.toml` está corretamente configurado.

### 2. Criar o arquivo LICENSE

Crie um arquivo LICENSE com o texto da licença MIT ou outra de sua escolha.

### 3. Construir o pacote

Na pasta raiz do projeto, execute:

```bash
python -m build
```

Isso criará os pacotes de distribuição na pasta `dist/`:

- `muffinscorp-0.1.0-py3-none-any.whl` (formato wheel)
- `muffinscorp-0.1.0.tar.gz` (formato source)

### 4. Testar o pacote localmente (opcional)

Você pode instalar e testar o pacote localmente antes de publicá-lo:

```bash
pip install dist/muffinscorp-0.1.0-py3-none-any.whl
```

Teste se o pacote funciona corretamente:

```python
from muffinscorp import MuffinsCorp
# Teste a funcionalidade básica
```

### 5. Publicar no TestPyPI (recomendado)

Antes de publicar no PyPI oficial, é recomendável testar no TestPyPI:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Você será solicitado a inserir seu nome de usuário e senha do TestPyPI.

Teste a instalação a partir do TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ muffins-ai
```

### 6. Publicar no PyPI oficial

Se o teste no TestPyPI for bem-sucedido, publique no PyPI oficial:

```bash
twine upload dist/*
```

Insira seu nome de usuário e senha do PyPI quando solicitado.

### 7. Verificar a publicação

Após alguns minutos, seu pacote estará disponível para instalação através do pip:

```bash
pip install muffins-ai
```

## Atualizando o Pacote

Para publicar uma nova versão:

1. Atualize o número da versão em `muffinscorp/__init__.py` e `pyproject.toml`
2. Repita os passos 3-6 acima

## Automação com GitHub Actions (opcional)

Para automatizar o processo de publicação, você pode configurar um fluxo de trabalho do GitHub Actions que publica automaticamente ao PyPI quando você cria uma nova tag.

Crie um arquivo `.github/workflows/publish.yml`:

```yaml
name: Publish Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.x"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      - name: Build and publish
        env:
          TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
          TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
        run: |
          python -m build
          twine upload dist/*
```

## Dicas Adicionais

1. **Documentação**: Considere criar documentação mais detalhada com Sphinx ou MkDocs.
2. **Testes**: Adicione testes unitários usando pytest antes de publicar.
3. **Badges**: Adicione badges ao seu README.md para mostrar status de build, cobertura de testes, etc.
4. **CHANGELOG.md**: Mantenha um registro de alterações para cada versão.
