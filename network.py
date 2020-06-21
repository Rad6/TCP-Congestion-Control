import os
import matplotlib.pyplot as plt

tr_dir = "results/tr/"
tcl_file = "network.tcl"
types = ["Newreno", "Tahoe", "Vegas"]
n_run = 1
exec_time = 10
received = []
dropped = []
enqueued = []
dequeued = []
cwnd = []
rtt = []


def execAllRuns():
    for each in types:
        for i in range (1, n_run + 1):
            command = "ns " + tcl_file + " " + each + " " + str(i) + " false"+ f" {exec_time}"
            print(command)
            os.system(command)


def readAndParseAllData():
    for type_ in types:
        for i in range(1, n_run + 1):
            file = open(tr_dir + type_ + str(i) + ".tr", 'r')
            lines = file.readlines()

            for line in lines:
                if "cwnd_" in line:
                    splt = line.split()
                    splt.append(type_)
                    splt.append(i)
                    cwnd.append(splt)
                elif "rtt_" in line:
                    splt = line.split()
                    splt.append(type_)
                    splt.append(i)
                    rtt.append(splt)
                elif line[0] == '+':
                    # splt = line.split()
                    # splt.append(type_)
                    # splt.append(i)
                    # enqueued.append(splt)
                    pass
                elif line[0] == '-':
                    # splt = line.split()
                    # splt.append(type_)
                    # splt.append(i)
                    # dequeued.append(splt)
                    pass
                elif line[0] == 'r':
                    splt = line.split()
                    splt.append(type_)
                    splt.append(i)
                    received.append(splt)
                elif line[0] == 'd':
                    splt = line.split()
                    splt.append(type_)
                    splt.append(i)
                    dropped.append(splt)


def append_to_list(lst, time, value):
    if len(lst) == 0:
        lst.append([time, value])
        return
    if lst[-1][0] == time and lst[-1][1] == value:
        return
    if lst[-1][0] == time:
        lst[-1][1] = (value + lst[-1][1])/2
        return
    lst.append([time, value])


def calculateAvgRtt():
    global rtt
    newreno_f1 = []
    newreno_f2 = []
    tahoe_f1 = []
    tahoe_f2 = []
    vegas_f1 = []
    vegas_f2 = []

    # data structure for saving current values
    # shape: [agent type][flow id][run number]
    curr_vals = [ [ [0]*n_run for i in range(2) ] for i in range(len(types)) ]
    for each in rtt:
        each[0] = float(each[0])
    rtt.sort() # sort by time
    for each in rtt:
        time_ = float(each[0])
        rtt_ = float(each[6])
        src = int(each[1])
        flow_id = 0
        if (src == 1):
            flow_id = 1
        type_ = each[7]
        run_id = int(each[len(each) - 1]) - 1
        curr_vals[types.index(type_)][flow_id][run_id] = rtt_
        avg = sum(curr_vals[types.index(type_)][flow_id]) / len(curr_vals[types.index(type_)][flow_id])
        if type_ == "Newreno":
            append_to_list(newreno_f1, time_, avg) if (src == 0) else append_to_list(newreno_f2, time_, avg)
        elif type_ == "Tahoe":
            append_to_list(tahoe_f1, time_, avg) if (src == 0) else append_to_list(tahoe_f2, time_, avg)
        else:
            append_to_list(vegas_f1, time_, avg) if (src == 0) else append_to_list(vegas_f2, time_, avg)
    
    newreno_result = []
    newreno_result.append(newreno_f1)
    newreno_result.append(newreno_f2)
    tahoe_result = []
    tahoe_result.append(tahoe_f1)
    tahoe_result.append(tahoe_f2)
    vegas_result = []
    vegas_result.append(vegas_f1)
    vegas_result.append(vegas_f2)

    return newreno_result, tahoe_result, vegas_result


