## 生成灰度图

```
import cv2
img = cv2.imread("2.jpg")

# 灰度
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(grey)

# 保存
cv2.imwrite('grey.jpg', invert)
print("inverted grey image")

cv2.imshow('sketch', invert)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## 生成轮廓图

```
import cv2

img = cv2.imread("img.jpg")

# 灰度
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(grey)

# 高斯滤波
blur_img = cv2.GaussianBlur(invert, (7, 7), 0)
inverse_blur = cv2.bitwise_not(blur_img)
sketch_img = cv2.divide(grey, inverse_blur, scale=256.0)

# 保存
cv2.imwrite('sketch.jpg', sketch_img)
print("inverted grey image")

cv2.imshow('sketch', sketch_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
