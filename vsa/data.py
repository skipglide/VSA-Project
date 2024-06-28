from dataclasses import dataclass
from numpy import ndarray
from .vector import generate_symbol

@dataclass
class FHRR:
    symbol: ndarray

@dataclass
class BSC:
    symbol: ndarray