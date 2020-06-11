import os

tr_dir = "results/tr/"
tcl_file = "network.tcl"
types = ["Newreno", "Tahoe", "Vegas"]
n_run = 10

received = []
dropped = []
enqueued = []
dequeued = []
cwnd = []
rtt = []


def execAllRuns():
    for each in types:
        for i in range (1, n_run + 1):
            command = "ns " + tcl_file + " " + each + " " + str(i) + " false"
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
                    splt.append(i)
                    cwnd.append(splt)
                elif "rtt_" in line:
                    splt = line.split()
                    splt.append(i)
                    rtt.append(splt)
                elif line[0] == '+':
                    splt = line.split()
                    splt.append(i)
                    enqueued.append(splt)
                elif line[0] == '-':
                    splt = line.split()
                    splt.append(i)
                    dequeued.append(splt)
                elif line[0] == 'r':
                    splt = line.split()
                    splt.append(i)
                    received.append(splt)
                elif line[0] == 'd':
                    splt = line.split()
                    splt.append(i)
                    dropped.append(splt)
                

def calculateAvgRtt():
    global rtt
    flow1_result = []
    flow2_result = []
    curr_vals = [0] * n_run
    rtt = sorted(rtt) # sort by time
    # for each in rtt:
    #     print(each)
    #     print("\n")
    for each in rtt:
        time_ = float(each[0])
        rtt_ = float(each[6])
        src = int(each[1])
        run_id = int(each[len(each) - 1])
        curr_vals[run_id - 1] = rtt_
        avg = sum(curr_vals) / len(curr_vals)
        flow1_result.append([time_, avg]) if (src == 0) else flow2_result.append([time_, avg])
    return flow1_result, flow2_result


def calculateAvgCwnd():
    global cwnd
    flow1_result = []
    flow2_result = []
    curr_vals = [0] * n_run
    cwnd = sorted(cwnd) # sort by time
    # for each in cwnd:
    #     print(each)
    #     print("\n")
    for each in cwnd:
        time_ = float(each[0])
        cwnd_ = float(each[6])
        src = int(each[1])
        run_id = int(each[len(each) - 1])
        curr_vals[run_id - 1] = cwnd_
        avg = sum(curr_vals) / len(curr_vals)
        flow1_result.append([time_, avg]) if (src == 0) else flow2_result.append([time_, avg])
    return flow1_result, flow2_result


execAllRuns()
readAndParseAllData()
f1_rtt, f2_rtt = calculateAvgRtt()
f1_cwnd, f2_cwnd = calculateAvgCwnd()
