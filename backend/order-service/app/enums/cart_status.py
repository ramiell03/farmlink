from enum import Enum
import enum

class CartStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ORDERED = "ORDERED"