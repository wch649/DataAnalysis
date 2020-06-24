'''
fit the <hop_count, max_buffer, min_buffer, ave_buffer, ...> with each flit latency
'''
if __name__ == "__main__":
    # m*n 2D mesh topology
    n = 8
    m = 8
    vc_num = 4
    vc_size = 8

    folder = "..\Data\data20200611_uniform_vc_4_size_8\\"

    # extract node injecting to hotspot node
    filename = folder + "total_flit.txt"
    totalfile = open(filename, 'r')
    totalflit = []
    for eachtotalline in totalfile:
        if eachtotalline.split('[')[1].split()[0] != eachtotalline.split('[')[1].split()[1]:
            totalflit.append(eachtotalline.split('{')[1].split()[0])
    # print(totalflit)
    totalfile.close()

    # extract latency
    '''
    [flitid-latency, ...]
    '''
    filename = folder + "end_filt.txt"
    endflitfile = open(filename, 'r')
    endinfo = []
    for eachendflit in endflitfile:
        curtempflit = eachendflit.split('{')[1].split()[0]
        # packet latency = atime - ctime
        curlatency = int(eachendflit.split('[')[1].split()[2]) - int(eachendflit.split('[')[1].split()[1])
        endinfo.append(curtempflit + "-" + str(curlatency))
    # print(endinfo)
    endflitfile.close()

    # extract vc occupancy
    '''
    2>,0[0000[0000[0000[0000,1[0000[0000[0000[0000
    '''
    filename = folder + "occupancy_set.txt"
    bufferfile = open(filename, 'r')
    bufferinfo = []
    for bufferline in bufferfile:
        bufferinfo.append(bufferline)
    bufferfile.close()
    # for i in range(len(bufferinfo)):
    #     print(bufferinfo[i])

    filename = folder + "pretreatment_flitpath.txt"
    flitpathfile = open(filename, 'r')
    # 0:3_4_0=7_12_0=10_20_0=13_28_0=16_36.
    filename = folder + "fitdata.txt"
    fitfile = open(filename, 'w')
    for eachline in flitpathfile:
        if eachline.find("=", 0, len(eachline) - 1) != -1:
            eachline = eachline.split('.')[0]
            curflit = eachline.split(':')[0]
            hopcount = eachline.count("=", 0, len(eachline) - 1)
            # extract average local age
            tempage = 0
            temppath = eachline.split(':')[1]  # 3_4_0=7_12_0=10_20_0=13_28_0=16_36.
            for hop_i in range(hopcount):
                tempage = tempage + int(temppath.split('=')[hop_i + 1].split('_')[0]) - int(
                    temppath.split('=')[hop_i].split('_')[0])
            average_age = round(tempage / hopcount, 2)
            localage = average_age
            # extract average vc occupancy
            tempvcbuffer = 0
            for hop_i in range(hopcount):
                arrive_nextnode_time = int(temppath.split('=')[hop_i].split('_')[0]) + 1
                nextnode = int(temppath.split('=')[hop_i + 1].split('_')[1])
                curdirection = temppath.split('=')[hop_i].split('_')[2]
                if curdirection == '0' or curdirection == '2':
                    nextnode_inputunit = int(curdirection) + 1
                elif curdirection == '1' or curdirection == '3':
                    nextnode_inputunit = int(curdirection) - 1
                else:
                    print("ERROR: current direction error!")
                    break
                # 2>,0[0000[0000[0000[0000,1[0000[0000[0000[0000,2[0000[0000[0000[0000,
                for eachbufferinfo in bufferinfo:
                    if eachbufferinfo.split('>')[0] == str(arrive_nextnode_time):
                        cur_router_occupancy = eachbufferinfo.split(',')[nextnode + 1]
                        cur_input_occupancy = cur_router_occupancy.split('[')[nextnode_inputunit + 1]
                        for vc_i in range(vc_num):
                            tempvcbuffer = tempvcbuffer + int(cur_input_occupancy[vc_i])
                        break
            average_buffer_occupancy = round((tempvcbuffer / vc_num) / hopcount, 2)
            cur_latency = ""
            for lat_i in endinfo:
                if lat_i.split('-')[0] == curflit:
                    cur_latency = lat_i.split('-')[1]
                    break
            # print(curflit, cur_latency)
            writefiledata = curflit + "," + str(hopcount) + "," + str(localage) + "," + str(
                average_buffer_occupancy) + "," + cur_latency + "\n"
            print("Write the " + curflit + " 's info!")
            fitfile.write(writefiledata)
    flitpathfile.close()
    fitfile.close()
