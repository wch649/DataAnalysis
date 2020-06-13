"""
统计相同时刻相同路由下的不用输入单元的CV情况
"""

import re
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
import numpy as np


# 获取每个时刻的数据数据
def get_clock(filename, process_file, clock):
    f = open(filename, "r")
    outfile = open(process_file, "w")
    for line in f:
        new_line = re.sub(r'[^A-Za-z0-9]+', ' ', line)
        str_list = new_line.split()
        if str_list[0] == clock:
            for i in range(len(str_list)):
                s = str(str_list[i]).replace('[', '').replace(']', '') + " "  # 去除[],这两行按数据不同，可以选择
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
                  '41','42','43','44','45','46','47','48','49','50',
                  '51','52']
    # print(df)
    # print(df.loc[df['1'] == '0'])
    # df.loc[(df['column'] == some_value) & df['other_column'].isin(some_values)]
    # data = df.loc[(df['0'] == '500') & (df['1'] == '0') & (df['2'] == '0')]
    # data = data.values.tolist()
    # print(len(data))
    i = 0
    while i < len(all_list):
        data = df.loc[(df['0'] == all_list[i][0]) & (df['1'] == all_list[i][1]) & (df['2'] == all_list[i][2])]
        data = data.values.tolist()
        # print(len(data))
        s = str(data[len(data)-1]).replace('[', '').replace(']', '') + " "  # 去除[],这两行按数据不同，可以选择
        s = re.sub(r'[^A-Za-z0-9]+', ' ', s)
        outfile.write(s + '\n')
        i = i + len(data)

# 排序函数
def mySort(list):
    newList=[]
    for i in range(len(list)):
        number=min(list)
        newList.append(number)
        list.remove(number)
    return newList

# 绘制子图
def draw(data,router_id):
    data = np.array(data)
    data = data.astype(np.int).tolist()
    # 定义热图的横纵坐标
    xLabel = ['0', '1', '2', '3', '4', '5', '6', '7', '8','9']
    yLabel = ['0', '1', '2', '3', '4']
    color_list = {-1:'white', 0:'white', 1:'green', 2:'yellow', 3:'darkorange', 4:'red'}
    color_kay = []
    color_value = []
    color_item = []
    # 统计结果中的-1,0,1,2的情况进行具体的绘制
    # 统计data中不同的元素
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
        color_value.append(color_list[int(key)])
    # print(color_value)
    # 作图阶段
    fig = plt.figure()
    # 定义画布为1*1个划分，并在第1个位置上进行作图
    ax = fig.add_subplot(111)
    # 定义横纵坐标的刻度
    ax.set_yticks(range(len(yLabel)))
    ax.set_yticklabels(yLabel)
    ax.set_xticks(range(len(xLabel)))
    ax.set_xticklabels(xLabel)
    # 作图并选择热图的颜色填充风格(自定义)
    cmap = colors.ListedColormap(color_value)
    heatmap = plt.pcolor(data, cmap=cmap)
    plt.grid(linestyle='-.')
    plt.colorbar(heatmap, ticks=color_kay)
    #
    #im = ax.imshow(data, cmap=plt.cm.YlGnBu, linewidths = 0.05)
    # 增加右侧的颜色刻度条
    #plt.colorbar(im)
    # 增加标题
    plt.title(router_id + "VC buffer occupation")
    # 保存图片
    str_file = router_id + '.PNG'
    plt.savefig('uniform_router'+ str_file)
    # show
    plt.show()

def process_vc(pro_file):
    f = open(pro_file, "r")
    all_list = []
    for line in f:
        new_line = re.sub(r'[^A-Za-z0-9]+', ' ', line)
        str_list = new_line.split()
        # print(str_list)
        all_list.append(str_list[3:12])
        all_list.append(str_list[13:22])
        all_list.append(str_list[23:32])
        all_list.append(str_list[33:42])
        all_list.append(str_list[43:52])
        print(all_list)
        draw(all_list,str_list[1] + '_' + str_list[2])
        all_list.clear()




if __name__ == '__main__':
    clock = 500
    # 获取某一个时刻的数据
    get_clock('vc_new1.txt', 'process_data.txt', str(clock))
    # 获取相同时刻相同路由下的最后一行
    del_data('process_data.txt', 'pro_data.txt')
    # 处理并统计某一个时刻的数据
    process_vc('pro_data.txt')
