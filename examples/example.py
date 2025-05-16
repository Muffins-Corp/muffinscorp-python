import os
import time
from typing import Dict, Any, List
from datetime import datetime
from muffinscorp import MuffinsCorp

def format_date(date_str: str | None) -> str:
    if date_str is None:
        return 'N/A'
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        return date_str
    
def display_balance(client: MuffinsCorp) -> None:
    """Exibe o saldo de créditos do usuário com base na estrutura fornecida."""
    try:
        balance_data = client.credits.get_balance()
        
        if not balance_data.get('success', False):
            print("\n⚠️ Não foi possível obter o saldo")
            return
            
        balance = balance_data.get('balance', {})
        
        print("\n🔹 Saldo de Créditos:")
        print(f"  • Total: {balance.get('totalBalance', 'N/A')}")
        print(f"  • Regular: {balance.get('regularBalance', 'N/A')}")
        print(f"  • Diário: {balance.get('dailyBalance', 'N/A')}")
        print(f"  • Tem crédito diário? {'Sim' if balance.get('hasDailyCredit') else 'Não'}")
        
        # Mostrar créditos individuais
        if 'credits' in balance and balance['credits']:
            print("\n  💳 Créditos individuais:")
            for credit in balance['credits']:
                print(f"    - ID: {credit.get('id')}")
                print(f"      Valor: {credit.get('amount')} (usados: {credit.get('usedAmount')})")
                print(f"      Tipo: {credit.get('type')}")
                print(f"      Expira em: {format_date(credit.get('expiresAt'))}")
                
        # Mostrar crédito diário se existir
        if 'dailyCredit' in balance and balance['dailyCredit']:
            daily = balance['dailyCredit']
            print("\n  🌞 Crédito diário:")
            print(f"    - Concedido: {daily.get('grantedAmount')}")
            print(f"    - Disponível: {daily.get('amount')}")
            print(f"    - Data: {daily.get('grantedDate')}")
            print(f"    - Já usado? {'Sim' if daily.get('used') else 'Não'}")
            
    except Exception as e:
        print(f"\n⚠️ Erro ao obter saldo: {e}")

def list_available_models(client: MuffinsCorp) -> None:
    """Lista os modelos disponíveis na API com base na estrutura fornecida."""
    try:
        models = client.models.list()
        print("\n📊 Modelos disponíveis:")
        
        if not models:
            print("  Nenhum modelo disponível")
            return
            
        for idx, model in enumerate(models, 1):
            print(f"  {idx}. {model.get('name', 'N/A')} (ID: {model.get('id')})")
            print(f"     Tipo: {model.get('type')}")
            print(f"     Custo: {model.get('costInCreditPerUse')} créditos por uso")
            print(f"     Máx tokens: {model.get('max_tokens')}")
            print(f"     Ativo? {'Sim' if model.get('isActive') else 'Não'}")
            print(f"     Criado em: {format_date(model.get('createdAt'))}\n")
            
    except Exception as e:
        print(f"\n⚠️ Erro ao listar modelos: {e}")

def streaming_chat_example(client: MuffinsCorp, messages: List[Dict[str, str]]) -> None:
    """Demonstra o uso do chat com streaming."""
    print("\n🌀 Gerando resposta (streaming)...")
    try:
        print("\n💬 Resposta:", end=" ")
        for chunk in client.chat.create(
            messages=messages,
            model="chat-model-small",
            stream=True
        ):
            if isinstance(chunk, dict):
                # Se for um dicionário, verifica a chave 'text'
                content = chunk.get('text', '')
                if content:
                    print(content, end="", flush=True)
            elif isinstance(chunk, str):
                # Se for string direta, imprime normalmente
                print(chunk, end="", flush=True)
            
            time.sleep(0.01)
        print("\n")
    except Exception as e:
        print(f"\n⚠️ Erro durante a streaming: {e}")
def complete_chat_example(client: MuffinsCorp, messages: List[Dict[str, str]]) -> None:
    """Demonstra o uso do chat com resposta completa."""
    print("\n🔄 Gerando resposta (completa)...")
    try:
        response = client.chat.create(
            messages=messages,
            model="chat-model-small",
            stream=False
        )
        print("\n💬 Resposta completa:")
        
        # Verifica se a resposta é um dicionário
        if isinstance(response, dict):
            print(f"ID: {response.get('id', 'N/A')}")
            print(f"Conteúdo: {response.get('content', 'N/A')}")
            print(f"Modelo usado: {response.get('model', 'N/A')}")
            print(f"Créditos usados: {response.get('creditsUsed', 'N/A')}")
            print(f"Créditos restantes: {response.get('creditsRemaining', 'N/A')}")
            print(f"Criado em: {format_date(response.get('createdAt', 'N/A'))}")
        
        # Verifica se a resposta é uma string (caso o conteúdo venha diretamente)
        elif isinstance(response, str):
            print(f"Conteúdo: {response}")
        
        # Caso seja uma lista de respostas
        elif isinstance(response, list):
            for item in response:
                if isinstance(item, dict):
                    print(f"\nID: {item.get('id', 'N/A')}")
                    print(f"Conteúdo: {item.get('content', 'N/A')}")
                    print(f"Modelo usado: {item.get('model', 'N/A')}")
                    print(f"Créditos usados: {item.get('creditsUsed', 'N/A')}")
                    print(f"Créditos restantes: {item.get('creditsRemaining', 'N/A')}")
                    print(f"Criado em: {format_date(item.get('createdAt', 'N/A'))}")
                else:
                    print(f"Item da resposta: {item}")
        
        # Outros tipos de resposta
        else:
            print(f"Resposta recebida em formato não esperado: {response}")

    except Exception as e:
        print(f"\n⚠️ Erro ao gerar resposta: {e}")
def get_api_key() -> str:
    """Obtém a chave de API do ambiente ou do usuário."""
    api_key = os.environ.get("MUFFINS_AI_API_KEY")
    if not api_key:
        print("\n🔐 AVISO: A variável de ambiente MUFFINS_AI_API_KEY não está definida.")
        api_key = input("Por favor, insira sua chave de API: ").strip()
        if not api_key:
            raise ValueError("A chave de API é obrigatória para continuar")
    return api_key

def main() -> None:
    """Função principal que demonstra o uso da biblioteca MuffinsCorp."""
    print("\n" + "="*50)
    print("  DEMONSTRAÇÃO DA BIBLIOTECA MUFFINS-AI  ".center(50))
    print("="*50)
    
    try:
        # Obter e validar a chave de API
        api_key = get_api_key()
        
        # Inicializar o cliente
        client = MuffinsCorp(api_key=api_key)
        print("\n✅ Cliente MuffinsCorp inicializado com sucesso!")
        
        # Exibir informações
        display_balance(client)
        list_available_models(client)
        
        # Configurar mensagens de exemplo
        messages = [
            {"role": "system", "content": "Você é um assistente útil que responde em português."},
            {"role": "user", "content": "Olá! Pode me dar três ideias criativas para um projeto de ciências do ensino médio?"}
        ]
        
        # Demonstrar funcionalidades
        streaming_chat_example(client, messages)
        complete_chat_example(client, messages)
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Operação cancelada pelo usuário.")
    except ValueError as ve:
        print(f"\n❌ Erro de validação: {ve}")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
    finally:
        print("\n" + "="*50)
        print("  FIM DA DEMONSTRAÇÃO  ".center(50))
        print("="*50 + "\n")

if __name__ == "__main__":
    main()