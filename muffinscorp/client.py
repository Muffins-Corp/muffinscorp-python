import os
import json
from typing import Dict, List, Union, Optional, Generator, Any
import uuid
from datetime import datetime

import requests
from requests.exceptions import RequestException
from sseclient import SSEClient

from .exceptions import AuthenticationError, CreditError
from .utils import format_messages, parse_stream_chunk


class MuffinsCorp:
    """Main client for MuffinsCorp API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the MuffinsCorp client.
        
        Args:
            api_key: API key for authentication. If not provided, will look for MUFFINS_AI_API_KEY env variable.
            base_url: Base URL for the API. Defaults to the official API endpoint.
        """
        self.api_key = api_key or os.environ.get("MUFFINS_AI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as MUFFINS_AI_API_KEY environment variable")
            
        self.base_url = base_url or "https://chat.muffinscorp.com/api/public"
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        })
        
        # Initialize resource classes
        self.chat = Chat(self)
        self.models = Models(self)
        self.subscriptions = Subscriptions(self)
        self.credits = Credits(self)
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response: # type: ignore
        """
        Makes a request to the API.
        
        Args:
            method: HTTP method to use
            endpoint: API endpoint to call
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.HTTPError as e:
            self._handle_http_error(e.response)
        except RequestException as e:
            raise Exception(f"Request error: {str(e)}")
    
    def _handle_http_error(self, response: requests.Response) -> None:
        """
        Handle HTTP errors from the API.
        
        Args:
            response: Response object from failed request
        
        Raises:
            AuthenticationError: For authentication-related failures
            CreditError: For credit-related failures
            Exception: For other API errors
        """
        status_code = response.status_code
        
        try:
            data = response.json()
        except ValueError:
            data = {"error": response.text}
        
        if status_code in (401, 403):
            raise AuthenticationError(
                message=data.get("error", "Authentication failed"),
                status_code=status_code,
                error_code=data.get("code", "AUTHENTICATION_ERROR")
            )
        
        if status_code == 402:
            raise CreditError(
                message=data.get("error", "Insufficient credits"),
                status_code=status_code,
                error_code=data.get("code", "INSUFFICIENT_CREDITS"),
                credits_remaining=int(data.get("creditsRemaining", 0))
            )
        
        # Generic error for other cases
        raise Exception(
            f"API Error ({status_code}): {data.get('error') or data.get('message') or 'Unknown error'}"
        )


class Chat:
    """Chat completions resource."""
    
    def __init__(self, client: MuffinsCorp):
        """
        Initialize the Chat resource.
        
        Args:
            client: MuffinsCorp client instance
        """
        self.client = client
    
    def _handle_stream(self, response: requests.Response) -> Generator[Dict[str, Any], None, None]:
        """
        Handle streaming response from the API.
        
        Args:
            response: Streaming response from the API
                
        Yields:
            Parsed response chunks
        """
        def chunk_generator():
            for chunk in response.iter_content(chunk_size=1024):
                yield chunk

        client = SSEClient(chunk_generator())
            
        for event in client.events():
            if event.data == "[DONE]":
                break
                    
            try:
                yield json.loads(event.data)
            except json.JSONDecodeError:
                yield {"text": event.data}

    def create(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "chat-model-small", 
        stream: bool = True
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        """
        Creates a chat completion.
        
        Args:
            messages: List of message dictionaries (role and content)
            model: Model ID to use
            stream: Whether to stream the response
                
        Returns:
            If stream=True, returns a generator yielding response chunks
            If stream=False, returns the complete response as a dictionary
        """
        if not isinstance(messages, list) or len(messages) == 0:
            raise ValueError("Messages must be a non-empty list")
            
        payload = {
            "messages": messages,
            "model": model,
            "stream": stream
        }
            
        if stream:
            response = self.client._request(
                "post",
                "/chat",
                json=payload,
                stream=True
            )
            return self._handle_stream(response)
        else:
            response = self.client._request(
                "post",
                "/chat",
                json=payload
            )
            return response.json()


class Models:
    """Models resource."""
    
    def __init__(self, client: MuffinsCorp):
        """
        Initialize the Models resource.
        
        Args:
            client: MuffinsCorp client instance
        """
        self.client = client
    
    def list(self) -> List[Dict[str, Any]]:
        """
        List available models.
        
        Returns:
            List of model objects with structure:
            {
                "id": "string",
                "valueId": "string",
                "name": "string",
                "type": "string",
                "costInCreditPerUse": int,
                "isActive": bool,
                "createdAt": "datetime",
                "totalUses": "string",
                "totalCreditsSpent": "string",
                "max_tokens": int
            }
        """
        response = self.client._request("get", "/ai-model")
        return response.json()


class Subscriptions:
    """Subscriptions resource."""
    
    def __init__(self, client: MuffinsCorp):
        """
        Initialize the Subscriptions resource.
        
        Args:
            client: MuffinsCorp client instance
        """
        self.client = client
    
    def list(self) -> List[Dict[str, Any]]:
        """
        List available subscription plans.
        
        Returns:
            List of plan objects
        """
        response = self.client._request("get", "/subscription")
        return response.json()


class Credits:
    """Credits resource."""
    
    def __init__(self, client: MuffinsCorp):
        """
        Initialize the Credits resource.
        
        Args:
            client: MuffinsCorp client instance
        """
        self.client = client
    
    def get_balance(self) -> Dict[str, Any]:
        """
        Get current credit balance.
        
        Returns:
            Balance information with structure:
            {
                "balance": {
                    "regularBalance": int,
                    "dailyBalance": int,
                    "totalBalance": int,
                    "hasDailyCredit": bool,
                    "credits": [
                        {
                            "id": "string",
                            "userId": "string",
                            "amount": int,
                            "expiresAt": "datetime",
                            "extendedExpiresAt": "datetime",
                            "createdAt": "datetime",
                            "usedAmount": int,
                            "type": "string"
                        }
                    ],
                    "dailyCredit": {
                        "id": "string",
                        "userId": "string",
                        "grantedAmount": int,
                        "amount": int,
                        "grantedDate": "date",
                        "used": bool
                    }
                },
                "success": bool,
                "timestamp": "datetime"
            }
        """
        response = self.client._request("get", "/user/balance")
        return response.json()