"""
show the buffer changes
Automatically close window after 2 second

"""

import tkinter as tk


def dealLeastData(_time, leastdata, vc_num, vc_size, m, n):
    rectangle_size = 120  # rectangle is 120 * 120
    canwidth = 960
    canheight = 960

    input_num = 4
    time_space = 1000
    buffer_space = rectangle_size / 3
    littlerect_len = buffer_space / vc_num
    littlerect_wid = buffer_space / vc_size

    root = tk.Tk()
    root.title("the link status of the time " + str(_time))
    b1 = tk.Canvas(root, width=canwidth, height=canheight, bg='white')
    for i in range(m):
        for j in range(n):
            # Notice !!!!!!!! Associated (x,y) with (j,i)
            x1 = rectangle_size * j
            y1 = rectangle_size * i
            x2 = x1 + rectangle_size
            y2 = y1 + rectangle_size
            # router rectangle is drawn last

            router_id = (m - 1 - i) * n + j
            router_rightbuffer = leastdata[router_id].split('[')[1][1:vc_num * 2]  # 0 +X
            router_leftbuffer = leastdata[router_id].split('[')[2][1:vc_num * 2]  # 1 -X
            router_upbuffer = leastdata[router_id].split('[')[3][1:vc_num * 2]  # 2 +Y
            router_downbuffer = leastdata[router_id].split('[')[4][1:vc_num * 2]  # 3 -Y
            # print(router_id, router_rightbuffer, router_leftbuffer, router_upbuffer, router_downbuffer)

            # draw the 0 input buffer (+X)
            rightbuffer_x1 = x2 - buffer_space
            rightbuffer_y1 = y1 + buffer_space
            rightbuffer_x2 = x2
            rightbuffer_y2 = y2 - buffer_space
            b1.create_rectangle(rightbuffer_x1, rightbuffer_y1, rightbuffer_x2, rightbuffer_y2, fill='cyan')
            for post_x in range(vc_num):
                if int(router_rightbuffer.split()[post_x]) != 0:
                    postx_vc_x1 = rightbuffer_x2 - littlerect_wid * int(router_rightbuffer.split()[post_x])
                    postx_vc_y1 = rightbuffer_y1 + post_x * littlerect_len
                    postx_vc_x2 = rightbuffer_x2
                    postx_vc_y2 = rightbuffer_y1 + (post_x + 1) * littlerect_len
                    b1.create_rectangle(postx_vc_x1, postx_vc_y1, postx_vc_x2, postx_vc_y2, fill='red')

            # draw the 1 input buffer (-X)
            leftbuffer_x1 = x1
            leftbuffer_y1 = y1 + buffer_space
            leftbuffer_x2 = x1 + buffer_space
            leftbuffer_y2 = y2 - buffer_space
            b1.create_rectangle(leftbuffer_x1, leftbuffer_y1, leftbuffer_x2, leftbuffer_y2, fill='cyan')
            for neg_x in range(vc_num):
                if int(router_leftbuffer.split()[neg_x]) != 0:
                    negx_vc_x1 = leftbuffer_x1
                    negx_vc_y1 = leftbuffer_y1 + neg_x * littlerect_len
                    negx_vc_x2 = leftbuffer_x1 + littlerect_wid * int(router_leftbuffer.split()[neg_x])
                    negx_vc_y2 = leftbuffer_y1 + (neg_x + 1) * littlerect_len
                    b1.create_rectangle(negx_vc_x1, negx_vc_y1, negx_vc_x2, negx_vc_y2, fill='red')

            # draw the 2 input buffer (+Y)
            upbuffer_x1 = x1 + buffer_space
            upbuffer_y1 = y1
            upbuffer_x2 = x2 - buffer_space
            upbuffer_y2 = y1 + buffer_space
            b1.create_rectangle(upbuffer_x1, upbuffer_y1, upbuffer_x2, upbuffer_y2, fill='cyan')
            for post_y in range(vc_num):
                if int(router_upbuffer.split()[post_y]) != 0:
                    posty_vc_x1 = upbuffer_x1 + post_y * littlerect_len
                    posty_vc_y1 = upbuffer_y1
                    posty_vc_x2 = upbuffer_x1 + (post_y + 1) * littlerect_len
                    posty_vc_y2 = upbuffer_y1 + littlerect_wid * int(router_upbuffer.split()[post_y])
                    b1.create_rectangle(posty_vc_x1, posty_vc_y1, posty_vc_x2, posty_vc_y2, fill='red')

            # draw the 3 input buffer (-Y)
            downbuffer_x1 = x1 + buffer_space
            downbuffer_y1 = y2 - buffer_space
            downbuffer_x2 = x2 - buffer_space
            downbuffer_y2 = y2
            b1.create_rectangle(downbuffer_x1, downbuffer_y1, downbuffer_x2, downbuffer_y2, fill='cyan')
            for neg_y in range(vc_num):
                if int(router_downbuffer.split()[neg_y]) != 0:
                    negy_vc_x1 = downbuffer_x1 + neg_y * littlerect_len
                    negy_vc_y1 = downbuffer_y2 - littlerect_wid * int(router_downbuffer.split()[neg_y])
                    negy_vc_x2 = downbuffer_x1 + (neg_y + 1) * littlerect_len
                    negy_vc_y2 = downbuffer_y2
                    b1.create_rectangle(negy_vc_x1, negy_vc_y1, negy_vc_x2, negy_vc_y2, fill='red')
            # Draw the border of the rectangle
            b1.create_rectangle(x1, y1, x2, y2, width=4)

    b1.pack()
    # Automatically close window after a certain time
    root.after(time_space, lambda: root.destroy())
    root.mainloop()


