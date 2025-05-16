# MuffinsCorp AI Cliente Python

Uma biblioteca cliente em Python para a API MuffinsCorp AI.

## Instalação

```bash
pip install muffinscorp
```

## Começo Rápido

```python
import os
from muffinscorp import MuffinsCorp

# Definir chave da API como variável de ambiente
os.environ["MUFFINS_AI_API_KEY"] = "sua-chave-de-api-aqui"

# Inicializar cliente
client = MuffinsCorp()

# Enviar mensagem ao modelo de IA
response = client.chat.create(
    messages=[
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Olá, como você está hoje?"}
    ],
    model="chat-model-small",
    stream=False
)

print(response)
```

## Respostas em Fluxo Contínuo (Streaming)

```python
import os
from muffinscorp import MuffinsCorp

# Definir chave da API como variável de ambiente
os.environ["MUFFINS_AI_API_KEY"] = "sua-chave-de-api-aqui"

# Inicializar cliente
client = MuffinsCorp()

# Transmitir a resposta em fluxo
for chunk in client.chat.create(
    messages=[
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Escreva uma curta história sobre um robô padeiro."}
    ],
    model="chat-model-small",
    stream=True
):
    # Processar cada parte conforme chega
    print(chunk)
```

## Recursos Disponíveis

### Chat

Criar conclusões de chat com vários modelos.

```python
# Criar uma conclusão de chat
response = client.chat.create(
    messages=[
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Olá, como você está hoje?"}
    ],
    model="chat-model-small",
    stream=False
)
```

### Modelos

Listar modelos disponíveis.

```python
# Obter modelos disponíveis
models = client.models.list()
print(models)
```

### Assinaturas

Listar planos de assinatura disponíveis.

```python
# Obter planos de assinatura disponíveis
plans = client.subscriptions.list()
print(plans)
```

### Créditos

Verificar saldo da conta.

```python
# Obter saldo de créditos
balance = client.credits.get_balance()
print(f"Créditos restantes: {balance['credits']}")
```

## Tratamento de Erros

```python
from muffinscorp import MuffinsCorp, AuthenticationError, CreditError

try:
    client = MuffinsCorp(api_key="chave-inválida")
    response = client.chat.create(
        messages=[{"role": "user", "content": "Olá"}]
    )
except AuthenticationError as e:
    print(f"Erro de autenticação: {e}")
except CreditError as e:
    print(f"Erro de crédito: {e}, créditos restantes: {e.credits_remaining}")
except Exception as e:
    print(f"Erro geral: {e}")
```

## Licença

MIT
