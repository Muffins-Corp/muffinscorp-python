from typing import Dict, List, Any, Optional
import uuid


def parse_stream_chunk(chunk: bytes) -> Dict[str, Any]:
    """
    Parse stream data according to the format used by the API.
    
    Args:
        chunk: Raw chunk from stream
        
    Returns:
        Parsed data object
    """
    try:
        # This assumes chunks are sent as JSON objects with a data field
        # Adjust according to your API's actual stream format
        data = chunk.decode('utf-8')
        return {"text": data}
    except Exception:
        # If parsing fails, return the raw chunk as text
        return {"text": str(chunk)}


def format_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Formats messages in the expected structure for the API.
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        Formatted message list
        
    Raises:
        ValueError: If a message is missing required fields or has invalid role
    """
    allowed_roles = ["system", "user", "assistant"]
    
    formatted_messages = []
    for msg in messages:
        # Ensure each message has the required role and content properties
        if not msg.get("role") or not msg.get("content"):
            raise ValueError("Each message must have a role and content")
        
        # Ensure role is one of the expected values
        if msg["role"] not in allowed_roles:
            raise ValueError(
                f"Invalid message role: {msg['role']}. Must be one of: {', '.join(allowed_roles)}"
            )
        
        formatted_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    return formatted_messages


def generate_uuid() -> str:
    """
    Generates a UUID v4.
    
    Returns:
        A random UUID string
    """
    return str(uuid.uuid4())
