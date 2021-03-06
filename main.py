"""Main module of kytos/pathfinder Kytos Network Application."""

from kytos.core import KytosNApp, log, rest
from kytos.core.helpers import listen_to
from flask import jsonify

# pylint: disable=import-error
from napps.kytos.pathfinder.graph import KytosGraph

# pylint: enable=import-error


class Main(KytosNApp):
    """Main class of kytos/pathfinder NApp.

    This class is the entry point for this napp.
    """

    def setup(self):
        """Create a graph to handle the nodes and edges."""
        self.graph = KytosGraph()

    def execute(self):
        """Do nothing."""
        pass

    def shutdown(self):
        """Shutdown the napp."""
        pass

    @rest('v1/<source>/<destination>')
    @rest('v1/<source>/<destination>/<parameter>')
    def shortest_path(self, source, destination, parameter=None):
        """Calculate the best path between the source and destination."""
        paths = []
        for path in self.graph.shortest_paths(source, destination, parameter):
            paths.append({'hops': path})
        return jsonify({'paths': paths})

    @listen_to('kytos.topology.updated')
    def update_topology(self, event):
        """Update the graph when the network topology was updated.

        Clear the current graph and create a new with the most topoly updated.
        """
        if 'topology' not in event.content:
            return
        topology = event.content['topology']
        self.graph.update_topology(topology)
        log.debug('Topology graph updated.')
