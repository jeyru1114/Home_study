import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 초기 설정
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(color='gray', linestyle='--', linewidth=0.5)
ax.set_xlabel('r')
ax.set_ylabel('i')
ax.set_title('random vector animation')

# 초기 벡터 설정
vector, = ax.plot([], [], 'r', label='Vector')
vector_angle_deg = np.random.uniform(0, 360)
radius = np.random.uniform(0.5, 1.5)


# 초기화 함수
def init():
    vector.set_data([], [])
    return vector,


# 애니메이션 업데이트 함수
def update(frame):
    global vector_angle_deg, radius

    # 새로운 각도와 크기 무작위로 설정
    vector_angle_deg = np.random.uniform(0, 360)
    radius = np.random.uniform(0.5, 1.5)

    # 벡터 계산
    vector_x = radius * np.cos(np.deg2rad(vector_angle_deg)) #싨수축
    vector_y = radius * np.sin(np.deg2rad(vector_angle_deg)) #허수 축

    # 벡터 업데이트
    vector.set_data([0, vector_x], [0, vector_y])

    return vector,


# 애니메이션 생성
ani = FuncAnimation(fig, update, init_func=init, frames=100, interval=100)

# 벡터의 이름을 레이블로 추가
ax.text(1, 1, 'Vector', fontsize=12, color='r')

# 그래프 그리기
plt.legend()
plt.show()
