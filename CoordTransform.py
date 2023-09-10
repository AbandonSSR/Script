import numpy as np

# 同名点，每组数据相互对应
# 局部坐标，每组按 X、Y、Z 顺序排列。
local_coord = np.array([[-194.438, 309.283, 1211.099], [-245.192, 257.910, 1207.994], [-103.623, 9.779, 1207.012], [177.717, -88.425, 1209.289]])
# 全局坐标，每组按 X、Y、Z 顺序排列。
global_coord = np.array([[430349.3715, 4345549.531, 1204.032], [430303.7735, 4345605.175, 1200.778], [430041.428, 4345492.008, 1199.395], [429912.294, 4345223.277, 1201.119]])


# 求解平移向量和旋转矩阵
def solve_transform(a: np.array, b: np.array):
    # 计算两组点的质心
    center_1 = np.mean(a, axis=0)
    center_2 = np.mean(b, axis=0)
    # 计算两组点的去质心坐标
    a_1 = a - center_1
    b_1 = b - center_2
    # 计算两组点的协方差矩阵
    covariance_matrix = np.dot(a_1.T, b_1)
    # 对协方差矩阵进行奇异值分解
    u, s, v = np.linalg.svd(covariance_matrix)
    # 计算旋转矩阵
    rotation_matrix = np.dot(v.T, u.T)
    # 计算平移向量
    translation_vector = center_2 - np.dot(rotation_matrix, center_1)
    return rotation_matrix, translation_vector


# 构造齐次变换矩阵
def make_transform(rotation_matrix: np.array, translation_vector: np.array):
    transition_matrix = np.eye(4)
    transition_matrix[:3, :3] = rotation_matrix
    transition_matrix[:3, -1] = translation_vector
    return transition_matrix


# 测试代码
np.set_printoptions(precision=6, suppress=True)
R, t = solve_transform(local_coord, global_coord)
T = make_transform(R, t)
print("平移向量：\n", t)
print("旋转矩阵：\n", R)
print("齐次变换矩阵：\n", T)
