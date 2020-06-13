"""
统计数据中的路由拥塞程度
主要思路如下：
1、统计同一个时刻下的路由VC的拥塞情况
2、统计路由VC中缓存0的个数和4的个数
3、通过热图进行展示结果
"""

import re
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd


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
        print(len(data))
        s = str(data[len(data)-1]).replace('[', '').replace(']', '') + " "  # 去除[],这两行按数据不同，可以选择
        s = re.sub(r'[^A-Za-z0-9]+', ' ', s)
        outfile.write(s + '\n')
        i = i + len(data)


# 处理某一时刻的数据以及进行统计

# 统计每个列表中的10个VC缓存
def statistic_data(list):
    # 统计列表中个数
    count_0 = 0
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count = []
    result = {}
    for i in set(list):
        result[i] = list.count(i)
    # print(result)
    for key in result:
        if key == '0':
            count_0 = result[key]
        if key == '1':
            count_1 = result[key]
        if key == '2':
            count_2 = result[key]
        if key == '3':
            count_3 = result[key]
        if key == '4':
            count_4 = result[key]
    count.append(count_0 + count_1)
    count.append(count_2 + count_3)
    count.append(count_4)

    return count


# 汇总统计结果
def process_data(process_file, n, m):
    data = [[-1] * n for _ in range(m)]
    f = open(process_file, "r")
    all_list = []
    R_mn = set()
    count = []
    for line in f:
        new_line = re.sub(r'[^A-Za-z0-9]+', ' ', line)
        str_list = new_line.split()
        all_list.append(str_list)
    # 统计同一路由器下的所有输入单元下VC缓存情况：
    for i in range(len(all_list)):
        # print("第" + str(i) + "行:")
        if all_list[i][1] + all_list[i][2] in R_mn:
            #print(all_list[i])
            count_1 = statistic_data(all_list[i][-50:])
            m = int(all_list[i][1])
            n = int(all_list[i][2])
            for i in range(len(count_1)):
                count[i] = count_1[i] + count[i]
            # print(m, n)
            # print(count)
            # print(count.index(max(count[0], count[1], count[2])))
            data[m][n] = count.index(max(count[0], count[1], count[2]))
        else:
            # print(all_list[i])
            count = statistic_data(all_list[i][-50:])
            R_mn.add(all_list[i][1] + all_list[i][2])
            # print(int(all_list[i][1]), int(all_list[i][2]))
            # print(count)
            # print(count.index(max(count[0], count[1], count[2])))
            data[int(all_list[i][1])][int(all_list[i][2])] = count.index(max(count[0], count[1], count[2]))

    return data
# 排序函数
def mySort(list):
    newList=[]
    for i in range(len(list)):
        number=min(list)
        newList.append(number)
        list.remove(number)
    return newList

# 绘制显示图
def draw(data, clock):
    # 定义热图的横纵坐标
    xLabel = ['0', '1', '2', '3', '4', '5', '6', '7']
    yLabel = ['0', '1', '2', '3', '4', '5', '6', '7']
    color_list = {-1:'white', 0:'green', 1:'yellow', 2:'red'}
    color_kay = []
    color_value = []
    color_item = []
    """
    # 准备数据阶段
    data = [[0,0,0,0,1,1,1,1], [1,1,1,1,2,2,2,2], [0,1,2,0,1,2,0,1],
     [0,0,1,1,2,2,0,1], [0,0,0,1,1,1,2,2], [1,1,1,2,2,2,0,0],
     [0,0,0,1,1,1,2,2], [1,1,1,2,2,2,0,0]]
    """
    # 统计结果中的-1,0,1,2的情况进行具体的绘制
    # 统计data中不同的元素
    for i in range(len(data)):
        color_set = set(data[i])
        for j in color_set:
            color_item.append(j)
    print(color_item)
    color_set2 = set(color_item)
    print(color_set2)
    # 将不同的元素对应不同的颜色
    for i in color_set2:
        color_kay.append(i)
    color_kay = mySort(color_kay)
    print(color_kay)
    for key in color_kay:
        color_value.append(color_list[key])
    print(color_value)
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
    plt.title(clock + "Moments VC buffer occupation")
    # 保存图片
    str_file = clock + '.PNG'
    plt.savefig('./process_data/uniform_router'+ str_file)
    # show
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
    end_clock = clock[len(clock) - 1 ]
    return first_clock, end_clock


# 控制循环函数
def run_clock(n, m, first_clock, end_clock, control_num, data_film, process_film, pro_film, result_film):
    clock = int(first_clock)
    while True:
        if clock > int(end_clock):
            break
        else:
            # 获取某一个时刻的数据
            get_clock(data_film, process_film, str(clock))
            # 获取相同时刻相同路由下的最后一行
            del_data(process_film, pro_film)
            # 处理并统计某一个时刻的数据
            data = process_data(pro_film, n, m)
            print(data)
            # 保存结果
            filename = result_film
            with open(filename, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                id = "第" + str(clock) + "时刻统计结果：" + '\n'
                file.write(id)
                for i in range(len(data)):
                    s = str(data[i]).replace('[', '').replace(']', '') + " "  # 去除[],这两行按数据不同，可以选择
                    file.write(s)
                    file.write('\n')
                file.write('\n')
            file.close()
            draw(data, str(clock))
            clock = int(clock) + int(control_num)



if __name__ == '__main__':
    """
    注意里面控制clock的参数变化
    由于初始的时刻为3，所以这里初始化为3
    最后控制while循环的结束条件，收集数据的最后时刻
    """
    # 网络拓扑为8*8 2D meshes 结构
    n = 8
    m = 8
    # 循环步长
    control_num = 500
    # 数据文件
    data_film = './process_data/uniform_router.txt'
    # 处理文件
    process_film = './process_data/process_data.txt'
    pro_film = './process_data/pro_data.txt'
    # 统计结果文件
    result_film = './process_data/result_router.txt'
    # 获取开始时刻和结束时刻
    first, end = seak_clock(data_film)
    print(first, end)
    # 开始时刻
    first_clock = first
    # 结束时刻
    end_clock = end
    run_clock(n, m, first_clock, end_clock, control_num, data_film, process_film, pro_film, result_film)
    print("success")





