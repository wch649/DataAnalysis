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
        if str_list[5] != '4':
            for i in range(len(str_list)):
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
        if str_list[0] == clock:
            for i in range(len(str_list)):
                s = str(str_list[i]).replace('[', '').replace('','').replace(']', '') + " "  # 去除[],这两行按数据不同，可以选择
                outfile.write(s)
            outfile.write('\n')
    outfile.close()

# 列表转置函数
def transpose(matrix):
    new_matrix = []
    for i in range(len(matrix[0])):
        matrix1 = []
        for j in range(len(matrix)):
            matrix1.append(matrix[j][i])
        new_matrix.append(matrix1)
    return new_matrix

# 处理每个时刻的数据情况
def process_data(process_file,result_file, n, m):
    # m 表示行数
    # n 表示列数
    size = n * 2 + m + 2
    print(size)
    data = [[-1] * size for _ in range(size)]
    all_data = []
    Router_i = []
    Router_j = []
    f = open(process_file, "r")
    outfile = open(result_file, "w+")
    list = f.readlines()
    all_list = []
    for i in range(len(list)):
        new_line = re.sub(r'[^A-Za-z0-9]+', ' ', list[i])
        str_list = new_line.split()
        # print(str_list)
        all_list.append(str_list)
    # print(len(all_list[0]))

    # print(len(str_list))
    df = pd.DataFrame(all_list)
    columns_id = []
    for i in range(len(str_list)):
        # print(str(i))
        columns_id.append(str(i))
    # print(columns_id)
    df.columns = columns_id
    # print(df)
    # df.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
    #               '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    #               '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
    #               '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
    #               '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
    #               '51', '52']
    # 获取相同时刻下的相同路由的数据
    i = 0
    while i < len(all_list):
        id = df.loc[(df['1'] == all_list[i][1]) & (df['2'] == all_list[i][2])]
        # 获取路由编号
        R_i = all_list[i][1]
        R_j = all_list[i][2]
        # id表示的为DataFrame类型的格式
        # print(id)
        # 将id的DataFrame类型的格式转化列表类型的格式
        id = id.values.tolist()
        # print(id)
        # 处理获得相同路由下的数据，并进行显示。
        vc_0 = []
        vc_1 = []
        vc_2 = []
        vc_3 = []
        # print(len(id))
        # print(len(id[0]))
        # print(len(data))
        # print(len(data[0]))
        for j in range(len(id)):
            if id[j][5] == '0':
                # print('0')
                # 获取最后50个数字
                vc_0.append(id[j][6:16])
                vc_0.append(id[j][16:26])
                vc_0.append(id[j][26:36])
                vc_0.append(id[j][36:46])
                vc_0.append(id[j][46:56])
                # print(len(vc_0))
                # print(len(vc_0[0]))
                # 将获取的vc_0进行转置
                # print(vc_0)
                vc_0 = transpose(vc_0)
                # print(vc_0)
                vc_0 = np.array(vc_0)
                vc_0 = vc_0.astype(np.int).tolist()
                for p in range(10):
                    for q in range(5):
                        data[p][q+11] = vc_0[p][q]
            if id[j][5] == '1':
                # print('1')
                # 获取最后50个数字
                vc_1.append(id[j][6:16])
                vc_1.append(id[j][16:26])
                vc_1.append(id[j][26:36])
                vc_1.append(id[j][36:46])
                vc_1.append(id[j][46:56])
                # print(vc_1)
                vc_1 = np.array(vc_1)
                vc_1 = vc_1.astype(np.int).tolist()
                for p in range(5):
                    for q in range(10):
                        # print(vc_1[p][q])
                        # print(p+11)
                        # print(q+17)
                        data[p+11][q+17] = vc_1[p][q]
            if id[j][5] == '2':
                # print('2')
                # 获取最后50个数字
                vc_2.append(id[j][6:16])
                vc_2.append(id[j][16:26])
                vc_2.append(id[j][26:36])
                vc_2.append(id[j][36:46])
                vc_2.append(id[j][46:56])

                vc_2 = transpose(vc_2)
                vc_2 = np.array(vc_2)
                vc_2 = vc_2.astype(np.int).tolist()
                for p in range(10):
                    for q in range(5):
                        data[p + 17][q + 11] = vc_0[p][q]
            if id[j][5] == '3':
                # print('3')
                # 获取最后50个数字
                vc_3.append(id[j][6:16])
                vc_3.append(id[j][16:26])
                vc_3.append(id[j][26:36])
                vc_3.append(id[j][36:46])
                vc_3.append(id[j][46:56])
                vc_3 = np.array(vc_3)
                vc_3 = vc_3.astype(np.int).tolist()
                for p in range(5):
                    for q in range(10):
                        # print(vc_3[p][q])
                        # print(p + 11)
                        # print(q)
                        data[p + 11][q] = vc_3[p][q]
        # 绘制图形
        draw(R_i, R_j, data)



        # 将结果保存到文件
        # print(R_i,R_j)
        # Router_i.append(R_i)
        # Router_j.append(R_j)
        # all_data.append(data)

        # s = R_i + ' ' + R_j + "\n"
        # outfile.write(s)
        # for a in range(len(data)):
        #     # print(data[a])
        #     s = str(data[a]).replace('[', '').replace('', '').replace(']', '') + " "  # 去除[],这两行按数据不同，可以选择
        #     s = re.sub(r',', ' ', s)
        #     outfile.write(s + "\n")
        i = i + len(id)



# 排序函数
def mySort(list):
    newList = []
    for i in range(len(list)):
        number = min(list)
        newList.append(number)
        list.remove(number)
    return newList

# 绘制图形函数
def draw(Router_i, Router_j, data):
    # f = open(filename, "r")
    # list = f.readlines()
    # for i in range(len(list)):
    #     str_list = list[i].split()
    # for i in list[0]:
    #     print(i)

    # for i in range(len(all_data)):
    #     print(all_data[i])
    # for i in Router_i:
    #     print(i)
    # for j in Router_j:
    #     print(j)
    xLabel = []
    yLabel = []
    for i in range(27):
        xLabel.append(str(i))
    for j in range(27):
        yLabel.append(str(j))
    color_list = {-1: 'white', 0: 'green', 1: 'yellow', 2: 'red'}
    color_kay = []
    color_value = []
    color_item = []

    # data = [[0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 1, 1, 1], [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]
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
    # print(color_value)
    #
    #     # 必须通过add_subplot()创建一个或多个绘图
    # 绘制n*n个图，编号从1开始
    # for i in range(len(Router_i)):
    #     print(Router_i[i], Router_j[i])
    # 创建新的figure
    fig = plt.figure()
    plt.figure(figsize=(40, 40))
    ax = plt.subplot2grid((8, 8), (int(Router_i), int(Router_j)))
    ax.set_xlabel('ax4_x')
    ax.set_yticks([])
    ax.set_yticklabels(yLabel)
    ax.set_xticks([])
    ax.set_xticklabels(xLabel)
    # 作图并选择热图的颜色填充风格(自定义)
    cmap = colors.ListedColormap(color_value)
    heatmap = plt.pcolor(data, cmap=cmap)
    plt.grid(linestyle='-.')
    plt.colorbar(heatmap, ticks=color_kay)
    # 图片的显示
    plt.show()




    


if __name__ == '__main__':
    input_4('vc_new1.txt', 'vc_new2.txt')
    get_clock('vc_new2.txt', 'process_data.txt', str(6))
    process_data('process_data.txt','result_data.txt', 10, 5)
    # draw(Router_i, Router_j, all_data)
