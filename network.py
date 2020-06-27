import os
import matplotlib.pyplot as plt
import pandas as pd

tr_dir = "results/tr/"
tcl_file = "network.tcl"
types = ["Newreno", "Tahoe", "Vegas"]
fig_size = (10, 10)
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
                    pass
                elif line[0] == '-':
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


def calculateAvgRtt():
    global rtt
    results   = [ [ [ [i, None] for i in range(exec_time + 1)] for i in range(2) ] for i in range(len(types)) ]
    curr_vals = [ [ [0]*n_run for i in range(2) ] for i in range(len(types)) ]

    for each in rtt:
        each[0] = float(each[0])
    rtt.sort()

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
        results[types.index(type_)][flow_id][int(time_)][1] = avg

    for i in range (len(types)):
        for j in range(2):
            for k in range(exec_time + 1):
                if i == 0:
                    prev = results[i][j][k][1]
                    continue
                if results[i][j][k][1] == None:
                    results[i][j][k][1] = prev
                prev = results[i][j][k][1]

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


def calculateAvgCwnd():
    global cwnd
    results   = [ [ [ [i, None] for i in range(exec_time + 1)] for i in range(2) ] for i in range(len(types)) ]
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
        results[types.index(type_)][flow_id][int(time_)][1] = avg

    for i in range (len(types)):
        for j in range(2):
            for k in range(exec_time + 1):
                if i == 0:
                    prev = results[i][j][k][1]
                    continue
                if results[i][j][k][1] == None:
                    results[i][j][k][1] = prev
                prev = results[i][j][k][1]

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


def calculateAvgDropped():
    global dropped
    results   = [ [ [ [i, 0] for i in range(exec_time + 1)] for i in range(2) ] for i in range(len(types)) ]

    for each in dropped:
        each[1] = float(each[1])
    dropped.sort() # sort by time
    for each in dropped:
        time_ = float(each[1])
        flow_id = int(each[7]) - 1
        type_ = each[len(each) - 2]
        results[types.index(type_)][flow_id][int(time_)][1] += 1

    for i in range(len(types)):
        for j in range(2):
            for k in range(exec_time + 1):
                results[i][j][k][1] /= n_run

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


def calculateAvgGoodput():
    global received
    # [type][flow][data]
    results   = [ [ [0]*exec_time for i in range(2) ] for i in range(len(types)) ]
    separated = [ [ [] for i in range(2) ] for i in range(len(types)) ]
    curr_vals = [ [ [0]*n_run for i in range(2) ] for i in range(len(types)) ]    

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
                msg_type = each[4]
                run_id = int(each[len(each) - 1]) - 1
                if msg_type != "ack":
                    continue
                if dst_node != 0 and dst_node != 1:
                    continue
                acked = int(each[10])
                curr_vals[i][j][run_id] = acked
                avg = sum(curr_vals[i][j]) / n_run
                avg *= (8*1000/(1000000)) # Mb
                if int(time_) != exec_time:
                    results[i][j][int(time_)] = [time_, avg]

    for i in range(len(types)):
        for j in range(2):
            for k in range(exec_time):
                if k == exec_time - 1:
                    break
                results[i][j][exec_time - 1 - k][1] -= results[i][j][exec_time - 1 - k - 1][1]
    
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

def plotByCalc(_func, _title, _mode):
    mapper = {0 : 'NewReno', 1 : 'Tahoe', 2 : 'Vegas'}
    data = [[] for i in range(3)]
    data[0], data[1], data[2] = _func()
    xy_data = [ [{'x' : [], 'y' : []} for _ in range(2)]  for _ in range(3)]
    
    for j, dt in enumerate(data):
        for flow_num in range(2):
            for i in range(len(dt[flow_num])):
                xy_data[j][flow_num]['x'].append(dt[flow_num][i][0])
                xy_data[j][flow_num]['y'].append(dt[flow_num][i][1])
    
    if _mode == 'single':
        fig = plt.figure(figsize=fig_size)
        ax = fig.add_subplot(111)
        ax.set_xlabel("Time")
        ax.set_ylabel("y")
        ax.set_title(_title)
        for _type, dt1 in enumerate(xy_data):
            for _flow, dt2 in enumerate(dt1):
                pd.DataFrame({'time': dt2['x'], 'y': dt2['y']}).to_csv(
                    f"results_data/{_title}_{mapper[_type]}_flow_{_flow}.csv", index=False)
                ax.plot(dt2['x'], dt2['y'], alpha=0.55, label=f"{mapper[_type]} flow {_flow}")
        ax.legend()
        fig.savefig(f"Figs/{_title}")
        plt.show()
    
    elif _mode == 'double':
        for _type, dt1 in enumerate(xy_data):
            fig = plt.figure(figsize=fig_size)
            ax = fig.add_subplot(111)
            ax.set_xlabel("Time")
            ax.set_ylabel("y")
            ax.set_title(f"{_title}_{mapper[_type]}")
            for _flow, dt2 in enumerate(dt1):
                pd.DataFrame({'time': dt2['x'], 'y': dt2['y']}).to_csv(
                    f"results_data/{_title}_{mapper[_type]}_flow_{_flow}.csv", index=False)
                ax.plot(dt2['x'], dt2['y'], alpha=0.55, label=f"{mapper[_type]} flow {_flow}")
            ax.legend()
            fig.savefig(f"Figs/{_title}_{mapper[_type]}")
            plt.show()

if __name__ == '__main__':
    n_run = 10
    exec_time = 1000
    fig_size = (10, 10)

    execAllRuns()
    readAndParseAllData()

    plotByCalc(calculateAvgCwnd,    f"CWND Average({n_run} Runs, {exec_time} Time)",    "single")
    plotByCalc(calculateAvgRtt,     f"RTT Average({n_run} Runs, {exec_time} Time)",     "single")
    plotByCalc(calculateAvgDropped, f"Dropped Average({n_run} Runs, {exec_time} Time)", "single")
    plotByCalc(calculateAvgGoodput, f"Goodput Average({n_run} Runs, {exec_time} Time)", "single")

    # plotByCalc(calculateAvgCwnd,    f"CWND Average({n_run} Runs, {exec_time} Time)",    "double")
    # plotByCalc(calculateAvgRtt,     f"RTT Average({n_run} Runs, {exec_time} Time)",     "double")
    # plotByCalc(calculateAvgDropped, f"Dropped Average({n_run} Runs, {exec_time} Time)", "double")
    # plotByCalc(calculateAvgGoodput, f"Goodput Average({n_run} Runs, {exec_time} Time)", "double")