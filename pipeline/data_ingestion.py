"""
NEXUS Data Ingestion & Database Population Pipeline
Loads raw public datasets, generates calibrated digital twin network entities,
validates integrity, and populates the relational database.
"""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from typing import Dict, Any
import pandas as pd
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.database import SessionLocal, init_db
from backend.app.models import (
    Supplier, Product, ProductionUnit, Warehouse, DistributionHub,
    Inventory, DemandZone, Route, Order, Disruption
)
from backend.app.utils.logger import logger
from digital_twin.network_builder import NetworkBuilder
from pipeline.data_preprocessing import DataPreprocessor


class DataIngestionPipeline:
    """
    Orchestrates raw data ingestion, digital twin generation, validation, and database population.
    """

    def __init__(self, db_session: Session = None):
        self.db = db_session or SessionLocal()
        self.builder = NetworkBuilder(seed=settings.RANDOM_SEED)

    def run(self) -> Dict[str, Any]:
        """Execute the end-to-end ingestion and database seeding."""
        logger.info("==================================================")
        logger.info("Starting NEXUS Data Ingestion & Digital Twin Setup")
        logger.info("==================================================")

        # Ensure database tables exist
        init_db()

        # Step 1: Process empirical Walmart demand patterns
        walmart_path = Path(settings.DATA_RAW_DIR) / "train.csv"
        if walmart_path.exists():
            logger.info(f"Loading empirical Walmart sales dataset from {walmart_path}")
            df_walmart = pd.read_csv(walmart_path)
            df_walmart_clean = DataPreprocessor.clean_walmart_sales(df_walmart)
            processed_demand_path = Path(settings.DATA_PROCESSED_DIR) / "walmart_demand_cleaned.parquet"
            df_walmart_clean.to_parquet(processed_demand_path, index=False)
            logger.info(f"Saved processed demand series to {processed_demand_path}")
        else:
            logger.warning(f"Raw Walmart dataset not found at {walmart_path}")

        # Step 2: Process empirical DataCo logistics patterns
        dataco_path = Path(settings.DATA_RAW_DIR) / "dataco_supply_chain.csv"
        if dataco_path.exists():
            logger.info(f"Loading empirical DataCo supply chain dataset from {dataco_path}")
            df_dataco = pd.read_csv(dataco_path, encoding="latin1")
            df_dataco_clean = DataPreprocessor.clean_dataco_logistics(df_dataco)
            processed_dataco_path = Path(settings.DATA_PROCESSED_DIR) / "dataco_logistics_cleaned.parquet"
            df_dataco_clean.to_parquet(processed_dataco_path, index=False)
            logger.info(f"Saved processed logistics series to {processed_dataco_path}")
        else:
            logger.warning(f"Raw DataCo dataset not found at {dataco_path}")

        # Step 3: Generate Calibrated Digital Supply Chain Twin Network
        logger.info("Generating calibrated Digital Supply Chain Twin entities...")
        suppliers = self.builder.generate_suppliers()
        prod_units = self.builder.generate_production_units()
        products = self.builder.generate_products(suppliers)
        warehouses = self.builder.generate_warehouses()
        hubs = self.builder.generate_distribution_hubs()
        demand_zones = self.builder.generate_demand_zones(products)
        routes = self.builder.generate_routes(suppliers, prod_units, warehouses, hubs, demand_zones)
        inventories = self.builder.generate_inventory(warehouses, products)
        orders = self.builder.generate_orders(products, routes, num_orders=50000)
        disruptions = self.builder.generate_disruptions(suppliers, warehouses, routes, count=500)

        # Validate entity counts
        entities_dict = {
            "suppliers": suppliers,
            "production_units": prod_units,
            "products": products,
            "warehouses": warehouses,
            "distribution_hubs": hubs,
            "demand_zones": demand_zones,
            "routes": routes,
            "orders": orders,
            "disruptions": disruptions,
        }
        DataPreprocessor.validate_entity_counts(entities_dict)

        # Step 4: Populate Relational Database
        logger.info("Populating relational database tables...")

        # Clear existing digital twin tables to maintain clean idempotency
        for model in [Disruption, Order, Inventory, Route, DemandZone, DistributionHub, Warehouse, ProductionUnit, Product, Supplier]:
            self.db.query(model).delete()
        self.db.commit()

        # Insert Suppliers
        self.db.bulk_insert_mappings(Supplier, suppliers)
        self.db.commit()
        logger.info(f"Inserted {len(suppliers)} suppliers")

        # Insert Production Units
        self.db.bulk_insert_mappings(ProductionUnit, prod_units)
        self.db.commit()
        logger.info(f"Inserted {len(prod_units)} production units")

        # Insert Products
        self.db.bulk_insert_mappings(Product, products)
        self.db.commit()
        logger.info(f"Inserted {len(products)} products")

        # Insert Warehouses
        self.db.bulk_insert_mappings(Warehouse, warehouses)
        self.db.commit()
        logger.info(f"Inserted {len(warehouses)} warehouses")

        # Insert Distribution Hubs
        self.db.bulk_insert_mappings(DistributionHub, hubs)
        self.db.commit()
        logger.info(f"Inserted {len(hubs)} distribution hubs")

        # Insert Demand Zones
        self.db.bulk_insert_mappings(DemandZone, demand_zones)
        self.db.commit()
        logger.info(f"Inserted {len(demand_zones)} demand zones")

        # Insert Routes
        self.db.bulk_insert_mappings(Route, routes)
        self.db.commit()
        logger.info(f"Inserted {len(routes)} routes")

        # Insert Inventory
        self.db.bulk_insert_mappings(Inventory, inventories)
        self.db.commit()
        logger.info(f"Inserted {len(inventories)} inventory rows")

        # Insert Orders in chunks of 5000 for database efficiency
        chunk_size = 5000
        for i in range(0, len(orders), chunk_size):
            chunk = orders[i:i + chunk_size]
            self.db.bulk_insert_mappings(Order, chunk)
            self.db.commit()
        logger.info(f"Inserted {len(orders)} historical orders")

        # Insert Disruptions
        self.db.bulk_insert_mappings(Disruption, disruptions)
        self.db.commit()
        logger.info(f"Inserted {len(disruptions)} historical disruptions")

        # Step 5: Save processed entities to disk for fast offline ML access
        pd.DataFrame(suppliers).to_csv(Path(settings.DATA_PROCESSED_DIR) / "suppliers.csv", index=False)
        pd.DataFrame(products).to_csv(Path(settings.DATA_PROCESSED_DIR) / "products.csv", index=False)
        pd.DataFrame(warehouses).to_csv(Path(settings.DATA_PROCESSED_DIR) / "warehouses.csv", index=False)
        pd.DataFrame(routes).to_csv(Path(settings.DATA_PROCESSED_DIR) / "routes.csv", index=False)
        pd.DataFrame(demand_zones).to_csv(Path(settings.DATA_PROCESSED_DIR) / "demand_zones.csv", index=False)

        summary = {
            "status": "SUCCESS",
            "suppliers_count": len(suppliers),
            "production_units_count": len(prod_units),
            "products_count": len(products),
            "warehouses_count": len(warehouses),
            "hubs_count": len(hubs),
            "demand_zones_count": len(demand_zones),
            "routes_count": len(routes),
            "inventory_records": len(inventories),
            "orders_count": len(orders),
            "disruptions_count": len(disruptions)
        }
        logger.info("Data Ingestion Pipeline completed successfully.")
        return summary


def run_ingestion():
    db = SessionLocal()
    try:
        pipeline = DataIngestionPipeline(db)
        return pipeline.run()
    finally:
        db.close()


if __name__ == "__main__":
    run_ingestion()