def calculateAvgCwnd():
    global cwnd
    newreno_f1 = []
    newreno_f2 = []
    tahoe_f1 = []
    tahoe_f2 = []
    vegas_f1 = []
    vegas_f2 = []

    # data structure for saving current values
    # shape: [agent type][flow id][run number]
    curr_vals = [ [ [0]*n_run for i in range(2) ] for i in range(len(types)) ]
    for each in cwnd:
        each[0] = float(each[0])
    cwnd.sort()
    for each in cwnd:
        time_ = float(each[0])
        cwnd_ = float(each[6])
        src = int(each[1])
        flow_id = 0
        if (src == 1):
            flow_id = 1
        type_ = each[7]
        run_id = int(each[len(each) - 1]) - 1
        curr_vals[types.index(type_)][flow_id][run_id] = cwnd_
        avg = sum(curr_vals[types.index(type_)][flow_id]) / len(curr_vals[types.index(type_)][flow_id])
        if type_ == "Newreno":
            append_to_list(newreno_f1, time_, avg) if (src == 0) else append_to_list(newreno_f2, time_, avg)
        elif type_ == "Tahoe":
            append_to_list(tahoe_f1, time_, avg) if (src == 0) else append_to_list(tahoe_f2, time_, avg)
        else:
            append_to_list(vegas_f1, time_, avg) if (src == 0) else append_to_list(vegas_f2, time_, avg)
    
    newreno_result = []
    newreno_result.append(newreno_f1)
    newreno_result.append(newreno_f2)
    tahoe_result = []
    tahoe_result.append(tahoe_f1)
    tahoe_result.append(tahoe_f2)
    vegas_result = []
    vegas_result.append(vegas_f1)
    vegas_result.append(vegas_f2)

    return newreno_result, tahoe_result, vegas_result


def calculateAvgDropped():
    global dropped
    newreno_f1 = []
    newreno_f2 = []
    tahoe_f1 = []
    tahoe_f2 = []
    vegas_f1 = []
    vegas_f2 = []

    # data structure for saving current values
    # shape: [agent type][flow id][run number]
    curr_vals = [ [ [0]*n_run for i in range(2) ] for i in range(len(types)) ]
    for each in dropped:
        each[1] = float(each[1])
    dropped.sort() # sort by time
    for each in dropped:
        time_ = float(each[1])
        flow_id = int(each[7]) - 1
        type_ = each[len(each) - 2]
        run_id = int(each[len(each) - 1]) - 1
        curr_vals[types.index(type_)][flow_id][run_id] += 1
        avg = sum(curr_vals[types.index(type_)][flow_id]) / len(curr_vals[types.index(type_)][flow_id])
        avg /= time_
        if type_ == "Newreno":
            append_to_list(newreno_f1, time_, avg) if (flow_id == 0) else append_to_list(newreno_f2, time_, avg)
        elif type_ == "Tahoe":
            append_to_list(tahoe_f1, time_, avg) if (flow_id == 0) else append_to_list(tahoe_f2, time_, avg)
        else:
            append_to_list(vegas_f1, time_, avg) if (flow_id == 0) else append_to_list(vegas_f2, time_, avg)
    
    newreno_result = []
    newreno_result.append(newreno_f1)
    newreno_result.append(newreno_f2)
    tahoe_result = []
    tahoe_result.append(tahoe_f1)
    tahoe_result.append(tahoe_f2)
    vegas_result = []
    vegas_result.append(vegas_f1)
    vegas_result.append(vegas_f2)

    return newreno_result, tahoe_result, vegas_result



