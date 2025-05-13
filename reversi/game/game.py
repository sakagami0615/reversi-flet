from reversi.game.player.user_input import UserInput
from reversi.game.player.simple_computer import SimpleComputer
from reversi.game.board import Board
from reversi.game.controller import Controller
from reversi.game.cell import CellValue



class Game:
    """リバーシ本体"""

    def __init__(self):
        self._board = Board()
        
        """
        self._control = Controller(
            UserInput(CellValue.WHITE),
            SimpleComputer(CellValue.BLACK, self._board)
        )
        """
        self._control = Controller(
            SimpleComputer(CellValue.WHITE, self._board),
            SimpleComputer(CellValue.BLACK, self._board)
        )

    def _display_result(self) -> None:
        values = self._board.count_value()
        
        n_black = values[CellValue.BLACK]
        n_white = values[CellValue.WHITE]
        print("----- Result -----")
        print(f"black: {n_black}, white: {n_white}")
        if n_white > n_black:
            print("WHITE WON!")
        elif n_white < n_black:
            print("BLACK WON!")
        else:
            print("DRAW...")
        

    def run(self):
        while (self._control.n_pass < 2) and (not self._board.is_fill()):
            self._board.display(self._control.curr_player.color)
            cand_addrs = self._board.get_enable_put_address(self._control.curr_player.color)
            put_addr = self._control.action(cand_addrs)
            if put_addr is not None:
                self._board.put(self._control.curr_player.color, put_addr)
            self._control.turn_change()

        self._display_result()
