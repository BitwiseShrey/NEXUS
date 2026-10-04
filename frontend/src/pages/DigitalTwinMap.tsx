import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import {
  MapPin,
  Filter,
  Layers,
  Info,
  Truck,
  Building2,
  Factory,
  Package,
  Store,
} from 'lucide-react';
import { getGisFacilities, getRoutes } from '../api';
import { GeoFacilityFeature, RouteItem } from '../types';
import { RiskBadge } from '../components/common/RiskBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import { LoadingSkeleton, ErrorState } from '../components/common/FeedbackStates';
import { formatNumber } from '../utils/formatters';

// Custom marker styles by node type
const createCustomMarker = (type: string, riskScore: number = 0) => {
  let color = '#3B82F6'; // Default Blue
  if (type === 'SUPPLIER') color = riskScore > 0.3 ? '#EF4444' : '#3B82F6';
  if (type === 'PRODUCTION') color = '#8B5CF6'; // Purple
  if (type === 'WAREHOUSE') color = '#10B981'; // Emerald
  if (type === 'HUB') color = '#06B6D4'; // Cyan
  if (type === 'DEMAND_ZONE') color = '#F59E0B'; // Amber

  return L.divIcon({
    className: 'custom-leaflet-marker',
    html: `
      <div style="
        background-color: ${color};
        width: 14px;
        height: 14px;
        border-radius: 50%;
        border: 2px solid #FFFFFF;
        box-shadow: 0 0 10px ${color};
      "></div>
    `,
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  });
};

