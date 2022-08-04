import math


class MyCar:
    def __init__(self) -> None:
        self.w = math.pi
        self.b = 6
        # 최대 조향
        self.maxSteer = 70
        # 최소 조향
        self.minSteer = -70
        # 기본 속도
        self.normalVel = 150
        # 후진 속도
        self.backVel = -120
        # 후진 회전 속도
        self.turnBackVel = -100
        # 정지 속도
        self.stopVel = 0
        # 거리유지 후진 시작 거리
        self.backStartDistant = 70
        # 거리유지 후진 종료
        self.backEndDistant = 150
        # 회전 전진속도
        self.turnVel = 120
        # 장애물 우회
        self.vpn = False

        # 후진 상태
        self.back = False
        # 정지 상태
        self.stop = False
        print('My Car Initiatied')

    def displayData(
        self,
        L,
        R,
        V,
        frontLidar,
        rearLidar,
        e,
        steer,
        velocity,
        waiting,
        resent
    ):
        print('L[0]=', L[0], 'L[1]=', L[1], 'L[2]=', L[2], end="  //  ")
        print('R[0]=', R[0], 'R[1]=', R[1], 'R[2]=', R[2])
        print('V[0]=', V[0], 'V[1]=', V[1], 'V[2]=', V[2], 'V[3]=',
              V[3], 'V[4]=', V[4], 'V[5]=', V[5], 'V[6]=', V[6])
        print('frontLidar=', frontLidar, end="..//..")
        print('rearLidar=', rearLidar, end="       => => =>    ")
        print('[e=', math.floor(e * 10) / 10, end="]  ")
        print('[steer=', steer, end="]  ")
        print('[waiting=', waiting, end="]  ")
        print('[velocity=', velocity, end="] ")
        print('[road=', self.checkRoad(V, L, R, 9999), end="] ")
        print('[back=', self.back, end="] ")
        print('[vpn=', self.vpn, end="] ") 
        print('[resent=', resent, "]")
        print()

    def getSteer(self, e):
        steer = int(e / self.w) + self.b

        return max(self.minSteer, min(self.maxSteer, steer))

    def getVel(self, V, turn=False):
        if self.back and V[3] < self.backEndDistant:
            if turn:
                if not self.stop:
                    self.stop = True
                    return self.stopVel
                else:
                    return self.turnBackVel
            else:
                if not self.stop:
                    self.stop = True
                    return self.stopVel
                else:
                    return self.backVel
        else:
            self.back = False
            self.stop = False

            if turn:
                if V[3] < self.backStartDistant:
                    self.back = True
                    return self.turnBackVel
                return self.turnVel
            else:   
                if V[3] < self.backStartDistant:
                    self.back = True
                    return self.backVel
                return self.normalVel

    def checkRoad(self, V, L, R, lidar):
        # leftV = self.leftVDiff(V)
        # rightV = self.rightVDiff(V)

        # if (
        #     (sorte
        # d(leftV, reverse=True) == leftV) and
        #     (sorted(rightV, reverse=True) == rightV) and
        #     leftV[-1] > rightV[0]
        # ):
        #     return 'left'
        # elif ((sorted(leftV) == leftV) and
        #       (sorted(rightV) == rightV) and
        #       leftV[-1] < rightV[0]
        #       ):
        #     return 'right'
        # else:
        #     return 'linear'

        copyV = 0
        if V[0] > V[1] and V[-1] > V[-2]:
            copyV = V[1:-2]
        elif V[0] > V[1]:
            copyV = V[1:]
        elif V[-1] > V[-2]:
            copyV = V[:-1]
        else:
            copyV = V
        
        
        # if self.vpn or lidar <= 400:
        #     self.vpn = True
            
        #     countLeft, countRight = 0, 0
            
        #     for l in L:
        #         if l > 315:
        #             countLeft += 1
                    
        #     for r in R:
        #         if r > 315:
        #             countRight += 1
        
        #     print(countLeft, countRight)
        
        #     if countLeft < countRight:
        #         return 'right'
        #     elif countRight < countLeft:
        #         return 'left'
        #     else:
        #         self.vpn = False
        #         return 'linear'
        if (sorted(copyV) == copyV and R[2] > 315 and V[0] < 120):
            # if (sorted(copyV) == copyV and R[2] > 315):
            return 'right'
        elif (sorted(copyV, reverse=True) == copyV and L[2] > 315 and V[-1] < 120):
        # elif (sorted(copyV, reverse=True) == copyV and L[2] > 315):
            return 'left'
        else:
            return 'linear'

    def limitSteer(self, steer):
        return max(self.minSteer, min(self.maxSteer, steer))

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
        velocity = self.getVel(V)

        return steer, e, velocity
