proc randGen {min max} { 
    return [expr int(rand()*($max - $min + 1)) + $min] 
}

set ns [new Simulator]

set trace_file [open "out.tr" w]
$ns trace-all $trace_file

set nam_file [open "out.nam" w]
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


$ns queue-limit $n1 $n3 10
$ns queue-limit $n2 $n3 10
$ns queue-limit $n3 $n4 10
$ns queue-limit $n4 $n5 10
$ns queue-limit $n4 $n6 10


set tcp1 [new Agent/TCP]
$tcp1 set class_ 1

set tcp5 [new Agent/TCPSink]
$tcp5 set class_ 1

set tcp2 [new Agent/TCP]
$tcp2 set class_ 2

set tcp6 [new Agent/TCPSink]
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


proc finish {} {
    global ns trace_file nam_file
    $ns flush-trace
    close $trace_file
    close $nam_file
    exec nam out.nam &
    exit
}


$ns at 0.0 "$ftp1 start"
$ns at 0.0 "$ftp2 start"
$ns at 2.0 "$ftp1 stop"
$ns at 2.0 "$ftp2 stop"
$ns at 2.1 "finish"

$ns run