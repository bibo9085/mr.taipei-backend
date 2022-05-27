import numpy as np
import cv2

# 製作黑色底圖
# img = np.zeros((512,512,3), np.uint8)
img = cv2.imread('stationMap_Daan.jpg')

# 畫粗度為7的紅色線
pts = np.array([[75, 868], [500, 868], [750, 1295], [980, 1295], [850, 1505]], np.int32)
# pts = pts.reshape((-1, 1, 2))

red_color = (0, 0, 255)
cv2.polylines(img, pts=[pts], isClosed=False, color=red_color, thickness=10)
print(pts) #維度
# 顯示圖片
cv2.imshow('image',img)

# 按任意鍵關閉圖片視窗
cv2.waitKey(0)
cv2.destroyAllWindows()