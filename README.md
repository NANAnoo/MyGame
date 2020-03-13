# MyGame
interacting N-body simulator
交互式N体模拟游戏

start:
python GravitySimulator.py

need: numpy , pygame
需要: numpy , pygame 

HELP：
操作指南：

Normal mode
MOUSE_LEFT :move,
MOUSE_RIGHT:select a body,
MOUSE_MID:scale
key S:stop/continue;
key esc: quit
key space: switch max and select
key o:switch orbit showing mode
key up:speed up
key down:speed down
key m:tracing max
key a: add mode
普通模式：
左键拖动，
右键选择body ,
中键缩放
S:开始暂停
空格：切换追踪对象
O：切换轨迹显示模式
up:加速
down:减速
m：追踪最大质量
a:添加模式

ADD MODE:
key ESC: back to normal mode
MOUSE_LEFT : select a position
MOUSE_MOVE: change speed of body
MOUSE_MID: scale the mass of body
key y: add body
key n:cancel  add
ESC:回到普通模式
鼠标左键：选择添加的位置
鼠标移动：选择添加body的速度
鼠标中键：缩放添加天体质量
Y键：确认添加
N键：取消添加
