from jajucha.planning import BasePlanning
from jajucha.graphics import Graphics
from jajucha.control import mtx
from jajucha.MyCar import MyCar
import cv2
import numpy as np
import sys
import io
import time


class Planning(BasePlanning):
    def __init__(self, graphics):
        super().__init__(graphics)
        # --------------------------- #
        self.vars.redCnt = 0  # 변수 설정
        self.vars.greenCnt = 0  # 변수 설정
        self.vars.stop = True
        self.vars.steer = 0
        self.vars.velocity = 0
        self.path = './record/linear.mp4'

        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

        width = 640
        height = 480
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.path, fourcc, 20.0, (width, height))

    def process(self, t, frontImage, rearImage, frontLidar, rearLidar):
        # self.out.write(frontImage)

        self.vars.steer = 0
        self.vars.velocity = 0
        return self.vars.steer, self.vars.velocity


if __name__ == "__main__":
    g = Graphics(Planning)  # 자주차 컨트롤러 실행
    g.root.mainloop()  # 클릭 이벤트 처리
    g.exit()  # 자주차 컨트롤러 종료
