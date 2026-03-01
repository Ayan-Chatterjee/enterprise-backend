"""Phone value object"""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Phone:
    """Immutable Phone value object with validation"""
    
    value: str
    
    def __post_init__(self):
        """Validate phone format"""
        # Basic phone validation - allows +country code and numbers
        pattern = r'^\+?1?\d{9,15}$'
        clean = re.sub(r'[\s\-\(\)]', '', self.value)
        if not re.match(pattern, clean):
            raise ValueError(f"Invalid phone format: {self.value}")
    
    def __str__(self) -> str:
        """String representation"""
        return self.value
    
    def is_international(self) -> bool:
        """Check if phone number is international"""
        return self.value.startswith('+')
