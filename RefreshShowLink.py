"""
show the link changes
Automatically show next picture after 1 second

"""

import tkinter as tk
import sys


def dealCurtimeData():
    global tracker
    if tracker <= len(totalData):
        each_flit = totalData[tracker].split('-')[1:]
        linkinfo = "."
        for i in each_flit:
            each_data = i.split()
            if each_data[2] != '4':
                linkinfo = linkinfo + each_data[0] + "=" + each_data[2] + "=" + each_data[3] + "."
                # print(each_data[0] + "===" + each_data[2] + "===" + each_data[3])
        for i in range(rownum):
            for j in range(colnum):
                if i % 2 == 0 and j % 2 == 0:
                    x1 = i * rectangle_size
                    y1 = j * rectangle_size
                    x2 = x1 + rectangle_size
                    y2 = y1 + rectangle_size
                    b1.create_rectangle(x1, y1, x2, y2, fill='cyan')

                elif i % 2 == 0 and j % 2 != 0:
                    # r(i, j-1) have output 0(+X)  or  r(i, j+1) have output 1(-X)
                    rightrouter = int(((rownum - 1 - i) / 2) * n + (j + 1) / 2)
                    leftrouter = int(((colnum - 1 - i) / 2) * n + (j - 1) / 2)
                    rightrouter = "." + str(rightrouter) + "=" + '1'
                    leftrouter = "." + str(leftrouter) + "=" + "0"

                    # only draw horizontal lines
                    for linenum in range(vc_num):
                        # add vc for testrouter
                        test_leftrouter = leftrouter + "=" + str(linenum)
                        test_rightrouter = rightrouter + "=" + str(linenum)
                        # caculate the (x1,y1,x2,y2) for line
                        line_x1 = j * rectangle_size
                        line_y1 = i * rectangle_size + linenum * (linespace + linewidth) + linespace / 2
                        line_x2 = (j + 1) * rectangle_size
                        line_y2 = line_y1

                        if (test_leftrouter in linkinfo):
                            b1.create_line(line_x1, line_y1, line_x2, line_y2, width=linewidth, fill='red',
                                           arrow=tk.LAST)
                        if (test_rightrouter in linkinfo):
                            b1.create_line(line_x1, line_y1, line_x2, line_y2, width=linewidth, fill='red',
                                           arrow=tk.FIRST)

                elif i % 2 != 0 and j % 2 == 0:
                    # r(i-1, j) have output 3(-Y)  or  r(i+1, j) have output 2(+Y)
                    uprouter = int(((rownum - i) / 2) * 8 + (j / 2))
                    downrouter = int((((rownum - i) / 2) - 1) * 8 + (j / 2))
                    uprouter = "." + str(uprouter) + "=" + '3'
                    downrouter = "." + str(downrouter) + "=" + "2"

                    # Only draw vertical lines
                    for linenum in range(vc_num):
                        test_uprouter = uprouter + "=" + str(linenum)
                        test_downrouter = downrouter + "=" + str(linenum)
                        # caculate the (x1,y1,x2,y2) for line
                        line_x1 = j * rectangle_size + linenum * (linespace + linewidth) + linespace / 2
                        line_y1 = i * rectangle_size
                        line_x2 = line_x1
                        line_y2 = (i + 1) * rectangle_size

                        if (test_uprouter in linkinfo):
                            b1.create_line(line_x1, line_y1, line_x2, line_y2, width=linewidth, fill='red',
                                           arrow=tk.LAST)
                        if (test_downrouter in linkinfo):
                            b1.create_line(line_x1, line_y1, line_x2, line_y2, width=linewidth, fill='red',
                                           arrow=tk.FIRST)
        tracker += 1
        if tracker > len(totalData):
            sys.exit(0)
        root.after(time_space, lambda x='all': b1.delete(x))
        root.after(time_space, dealCurtimeData)


if __name__ == '__main__':
    # m*n 2D mesh topology
    n = 8
    m = 8
    vc_num = 4

    # drawing parameter
    rectangle_size = 40  # rectangle is 40 * 40
    rownum = 2 * m - 1
    colnum = 2 * n - 1
    canwidth = 600
    canheight = 600
    linewidth = 2
    linespace = rectangle_size / (vc_num + 1)

    #showing parameter
    tracker = 0
    time_space = 1000
    show_space = 10

    # start Draw
    root = tk.Tk()
    # root.title("the link status of the time " + str(_time))
    b1 = tk.Canvas(root, width=canwidth, height=canheight, bg='white')
    b1.pack()

    filename = "..\Data\data20200611_uniform_vc_4_size_8\\flitpath.txt"
    flitpath = open(filename, "r")
    _time = 0
    totalData = []

    for eachline in flitpath:
        templine = eachline.split()
        if _time == 0:
            _time = templine[0]
            curTimeData = str(_time) + ":"
        # caculate the router number
        router = int(templine[2][17:].split('_')[0]) * n + int(templine[2][17:].split('_')[1])
        usedata = str(router) + ' ' + templine[4] + ' ' + templine[7] + ' ' + templine[9]

        if _time == templine[0]:
            curTimeData = curTimeData + '-' + usedata
        else:
            totalData.append(curTimeData)
            curTimeData = str(templine[0]) + ":"
            _time = templine[0]
            curTimeData = curTimeData + '-' + usedata
    # dont forgrt this line !!!
    totalData.append(curTimeData)
    flitpath.close()

    for i in range(len(totalData)):
        print(totalData[i])
    dealCurtimeData()
    root.mainloop()
