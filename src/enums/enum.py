from enum import Enum


class Account_status(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    

class Wallet_status(Enum):
    FROZEN = "Frozen"
    UNFROZEN = "Unfrozen"