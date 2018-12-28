#!/usr/bin/python


'''
    HTTP test to show BBR performances on path loss.
    Results saved to http_tests folder
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
import time
# It would be nice if we didn't have to do this:
# pylint: disable=arguments-differ

# Protocols to run tests for
protocols = ['reno', 'cubic', 'bbr']


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
    res= client.cmd("bash client.sh " + server.IP())
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
    h2 = net.getNodeByName('h2')

    pid = server.cmd("./server.sh")
    time.sleep(1)

    with open("http.dat", "a+") as f:
        for protocol in protocols:
            # Set the congestion protocol
            os.system("echo '"+protocol +
                  "'| sudo tee /proc/sys/net/ipv4/tcp_congestion_control")

            info("Running test for "+protocol+" congestion protocol\n")
            # info("timeout "+str(time)+" wget -r " + server.IP()+":8000")
            # Run the test
            results=test(net,server, h2)

            # File output
            if results:
                f.write( ("%i\t%s\t%s\n"
                       % (loss,protocol,results)))
        f.close()

    server.cmd("kill -9 "+pid)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    # Prevent test_simpleperf from failing due to packet loss
#perfTest( lossy=( 'testmode' not in argv ) )

for loss in [0,1,2,3,5,7,10]:
    info('-------------------------------------\n')
    info('-------------- '+dt.datetime.now().strftime('%X')+' -------------\n')
    info('   '+str(loss)+'% loss on server\'s link\n')
    info('-------------------------------------\n')
    perfTest(loss)

