proc randGen {min max} { 
    return [expr int(rand()*($max - $min + 1)) + $min] 
}


Class TraceApp -superclass Application     

TraceApp instproc init {args} {
    $self set bytes_ 0
    eval $self next $args
}

TraceApp instproc recv {byte} {
    $self instvar bytes_
    set bytes_ [expr $bytes_ + $byte]
    return $bytes_
}

proc doSimulation {type number verbose max_time} {

    global ns trace_file nam_file

    set ns [new Simulator]

    set trace_dir "results/tr/$type$number.tr"
    set nam_dir "results/nam/$type$number.nam"

    set trace_file [open $trace_dir w]
    $ns trace-all $trace_file

    set nam_file [open $nam_dir w]
    $ns namtrace-all $nam_file


    set n1 [$ns node]
    set n2 [$ns node]
    set n3 [$ns node]
    set n4 [$ns node]
    set n5 [$ns node]
    set n6 [$ns node]

    $ns color 1 Red
    $ns color 2 Blue

    $ns duplex-link $n1 $n3 100Mb 5ms DropTail
    $ns duplex-link $n4 $n5 100Mb 5ms DropTail
    $ns duplex-link $n3 $n4 100Kb 1ms DropTail
    $ns duplex-link $n2 $n3 100Mb [randGen 5 25]ms DropTail
    $ns duplex-link $n4 $n6 100Mb [randGen 5 25]ms DropTail



    $ns duplex-link-op $n1 $n3 orient right-down
    $ns duplex-link-op $n2 $n3 orient right-up
    $ns duplex-link-op $n3 $n4 orient right
    $ns duplex-link-op $n4 $n5 orient right-up
    $ns duplex-link-op $n4 $n6 orient right-down


    $ns queue-limit $n3 $n1 10
    $ns queue-limit $n3 $n2 10
    $ns queue-limit $n3 $n4 10
    $ns queue-limit $n4 $n3 10
    $ns queue-limit $n4 $n5 10
    $ns queue-limit $n4 $n6 10

    if {$type == "Tahoe"} {
        set tcp1 [new Agent/TCP]
        set tcp2 [new Agent/TCP]
    } else {
        set tcp1 [new Agent/TCP/$type]
        set tcp2 [new Agent/TCP/$type]
    }

    set tcp5 [new Agent/TCPSink]
    set tcp6 [new Agent/TCPSink]

    set traceapp5 [new TraceApp]
    $traceapp5 attach-agent $tcp5
    set traceapp6 [new TraceApp]
    $traceapp6 attach-agent $tcp6

    $tcp1 set class_ 1
    $tcp1 set fid_ 1
    # $tcp1 set packtsize_ 960
    $tcp1 set ttl_ 64

    $tcp5 set class_ 1

    $tcp2 set class_ 2
    $tcp2 set fid_ 2
    # $tcp2 set packtsize_ 960
    $tcp2 set ttl_ 64

    $tcp6 set class_ 2


    $ns attach-agent $n1 $tcp1
    $ns attach-agent $n5 $tcp5
    $ns attach-agent $n2 $tcp2
    $ns attach-agent $n6 $tcp6


    $ns connect $tcp1  $tcp5
    $ns connect $tcp2  $tcp6


    set ftp1 [new Application/FTP]
    set ftp2 [new Application/FTP]

    $ftp1 attach-agent $tcp1
    $ftp2 attach-agent $tcp2

    $tcp1 attach $trace_file
    $tcp1 tracevar cwnd_
    $tcp1 tracevar rtt_

    $tcp2 attach $trace_file
    $tcp2 tracevar cwnd_
    $tcp2 tracevar rtt_

    proc finish { nam_dir show } {
        global ns trace_file nam_file
        $ns flush-trace
        close $trace_file
        close $nam_file
        if {$show == true} {
            exec nam  $nam_dir &
            exit
        } else {
            exit 0   
        }
    }

    proc addGoodPutToTrace {tcpSink outfile id} {
        global ns
        set now [$ns now];
        set nbytes [$tcpSink set bytes_];
        $tcpSink set bytes_ 0;
        set time_incr 1.0
        set throughput [expr ($nbytes * 8.0 / 1000000) / $time_incr]
        puts  $outfile  "#### $now $throughput $id"
        $ns at [expr $now+$time_incr] "addGoodPutToTrace $tcpSink  $outfile $id"
    }

    $ns at 0.0 "$ftp1 start"
    $ns at 0.0 "$ftp2 start"
    $ns at 0.0 "$traceapp5 start"
    $ns at 0.0 "$traceapp6 start"
    $ns at 0.0 "addGoodPutToTrace $traceapp5 $trace_file 5"
    $ns at 0.0 "addGoodPutToTrace $traceapp6 $trace_file 6"
    $ns at $max_time "$ftp1 stop"
    $ns at $max_time "$ftp2 stop"
    $ns at [expr $max_time + 0.1] "finish $nam_dir $verbose"

    $ns run
}

# set types [list "Newreno" "Tahoe" "Vegas"]
# doSimulation [lindex $types 1] 2 0
set type [lindex $argv 0]
set num [lindex $argv 1]
set verbose [lindex $argv 2]
set max_time [lindex $argv 3]
doSimulation $type $num $verbose $max_time