export const DigitalTwinMap: React.FC = () => {
  const [selectedType, setSelectedType] = useState<string>('ALL');
  const [selectedEntity, setSelectedEntity] = useState<GeoFacilityFeature['properties'] | null>(null);

  const { data: geoData, isLoading: loadingGis, error: errorGis } = useQuery({
    queryKey: ['gis-facilities'],
    queryFn: getGisFacilities,
  });

  const { data: routes, isLoading: loadingRoutes } = useQuery({
    queryKey: ['transit-routes'],
    queryFn: () => getRoutes({ limit: 120 }),
  });

  if (loadingGis || loadingRoutes) {
    return <LoadingSkeleton rows={8} height="h-24" />;
  }

  if (errorGis) {
    return <ErrorState message="Failed to load GIS spatial facilities from backend." />;
  }

  const facilities = geoData?.features || [];

  // Filter facilities
  const filteredFacilities =
    selectedType === 'ALL'
      ? facilities
      : facilities.filter((f) => f.properties.type === selectedType);

  // Map facilities coordinates for route line rendering
  const coordMap = new Map<string, [number, number]>();
  facilities.forEach((f) => {
    coordMap.set(f.properties.id, [f.geometry.coordinates[1], f.geometry.coordinates[0]]);
  });

  return (
    <div className="space-y-4">
      {/* Header and Filter Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            Digital Supply Chain Twin (Indian Network)
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Simulated digital twin topology calibrated with authentic geodesic coordinates across Indian industrial corridors.
          </p>
        </div>

        {/* Filter Badges */}
        <div className="flex flex-wrap items-center gap-1.5 p-1 rounded-xl bg-nexus-900 border border-nexus-700">
          {[
            { id: 'ALL', label: 'All Nodes' },
            { id: 'SUPPLIER', label: 'Suppliers (20)' },
            { id: 'PRODUCTION', label: 'Plants (8)' },
            { id: 'WAREHOUSE', label: 'Warehouses (10)' },
            { id: 'HUB', label: 'Hubs (15)' },
            { id: 'DEMAND_ZONE', label: 'Demand Zones (30)' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setSelectedType(tab.id)}
              className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                selectedType === tab.id
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Map + Detail Inspector Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 h-[650px]">
        {/* Leaflet GIS Map Canvas */}
        <div className="lg:col-span-3 rounded-xl border border-nexus-700/60 overflow-hidden relative shadow-2xl bg-nexus-950">
          <MapContainer
            center={[22.5, 78.9]} // Centered on India
            zoom={5}
            minZoom={4}
            maxZoom={12}
            scrollWheelZoom={true}
            className="w-full h-full"
          >
            {/* Dark Basemap CartoDB */}
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>'
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            />

            {/* Multimodal Route Corridors */}
            {routes?.map((route) => {
              const start = coordMap.get(route.origin);
              const end = coordMap.get(route.destination);
              if (!start || !end) return null;

              const isBlocked = route.status === 'BLOCKED';
              const lineColor = isBlocked
                ? '#EF4444' // Red if blocked
                : route.transport_mode === 'RAIL'
                ? '#8B5CF6' // Purple for Rail
                : '#3B82F6'; // Blue for Road

              return (
                <Polyline
                  key={route.route_id}
                  positions={[start, end]}
                  color={lineColor}
                  weight={isBlocked ? 2.5 : 1.2}
                  opacity={isBlocked ? 0.9 : 0.4}
                  dashArray={isBlocked ? '6, 6' : route.transport_mode === 'RAIL' ? '4, 4' : undefined}
                >
                  <Popup>
                    <div className="text-xs space-y-1">
                      <div className="font-semibold text-white">Route {route.route_id}</div>
                      <div>{route.origin} &rarr; {route.destination}</div>
                      <div>Mode: <span className="font-mono text-blue-400">{route.transport_mode}</span></div>
                      <div>Distance: {route.distance} km ({route.transit_time} days)</div>
                      <div>Status: <span className={isBlocked ? 'text-rose-400 font-bold' : 'text-emerald-400'}>{route.status}</span></div>
                    </div>
                  </Popup>
                </Polyline>
              );
            })}

            {/* Facility Markers */}
            {filteredFacilities.map((facility) => {
              const [lon, lat] = facility.geometry.coordinates;
              const prop = facility.properties;

              return (
                <Marker
                  key={prop.id}
                  position={[lat, lon]}
                  icon={createCustomMarker(prop.type, prop.risk_score || 0)}
                  eventHandlers={{
                    click: () => setSelectedEntity(prop),
                  }}
                >
                  <Popup>
                    <div className="text-xs space-y-1">
                      <div className="font-bold text-white">{prop.name}</div>
                      <div className="text-slate-400">{prop.location}</div>
                      <div className="text-slate-300">Type: <span className="font-mono text-blue-400">{prop.type}</span></div>
                      {prop.capacity && <div>Capacity: {formatNumber(prop.capacity)} units</div>}
                      {prop.risk_score !== undefined && (
                        <div>Risk: <RiskBadge scoreOrTier={prop.risk_score} /></div>
                      )}
                    </div>
                  </Popup>
                </Marker>
              );
            })}
          </MapContainer>

          {/* Map Overlay Legend */}
          <div className="absolute bottom-4 left-4 z-[1000] p-3 rounded-lg bg-nexus-900/90 backdrop-blur-md border border-nexus-700 text-[11px] space-y-1.5 shadow-xl pointer-events-auto">
            <div className="font-semibold text-white text-xs mb-1">Network Legend</div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block" />
              <span className="text-slate-300">Suppliers (20)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-purple-500 inline-block" />
              <span className="text-slate-300">Production Plants (8)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block" />
              <span className="text-slate-300">Warehouses (10)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 inline-block" />
              <span className="text-slate-300">Distribution Hubs (15)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-400 inline-block" />
              <span className="text-slate-300">Demand Zones (30)</span>
            </div>
            <div className="pt-1 border-t border-nexus-700/60 flex items-center gap-2">
              <span className="w-4 h-0.5 bg-rose-500 inline-block" />
              <span className="text-rose-400 font-semibold">Severed Route</span>
            </div>
          </div>
        </div>

        {/* Selected Entity Inspector Side Panel */}
        <div className="lg:col-span-1 p-5 rounded-xl bg-nexus-900 border border-nexus-700/60 flex flex-col justify-between overflow-y-auto">
          {selectedEntity ? (
            <div className="space-y-4">
              <div className="border-b border-nexus-800 pb-3">
                <span className="text-[10px] font-bold uppercase tracking-wider text-blue-400 font-mono">
                  {selectedEntity.type}
                </span>
                <h3 className="text-base font-bold text-white mt-1">{selectedEntity.name}</h3>
                <p className="text-xs text-slate-400 mt-0.5">{selectedEntity.location}</p>
              </div>

              <div className="space-y-2.5 text-xs">
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Node Identifier:</span>
                  <span className="font-mono text-white font-medium">{selectedEntity.id}</span>
                </div>

                {selectedEntity.capacity !== undefined && (
                  <div className="flex justify-between p-2 rounded bg-nexus-850">
                    <span className="text-slate-400">Throughput Capacity:</span>
                    <span className="font-mono text-white font-medium">
                      {formatNumber(selectedEntity.capacity)} units
                    </span>
                  </div>
                )}

                {selectedEntity.utilization !== undefined && (
                  <div className="flex justify-between p-2 rounded bg-nexus-850">
                    <span className="text-slate-400">Current Utilization:</span>
                    <span className="font-mono text-white font-medium">
                      {(selectedEntity.utilization * 100).toFixed(1)}%
                    </span>
                  </div>
                )}

                {selectedEntity.historical_demand !== undefined && (
                  <div className="flex justify-between p-2 rounded bg-nexus-850">
                    <span className="text-slate-400">Historical Demand:</span>
                    <span className="font-mono text-white font-medium">
                      {formatNumber(selectedEntity.historical_demand)} units
                    </span>
                  </div>
                )}

                {selectedEntity.risk_score !== undefined && (
                  <div className="flex justify-between p-2 rounded bg-nexus-850 items-center">
                    <span className="text-slate-400">Risk Assessment:</span>
                    <RiskBadge scoreOrTier={selectedEntity.risk_score} />
                  </div>
                )}

                <div className="flex justify-between p-2 rounded bg-nexus-850 items-center">
                  <span className="text-slate-400">Status:</span>
                  <StatusBadge status={selectedEntity.status || 'ACTIVE'} />
                </div>

                <div className="flex justify-between p-2 rounded bg-nexus-850 items-center">
                  <span className="text-slate-400">Node Provenance:</span>
                  <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/60 px-1.5 py-0.5 rounded border border-cyan-800">
                    SIMULATED TWIN NODE
                  </span>
                </div>
              </div>

              <div className="p-3 rounded-lg bg-blue-500/10 border border-blue-500/20 text-[11px] text-blue-300">
                <p className="font-semibold mb-1">Impact Analysis Tip:</p>
                To test failure propagation for this facility, navigate to the Impact Analysis module.
              </div>
            </div>
          ) : (
            <div className="text-center py-20 text-slate-500 space-y-2">
              <MapPin className="w-8 h-8 mx-auto text-slate-600 stroke-[1.5]" />
              <p className="text-xs">Click any facility node on the map to inspect its real-time telemetry.</p>
            </div>
          )}

          <div className="pt-4 border-t border-nexus-800 text-[10px] text-slate-500 space-y-1">
            <div className="font-semibold text-slate-400">Digital Twin Topology Disclaimer</div>
            <p>
              Facilities represent calibrated synthetic nodes positioned across authentic Indian logistics hubs.
              Telemetry is parameterized from empirical Walmart Sales and DataCo supply chain datasets.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
