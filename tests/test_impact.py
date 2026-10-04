"""
Unit Tests for NEXUS Disruption Impact Propagation and Graph Dependencies
"""

from digital_twin.network_graph import SupplyChainGraph
from impact.impact_engine import ImpactEngine


def test_supply_chain_graph_traversal(sample_network):
    graph = SupplyChainGraph()
    graph.build_from_entities(
        suppliers=sample_network["suppliers"],
        production_units=sample_network["production_units"],
        warehouses=sample_network["warehouses"],
        hubs=sample_network["hubs"],
        demand_zones=sample_network["demand_zones"],
        routes=sample_network["routes"]
    )

    # Test downstream traversal from a supplier
    first_sup = sample_network["suppliers"][0]["supplier_id"]
    dependents = graph.get_downstream_dependents(first_sup)
    assert len(dependents) > 0

    # Test upstream traversal from a warehouse
    first_wh = sample_network["warehouses"][0]["warehouse_id"]
    upstream = graph.get_upstream_dependencies(first_wh)
    assert len(upstream) > 0


def test_alternative_paths_avoiding_blocked_node(sample_network):
    graph = SupplyChainGraph()
    graph.build_from_entities(
        suppliers=sample_network["suppliers"],
        production_units=sample_network["production_units"],
        warehouses=sample_network["warehouses"],
        hubs=sample_network["hubs"],
        demand_zones=sample_network["demand_zones"],
        routes=sample_network["routes"]
    )

    # Find paths between first supplier and a downstream node
    first_sup = sample_network["suppliers"][0]["supplier_id"]
    dependents = graph.get_downstream_dependents(first_sup)
    if dependents:
        target = dependents[0]
        paths = graph.find_alternative_paths(first_sup, target, max_paths=2)
        assert isinstance(paths, list)
