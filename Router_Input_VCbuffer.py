"""
直观描述数据信息
时刻、路由编号、输入单元编号、VC通道编号、VC缓存情况
"""

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# 去除input4的数据函数
def input_4(readfile,writefile):
    f = open(readfile, "r")
    outfile = open(writefile, "w")
    for line in f:
        new_line = re.sub(r'[^A-Za-z0-9]+', ' ', line)
        str_list = new_line.split()
        # print(str_list)
        for i in range(len(str_list)-10):
            s = str(str_list[i]).replace('[', '').replace('', '').replace(']', '') + " "  # 去除[],这两行按数据不同，可以选择
            outfile.write(s)
        outfile.write('\n')
    outfile.close()

# 获取每个时刻的数据进行处理
def get_clock(filename, process_file, clock):
    f = open(filename, "r")
    outfile = open(process_file, "w")
    for line in f:
        new_line = re.sub(r'[^A-Za-z0-9]+', ' ', line)
        str_list = new_line.split()
        # print(str_list)
        if str_list[0] == str(clock) :
            for i in range(len(str_list)):
                # print(str_list[i])
                s = str(str_list[i]).replace('[', '').replace('', '').replace(']', '') + " "  # 去除[],这两行按数据不同，可以选择
                outfile.write(s)
            outfile.write('\n')
    outfile.close()

# 只保留相同时刻下的相同路由的最后一行数据
def del_data(process_file,pro_file):
    f = open(process_file, "r")
    outfile = open(pro_file, "w")
    all_list = []
    for line in f:
        new_line = re.sub(r'[^A-Za-z0-9]+', ' ', line)
        str_list = new_line.split()
        all_list.append(str_list)

    df = pd.DataFrame(all_list)
    df.columns = ['0','1','2','3','4','5','6','7','8','9','10',
                  '11','12','13','14','15','16','17','18','19','20',
                  '21','22','23','24','25','26','27','28','29','30',
                  '31','32','33','34','35','36','37','38','39','40',
                  '41','42']
    i = 0
    while i < len(all_list):
        data = df.loc[(df['0'] == all_list[i][0]) & (df['1'] == all_list[i][1]) & (df['2'] == all_list[i][2])]
        data = data.values.tolist()
        # print(len(data))
        s = str(data[len(data)-1]).replace('[', '').replace(']', '') + " "  # 去除[]
        s = re.sub(r'[^A-Za-z0-9]+', ' ', s)
        outfile.write(s + '\n')
        i = i + len(data)


# 列表转置函数
def transpose(matrix):
    new_matrix = []
    for i in range(len(matrix[0])):
        matrix1 = []
        for j in range(len(matrix)):
            matrix1.append(matrix[j][i])
        new_matrix.append(matrix1)
    return new_matrix

# 列表倒序函数
def turn (matrix):
    new_matrix =list(reversed(matrix))
    return new_matrix
# 列表扩充矩阵
def expend_matrix(list):
    data = []
    # print(list)
    for i in list:
        if i == '0':
            data.append([0,0,0,0])
        if i == '1':
            data.append([1,0,0,0])
        if i == '2':
            data.append([2,2,0,0])
        if i == '3':
            data.append([3,3,3,0])
        if i == '4':
            data.append([4,4,4,4])
    data = transpose(data)
    # print(data)
    return data


