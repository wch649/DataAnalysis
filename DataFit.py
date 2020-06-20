'''
fit the <hop_count, max_buffer, min_buffer, ave_buffer, ...> with each flit latency
'''
if __name__ == "__main__":
    # m*n 2D mesh topology
    n = 8
    m = 8
    vc_num = 4
    vc_size = 8

    filename = "..\Data\data20200611_uniform_vc_4_size_8\\end_filt.txt"
    endflitfile = open(filename, 'r')
    endinfo = []
    for eachendflit in endflitfile:
        curtime = eachendflit.split()[0]
        curtempflit = eachendflit.split('{')[1].split()[0]
        # packet latency = atime - ctime
        curlatency = int(eachendflit.split('[')[1].split()[2]) - int(eachendflit.split('[')[1].split()[1])
        endinfo.append(curtime + "-" + curtempflit + "-" + str(curlatency))
    # print(endinfo)
    endflitfile.close()

    '''
    2>,0[0000[0000[0000[0000,1[0000[0000[0000[0000,2[0000[0000[0000[0000,3[0000[0000[0000[0000,4[0000[0000[0000[0000,
    '''
    filename = "..\Data\data20200611_uniform_vc_4_size_8\\occupancy_set.txt"
    bufferfile = open(filename, 'r')
    bufferinfo = []
    for bufferline in bufferfile:
        bufferinfo.append(bufferline)
    print(bufferinfo)
    bufferfile.close()

    filename = "..\Data\data20200611_uniform_vc_4_size_8\\pretreatment_flitpath.txt"
    flitpathfile = open(filename, 'r')

    # # 0:3_4_0=7_12_0=10_20_0=13_28_0=16_36.
    # # 1:3_5_0=6_4_0=9_3_0=13_2_1=17_10_0=20_18_2=25_26_0=30_34_1=34_42_0=38_50.
    # for eachline in flitpathfile:
    #     curflit = eachline.split(':')[0]
    #
    # flitpathfile.close()