def calculateAvgGoodput():
    # global received
    # newreno_f1 = []
    # newreno_f2 = []
    # tahoe_f1 = []
    # tahoe_f2 = []
    # vegas_f1 = []
    # vegas_f2 = []

    # # data structure for saving current values
    # # shape: [agent type][flow id][run number]
    # curr_vals = [ [ [0]*n_run for i in range(2) ] for i in range(len(types)) ]
    # curr_secs = [ [ [0]*n_run for i in range(2) ] for i in range(len(types)) ]
    # for each in received:
    #     each[1] = float(each[1])
    # received.sort() # sort by time
    # for each in received:
    #     time_ = float(each[1])
    #     dst_node = int(each[3])
    #     if dst_node != 4 and dst_node != 5:
    #         continue
    #     flow_id = int(each[7]) - 1
    #     type_ = each[len(each) - 2]
    #     run_id = int(each[len(each) - 1]) - 1
    #     if int(time_) == curr_secs[types.index(type_)][flow_id][run_id]:
    #         curr_vals[types.index(type_)][flow_id][run_id] += 1
    #         continue
    #     else:
    #         curr_secs[types.index(type_)][flow_id][run_id] += 1
    #     avg = sum(curr_vals[types.index(type_)][flow_id]) / len(curr_vals[types.index(type_)][flow_id])
    #     curr_vals[types.index(type_)][flow_id][run_id] = 1
    #     if type_ == "Newreno":
    #         append_to_list(newreno_f1, time_, avg) if (flow_id == 0) else append_to_list(newreno_f2, time_, avg)
    #     elif type_ == "Tahoe":
    #         append_to_list(tahoe_f1, time_, avg) if (flow_id == 0) else append_to_list(tahoe_f2, time_, avg)
    #     else:
    #         append_to_list(vegas_f1, time_, avg) if (flow_id == 0) else append_to_list(vegas_f2, time_, avg)
    
    # newreno_result = []
    # newreno_result.append(newreno_f1)
    # newreno_result.append(newreno_f2)
    # tahoe_result = []
    # tahoe_result.append(tahoe_f1)
    # tahoe_result.append(tahoe_f2)
    # vegas_result = []
    # vegas_result.append(vegas_f1)
    # vegas_result.append(vegas_f2)

    # return newreno_result, tahoe_result, vegas_result

    global received

    # [type][flow][data]
    results   = [ [ [] for i in range(2) ] for i in range(len(types)) ]
    separated = [ [ [] for i in range(2) ] for i in range(len(types)) ]
    # [type][flow]
    counters  = [ [0]*2 for i in range(len(types)) ]
    curr_secs = [ [0]*2 for i in range(len(types)) ]
    
    for each in received:
        each[1] = float(each[1])
    received.sort() # sort by time

    for each in received:
        _type = each[len(each) - 2]
        flow_id = int(each[7]) - 1
        separated[types.index(_type)][flow_id].append(each)


    for i in range (len(types)):
        for j in range(2): # 2 flows
            for each in separated[i][j]:
                time_ = each[1]
                dst_node = int(each[3])
                if dst_node != 4 and dst_node != 5:
                    continue
                if int(time_) == curr_secs[i][j]:
                    counters[i][j] += 1
                    continue
                point_time = curr_secs[i][j]
                point_avg = counters[i][j] / n_run
                results[i][j].append([point_time, point_avg])
                curr_secs[i][j] += 1
                counters[i][j] = 1
    
    newreno_result = []
    newreno_result.append(results[0][0])
    newreno_result.append(results[0][1])
    tahoe_result = []
    tahoe_result.append(results[1][0])
    tahoe_result.append(results[1][1])
    vegas_result = []
    vegas_result.append(results[2][0])
    vegas_result.append(results[2][1])

    return newreno_result, tahoe_result, vegas_result

def plotByCalc(_func, _title):
    mapper = {0 : 'NewReno', 1 : 'Tahoe', 2 : 'Vegas'}
    data = [[] for i in range(3)]
    data[0], data[1], data[2] = _func()
    xy_data = [ [{'x' : [], 'y' : []} for _ in range(2)]  for _ in range(3)]
    
    for j, dt in enumerate(data):
        for flow_num in range(2):
            for i in range(len(dt[flow_num])):
                xy_data[j][flow_num]['x'].append(dt[flow_num][i][0])
                xy_data[j][flow_num]['y'].append(dt[flow_num][i][1])
    
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111)
    ax.set_xlabel("Time")
    ax.set_ylabel("y")
    ax.set_title(_title)
    for _type, dt1 in enumerate(xy_data):
        for _flow, dt2 in enumerate(dt1):
            ax.scatter(dt2['x'], dt2['y'], alpha=0.55, label=f"{mapper[_type]} flow {_flow}")
    ax.legend()
    fig.savefig(f"Figs/{_title}")
    plt.show()

