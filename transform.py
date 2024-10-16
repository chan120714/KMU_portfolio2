import numpy as np
import cv2

def order_points(pts):
  # 좌표의 초기화. 순서는 좌측상단, 우측상단, 우측하단,
  # 좌측하단으로 정렬하자.
  rect = np.zeros((4, 2), dtype = "float32")
    
  # 좌측상단 좌표의 합이 가장 작을 것이고,
  # 우측하단 좌표의 합이 가장 클 것이다.
  s = pts.sum(axis = 1)
  rect[0] = pts[np.argmin(s)]
  rect[2] = pts[np.argmax(s)]
    
  # 좌표들 간의 차이를 구해보자.
  # 우측상단 좌표의 차가 가장 작을 것이고,
  # 좌측하단 좌표의 차가 가장 클 것이다.
  diff = np.diff(pts, axis = 1)
  rect[1] = pts[np.argmin(diff)]
  rect[3] = pts[np.argmax(diff)]
    
  # 정렬된 좌표를 반환한다.
  return rect
def four_point_transform(image, pts):
  # 일정하게 정렬된 좌표들을 가져와서
  # 각각 개별적으로 unpack해준다.
  rect = order_points(pts)
  (tl, tr, br, bl) = rect
    
  # 새로운 이미지의 너비를 계산하자.
  # 새로운 너비 = max(dist(우측하단 x 좌표, 좌측하단 x 좌표))
  #             = max(dist(우측상단 x 좌표, 좌측상단 x 좌표))
  widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
  widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
  maxWidth = max(int(widthA), int(widthB))
  
  # 새로운 이미지의 높이를 계산하자.
  # 새로운 높이 = max(dist(우측상단 y 좌표, 우측하단 y 좌표))
  #             = max(dist(좌측상단 y 좌표, 좌측하단 y 좌표))
  heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
  heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
  maxHeight = max(int(heightA), int(heightB))
  
  # 새로운 이미지에 대한 정보를 통해
  # 목표 좌표를 구성해보자.
  # 좌표의 정렬 순서는 동일하게 좌측상단으로부터
  # 시계방향 순서이다.
  dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
        
  # 시점 변환 행렬을 계산하고 적용하자
  M = cv2.getPerspectiveTransform(rect, dst)
  warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
  # 변형된 이미지를 반환하자
  return warped