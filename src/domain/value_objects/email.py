"""Email value object"""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """Immutable Email value object with validation"""
    
    value: str
    
    def __post_init__(self):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, self.value):
            raise ValueError(f"Invalid email format: {self.value}")
    
    def __str__(self) -> str:
        """String representation"""
        return self.value
    
    def domain(self) -> str:
        """Extract email domain"""
        return self.value.split('@')[1]
