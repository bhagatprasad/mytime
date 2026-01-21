from typing import Any, Dict, List
import re

def format_prompt(prompt: str) -> str:
    """Format and clean prompt"""
    if not prompt:
        return ""
    
    # Remove extra whitespace
    prompt = prompt.strip()
    
    # Remove multiple spaces
    prompt = re.sub(r'\s+', ' ', prompt)
    
    return prompt

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(input_string: str) -> str:
    """Sanitize user input"""
    if not input_string:
        return ""
    
    # Remove potentially dangerous characters
    return re.sub(r'[<>"\']', '', input_string.strip())

def format_response(data: Any, message: str = "Success", status: str = "success") -> Dict:
    """Format API response"""
    return {
        "status": status,
        "message": message,
        "data": data
    }