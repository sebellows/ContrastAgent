import json
from enum import Enum
from dataclasses import is_dataclass, fields
from datetime import datetime, date
from typing import Any


def serialize(obj: Any) -> Any:
    """
    Serializes a Python dictionary containing non-JSON types into a JSON-compatible format.
    
    Handles the following Python types:
    - Basic types (int, float, str, bool, None)
    - Complex types (dict, list)
    - Special types (set, tuple, Enum)
    - Date/time objects
    
    Args:
        obj: Any Python object to serialize
        
    Returns:
        JSON-serializable version of the input object
        
    Examples:
        >>> from enum import Enum
        >>> class Color(Enum):
        ...     RED = 1
        ...     BLUE = 2
        >>> data = {
        ...     'set': {1, 2, 3},
        ...     'tuple': (4, 5, 6),
        ...     'color': Color.RED
        ... }
        >>> serialize(data)
        {
            'set': [1, 2, 3],
            'tuple': [4, 5, 6],
            'color': 1
        }
    """
    if is_dataclass(obj):
        if '__pydantic_validator__' in obj.__dict__:
            # Pydantic dataclass
            return obj.model_dump()
        # Regular dataclass
        return {
            field.name: serialize(getattr(obj, field.name))
            for field in fields(obj)
        }
    
    elif isinstance(obj, dict):
        return {key: serialize(value) for key, value in obj.items()}
    
    elif isinstance(obj, (list, tuple)):
        if isinstance(obj, tuple):
            return [serialize(item) for item in obj]
        return [serialize(item) for item in obj]
    
    elif isinstance(obj, set):
        return [serialize(item) for item in sorted(obj)]
    
    elif isinstance(obj, Enum):
        return obj.value
    
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    
    elif isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj
    
    else:
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def to_json(obj: Any, indent: int = 2) -> str:
    """
    Converts a Python object to a JSON string, handling non-JSON types.
    
    Args:
        obj: Python object to convert
        indent: Number of spaces for indentation (default: 2)
        
    Returns:
        JSON string representation of the object
    """
    return json.dumps(serialize(obj), indent=indent)
