from typing import Union

from collections import defaultdict
from string import ascii_lowercase

from reversi.game.cell import CellValue, Cell


class BoardViewerMixin:
    """盤面描画用Mixin"""

    def display(self, color: CellValue):
        marks = ["‐", "●", "○"]

        cand_addrs = self.get_enable_put_address(color)

        print("   " + " ".join(ascii_lowercase[:self.SIZE]))
        for i in range(Board.SIZE):
            line = f"{i + 1:02} "
            for j in range(Board.SIZE):
                mark = marks[self._cells[i][j].value.value]
                if mark == marks[0] and self._pos2addr[(i, j)] in cand_addrs:
                    mark = "P"
                line += mark + " "
            print(line)


class Board(BoardViewerMixin):
    """盤面管理クラス"""

    SIZE = 8

    def __init__(self):
        # 盤面初期化
        self._cells = [[Cell() for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]
        self._cells[Board.SIZE // 2 - 1][Board.SIZE // 2 - 1].value = CellValue.WHITE
        self._cells[Board.SIZE // 2 - 1][Board.SIZE // 2    ].value = CellValue.BLACK
        self._cells[Board.SIZE // 2    ][Board.SIZE // 2 - 1].value = CellValue.BLACK
        self._cells[Board.SIZE // 2    ][Board.SIZE // 2    ].value = CellValue.WHITE

        # 座標(row, col)とアドレス(a1等)を相互に変換するための辞書
        self._pos2addr = {(i, j): f"{ascii_lowercase[j]}{i + 1}" for i in range(self.SIZE) for j in range(self.SIZE)}
        self._addr2pos = {v: k for k, v in self._pos2addr.items()}

    def _is_over_boundary(self, row, col):
        """指定位置が盤面内の座標かを判定する"""
        return row < 0 or col < 0 or row >= self.SIZE or col >= self.SIZE

    def _get_flip_line_count(self, color: CellValue, row: int, col: int, d_row: int, d_col: int) -> int:
        """一方向の反転できる数をカウント"""
        if d_row == 0 and d_col == 0:
            return 0

        # own: 自分、opp: 敵
        own_color = CellValue.BLACK if color == CellValue.BLACK else CellValue.WHITE
        opp_color = CellValue.WHITE if color == CellValue.BLACK else CellValue.BLACK

        curr_row, curr_col, n_flips = row, col, 0
        while True:
            # マスを進める
            curr_row += d_row
            curr_col += d_col
            # はみ出した場合、ひっくり返すものはない
            if self._is_over_boundary(curr_row, curr_col):
                n_flips = 0
                break

            # 自信と反対色の場合は、カウントをインクリメント
            if self._cells[curr_row][curr_col].value == opp_color:
                n_flips += 1
            # 自信と同じ色があったら、それまでにカウントした値がひっくり返せる個数となる
            elif self._cells[curr_row][curr_col].value == own_color:
                break
            # 空マスの場合、ひっくり返すものはない
            else:
                n_flips = 0
                break

        return n_flips

    def _flip_line(self, color: CellValue, row: int, col: int, d_row: int, d_col: int) -> int:
        """一方向の駒を反転する"""
        if d_row == 0 and d_col == 0:
            return 0
        
        # ひっくり返すものがない場合は、処理せずに終了
        n_flips = self._get_flip_line_count(color, row, col, d_row, d_col)
        if n_flips == 0:
            return 0

        # own: 自分、opp: 敵
        own_color = CellValue.BLACK if color == CellValue.BLACK else CellValue.WHITE
        opp_color = CellValue.WHITE if color == CellValue.BLACK else CellValue.BLACK

        # 指定したマスに駒を置く
        self._cells[row][col].value = own_color

        # ひっくり返す
        curr_row, curr_col = row + d_row, col + d_col
        while self._cells[curr_row][curr_col].value == opp_color:
            self._cells[curr_row][curr_col].flip()            
            curr_row += d_row
            curr_col += d_col

        return n_flips

    def get_flip_count(self, color: CellValue, address=str) -> int:
        """指定マスに置いた際にひっくり返せる駒の個数を取得"""
        # 指定色無しの場合はエラーにする
        if color == CellValue.EMPTY:
            raise ValueError("T.B.D")

        (row, col) = self._addr2pos[address]

        # すでに駒が置かれている場合は処理しない
        if self._cells[row][col].value != CellValue.EMPTY:
            return 0

        n_flips = 0
        for d_row in [-1, 0, 1]:
            for d_col in [-1, 0, 1]:
                n_flips += self._get_flip_line_count(color, row, col, d_row, d_col)

        return n_flips

    def get_enable_put_address(self, color: CellValue) -> list[str]:
        """駒を置くことができるマスのアドレスを取得する"""
        return [address for address in self._addr2pos.keys() if self.get_flip_count(color, address) > 0]

    def put(self, color: CellValue, address=str) -> Union[int, None]:
        # 指定色無しの場合はエラーにする
        if color == CellValue.EMPTY:
            raise ValueError("T.B.D")

        (row, col) = self._addr2pos[address]

        # すでに駒が置かれている場合は処理しない
        if self._cells[row][col].value != CellValue.EMPTY:
            return None

        n_flips = 0
        for d_row in [-1, 0, 1]:
            for d_col in [-1, 0, 1]:
                n_flips += self._flip_line(color, row, col, d_row, d_col)

        return n_flips
    
    def is_fill(self):
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if self._cells[i][j].value == CellValue.EMPTY:
                    return False
        return True
    
    def count_value(self) -> dict:
        counter = defaultdict(int)
        for line in self._cells:
            for cell in line:
                counter[cell.value] += 1
        return counter
