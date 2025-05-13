from typing import Union
from abc import ABC, abstractmethod

from reversi.game.cell import CellValue


class PlayerInterface(ABC):
    """プレイヤーインタフェースクラス"""

    def __init__(self, color: CellValue):
        # 指定色無しの場合はエラーにする
        if color.value == CellValue.EMPTY:
            raise ValueError("プレイヤーの駒色にはCellValue.EMPTYを与えることはできません")

        self._color = color

    @property
    def color(self):
        return self._color
    
    @abstractmethod
    def _decide_move(self, cand_addrs: list[str]) -> str:
        """置くコマの場所を決定する関数(純粋仮想関数)"""
        pass

    def action(self, cand_addrs: list[str]) -> Union[str, None]:
        """行動関数"""
        if len(cand_addrs) == 0:
            print(self._color, "pass")
            return None

        return self._decide_move(cand_addrs)