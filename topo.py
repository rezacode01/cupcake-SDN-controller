from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
import cupcake
 
def topology():
        net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )


        cupcake.addNodes("./topo.json",net=net)

        c0 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )

        cupcake.addLinkes(net=net)
 
        net.build()
        c0.start()
        r1.start( [c0] )
        b1.start( [c0] )

        cupcake.configHostsRoute(net=net)

        cupcake.configSwitches(net=net)

        print "*** Running CLI"
        CLI( net )
 
        print "*** Stopping network"
        net.stop()
      
if __name__ == '__main__':
    setLogLevel( 'info' )
    topology() 
