import tkinter as tk
import re

def draw(flit_data,node,vc_data):
    root = tk.Tk()
    root.title("网络依赖图")
    Router_b = tk.Canvas(root, width=1075, height=1075, bg='white')
    Router_r = 75
    Router_size = 50
    Router_b.pack()
    for i in range(8):
        for j in range(8):
            x0 = Router_r * (j + 1) + Router_size * j
            y0 = Router_r * (i + 1) + Router_size * i
            x1 = x0 + Router_size
            y1 = y0 + Router_size
            Router_b.create_rectangle(x0, y0, x1, y1, fill='MediumBlue')
            Router_b.create_text(x0 + Router_size / 2, y0 + Router_size / 2, text=str(i * 8 + j), fill='yellow')
            for n in range(4):
                Router_b.create_rectangle(x0, y0 - Router_size / 2, x0 + (n + 1) * (Router_size / 4), y0)
                Router_b.create_rectangle(x1, y0, x1 + Router_size / 2, y0 + (n + 1) * (Router_size / 4))
                Router_b.create_rectangle(x1, y1, x1 - (n + 1) * (Router_size / 4), y1 + Router_size / 2)
                Router_b.create_rectangle(x0, y1, x0 - Router_size / 2, y1 - (n + 1) * (Router_size / 4))

    for j in range(len(node)):

        y_id = int(node[j]) // 8 * 125 + 100
        x_id = int(node[j]) % 8 * 125 + 100
        #绘制VC情况
        Router_b.create_rectangle(x_id - 25, y_id - 25, x_id - 25 + Router_size / 4,
                                  y_id - 25 - Router_size / 16 * int(vc_data[j][0]), fill='red')
        Router_b.create_rectangle(x_id - 25 + Router_size / 4, y_id - 25, x_id - 25 + Router_size / 4 * 2,
                                  y_id - 25 - Router_size / 16 * int(vc_data[j][1]), fill='red')
        Router_b.create_rectangle(x_id - 25 + Router_size / 4 * 2, y_id - 25, x_id - 25 + Router_size / 4 * 3,
                                  y_id - 25 - Router_size / 16 * int(vc_data[j][2]), fill='red')
        Router_b.create_rectangle(x_id - 25 + Router_size / 4 * 3, y_id - 25, x_id - 25 + Router_size,
                                  y_id - 25 - Router_size / 16 * int(vc_data[j][3]), fill='red')

        Router_b.create_rectangle(x_id + 25, y_id - 25, x_id + 25 + Router_size / 16 * int(vc_data[j][4]),
                                  y_id - 25 + Router_size / 4, fill='red')
        Router_b.create_rectangle(x_id + 25, y_id - 25 + Router_size / 4,
                                  x_id + 25 + Router_size / 16 * int(vc_data[j][5]),
                                  y_id - 25 + Router_size / 4 * 2, fill='red')
        Router_b.create_rectangle(x_id + 25, y_id - 25 + Router_size / 4 * 2,
                                  x_id + 25 + Router_size / 16 * int(vc_data[j][6]),
                                  y_id - 25 + Router_size / 4 * 3, fill='red')
        Router_b.create_rectangle(x_id + 25, y_id - 25 + Router_size / 4 * 3,
                                  x_id + 25 + Router_size / 16 * int(vc_data[j][7]),
                                  y_id - 25 + Router_size,fill='red')

        Router_b.create_rectangle(x_id - 25, y_id + 25, x_id - 25 + Router_size / 4,
                                  y_id + 25 + Router_size / 16 * int(vc_data[j][8]), fill='red')
        Router_b.create_rectangle(x_id - 25 + Router_size / 4, y_id + 25, x_id - 25 + Router_size / 4 * 2,
                                  y_id + 25 + Router_size / 16 * int(vc_data[j][9]),fill='red')
        Router_b.create_rectangle(x_id - 25 + Router_size / 4 * 2, y_id + 25, x_id - 25 + Router_size / 4 * 3,
                                  y_id + 25 + Router_size / 16 * int(vc_data[j][10]),fill='red')
        Router_b.create_rectangle(x_id - 25 + Router_size / 4 * 3, y_id + 25, x_id - 25 + Router_size,
                                  y_id + 25 + Router_size / 16 * int(vc_data[j][11]),fill='red')

        Router_b.create_rectangle(x_id - 25, y_id - 25, x_id - 25 - Router_size / 16 * int(vc_data[j][12]),
                                  y_id - 25 + Router_size / 4,
                                  fill='red')
        Router_b.create_rectangle(x_id - 25, y_id - 25 + Router_size / 4,
                                  x_id - 25 - Router_size / 16 * int(vc_data[j][13]),
                                  y_id - 25 + Router_size / 4 * 2,
                                  fill='red')
        Router_b.create_rectangle(x_id - 25, y_id - 25 + Router_size / 4 * 2,
                                  x_id - 25 - Router_size / 16 * int(vc_data[j][14]),
                                  y_id - 25 + Router_size / 4 * 3,
                                  fill='red')
        Router_b.create_rectangle(x_id - 25, y_id - 25 + Router_size / 4 * 3,
                                  x_id - 25 - Router_size / 16 * int(vc_data[j][15]), y_id - 25 + Router_size,
                                  fill='red')
        # 确定输出那一条链路
        if (flit_data[j].split('_')[4] == '0'):
            # 确定下一跳的方向
            if (flit_data[j].split('_')[3] == '0'):
                Router_b.create_line(x_id + 50, y_id - 18.75, x_id + 75, y_id - 18.75, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '1'):
                Router_b.create_line(x_id + 50, y_id - 6.25, x_id + 50, y_id - 6.25, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '2'):
                Router_b.create_line(x_id + 50, y_id + 6.25, x_id + 50, y_id + 6.25, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '3'):
                Router_b.create_line(x_id + 50, y_id + 18.75, x_id + 50, y_id + 18.75, width='3', arrow=tk.LAST,
                                     fill='red')


        if (flit_data[j].split('_')[4] == '1'):
            if (flit_data[j].split('_')[3] == '0'):
                Router_b.create_line(x_id - 50, y_id - 18.75, x_id - 75, y_id - 18.75, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '1'):
                Router_b.create_line(x_id - 50, y_id - 6.25, x_id - 75, y_id - 6.25, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '2'):
                Router_b.create_line(x_id - 50, y_id + 18.75, x_id - 75, y_id + 18.75, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '3'):
                Router_b.create_line(x_id - 50, y_id + 6.25, x_id - 75, y_id + 6.25, width='3', arrow=tk.LAST,
                                     fill='red')


        if (flit_data[j].split('_')[4] == '2'):
            if (flit_data[j].split('_')[3] == '0'):
                Router_b.create_line(x_id - 18.75, y_id + 50, x_id - 18.75, y_id + 75, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '1'):
                Router_b.create_line(x_id - 6.25, y_id + 50, x_id - 6.25, y_id + 75, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '2'):
                Router_b.create_line(x_id + 18.75, y_id + 50, x_id + 18.75, y_id + 75, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '3'):
                Router_b.create_line(x_id + 6.25, y_id + 50, x_id + 6.25, y_id + 75, width='3', arrow=tk.LAST,
                                     fill='red')


        if (flit_data[j].split('_')[4] == '3'):
            if (flit_data[j].split('_')[3] == '0'):
                Router_b.create_line(x_id - 18.75, y_id - 50, x_id - 18.75, y_id - 75, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '1'):
                Router_b.create_line(x_id - 6.25, y_id - 50, x_id - 6.25, y_id - 75, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '2'):
                Router_b.create_line(x_id + 18.75, y_id - 50, x_id + 18.75, y_id - 75, width='3', arrow=tk.LAST,
                                     fill='red')

            if (flit_data[j].split('_')[3] == '3'):
                Router_b.create_line(x_id + 6.25, y_id - 50, x_id + 6.25, y_id - 75, width='3', arrow=tk.LAST,
                                     fill='red')

    root.after(3000, lambda: root.destroy())
    root.mainloop()