def plotByCalc2(_func, _title):
    mapper = {0 : 'NewReno', 1 : 'Tahoe', 2 : 'Vegas'}
    data = [[] for i in range(3)]
    data[0], data[1], data[2] = _func()
    xy_data = [ [{'x' : [], 'y' : []} for _ in range(2)]  for _ in range(3)]
    
    for j, dt in enumerate(data):
        for flow_num in range(2):
            for i in range(len(dt[flow_num])):
                xy_data[j][flow_num]['x'].append(dt[flow_num][i][0])
                xy_data[j][flow_num]['y'].append(dt[flow_num][i][1])
    
    for _type, dt1 in enumerate(xy_data):

        fig = plt.figure(figsize=(15,15))
        ax = fig.add_subplot(111)
        ax.set_xlabel("Time")
        ax.set_ylabel("y")
        ax.set_title(f"{_title}_{mapper[_type]}")
        for _flow, dt2 in enumerate(dt1):
            print(len(dt2['x']))
            ax.scatter(dt2['x'], dt2['y'], s=2, alpha=0.55, label=f"{mapper[_type]} flow {_flow}")
        ax.legend()
        fig.savefig(f"Figs/{_title}_{mapper[_type]}")
        plt.show()


if __name__ == '__main__':
    n_run = 10
    exec_time = 500

    execAllRuns()
    readAndParseAllData()

    plotByCalc2(calculateAvgCwnd,    f"CWND Average({n_run} Runs, {exec_time} Time)")
    plotByCalc2(calculateAvgRtt,     f"RTT Average({n_run} Runs, {exec_time} Time)")
    plotByCalc2(calculateAvgDropped, f"Dropped Average({n_run} Runs, {exec_time} Time)")
    plotByCalc2(calculateAvgGoodput, f"Goodput Average({n_run} Runs, {exec_time} Time)")

    # each list below is 3d : [flows][records][fields]
    # rtt_newreno_result, rtt_tahoe_result, rtt_vegas_result = calculateAvgRtt()
    # cwnd_newreno_result, cwnd_tahoe_result, cwnd_vegas_result = calculateAvgCwnd()
    # # drp_newreno_result, drp_tahoe_result, drp_vegas_result = calculateAvgDropped()

    # x_nr = []
    # y_nr = []
    
    # x_ta = []
    # y_ta = []
    
    # x_ve = []
    # y_ve = []

    # for i in range(len(cwnd_newreno_result[1])):
    #     x_nr.append(cwnd_newreno_result[1][i][0])
    #     y_nr.append(cwnd_newreno_result[1][i][1])

    # for i in range(len(cwnd_tahoe_result[1])):
    #     x_ta.append(cwnd_tahoe_result[1][i][0])
    #     y_ta.append(cwnd_tahoe_result[1][i][1])
    
    # for i in range(len(cwnd_vegas_result[1])):
    #     x_ve.append(cwnd_vegas_result[1][i][0])
    #     y_ve.append(cwnd_vegas_result[1][i][1])

    # fig = plt.figure(figsize=(20,20))
    # ax = fig.add_subplot(111)
    # ax.scatter(x_nr, y_nr, s=1.1, c='r', alpha='0.8')
    # ax.scatter(x_ta, y_ta, s=1.1, c='g', alpha='0.8')
    # ax.scatter(x_ve, y_ve, s=1.1, c='b', alpha='0.8')
    # plt.show()


    # ax.plot(x_nr, y_nr, s=1.1, c='r', alpha='0.8')
    # ax.plot(x_ta, y_ta, s=1.1, c='g', alpha='0.8')
    # ax.plot(x_ve, y_ve, s=1.1, c='b', alpha='0.8')