import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Source Code Pro for Powerline'
plt.rcParams['font.sans-serif'] = ['Arial']

# 生成轮速脉冲和方向的数据
t = np.arange(0, 10, 0.1)
v = 10 + np.random.randn(len(t))
theta = np.cumsum(v) * 0.1 + np.random.randn(len(t))

# 生成IMU的数据
gyro = np.cumsum(np.random.randn(len(t))) * 0.1
accel = np.random.randn(len(t))

# 初始化卡尔曼滤波器
x = np.array([0, 0, 0, 0, 0, 0])
P = np.eye(6) * 1
Q = np.eye(6) * 0.001
R = np.eye(2) * 1

# 定义状态转移矩阵和观测矩阵
A = np.array([[1, 0, 0.1, 0, 0, 0],
              [0, 1, 0, 0.1, 0, 0],
              [0, 0, 1, 0, 0.1, 0],
              [0, 0, 0, 1, 0, 0.1],
              [0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 1]])
H = np.array([[1, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0]])

# 存储估计值和观测值
estimates = []
observations = []

# 进行卡尔曼滤波
for i in range(len(t)):
    # 预测状态
    x = A @ x
    P = A @ P @ A.T + Q

    # 计算卡尔曼增益
    K = P @ H.T @ np.linalg.inv(H @ P @ H.T + R)

    # 更新状态
    z = np.array([v[i], theta[i]])
    y = z - H @ x
    x = x + K @ y
    P = (np.eye(6) - K @ H) @ P

    # 存储估计值和观测值
    estimates.append(x)
    observations.append(z)

# 将估计值和观测值转换为numpy数组
estimates = np.array(estimates)
observations = np.array(observations)

# 绘制结果
plt.plot(t, observations[:, 0], label='edge')
plt.plot(t, estimates[:, 0], label='karman')
plt.legend()
plt.xlabel('time')
plt.ylabel('speed')
plt.show()