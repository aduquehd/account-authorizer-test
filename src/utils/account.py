# Python utils
from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    """
    Immutable account in-memory state
    """
    is_active_card: False
    available_limit: 0
    is_initialized: False
    is_premium: False
