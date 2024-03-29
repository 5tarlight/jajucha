from jajucha.planning import BasePlanning
from jajucha.graphics import Graphics
from jajucha.control import mtx
from jajucha.MyCar import MyCar


class Planning(BasePlanning):
    def __init__(self, graphics):
        super().__init__(graphics)
        # --------------------------- #
        # 정지거리
        self.stopLidar = 50
        # 좌우회전 조향
        self.turnSteer = 55
        # 좌우회전 후진 역조향
        self.backSteer = 65
        # 후진 역조향 계수
        self. turnSteerMultiplier = 1.21

        self.vars.redCnt = 0  # 변수 설정
        self.vars.greenCnt = 0  # 변수 설정
        self.vars.stop = True
        self.vars.steer = 0
        self.vars.velocity = 0
        self.waiting = False
        self.resent = 'none'
        self.my = MyCar()

    def process(self, t, frontImage, rearImage, frontLidar, rearLidar):
        """
        자주차의 센서 정보를 바탕으로 조향과 속도를 결정하는 함수
        t: 주행 시점으로부터의 시간 (초)
                frontImage: 전면 카메라 이미지
                rearImage: 후면 카메라 이미지
                frontLidar: 전면 거리 센서 (mm), 0은 오류를 의미함
                rearLidar: 후면 거리 센서 (mm), 0은 오류를 의미함
        """

        # [1] 라이다 처리

        # canny 이미지 보기
        # print(frontImage)
        # canny = self.canny(frontImage)
        # self.imshow('canny', canny)

        # 차선 정보 파악
        V, L, R = self.gridFront(frontImage, cols=7, rows=3)
        # V, L, R = self.gridFront(frontImage, cols=7, rows=3) : 전방 이미지 행선, 열선 그리기
        # rearV, rearL, rearR = self.gridRear(rearImage, cols=4, rows=6) : 후방 이미지도 가능
        # rows : 행선값  cols : 열선값 (row, column) ex) rows=3 : 행선이 3개이고, 총 4개의 행 칸이 생성
        # L[0], L[1], L[2], R[0], R[1], R[2], V[0]~v[6]

        steer, e, velocity = 0, 0, 0
        road = self.my.checkRoad(V, L, R, lidar=frontLidar)

        if road == 'linear':
            steer, e, velocity = self.my.linear(L, R, V)
        elif road == 'left':
            self.resent = 'left'

            e = -9999
            steer = -self.turnSteer + self.my.b
            velocity = self.my.getVel(V, True)
        elif road == 'right':
            self.resent = 'right'

            e = 9999
            steer = self.turnSteer + self.my.b
            velocity = self.my.getVel(V, True)

        if not self.my.vpn:
            if not self.waiting and frontLidar < self.stopLidar and frontLidar > 0:
                velocity = 0
                self.waiting = True
            elif self.waiting and frontLidar == 0:
                velocity = 0
            elif self.waiting and frontLidar < self.stopLidar:
                velocity = 0
            elif self.waiting:
                self.waiting = False

        if velocity <= 0:
            if self.resent == 'left':
                steer = self.turnSteer * self.turnSteerMultiplier + self.my.b
            elif self.resent == 'right':
                steer = -self.turnSteer * self.turnSteerMultiplier + self.my.b
            else:
                steer = (-(steer - self.my.b) + self.my.b) * \
                    self.turnSteerMultiplier

        self.my.displayData(L, R, V, frontLidar, rearLidar,
                            e, steer, velocity, self.waiting, self.resent)

        self.vars.steer = self.my.limitSteer(steer)
        self.vars.velocity = velocity
        return self.vars.steer, self.vars.velocity


if __name__ == "__main__":
    g = Graphics(Planning)  # 자주차 컨트롤러 실행
    g.root.mainloop()  # 클릭 이벤트 처리
    g.exit()  # 자주차 컨트롤러 종료
