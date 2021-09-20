import cv2
from BoardManager import BoardManager
from DisplayUpdater import DisplayUpdater
from MouseObserver import MouseObserver


class GameManager:

    def __init__(self):
        # 表示するWindow名
        self.window_name = "Ostle"
        # ディスプレイ設定
        self.display_updater = DisplayUpdater(self.window_name)
        # コールバックの設定
        self.mouse_observer = MouseObserver(self.window_name)

        self.board_manager = BoardManager()

    def run(self):

        self.display_updater.update_board(self.board_manager.state)

        player = 1

        while True:
            self.__select_piece_phase(player)
            self.display_updater.update_board(self.board_manager.state)
            winner = self.judge_winner()
            if winner > 0:
                print("player", winner, "is win!!!")
                break

            if player == 1:
                player = 2
            else:
                player = 1

        cv2.destroyAllWindows()
        print("Finished")

    def __select_piece_phase(self, player):

        while True:
            cv2.waitKey(60)
            coord = self.mouse_observer.getCoord()

            if coord[0] is not None:
                pos = (int(coord[1] / 36), int(coord[0] / 36))
                self.display_updater.draw_mark(pos)

            # 左クリックがあったら表示
            if self.mouse_observer.getEvent() == cv2.EVENT_LBUTTONDOWN:
                if self.board_manager.is_own_piece(pos, player) is True:
                    if self.__select_direction_phase(pos) is True:
                        return

    def __select_direction_phase(self, mark_pos):

        # 今のマスから移動可能な方向を調べる
        move_dict = self.board_manager.ask_move_direction(mark_pos)
        if move_dict is not None:
            self.display_updater.draw_direction(move_dict)
        else:
            print("そのコマは移動できません")
            return

        while True:
            cv2.waitKey(60)

            coord = self.mouse_observer.getCoord()
            if coord[0] is not None:
                direct_pos = (int(coord[1] / 36), int(coord[0] / 36))
                direct = [k for k, v in move_dict.items() if v == direct_pos]
                self.display_updater.emphasis_direction_img(move_dict, direct)

            # 左クリックがあったらコマを移動
            if self.mouse_observer.getEvent() == cv2.EVENT_LBUTTONDOWN and len(direct) != 0:
                if self.board_manager.is_hole(mark_pos) is True:
                    self.board_manager.move_hole(mark_pos, direct[0])
                else:
                    self.board_manager.move_piece(mark_pos, direct[0])
                return True

            # 右クリックがあったら終了
            elif self.mouse_observer.getEvent() == cv2.EVENT_RBUTTONDOWN:
                print("push right click : __select_direction_phase")
                return False

    def judge_winner(self):
        winner = 0
        player1_count = self.board_manager.ask_piece_count(1)
        player2_count = self.board_manager.ask_piece_count(2)

        if player1_count <= 3:
            winner = 2
        if player2_count <= 3:
            winner = 1
        return winner
