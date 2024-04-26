from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel


class SimpleTopo(Topo):
    """
    A class that defines a simple network topology for use with Mininet.

    The topology consists of two hosts (h1 and h2) connected to a single switch (s1).
    This setup can be used to simulate a network with two computers connected via a local
    network switch, which is often the most basic form of networking setup in real life.
    """

    def build(self):
        """
        Build the network topology by adding hosts and a switch and connecting them.

        This function overrides the 'build' method of the Topo class and is called
        when the Mininet instance is started. Hosts and the switch are added here,
        and links are created to form the network structure.
        """
        # Add two hosts with default configurations
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # Add a switch with default configurations
        s1 = self.addSwitch('s1')

        # Add bidirectional links with default settings
        self.addLink(h1, s1)
        self.addLink(h2, s1)


if __name__ == '__main__':
    # Set the verbosity level of log messages
    setLogLevel('info')  # 'info' level includes things like host creation, start, and stop.

    # Instantiate the topology we've defined above
    topo = SimpleTopo()

    # Create a Mininet environment with this topology
    net = Mininet(topo=topo)

    # Activate the Mininet environment, setting up all the defined hosts and switches
    net.start()

    # Provide a command-line interface to interact with the Mininet environment
    # Users can issue commands like 'ping' or 'iperf' to test connectivity
    CLI(net)

    # Clean up and stop the network simulation when the CLI session is ended by the user
    net.stop()
