from enum import Enum


class CellValue(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2


class Cell:
    """マス情報クラス"""

    def __init__(self, value: CellValue = CellValue.EMPTY):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: CellValue):
        self._value = value

    def flip(self):
        """駒をひっくり返す"""
        if self._value == CellValue.BLACK:
            self._value = CellValue.WHITE
        elif self._value == CellValue.WHITE:
            self._value = CellValue.BLACK
