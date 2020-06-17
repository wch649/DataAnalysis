if __name__ == "__main__":
    # m*n 2D mesh topology
    n = 8
    m = 8
    vc_num = 4
    vc_size = 8

    filename = "..\Data\data20200611_uniform_vc_4_size_8\\vc_buffer_occupancy.txt"
    flitpath = open(filename, "r")
    filename = "..\Data\data20200611_uniform_vc_4_size_8\\occupancy_set.txt"
    occupancyfile = open(filename, "w")

    _time = 0
    curTimeData = "current time:"

    # initial leastdata and leastdataset
    leastdata = ""
    emptydata = "[ 0 0 0 0  ][ 0 0 0 0  ][ 0 0 0 0  ][ 0 0 0 0  ]"
    for routi in range(m * n):
        leastdata = leastdata + str(routi) + " " + emptydata + "-"
    leastdata = leastdata.split("-")

    for eachline in flitpath:
        leastdataset = []
        templine = eachline.split()
        if _time == 0:
            _time = templine[0]
        # caculate the router number: from "network_0/router_1_2" ==> 1 2 ==> router: 10
        router = int(templine[2].split('_')[2]) * n + int(templine[2].split('_')[3])
        usedata = str(router) + ' ' + str(eachline.split("==")[1][8:56])

        if _time == templine[0]:
            curTimeData = curTimeData + '-' + usedata
        else:
            # complete the least vc_buffer data
            each_router_data = curTimeData.split("-")
            curTimeData = "current time:"
            for routi in range(m * n):
                for each_index in each_router_data:
                    temp_each_index = each_index.split()
                    if temp_each_index[0] == str(routi):
                        leastdata[routi] = each_index
            leastdataset.append(_time + ":" + leastdata + ".\n")
            occupancyfile.write(leastdataset)
        # update the times
        _time = templine[0]
    flitpath.close()
    occupancyfile.close()
