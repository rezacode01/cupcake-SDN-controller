from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
 
def topology():
        net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
 
        # Add hosts and switches
        h1 = net.addHost( 'h1', ip="10.0.1.10/24", mac="00:00:00:00:00:01" )
        h2 = net.addHost( 'h2', ip="10.0.2.10/24", mac="00:00:00:00:00:02" )
        h3 = net.addHost( 'h3', ip="10.0.3.10/24", mac="00:00:00:00:00:03" )
        # Red switch
        r1 = net.addSwitch( 'r1')
        # black switch
        b1 = net.addSwitch( 'b1')
        c0 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )
 
        net.addLink( h1, r1 , delay="100ms", bw=1) # port one of r1 assigned to  h1
        net.addLink( b1, r1 , delay="10ms", bw=1) # port two of r1 assigned to  b1 port one
        net.addLink( b1, h2 , delay="10ms", bw=2)
        net.addLink( h3, r1 , delay="100ms", bw=2)
        net.build()
        c0.start()
        r1.start( [c0] )
        b1.start( [c0] )

        h1.cmd("ip route add default dev h1-eth0")
        h2.cmd("ip route add default dev h2-eth0")
        h3.cmd("ip route add default dev h3-eth0")

        r1.cmd("ovs-ofctl add-flow r1 priority=1,arp,actions=flood")
        r1.cmd("ovs-ofctl add-flow r1 priority=10,ip,nw_dst=10.0.1.0/24,actions=output:1")
        r1.cmd("ovs-ofctl add-flow r1 priority=10,ip,nw_dst=10.0.2.0/24,actions=output:2")
        r1.cmd("ovs-ofctl add-flow r1 priority=10,ip,nw_dst=10.0.3.0/24,actions=output:3")

        b1.cmd("ovs-ofctl add-flow b1 priority=1,arp,actions=flood")
        b1.cmd("ovs-ofctl add-flow b1 priority=10,ip,nw_dst=10.0.1.0/24,actions=output:1")
        b1.cmd("ovs-ofctl add-flow b1 priority=10,ip,nw_dst=10.0.2.10,actions=output:2")
        b1.cmd("ovs-ofctl add-flow b1 priority=10,ip,nw_dst=10.0.3.0/24,actions=output:1")
 
        print "*** Running CLI"
        CLI( net )
 
        print "*** Stopping network"
        net.stop()
      
if __name__ == '__main__':
    setLogLevel( 'info' )
    topology() 
