from reversi.game.player.interface import PlayerInterface
from reversi.game.cell import CellValue


class UserInput(PlayerInterface):
    """ユーザー操作用プレイヤー"""

    def __init__(self, color: CellValue):
        super().__init__(color)

    def _decide_move(self, cand_addrs: list[str]) -> str:

        while True:
            print(self._color, cand_addrs)
            put_addr = input(">> ")
            if put_addr in cand_addrs:
                break
            print(f"WARNING: You cannot place a piece on {put_addr} address.")
        return put_addr
