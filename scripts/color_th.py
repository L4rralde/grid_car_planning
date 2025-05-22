
import cv2 as cv
import numpy as np
from PIL import Image



img = Image.open('../world/parking.jpeg')
img = np.array(img)
blur = cv.blur(img,(5,5))
blur0 = cv.medianBlur(blur,5)
blur1 = cv.GaussianBlur(blur0,(5,5),0)
blur2 = cv.bilateralFilter(blur1,9,75,75)

low_th = np.array([180, 180, 180])
high_th = np.array([210, 210, 210])
mask = cv.inRange(blur2, low_th, high_th)
res = cv.bitwise_and(img,img, mask= mask)


step = 800//100
grid = []
for i in range(0, 800, step):
    grid_row = []
    for j in range(0, 800, step):
        tile = mask[i-step//2: i+step//2, j-step//2: j+step//2]
        grid_row.append(int(tile.mean() < 100))
    grid.append(grid_row)

grid = np.array(grid)

wg, hg = grid.shape
for i in range(wg):
    for j in range(hg):
        if not grid[i][j]:
            continue
        cv.circle(res,(j*8, i*8), 5, (0,0,255), 3)

cv.imshow("", res)
cv.waitKey(0)
cv.destroyAllWindows()

np.save("grid.npz", grid)