from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel


class SimpleTopo(Topo):
    def build(self):
        # Add hosts and switch
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')

        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s1)


if __name__ == '__main__':
    setLogLevel('info')  # Set the log level

    # Instantiate the topology
    topo = SimpleTopo()

    # Create the network
    net = Mininet(topo=topo)

    # Start the network
    net.start()

    # Drop the user into a CLI, so they can run commands on hosts
    CLI(net)

    # After the user exits the CLI, stop the network
    net.stop()