# 处理每个时刻的数据情况
def process_data(process_file, n, m, clock):
    # m 表示行数
    # n 表示列数
    size = n * 2 + m + 2
    print(size)
    data = [[-1] * size for _ in range(size)]

    f = open(process_file, "r")
    list = f.readlines()
    all_list = []
    for i in range(len(list)):
        new_line = re.sub(r'[^A-Za-z0-9]+', ' ', list[i])
        str_list = new_line.split()
        # print(str_list)
        all_list.append(str_list)
    # print(len(all_list[0]))
    # print("input_0"+ str(all_list[24][3:13]))
    # print("input_1" + str(all_list[24][13:23]))
    # print("input_2" + str(all_list[24][23:33]))
    # print("input_3" + str(all_list[24][33:43]))
    for i in range(len(all_list)):
        R_i = all_list[i][1]
        R_j = all_list[i][2]
        vc_0 = expend_matrix(all_list[i][3:13])
        vc_1 = turn(transpose(expend_matrix(all_list[i][13:23])))
        vc_2 = turn(expend_matrix(all_list[i][23:33]))
        vc_3 = transpose(expend_matrix(all_list[i][33:43]))
        vc_0 = np.array(vc_0)
        vc_0 = vc_0.astype(np.int).tolist()
        vc_1 = np.array(vc_1)
        vc_1 = vc_1.astype(np.int).tolist()
        vc_2 = np.array(vc_2)
        vc_2 = vc_2.astype(np.int).tolist()
        vc_3 = np.array(vc_3)
        vc_3 = vc_3.astype(np.int).tolist()
        for p in range(4):
            for q in range(10):
                data[p][q + 5] = vc_0[p][q]
        for a in range(10):
            for b in range(4):
                data[a + 5][b + 16] = vc_1[a][b]
        for c in range(4):
            for d in range(10):
                data[c + 16][d + 5] = vc_2[c][d]
        for e in range(10):
            for f in range(4):
                data[e + 5][f] = vc_3[e][f]
        # # 绘制图形
        # print(len(data))
        print(R_i,R_j)
        draw(R_i, R_j, data, clock)

# 排序函数
def mySort(list):
    newList = []
    for i in range(len(list)):
        number = min(list)
        newList.append(number)
        list.remove(number)
    return newList
# 绘制图形函数
def draw(R_i, R_j, data, clock):
    xLabel = []
    yLabel = []
    for i in range(20):
        xLabel.append(str(i))
    for j in range(20):
        yLabel.append(str(j))
    color_list = {-1: 'gray', 0: 'white', 1: 'green', 2: 'yellow', 3: 'darkorange', 4: 'red'}
    color_kay = []
    color_value = []
    color_item = []
    # 控制颜色
    for i in range(len(data)):
        color_set = set(data[i])
        for j in color_set:
            color_item.append(j)
    # print(color_item)
    color_set2 = set(color_item)
    # print(color_set2)
    # 将不同的元素对应不同的颜色
    for i in color_set2:
        color_kay.append(i)
    color_kay = mySort(color_kay)
    # print(color_kay)
    for key in color_kay:
        color_value.append(color_list[key])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_yticks(range(len(yLabel)))
    ax.set_yticklabels(yLabel)
    ax.set_xticks(range(len(xLabel)))
    ax.set_xticklabels(xLabel)
    # 作图并选择热图的颜色填充风格(自定义)
    cmap = colors.ListedColormap(color_value)
    heatmap = plt.pcolor(data, cmap=cmap)
    plt.grid(color="black")
    plt.colorbar(heatmap, ticks=color_kay)
    # 增加标题
    plt.title(str(R_i) +'_' + str(R_j) + "VC buffer occupation")
    # 保存图片
    str_file = str(R_i) + '_' + str(R_j) + '.PNG'
    plt.savefig('./process_data/Result_picture'+str(clock) + '_' + str_file)
    # 图片的显示
    plt.show()

# 统计开始时刻和结束时刻
def seak_clock(filename):
    f = open(filename, "r")
    clock_set = set()
    clock = []
    for line in f:
        new_line = re.sub(r'[^A-Za-z0-9]+', ' ', line)
        str_list = new_line.split()
        if str_list[0] not in clock_set:
            clock_set.add(str_list[0])
            clock.append(str_list[0])
    first_clock = clock[0]
    end_clock = clock[len(clock) - 1]
    return first_clock, end_clock

if __name__ == '__main__':
    # # 数据文件
    data_film = './process_data/uniform_router.txt'
    # 数据处理文件
    new_data_film = './process_data/new_uniform_router.txt'
    process_film = './process_data/process_data.txt'
    pro_film = './process_data/pro_data.txt'
    control_num = 500
    n = 4
    m = 10
    input_4(data_film, new_data_film)
    # 获取当前时刻处理文件
    # 获取开始时刻和结束时刻
    first_clock, end_clock = seak_clock(new_data_film)
    print(first_clock, end_clock)

    clock = int(first_clock)
    while True:
        if clock > int(end_clock):
            break
        else:
            # 获取某一个时刻的数据
            # print(clock)
            get_clock(new_data_film, process_film, clock)
            del_data(process_film, pro_film)
            process_data(pro_film, n, m, clock)
            clock = int(clock) + control_num

