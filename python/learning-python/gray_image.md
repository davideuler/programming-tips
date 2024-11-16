## 1.显示图片

``` python
import cv2

image = cv2.imread("2.jpg")

cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```


## 2.生成灰度图

``` python
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

## 3.生成轮廓图

``` python
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


## 4. 雪花图
随机雪花

```python
import turtle
import random

def draw_snowflake(t, size):
    colors = ["white", "light blue", "light cyan"]
    
    for _ in range(8):
        t.color(random.choice(colors))
        for _ in range(2):
            t.forward(size)
            t.right(60)
            t.forward(size)
            t.right(120)
        t.right(45)

# 设置画布和画笔
screen = turtle.Screen()
screen.bgcolor("midnight blue")
t = turtle.Turtle()
t.speed(0)
t.pensize(2)

# 绘制多个雪花
for _ in range(20):
    # 随机位置
    t.penup()
    t.goto(random.randint(-300, 300), random.randint(-300, 300))
    t.pendown()
    
    # 随机大小
    draw_snowflake(t, random.randint(5, 30))

screen.mainloop()

```


带颜色的雪花

``` python
import turtle
import random

def draw_snowflake(t, size):
    colors = ["white", "light blue", "light cyan"]
    
    for _ in range(8):
        t.color(random.choice(colors))
        for _ in range(2):
            t.forward(size)
            t.right(60)
            t.forward(size)
            t.right(120)
        t.right(45)

# 设置画布和画笔
screen = turtle.Screen()
screen.bgcolor("midnight blue")
t = turtle.Turtle()
t.speed(0)
t.pensize(2)

# 绘制多个雪花
for _ in range(20):
    # 随机位置
    t.penup()
    t.goto(random.randint(-300, 300), random.randint(-300, 300))
    t.pendown()
    
    # 随机大小
    draw_snowflake(t, random.randint(5, 30))

screen.mainloop()


```

## 5. 绘制星星

1. 简单星星
   
```python
import turtle

# 设置画布和画笔
screen = turtle.Screen()
screen.bgcolor("navy")
t = turtle.Turtle()
t.speed(0)
t.color("yellow")
t.pensize(2)

# 绘制五角星
for _ in range(5):
    t.forward(100)
    t.right(144)

screen.mainloop()

```

2.多个彩色星星：

``` python
import turtle
import random

def draw_star(t, size, color):
    t.color(color)
    t.begin_fill()
    for _ in range(5):
        t.forward(size)
        t.right(144)
    t.end_fill()

# 设置画布和画笔
screen = turtle.Screen()
screen.bgcolor("black")
t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# 颜色列表
colors = ["yellow", "red", "white", "orange", "pink"]

# 绘制多个星星
for _ in range(20):
    # 随机位置
    x = random.randint(-250, 250)
    y = random.randint(-250, 250)
    t.penup()
    t.goto(x, y)
    t.pendown()
    
    # 随机大小和颜色
    size = random.randint(10, 40)
    color = random.choice(colors)
    
    draw_star(t, size, color)

screen.mainloop()
```


闪烁的星星：

```python
import turtle
import random
import time

def draw_star(t, size):
    t.begin_fill()
    for _ in range(5):
        t.forward(size)
        t.right(144)
    t.end_fill()

# 设置画布和画笔
screen = turtle.Screen()
screen.bgcolor("black")
t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# 创建多个星星的位置和大小
stars = []
for _ in range(15):
    x = random.randint(-250, 250)
    y = random.randint(-250, 250)
    size = random.randint(10, 30)
    stars.append((x, y, size))

# 动画效果
for _ in range(50):  # 闪烁50次
    t.clear()
    
    for x, y, size in stars:
        t.penup()
        t.goto(x, y)
        t.pendown()
        
        # 随机改变亮度
        brightness = random.random()
        t.color(1, 1, 0, brightness)  # 黄色带透明度
        draw_star(t, size)
    
    screen.update()
    time.sleep(0.2)

screen.mainloop()

```

## 6.五行代码绘制多边形线条

```python
import turtle

t = turtle.Pen()
for x in range(360):
    t.forward(x)
    t.left(59)
```

## 6. 截图

``` python
import PIL.ImageGrab
scr = PIL.ImageGrab.grab()
scr.save("scr.png")
```
