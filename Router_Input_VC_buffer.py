"""
直观描述数据信息
时刻、路由编号、输入单元编号、VC通道编号、VC缓存情况
"""

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import cv2
import os

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

        for p in range(n):
            for q in range(m):
                data[p][q + n + 1] = vc_0[p][q]
        for a in range(m):
            for b in range(n):
                data[a + n + 1][b + n + m + 1] = vc_1[a][b]
        for c in range(n):
            for d in range(m):
                data[c + n + m + 1][d + n + 1] = vc_2[c][d]
        for e in range(m):
            for f in range(n):
                data[e + n + 1][f] = vc_3[e][f]
        # # # 绘制图形
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
def draw(R_i, R_j, data, n, m, clock):
    # print(data)
    xLabel = []
    yLabel = []
    size = n * 2 + m + 2
    for i in range(size):
        xLabel.append(str(i))
    for j in range(size):
        yLabel.append(str(j))

    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(111)
    ax.set_yticks(range(len(yLabel)))
    ax.set_yticklabels(yLabel)
    ax.set_xticks(range(len(xLabel)))
    ax.set_xticklabels(xLabel)
    # 作图并选择热图的颜色填充风格(自定义)
    cmap = colors.ListedColormap(['gray', 'white', 'green', 'yellow', 'darkorange', 'red'])
    bounds = [-1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    heatmap = plt.pcolor(np.array(data), cmap=cmap, norm=norm)
    plt.grid(color="black")
    # plt.colorbar(heatmap, ticks=color_kay)
    # 增加标题
    plt.title(str(clock) + '_'+ str(R_i) +'_' + str(R_j) + "VC buffer occupation")
    # 保存图片
    str_file = str(R_i) + '_' + str(R_j) + '.tif'
    plt.savefig(".\\Result_picture\\"+str(clock) + '\\' + str_file)
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

# 合并图像函数
def merge_picture(merge_path,num_of_cols,num_of_rows):
    filename=file_name(merge_path,".tif")
    shape=cv2.imread(filename[0],-1).shape    #三通道的影像需把-1改成1
    cols=shape[1]
    rows=shape[0]
    channels=shape[2]
    dst=np.zeros((rows*num_of_rows,cols*num_of_cols,channels),np.uint8)
    for i in range(len(filename)):
        img=cv2.imread(filename[i],-1)
        cols_th=int(filename[i].split("_")[-1].split('.')[0])
        print(cols_th)
        rows_th=int(filename[i].split("\\")[-1].split('_')[-2])
        print(rows_th)
        roi=img[0:rows,0:cols,:]
        dst[rows_th*rows:(rows_th+1)*rows,cols_th*cols:(cols_th+1)*cols,:]=roi
    cv2.imwrite(merge_path+"merge.tif",dst)

"""遍历文件夹下某格式图片"""
def file_name(root_path,picturetype):
    filename=[]
    for root,dirs,files in os.walk(root_path):
        for file in files:
            if os.path.splitext(file)[1]==picturetype:
                filename.append(os.path.join(root,file))
    return filename


if __name__ == '__main__':
    # # 数据文件
    data_film = './process_data/uniform_router.txt'
    # 数据处理文件
    new_data_film = './process_data/new_uniform_router.txt'
    process_film = './process_data/process_data.txt'
    pro_film = './process_data/pro_data.txt'
    control_num = 500
    n = 4 # VC缓存个数
    m = 10 # VC通道数据
    num_of_cols = 8  # 列数
    num_of_rows = 8  # 行数

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
            print(clock)
            get_clock(new_data_film, process_film, clock)
            del_data(process_film, pro_film)
            #创建文件
            root_pass = os.getcwd()
            filename = ".\\Result_picture\\" + str(clock)
            os.mkdir(filename)
            os.chdir(filename)
            os.chdir(root_pass)
            process_data(pro_film, n, m, clock)
            # 合并文件
            merge_path = ".\\Result_picture\\"+ str(clock)  # 要合并的小图片所在的文件夹
            merge_picture(merge_path, num_of_cols, num_of_rows)
            clock = int(clock) + control_num

