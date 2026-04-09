from mininet.topo import Topo

# Custom Mininet topology for Network Utilization Monitor
class MonitorTopo(Topo):

    def build(self):
        # Add two hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # Add two OpenFlow switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Create links between hosts and switches
        self.addLink(h1, s1)
        self.addLink(s1, s2)
        self.addLink(s2, h2)

# Register topology so Mininet can detect it
topos = {'monitor': MonitorTopo}