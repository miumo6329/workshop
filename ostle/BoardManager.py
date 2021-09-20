import numpy as np


class BoardManager:

    def __init__(self):
        self.state = np.zeros((5, 5))
        for i in range(5):
            self.state[0, i] = 1  # Player1
            self.state[4, i] = 2  # Player2
        self.state[2, 2] = 3  # Hole

    def move_hole(self, pos, direct):
        i, j = pos
        if direct == "Up":
            self.state[i - 1, j] = self.state[i, j]
            self.state[i, j] = 0
        elif direct == "Down":
            self.state[i + 1, j] = self.state[i, j]
            self.state[i, j] = 0
        elif direct == "Left":
            self.state[i, j - 1] = self.state[i, j]
            self.state[i, j] = 0
        elif direct == "Right":
            self.state[i, j + 1] = self.state[i, j]
            self.state[i, j] = 0

    def move_piece(self, pos, direct):
        i, j = pos
        f1 = np.vectorize(lambda x: x % 3)
        pieces_state = f1(self.state)
        f2 = np.vectorize(lambda x: 3 if x == 3 else 0)
        hole_state = f2(self.state)
        f3 = np.vectorize(lambda x: 3 if x > 3 else x)

        if direct == "Up":
            # 1マスずつ上に押し出しの終端を検索
            for k in range(i, -1, -1):
                push_end_row = k
                if pieces_state[k, j] == 0:
                    break
            # 押し出し処理
            for k in range(push_end_row, i, 1):
                pieces_state[k, j] = pieces_state[k + 1, j]
                if k == i - 1:
                    pieces_state[k + 1, j] = 0
        elif direct == "Down":
            # 1マスずつ下に押し出しの終端を検索
            for k in range(i, 5, 1):
                push_end_row = k
                if pieces_state[k, j] == 0:
                    break
            # 押し出し処理
            for k in range(push_end_row, i, -1):
                pieces_state[k, j] = pieces_state[k - 1, j]
                if k == i + 1:
                    pieces_state[k - 1, j] = 0
        elif direct == "Left":
            # 1マスずつ左に押し出しの終端を検索
            for k in range(j, -1, -1):
                push_end_row = k
                if pieces_state[i, k] == 0:
                    break
            # 押し出し処理
            for k in range(push_end_row, j, 1):
                pieces_state[i, k] = pieces_state[i, k + 1]
                if k == j - 1:
                    pieces_state[i, k + 1] = 0
        elif direct == "Right":
            # 1マスずつ右に押し出しの終端を検索
            for k in range(j, 5, 1):
                push_end_row = k
                if pieces_state[i, k] == 0:
                    break
            # 押し出し処理
            for k in range(push_end_row, j, -1):
                pieces_state[i, k] = pieces_state[i, k - 1]
                if k == j + 1:
                    pieces_state[i, k - 1] = 0

        self.state = pieces_state + hole_state
        self.state = f3(self.state)

    def is_own_piece(self, pos, player):
        i, j = pos
        if self.state[i, j] == player or self.state[i, j] == 3:
            return True
        else:
            return False

    def is_hole(self, pos):
        i, j = pos
        if self.state[i, j] == 3:
            return True
        else:
            return False

    def ask_move_direction(self, pos):
        i, j = pos
        move_dict = {}

        # コマ指定の場合
        if self.state[i, j] == 1 or self.state[i, j] == 2:
            # 1行目以外の場合、上へ移動可能
            if not i == 0: move_dict["Up"] = (i - 1, j)
            # 5行目以外の場合、下へ移動可能
            if not i == 4: move_dict["Down"] = (i + 1, j)
            # 1列目以外の場合、左へ移動可能
            if not j == 0: move_dict["Left"] = (i, j - 1)
            # 5列目以外の場合、左へ移動可能
            if not j == 4: move_dict["Right"] = (i, j + 1)
        # 穴指定の場合
        elif self.state[i, j] == 3:
            # 1行目以外 かつ 進行方向に駒がいない場合、上へ移動可能
            if not i == 0 and self.state[i - 1, j] == 0: move_dict["Up"] = (i - 1, j)
            # 5行目以外 かつ 進行方向に駒がいない場合、下へ移動可能
            if not i == 4 and self.state[i + 1, j] == 0: move_dict["Down"] = (i + 1, j)
            # 1列目以外 かつ 進行方向に駒がいない場合、左へ移動可能
            if not j == 0 and self.state[i, j - 1] == 0: move_dict["Left"] = (i, j - 1)
            # 5列目以外 かつ 進行方向に駒がいない場合、左へ移動可能
            if not j == 4 and self.state[i, j + 1] == 0: move_dict["Right"] = (i, j + 1)

        return move_dict

    def ask_piece_count(self, player):
        return np.count_nonzero(self.state == player)
