import osmnx as ox
import networkx as nx
from geopy.distance import geodesic


class MapService:
    """
    Real-world routing using OpenStreetMap
    """

    def get_route_distance_km(self, origin, destination):
        """
        origin & destination: (lat, lon)
        """

        # Load road network between points
        G = ox.graph_from_point(
            origin,
            dist=600000,  # 600 km radius (Chennai–Mumbai)
            network_type="drive"
        )

        orig_node = ox.nearest_nodes(G, origin[1], origin[0])
        dest_node = ox.nearest_nodes(G, destination[1], destination[0])

        shortest_path = nx.shortest_path(
            G,
            orig_node,
            dest_node,
            weight="length"
        )

        distance_m = nx.path_weight(G, shortest_path, weight="length")
        return round(distance_m / 1000, 2)
