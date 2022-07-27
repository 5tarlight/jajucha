import math


class MyCar:
    def __init__(self) -> None:
        self.w = math.pi
        self.b = -16
        print('My Car Initiatied')

    def displayData(self, L, R, V, frontLidar, rearLidar, e, steer, velocity, waiting):
        print('L[0]=', L[0], 'L[1]=', L[1], 'L[2]=', L[2], end="  //  ")
        print('R[0]=', R[0], 'R[1]=', R[1], 'R[2]=', R[2])
        print('V[0]=', V[0], 'V[1]=', V[1], 'V[2]=', V[2], 'V[3]=',
              V[3], 'V[4]=', V[4], 'V[5]=', V[5], 'V[6]=', V[6])
        print('frontLidar=', frontLidar, end="..//..")
        print('rearLidar=', rearLidar, end="       => => =>    ")
        print('[e=', math.floor(e * 10) / 10, end="]  ")
        print('[steer=', steer, end="]  ")
        print('[waiting=', waiting, end="]  ")
        print('[velocity=', velocity, "]")
        print()

    def getSteer(self, e):
        steer = int(e / self.w) + self.b

        if steer > 100:
            steer = 100
        elif steer < -100:
            steer = -100

        return steer

    def getVel(self):
        return 40

    def leftVDiff(V):
        return [V[1] - V[0], V[2] - V[1]]

    def linear(self, L, R, V):
        # 각 변수의 최댓값
        if V[3] == 255:  # V[i]가 잡히지 않은 경우
            ...
        if L[2] >= 320:  # L[i]가 잡히지 않은 경우  (중앙 픽셀이 324라서 왼쪽으로 최대 324)
            e = -90
        elif R[2] >= 305:  # R[i]가 잡히지 않은 경우  (중앙 픽셀이 324라서 오른쪽으로 최대 315)
            e = 90
        else:
            # 극단적으로 치우치지 않았을 때 가운데 맞추기
            arr1 = []
            arr2 = []

            # 왼쪽 라인과 오른쪽 라인의 기울기 비교
            if (V[0] < 255 and V[1] < 255):
                d = V[1] - V[0]
                if (d > 0):
                    arr1.append(d)
            if (V[1] < 255 and V[2] < 255):
                d = V[2] - V[1]
                if (d > 0):
                    arr1.append(d)

            if (V[0] < 255 and V[2] < 255):
                d = V[2] - V[0]
                if (d > 0):
                    arr1.append(d)

            # right
            if (V[0+4] < 255 and V[1+4] < 255):
                d = V[1+4] - V[0+4]
                if (d < 0):
                    arr2.append(d)
            if (V[1+4] < 255 and V[2+4] < 255):
                d = V[2+4] - V[1+4]
                if (d < 0):
                    arr2.append(d)

            if (V[0+4] < 255 and V[2+4] < 255):
                d = V[2+4] - V[0+4]
                if (d < 0):
                    arr2.append(d)

            # 유효한 기울기 중 가장 가파른 것 찾기 (다른 곳으로 튀었을때 대비)
            # 중심일때 서로 절댓값 일치(세로축 대칭)
            if (len(arr1) == 0):
                arr1.append(0)
            if (len(arr2) == 0):
                arr2.append(0)
            d1 = max(arr1)
            d2 = abs(min(arr2))

            e = (d2 - d1) * 0.7

        steer = self.getSteer(e)
        velocity = self.getVel()

        return steer, e, velocity
