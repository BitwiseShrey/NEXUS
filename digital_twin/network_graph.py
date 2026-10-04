"""
NEXUS Supply Chain Network Graph
NetworkX Directed Graph representation of facilities, multi-echelon flows, and transit routes.
"""

from typing import Dict, List, Set, Tuple, Optional
import networkx as nx
from backend.app.utils.logger import logger


class SupplyChainGraph:
    """
    Graph representation and topology engine for NEXUS supply chain.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def build_from_entities(
        self,
        suppliers: List[Dict],
        production_units: List[Dict],
        warehouses: List[Dict],
        hubs: List[Dict],
        demand_zones: List[Dict],
        routes: List[Dict]
    ):
        """Construct the NetworkX DiGraph from digital twin entities."""
        self.graph.clear()

        # Add Supplier Nodes
        for s in suppliers:
            self.graph.add_node(
                s["supplier_id"],
                type="SUPPLIER",
                name=s["supplier_name"],
                lat=s["latitude"],
                lon=s["longitude"],
                capacity=s["capacity"],
                status=s.get("status", "ACTIVE"),
                risk_score=s.get("risk_score", 0.1)
            )

        # Add Production Unit Nodes
        for p in production_units:
            self.graph.add_node(
                p["production_id"],
                type="PRODUCTION",
                name=p["name"],
                lat=p["latitude"],
                lon=p["longitude"],
                capacity=p["capacity"],
                status=p.get("operational_status", "OPERATIONAL")
            )

        # Add Warehouse Nodes
        for w in warehouses:
            self.graph.add_node(
                w["warehouse_id"],
                type="WAREHOUSE",
                name=w["name"],
                lat=w["latitude"],
                lon=w["longitude"],
                capacity=w["capacity"],
                status=w.get("status", "ACTIVE")
            )

        # Add Hub Nodes
        for h in hubs:
            self.graph.add_node(
                h["hub_id"],
                type="HUB",
                name=h["name"],
                lat=h["latitude"],
                lon=h["longitude"],
                capacity=h["capacity"],
                status=h.get("status", "ACTIVE")
            )

        # Add Demand Zone Nodes
        for d in demand_zones:
            self.graph.add_node(
                d["zone_id"],
                type="DEMAND_ZONE",
                name=d["name"],
                region=d["region"],
                lat=d["latitude"],
                lon=d["longitude"],
                status="ACTIVE"
            )

        # Add Edges (Routes)
        for r in routes:
            self.graph.add_edge(
                r["origin"],
                r["destination"],
                route_id=r["route_id"],
                distance=r["distance"],
                transit_time=r["transit_time"],
                cost=r["transportation_cost"],
                mode=r["transport_mode"],
                capacity=r["capacity"],
                risk_level=r.get("risk_level", 0.05),
                status=r.get("status", "OPEN")
            )

        logger.info(
            f"Supply chain graph initialized: {self.graph.number_of_nodes()} nodes, "
            f"{self.graph.number_of_edges()} edges"
        )

    def get_downstream_dependents(self, node_id: str) -> List[str]:
        """
        Traverse the graph downstream using BFS/DFS to identify all facilities,
        hubs, and demand zones directly or transitively dependent on this node.
        """
        if node_id not in self.graph:
            return []
        descendants = nx.descendants(self.graph, node_id)
        return list(descendants)

    def get_upstream_dependencies(self, node_id: str) -> List[str]:
        """
        Traverse the graph upstream to find all suppliers, plants, or warehouses feeding into this node.
        """
        if node_id not in self.graph:
            return []
        ancestors = nx.ancestors(self.graph, node_id)
        return list(ancestors)

    def find_alternative_paths(
        self,
        origin: str,
        destination: str,
        blocked_nodes: Optional[Set[str]] = None,
        blocked_edges: Optional[Set[Tuple[str, str]]] = None,
        max_paths: int = 3
    ) -> List[Dict]:
        """
        Find shortest alternative feasible paths in the graph, avoiding specified blocked nodes or edges.
        """
        sub_graph = self.graph.copy()
        if blocked_nodes:
            for b in blocked_nodes:
                if sub_graph.has_node(b):
                    sub_graph.remove_node(b)
        if blocked_edges:
            for u, v in blocked_edges:
                if sub_graph.has_edge(u, v):
                    sub_graph.remove_edge(u, v)

        if not sub_graph.has_node(origin) or not sub_graph.has_node(destination):
            return []

        try:
            paths = list(nx.shortest_simple_paths(sub_graph, origin, destination, weight="transit_time"))[:max_paths]
            result = []
            for path in paths:
                total_transit = 0.0
                total_dist = 0.0
                total_cost = 0.0
                for u, v in zip(path[:-1], path[1:]):
                    edge_data = sub_graph[u][v]
                    total_transit += edge_data.get("transit_time", 1.0)
                    total_dist += edge_data.get("distance", 100.0)
                    total_cost += edge_data.get("cost", 50.0)
                result.append({
                    "path": path,
                    "hops": len(path) - 1,
                    "total_distance_km": round(total_dist, 2),
                    "total_transit_days": round(total_transit, 2),
                    "total_cost": round(total_cost, 2)
                })
            return result
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    def compute_network_criticality(self) -> Dict[str, float]:
        """
        Compute betweenness centrality of all network nodes to identify supply chain single points of failure.
        """
        if self.graph.number_of_nodes() == 0:
            return {}
        centrality = nx.betweenness_centrality(self.graph, weight="transit_time")
        return {k: round(v, 4) for k, v in centrality.items()}

    def to_dict(self) -> Dict:
        """Serialize graph summary for API responses."""
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "nodes_by_type": {
                node_type: len([n for n, d in self.graph.nodes(data=True) if d.get("type") == node_type])
                for node_type in ["SUPPLIER", "PRODUCTION", "WAREHOUSE", "HUB", "DEMAND_ZONE"]
            }
        }
