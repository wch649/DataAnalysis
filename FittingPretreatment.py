'''
Preprocess the data:
flit:time_node_link=time_node_link=...=time_node.
'''

if __name__ == "__main__":
    # m*n 2D mesh topology
    n = 8
    m = 8
    vc_num = 4
    vc_size = 8

    # count the flit number
    flit_number = 0
    filename = "..\Data\data20200611_uniform_vc_4_size_8\\total_flit.txt"
    totalflit = open(filename, "r")
    while True:
        buffer = totalflit.read(1024 * 8192)
        if not buffer:
            break
        flit_number += buffer.count('\n')
    print(flit_number)
    totalflit.close()

    # count the path number
    filename = "..\Data\data20200611_uniform_vc_4_size_8\\flitpath.txt"
    pathflit = open(filename, "r")
    eachline = []
    for patheachline in pathflit:
        eachline.append(patheachline)
    pathnumber = len(eachline)
    pathflit.close()

    # 3 | network_0/router_1_5 | 6 output: [ 1 , 0 ].
    print(pathnumber)
    filename = "..\Data\data20200611_uniform_vc_4_size_8\\pretreatment_flitpath.txt"
    pretreatment_flit_path = open(filename, "w")

    for curflit in range(flit_number):
        flitpath = str(curflit) + ":"
        for curindex in range(pathnumber):
            _flit = eachline[curindex].split('|')[2].split()[0]
            if _flit == str(curflit):
                _output = eachline[curindex].split('|')[2].split()[3]
                _link = eachline[curindex].split('|')[2].split()[5]
                _time = eachline[curindex].split('|')[0][:-1]
                _router = int(eachline[curindex].split('|')[1].split('_')[2]) * m + int(
                    eachline[curindex].split('|')[1].split('_')[3])
                if _output == '4':
                    flitpath = flitpath + _time + "_" + str(_router) + ".\n"
                    break
                else:
                    flitpath = flitpath + _time + "_" + str(_router) + "_" + _link + "="
        pretreatment_flit_path.write(flitpath)
        # print(flitpath)
