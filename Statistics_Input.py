"""
统计路由器的每个输入单元的情况
主要思路如下：
1、获取同一时刻下的同一个路由的数据
2、然后分析路由器的输入单元下的VC情况

"""
import re
import matplotlib.pyplot as plt
from matplotlib import colors


# 获取每个时刻的数据数据
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

# 处理每个时刻每个路由的输入单元VC缓存的占用情况

# 处理路由编号问题
def Router_id(list, row):
    new_list = []
    for i in range(len(list)):
        list[i][1] = str(int(list[i][1]) * 8 + int(list[i][2]))
    for item in list:
        # 删除一行中第c列的值
        rest_l = item[:row]
        rest_l.extend(item[row + 1:])
        # 将删除后的结果加入结果数组
        new_list.append(rest_l)
    return new_list

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


# 处理数据
def process_data(process_file):
    f = open(process_file, "r")
    all_list = []
    row = 2
    for line in f:
        new_line = re.sub(r'[^A-Za-z0-9]+', ' ', line)
        str_list = new_line.split()
        all_list.append(str_list)
    # 将路由编号处理处理成一维编号
    new_list = Router_id(all_list, row)
    f.close()

    f = open(process_file, "w")
    for i in range(len(new_list)):
        s = str(new_list[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        f.write(s)

# 统计数据
def result_data(process_file, result_film,clock, n, m):
    data = [[-1] * n for _ in range(m)]
    f = open(process_file, "r")
    all_list = []
    # 将处理文件中的相同时刻的数据存入数组中
    for line in f:
        # print(line)
        str_list = line.split()
        all_list.append(str_list)
    # 进行统计汇总
    for i in range(len(all_list)):
        print(all_list[i])
        count = statistic_data(all_list[i][-50:])
        print(count)
        print(int(all_list[i][1]),int(all_list[i][2]))
        data[int(all_list[i][1])][int(all_list[i][2])] = count.index(max(count[0], count[1], count[2]))
    # print(len(data), len(data[0]))
    # print(data)
    # 将结果保存到文件中
    with open(result_film, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
        id = "第" + str(clock) + "时刻统计结果：" + '\n'
        file.write(id)
        for i in range(len(data)):
            s = str(data[i]).replace('[', '').replace(']', '') + " "  # 去除[],这两行按数据不同，可以选择
            file.write(s)
            file.write('\n')
        file.write('\n')
    file.close()
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
def draw(data, clock, n, m):
    # 定义热图的横纵坐标
    xLabel = []
    yLabel = []
    for i in range(m):
        xLabel.append(str(i))
    for j in range(n):
        yLabel.append(str(j))
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
    fig = plt.figure(figsize=(18,10))
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
    plt.savefig('./process_data/uniform_input'+ str_file)
    # show
    plt.show()

def transpose(matrix):
    new_matrix = []
    for i in range(len(matrix[0])):
        matrix1 = []
        for j in range(len(matrix)):
            matrix1.append(matrix[j][i])
        new_matrix.append(matrix1)
    return new_matrix

# 控制循环函数
def run_clock(n, m, first_clock, end_clock, control_num, data_film, process_film, result_film):
    clock = int(first_clock)
    while True:
        if clock > int(end_clock):
            break
        else:
            # 获取某一个时刻的数据
            get_clock(data_film, process_film, str(clock))
            # 处理并统计某一个时刻的数据
            process_data(process_film)
            # 保存数据
            data = result_data(process_film, result_film, clock, n, m)
            # print(data)
            data1 = transpose(data)
            # print(data1)
            draw(data1, str(clock), n, m)
            clock = int(clock) + int(control_num)

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

if __name__ == '__main__':
    data_film = './process_data/uniform_router.txt'
    process_film = './process_data/process_data.txt'
    result_film = './process_data/result_input.txt'
    control_num = 100
    n = 5
    m = 64
    first, end = seak_clock(data_film)
    print(first, end)
    # 开始时刻
    first_clock = first
    # 结束时刻
    end_clock = end
    run_clock(n, m, first_clock, end_clock, control_num, data_film, process_film, result_film)

    print("success")