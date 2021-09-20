import cv2
import numpy as np
from PIL import Image


class DisplayUpdater:

    def __init__(self, window_name):

        # 画像の表示
        self.window_name = window_name
        self.img_board = cv2.imread("image/ostle_board.png", cv2.IMREAD_UNCHANGED)
        self.img_piece_1 = cv2.imread("image/ostle_piece_1.png", cv2.IMREAD_UNCHANGED)
        self.img_piece_2 = cv2.imread("image/ostle_piece_2.png", cv2.IMREAD_UNCHANGED)
        self.img_hole = cv2.imread("image/ostle_hole.png", cv2.IMREAD_UNCHANGED)

        self.img_right = cv2.imread("image/ostle_direction.png", cv2.IMREAD_UNCHANGED)
        height = self.img_right.shape[0]
        width = self.img_right.shape[1]
        center = (int(width / 2), int(height / 2))
        trans = cv2.getRotationMatrix2D(center, 90.0, 1.0)
        self.img_up = cv2.warpAffine(self.img_right, trans, (width, height))
        self.img_left = cv2.warpAffine(self.img_up, trans, (width, height))
        self.img_down = cv2.warpAffine(self.img_left, trans, (width, height))

        self.now_state = self.img_board

        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(window_name, self.img_board)

    def update_board(self, state):

        img = self.img_board

        for i in range(5):
            for j in range(5):
                if state[i, j] == 1:
                    img = self.__draw_piece(img, self.img_piece_1, (i, j))
                elif state[i, j] == 2:
                    img = self.__draw_piece(img, self.img_piece_2, (i, j))
                elif state[i, j] == 3:
                    img = self.__draw_piece(img, self.img_hole, (i, j))

        self.now_state = img
        self.update_display(img)

    def update_display(self, image):

        cv2.imshow(self.window_name, image)

    def __draw_piece(self, base_img, piece_img, pos):

        image = self.__overlay_image(base_img, piece_img, (pos[1] * 36 + 3, pos[0] * 36 + 3))
        return image

    def draw_mark(self, pos):
        img = self.now_state.copy()
        cv2.rectangle(img, (pos[1] * 36 + 1, pos[0] * 36 + 1), ((pos[1] + 1) * 36, (pos[0] + 1) * 36), (0, 255, 0), 2,
                      cv2.LINE_AA)
        self.update_display(img)

    def draw_direction(self, move_dict):
        img = self.now_state.copy()
        for ml in move_dict:
            if ml == "Up":
                img = self.__draw_direction(img, self.img_up, move_dict["Up"])
            elif ml == "Down":
                img = self.__draw_direction(img, self.img_down, move_dict["Down"])
            elif ml == "Left":
                img = self.__draw_direction(img, self.img_left, move_dict["Left"])
            elif ml == "Right":
                img = self.__draw_direction(img, self.img_right, move_dict["Right"])

        self.update_display(img)

    def __draw_direction(self, img_base, img_direction, pos):

        image = self.__overlay_image(img_base, img_direction, (pos[1] * 36, pos[0] * 36))
        return image

    def emphasis_direction_img(self, move_dict, direct):
        return

    # 画像のオーバーレイ
    def __overlay_image(self, src, overlay, location):

        overlay_height, overlay_width = overlay.shape[:2]

        # 背景をPIL形式に変換
        src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
        pil_src = Image.fromarray(src)
        pil_src = pil_src.convert('RGBA')

        # オーバーレイをPIL形式に変換
        overlay = cv2.cvtColor(overlay, cv2.COLOR_BGRA2RGBA)
        pil_overlay = Image.fromarray(overlay)
        pil_overlay = pil_overlay.convert('RGBA')

        # 画像を合成
        pil_tmp = Image.new('RGBA', pil_src.size, (255, 255, 255, 0))
        pil_tmp.paste(pil_overlay, location, pil_overlay)
        result_image = Image.alpha_composite(pil_src, pil_tmp)

        # OpenCV形式に変換
        return cv2.cvtColor(np.asarray(result_image), cv2.COLOR_RGBA2BGRA)
