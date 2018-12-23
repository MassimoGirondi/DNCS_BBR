#!/usr/bin/python


'''
    Simple test to show BBR performances on path loss.
    Run iperf from client to server with different congestion control.
    Then add 1% path loss and repeat.
    Results saved to iperf_tests folder
'''
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from sys import argv
import os
import datetime as dt
# It would be nice if we didn't have to do this:
# pylint: disable=arguments-differ

# Protocols to run tests for
protocols = ['reno', 'cubic', 'bbr']

# Test lenght (seconds)
time = 20

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."

    def build(self, n=2, _loss=0):
        switch = self.addSwitch('s1')
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost('h%s' % (h + 1),
                                cpu=.5 / n)
            # 1Gbps link, no loss, 5 ms delay

            self.addLink(host, switch,
                         bw=1000, delay='5ms', loss=_loss, use_htb=True)


def test(net,server, client):
    #return net.iperf((client, server), l4Type='TCP', seconds=20)
    res= client.cmd("timeout "+str(time*1.2)+"s iperf -f k -c " + server.IP()+" -t "+str(time))
    res=res.split('\n')[-2].split(' ')[-2]
    try:
        float(res)
    except ValueError:
        res=0
    return res

def perfTest(loss=0):
    "Create network and run performance tests, one for each protocol"
    topo = SingleSwitchTopo(n=4, _loss=loss)
    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink,
                  autoStaticArp=True)
    net.start()
    info("Dumping host connections\n")
    dumpNodeConnections(net.hosts)
    
    # Assume h1 as server, h2 as the client
    

    server = net.getNodeByName('h1')
    server.cmd("iperf -s &")
    h2 = net.getNodeByName('h2')


    with open("iperf.dat", "a+") as f:
        for protocol in protocols:
            # Set the congestion protocol
            os.system("echo '"+protocol +
                  "'| sudo tee /proc/sys/net/ipv4/tcp_congestion_control")

            info("Running test for "+protocol+" congestion protocol\n")
            
            # Run the test
            results=test(net,server, h2)

            # File output
            if results:
                f.write( ("%i\t%s\t%s\n"
                       % (loss,protocol,results)))
        f.close()
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    # Prevent test_simpleperf from failing due to packet loss
#perfTest( lossy=( 'testmode' not in argv ) )

for loss in [0,1,2,5,10,15,20,30,50]:
    info('-------------------------------------\n')
    info('-------------- '+dt.datetime.now().strftime('%X')+' -------------\n')
    info('   '+str(loss)+'% loss on server\'s link\n')
    info('-------------------------------------\n')
    perfTest(loss)

