from reversi.game.player.interface import PlayerInterface
from reversi.game.board import Board
from reversi.game.cell import CellValue


class SimpleComputer(PlayerInterface):
    """単純CPUプレイヤー"""

    def __init__(self, color: CellValue, board: Board):
        super().__init__(color)
        self._board = board

    def _decide_move(self, cand_addrs: list[str]) -> str:
        flip_counts = {addr: self._board.get_flip_count(self._color, addr) for addr in cand_addrs}
        put_addr = max(flip_counts)
        print(self._color, f">> {put_addr}")
        return put_addr