if __name__ == '__main__':

    node = []
    vc_data = []
    all_router = []
    flit_data = []

    file = "./data/hot_4_VC_Size_8/vc_buffer_occupancy.txt"
    vc = open(file, "r")
    vc_item = []
    for vcline in vc:
        newvcline = re.sub(r'[^A-Za-z0-9]+', ' ', vcline)
        vc_list = newvcline.split()
        vc_item.append(vc_list)
    vc.close()


    #!!!!!!!pretreatment_flitpath这个文件我是添加了一些属性
    #!!!!!!!把路径的文件中的属性都添加上了
    #flitpath = flitpath + _time + "_" + str(_router) + "_" + _flit+ "_" + _link +  "_" +_output  + ".\n"

    filename = "./data/hot_4_VC_Size_8/pretreatment_flitpath.txt"
    path = open(filename, "r")
    for pathline in path:
        newline = pathline.split('.')
        router = newline[0].split('=')
        all_router.append(router)
    path.close()
    for i in range(len(all_router)):
        # print(all_router[i])
        for s in range(len(all_router[i])):
            flit_data.append(all_router[i][s])
            node.append(all_router[i][s].split('_')[1])
            for j in range(len(vc_item)):
                if (int(all_router[i][s].split('_')[1]) == int(vc_item[j][4]) * 8 + int(vc_item[j][5]) and int(
                        all_router[i][s].split('_')[2]) == int(vc_item[j][6])):
                    vc_data.append(vc_item[j][11:27])

        draw(flit_data,node,vc_data)
        flit_data.clear()
        node.clear()
        vc_data.clear()