if __name__ == '__main__':
    # m*n 2D mesh topology
    n = 8
    m = 8
    vc_num = 4
    vc_size = 8

    show_space = 10

    filename = "..\Data\data20200619_hotspot_vc_4_size_8_node{20}_rate_{1}_irate_0.3\\vc_buffer_occupancy.txt"
    flitpath = open(filename, "r")
    _time = 0
    leastdata = ""
    emptydata = "[ 0 0 0 0  ][ 0 0 0 0  ][ 0 0 0 0  ][ 0 0 0 0  ]"

    for routi in range(m * n):
        leastdata = leastdata + str(routi) + " " + emptydata + "-"
    leastdata = leastdata.split("-")

    for eachline in flitpath:
        templine = eachline.split()
        if _time == 0:
            _time = templine[0]
            curTimeData = str(_time) + ":"
        # caculate the router number: from "network_0/router_1_2" ==> 1 2 ==> router: 10
        router = int(templine[2][17:].split('_')[0]) * n + int(templine[2][17:].split('_')[1])
        usedata = str(router) + ' ' + str(eachline.split("==")[1][8:56])

        if _time == templine[0]:
            curTimeData = curTimeData + '-' + usedata
        else:
            # complete the least vc_buffer data
            each_router_data = curTimeData.split("-")
            curTimeData = str(_time) + ":"
            curTimeData = curTimeData + '-' + usedata
            for routi in range(m * n):
                for each_index in each_router_data:
                    temp_each_index = each_index.split()
                    if temp_each_index[0] == str(routi):
                        leastdata[routi] = each_index
            # deal the current least vc_buffer data, note: leastdata is a list
            print(leastdata)
            if int(_time) % show_space == 0:
                dealLeastData(_time, leastdata, vc_num, vc_size, m, n)
        _time = templine[0]
<<<<<<< HEAD:DrawBufferStatus.py
    if int(_time) % show_space == 0:
        dealLeastData(_time, leastdata, vc_num, vc_size, m, n)
    flitpath.close()
=======
>>>>>>> c3dfce07ca0c85506ee4bd0ad9a838c4ad61670e:fitting.py
