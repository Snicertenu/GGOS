"""
Exercise model for GGOS
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class UnitType(Enum):
    """Types of units for exercises"""
    REPS = "reps"
    SECONDS = "seconds"


@dataclass
class Exercise:
    """Represents an exercise with its configuration"""
    name: str
    unit_type: UnitType
    amount_per_death: int
    id: Optional[str] = None
    
    def __post_init__(self):
        """Generate ID if not provided"""
        if self.id is None:
            import uuid
            self.id = str(uuid.uuid4())
    
    def calculate_total(self, deaths: int) -> int:
        """Calculate total amount for given number of deaths"""
        return self.amount_per_death * deaths
    
    def get_unit_display(self) -> str:
        """Get display string for unit type"""
        return self.unit_type.value
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        return {
            'id': self.id,
            'name': self.name,
            'unit_type': self.unit_type.value,
            'amount_per_death': self.amount_per_death
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Exercise':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            name=data['name'],
            unit_type=UnitType(data['unit_type']),
            amount_per_death=data['amount_per_death']
        )
