"""
NEXUS Geospatial Engine
Handles spatial coordinates, distance matrices, nearest-facility lookups, and geographic risk exposure.
Uses realistic Indian logistics hubs and geodesic calculations.
"""

import math
from typing import Dict, List, Tuple, Optional
from shapely.geometry import Point, Polygon
import geopandas as gpd
import pandas as pd


# Canonical Indian Logistics & Industrial Hubs
INDIAN_HUBS = {
    # Northern Region
    "DELHI_NCR": {"city": "Delhi NCR", "state": "Delhi", "region": "North", "lat": 28.6139, "lon": 77.2090},
    "GURGAON": {"city": "Gurgaon", "state": "Haryana", "region": "North", "lat": 28.4595, "lon": 77.0266},
    "JAIPUR": {"city": "Jaipur", "state": "Rajasthan", "region": "North", "lat": 26.9124, "lon": 75.7873},
    "LUCKNOW": {"city": "Lucknow", "state": "Uttar Pradesh", "region": "North", "lat": 26.8467, "lon": 80.9462},
    "CHANDIGARH": {"city": "Chandigarh", "state": "Punjab", "region": "North", "lat": 30.7333, "lon": 76.7794},
    "LUDHIANA": {"city": "Ludhiana", "state": "Punjab", "region": "North", "lat": 30.9010, "lon": 75.8573},
    "KANPUR": {"city": "Kanpur", "state": "Uttar Pradesh", "region": "North", "lat": 26.4499, "lon": 80.3319},
    "VARANASI": {"city": "Varanasi", "state": "Uttar Pradesh", "region": "North", "lat": 25.3176, "lon": 82.9739},

    # Western Region
    "MUMBAI_BHIWANDI": {"city": "Mumbai (Bhiwandi)", "state": "Maharashtra", "region": "West", "lat": 19.2967, "lon": 73.0628},
    "PUNE_CHAKAN": {"city": "Pune (Chakan)", "state": "Maharashtra", "region": "West", "lat": 18.7606, "lon": 73.8617},
    "AHMEDABAD_ASLALI": {"city": "Ahmedabad (Aslali)", "state": "Gujarat", "region": "West", "lat": 22.9228, "lon": 72.5855},
    "SURAT": {"city": "Surat", "state": "Gujarat", "region": "West", "lat": 21.1702, "lon": 72.8311},
    "VADODARA": {"city": "Vadodara", "state": "Gujarat", "region": "West", "lat": 22.3072, "lon": 73.1812},
    "NAGPUR": {"city": "Nagpur (MIHAN)", "state": "Maharashtra", "region": "Central", "lat": 21.1458, "lon": 79.0882},

    # Southern Region
    "BENGALURU_HOSKOTE": {"city": "Bengaluru (Hoskote)", "state": "Karnataka", "region": "South", "lat": 13.0712, "lon": 77.7981},
    "CHENNAI_SRICITY": {"city": "Chennai (Sri City)", "state": "Tamil Nadu", "region": "South", "lat": 13.5284, "lon": 80.0270},
    "HYDERABAD_MEDCHAL": {"city": "Hyderabad (Medchal)", "state": "Telangana", "region": "South", "lat": 17.6297, "lon": 78.4814},
    "KOCHI": {"city": "Kochi", "state": "Kerala", "region": "South", "lat": 9.9312, "lon": 76.2673},
    "COIMBATORE": {"city": "Coimbatore", "state": "Tamil Nadu", "region": "South", "lat": 11.0168, "lon": 76.9558},
    "VISAKHAPATNAM": {"city": "Visakhapatnam", "state": "Andhra Pradesh", "region": "South", "lat": 17.6868, "lon": 83.2185},

    # Eastern & Central Region
    "KOLKATA_DANKUNI": {"city": "Kolkata (Dankuni)", "state": "West Bengal", "region": "East", "lat": 22.6841, "lon": 88.2917},
    "BHOPAL": {"city": "Bhopal", "state": "Madhya Pradesh", "region": "Central", "lat": 23.2599, "lon": 77.4126},
    "INDORE": {"city": "Indore (Pithampur)", "state": "Madhya Pradesh", "region": "Central", "lat": 22.6145, "lon": 75.6917},
    "PATNA": {"city": "Patna", "state": "Bihar", "region": "East", "lat": 25.5941, "lon": 85.1376},
    "BHUBANESWAR": {"city": "Bhubaneswar", "state": "Odisha", "region": "East", "lat": 20.2961, "lon": 85.8245},
    "GUWAHATI": {"city": "Guwahati", "state": "Assam", "region": "East", "lat": 26.1445, "lon": 91.7362},
    "RAIPUR": {"city": "Raipur", "state": "Chhattisgarh", "region": "Central", "lat": 21.2514, "lon": 81.6296},
    "JAMSHEDPUR": {"city": "Jamshedpur", "state": "Jharkhand", "region": "East", "lat": 22.8046, "lon": 86.2029},
    "SANAND": {"city": "Sanand", "state": "Gujarat", "region": "West", "lat": 22.9859, "lon": 72.3789},
    "PANTNAGAR": {"city": "Pantnagar", "state": "Uttarakhand", "region": "North", "lat": 29.0222, "lon": 79.4897},
}


