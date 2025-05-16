# MuffinsCorp AI Python Client

A Python client library for the MuffinsCorp AI API.

## Installation

```bash
pip install muffinscorp
```

## Quick Start

```python
import os
from muffinscorp import MuffinsCorp

# Set API key as environment variable
os.environ["MUFFINS_AI_API_KEY"] = "your-api-key-here"

# Initialize client
client = MuffinsCorp()

# Send a message to the AI model
response = client.chat.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you today?"}
    ],
    model="chat-model-small",
    stream=False
)

print(response)
```

## Streaming Responses

```python
import os
from muffinscorp import MuffinsCorp

# Set API key as environment variable
os.environ["MUFFINS_AI_API_KEY"] = "your-api-key-here"

# Initialize client
client = MuffinsCorp()

# Stream the response
for chunk in client.chat.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a short story about a robot baker."}
    ],
    model="chat-model-small",
    stream=True
):
    # Process each chunk as it arrives
    print(chunk)
```

## Available Resources

### Chat

Create chat completions with various models.

```python
# Create a chat completion
response = client.chat.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you today?"}
    ],
    model="chat-model-small",
    stream=False
)
```

### Models

List available models.

```python
# Get available models
models = client.models.list()
print(models)
```

### Subscriptions

List available subscription plans.

```python
# Get available subscription plans
plans = client.subscriptions.list()
print(plans)
```

### Credits

Check your account balance.

```python
# Get credit balance
balance = client.credits.get_balance()
print(f"Credits remaining: {balance['credits']}")
```

## Error Handling

```python
from muffinscorp import MuffinsCorp, AuthenticationError, CreditError

try:
    client = MuffinsCorp(api_key="invalid-key")
    response = client.chat.create(
        messages=[{"role": "user", "content": "Hello"}]
    )
except AuthenticationError as e:
    print(f"Authentication error: {e}")
except CreditError as e:
    print(f"Credit error: {e}, remaining credits: {e.credits_remaining}")
except Exception as e:
    print(f"General error: {e}")
```

## License

MIT
