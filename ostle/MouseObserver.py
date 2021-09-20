import cv2


class MouseObserver:
    def __init__(self, input_img_name):
        # マウス入力用のパラメータ
        self.mouseEvent = {"x": None, "y": None, "event": None, "flags": None}
        # マウス入力の設定
        cv2.setMouseCallback(input_img_name, self.__CallBackFunc, None)

    # コールバック関数
    def __CallBackFunc(self, event_type, x, y, flags, userdata):
        self.mouseEvent["x"] = x
        self.mouseEvent["y"] = y
        self.mouseEvent["event"] = event_type
        self.mouseEvent["flags"] = flags

        # マウス入力用のパラメータを返すための関数

    def getData(self):
        return self.mouseEvent

    # マウスイベントを返す関数
    def getEvent(self):
        return self.mouseEvent["event"]

        # マウスフラグを返す関数

    def getFlags(self):
        return self.mouseEvent["flags"]

        # xの座標を返す関数

    def getX(self):
        return self.mouseEvent["x"]

        # yの座標を返す関数

    def getY(self):
        return self.mouseEvent["y"]

        # xとyの座標を返す関数

    def getCoord(self):
        return self.mouseEvent["x"], self.mouseEvent["y"]
