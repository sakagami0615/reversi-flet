from reversi.game.player.interface import PlayerInterface


class Controller:
    """プレイヤー操作クラス"""
    def __init__(self, first_player: PlayerInterface, second_player: PlayerInterface):
        self._players = [first_player, second_player]
        self._index = 0
        self._n_pass = 0

    @property
    def curr_player(self) -> PlayerInterface:
        return self._players[self._index]

    @property
    def n_pass(self):
        return self._n_pass

    def action(self, cand_addrs: list[str]) -> str:
        put_addr = self._players[self._index].action(cand_addrs)
        if put_addr is None:
            self._n_pass += 1
        return put_addr

    def turn_change(self) -> None:
        self._index = (self._index + 1) % 2