class GeoEngine:
    """
    Geospatial calculations and spatial analysis for the supply chain network.
    """

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great-circle distance between two points on the Earth (in km).
        """
        R = 6371.0  # Earth radius in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 2)

    @classmethod
    def highway_distance(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Estimate practical Indian highway road distance (incorporates 1.22x road winding tortuosity factor).
        """
        haversine = cls.haversine_distance(lat1, lon1, lat2, lon2)
        # Tortuosity factor for Indian national highways
        return round(max(haversine * 1.22, 15.0), 2)

    @classmethod
    def transit_time_days(cls, distance_km: float, mode: str = "ROAD") -> float:
        """
        Estimate transit duration in days based on commercial Indian freight speeds.
        ROAD: avg 40 km/h with 10 hr/day driving window = 400 km/day.
        RAIL: avg 550 km/day including marshalling.
        AIR: 1 day within domestic network.
        """
        if mode == "AIR":
            return 1.0
        elif mode == "RAIL":
            return round(max(distance_km / 550.0, 1.0), 2)
        else:  # ROAD
            return round(max(distance_km / 400.0, 0.5), 2)

    @classmethod
    def find_nearest_facilities(
        cls,
        target_lat: float,
        target_lon: float,
        facilities: List[Dict],
        top_k: int = 3
    ) -> List[Dict]:
        """
        Find top K nearest facilities by highway distance.
        facilities list of dicts with 'id', 'lat', 'lon', etc.
        """
        ranked = []
        for fac in facilities:
            dist = cls.highway_distance(target_lat, target_lon, fac["latitude"], fac["longitude"])
            ranked.append({**fac, "distance_km": dist})
        ranked.sort(key=lambda x: x["distance_km"])
        return ranked[:top_k]

    @classmethod
    def check_geographic_risk_exposure(
        cls,
        center_lat: float,
        center_lon: float,
        radius_km: float,
        network_entities: List[Dict]
    ) -> List[Dict]:
        """
        Identify entities residing within a geographic disruption radius (e.g., cyclone, regional flood, strike).
        """
        exposed = []
        for entity in network_entities:
            dist = cls.haversine_distance(center_lat, center_lon, entity["latitude"], entity["longitude"])
            if dist <= radius_km:
                exposed.append({
                    "entity_id": entity.get("id") or entity.get("supplier_id") or entity.get("warehouse_id"),
                    "name": entity.get("name") or entity.get("supplier_name"),
                    "distance_from_epicenter_km": dist,
                    "exposure_level": round(1.0 - (dist / radius_km), 2)  # Closer = higher exposure
                })
        exposed.sort(key=lambda x: x["distance_from_epicenter_km"])
        return exposed

    @classmethod
    def build_geodataframe(cls, entities: List[Dict]) -> gpd.GeoDataFrame:
        """
        Convert list of entities into GeoPandas GeoDataFrame with Point geometries.
        """
        geometry = [Point(e["longitude"], e["latitude"]) for e in entities]
        gdf = gpd.GeoDataFrame(entities, geometry=geometry, crs="EPSG:4326")
        return gdf
