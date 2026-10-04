import React, { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import {
  GitFork,
  AlertTriangle,
  Boxes,
  Warehouse as WarehouseIcon,
  Store,
  TrendingDown,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
} from 'lucide-react';
import { analyzeImpact, getSuppliers, getWarehouses, getRoutes } from '../api';
import { ImpactAnalyzeRequest, ImpactAnalyzeResponse } from '../types';
import { KpiCard } from '../components/common/KpiCard';
import { RiskBadge } from '../components/common/RiskBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import { LoadingSkeleton, ErrorState } from '../components/common/FeedbackStates';
import { formatNumber, formatPercent } from '../utils/formatters';

export const ImpactAnalysis: React.FC = () => {
  const [entityType, setEntityType] = useState<'SUPPLIER' | 'WAREHOUSE' | 'ROUTE'>('SUPPLIER');
  const [entityId, setEntityId] = useState<string>('SUP_001');
  const [capacityReduction, setCapacityReduction] = useState<number>(0.80);
  const [durationDays, setDurationDays] = useState<number>(10);

  // Entities for dropdown selection
  const { data: suppliers } = useQuery({
    queryKey: ['impact-suppliers'],
    queryFn: () => getSuppliers({ limit: 30 }),
  });

  const { data: warehouses } = useQuery({
    queryKey: ['impact-warehouses'],
    queryFn: () => getWarehouses(),
  });

  const { data: routes } = useQuery({
    queryKey: ['impact-routes'],
    queryFn: () => getRoutes({ limit: 50 }),
  });

  // Impact Mutation
  const impactMutation = useMutation<ImpactAnalyzeResponse, Error, ImpactAnalyzeRequest>({
    mutationFn: (req) => analyzeImpact(req),
  });

  // Run on initial load with defaults
  React.useEffect(() => {
    impactMutation.mutate({
      entity_type: entityType,
      entity_id: entityId,
      capacity_reduction: capacityReduction,
      duration_days: durationDays,
    });
  }, []);

  const handleRunAnalysis = (e: React.FormEvent) => {
    e.preventDefault();
    impactMutation.mutate({
      entity_type: entityType,
      entity_id: entityId,
      capacity_reduction: capacityReduction,
      duration_days: durationDays,
    });
  };

  const impact = impactMutation.data;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          Disruption Impact Propagation Engine
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Trace how single-point facility or corridor disruptions propagate downstream through the NetworkX graph.
        </p>
      </div>

      {/* Disruption Configuration Form */}
      <form
        onSubmit={handleRunAnalysis}
        className="p-5 rounded-xl bg-nexus-900 border border-nexus-700/60 shadow-xl space-y-4"
      >
        <div className="flex items-center gap-2 border-b border-nexus-800 pb-3">
          <GitFork className="w-4 h-4 text-blue-400" />
          <h3 className="text-sm font-semibold text-white">Disruption Shock Injector</h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          {/* Entity Type */}
          <div>
            <label className="block text-slate-400 font-medium mb-1.5">Disrupted Entity Type:</label>
            <select
              value={entityType}
              onChange={(e) => {
                const newType = e.target.value as any;
                setEntityType(newType);
                if (newType === 'SUPPLIER') setEntityId('SUP_001');
                if (newType === 'WAREHOUSE') setEntityId('WH_01');
                if (newType === 'ROUTE') setEntityId('RT_0001');
              }}
              className="w-full p-2 rounded-lg bg-nexus-850 border border-nexus-700 text-white focus:outline-none focus:border-blue-500"
            >
              <option value="SUPPLIER">Tier-1 / Tier-2 Supplier</option>
              <option value="WAREHOUSE">Regional Warehouse Depot</option>
              <option value="ROUTE">Logistics Transit Corridor</option>
            </select>
          </div>

          {/* Specific Entity ID */}
          <div>
            <label className="block text-slate-400 font-medium mb-1.5">Target Facility / Corridor:</label>
            <select
              value={entityId}
              onChange={(e) => setEntityId(e.target.value)}
              className="w-full p-2 rounded-lg bg-nexus-850 border border-nexus-700 text-white focus:outline-none focus:border-blue-500 font-mono"
            >
              {entityType === 'SUPPLIER' &&
                suppliers?.map((s) => (
                  <option key={s.supplier_id} value={s.supplier_id}>
                    {s.supplier_id} - {s.supplier_name}
                  </option>
                ))}
              {entityType === 'WAREHOUSE' &&
                warehouses?.map((w) => (
                  <option key={w.warehouse_id} value={w.warehouse_id}>
                    {w.warehouse_id} - {w.name}
                  </option>
                ))}
              {entityType === 'ROUTE' &&
                routes?.map((r) => (
                  <option key={r.route_id} value={r.route_id}>
                    {r.route_id} ({r.origin} &rarr; {r.destination})
                  </option>
                ))}
            </select>
          </div>

          {/* Capacity Reduction */}
          <div>
            <div className="flex justify-between text-slate-400 font-medium mb-1.5">
              <span>Capacity Cut:</span>
              <span className="font-mono text-white">{(capacityReduction * 100).toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="0.20"
              max="1.0"
              step="0.05"
              value={capacityReduction}
              onChange={(e) => setCapacityReduction(parseFloat(e.target.value))}
              className="w-full accent-blue-500 bg-nexus-800"
            />
          </div>

          {/* Duration */}
          <div>
            <div className="flex justify-between text-slate-400 font-medium mb-1.5">
              <span>Duration:</span>
              <span className="font-mono text-white">{durationDays} Days</span>
            </div>
            <input
              type="range"
              min="3"
              max="30"
              step="1"
              value={durationDays}
              onChange={(e) => setDurationDays(parseInt(e.target.value))}
              className="w-full accent-blue-500 bg-nexus-800"
            />
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={impactMutation.isPending}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-bold text-white shadow-lg shadow-blue-500/20 transition-all disabled:opacity-50"
          >
            <GitFork className="w-3.5 h-3.5" />
            <span>{impactMutation.isPending ? 'Simulating Propagation...' : 'Propagate Disruption Impact'}</span>
          </button>
        </div>
      </form>

      {/* Propagation Stepper Diagram */}
      <div className="p-4 rounded-xl bg-nexus-900 border border-nexus-700/60 shadow-lg">
        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 block mb-3">
          Propagation Cascade Pipeline
        </span>
        <div className="grid grid-cols-2 md:grid-cols-6 gap-2 text-center text-xs">
          <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30">
            <span className="text-[10px] text-slate-400 font-medium uppercase">1. Disrupted Node</span>
            <div className="font-bold text-rose-400 mt-1 truncate">{entityId}</div>
            <div className="text-[10px] text-slate-400">-{(capacityReduction * 100).toFixed(0)}% Capacity</div>
          </div>

          <div className="p-3 rounded-lg bg-nexus-850 border border-nexus-800">
            <span className="text-[10px] text-slate-400 font-medium uppercase">2. Exposed SKUs</span>
            <div className="font-bold text-white mt-1">{impact?.dependent_products_count ?? 0} Products</div>
            <div className="text-[10px] text-slate-500">Tier-1 Direct</div>
          </div>

          <div className="p-3 rounded-lg bg-nexus-850 border border-nexus-800">
            <span className="text-[10px] text-slate-400 font-medium uppercase">3. Warehouses</span>
            <div className="font-bold text-white mt-1">{impact?.affected_warehouses_count ?? 0} Hubs</div>
            <div className="text-[10px] text-slate-500">Stock runway breach</div>
          </div>

          <div className="p-3 rounded-lg bg-nexus-850 border border-nexus-800">
            <span className="text-[10px] text-slate-400 font-medium uppercase">4. Demand Zones</span>
            <div className="font-bold text-white mt-1">{impact?.affected_demand_zones?.length ?? 0} Regions</div>
            <div className="text-[10px] text-slate-500">End consumer delivery</div>
          </div>

          <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/30">
            <span className="text-[10px] text-slate-400 font-medium uppercase">5. Potential Shortage</span>
            <div className="font-bold text-amber-400 mt-1">
              {formatNumber(impact?.estimated_shortage_units)} units
            </div>
            <div className="text-[10px] text-slate-400">Over {durationDays}d shock</div>
          </div>

          <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30">
            <span className="text-[10px] text-slate-400 font-medium uppercase">6. Service-Level</span>
            <div className="font-bold text-rose-400 mt-1">
              {formatPercent(impact?.projected_service_level)}
            </div>
            <div className="text-[10px] text-slate-400">
              -{(impact?.service_level_deficit ? impact.service_level_deficit * 100 : 0).toFixed(1)}% drop
            </div>
          </div>
        </div>
      </div>

      {/* Downstream Warehouse Runway Analysis & Alternative Suppliers */}
      {impact && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Warehouse Runway Depletion Analysis */}
          <div className="p-5 rounded-xl bg-nexus-900 border border-nexus-700/60 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-nexus-800 pb-3">
              <div className="flex items-center gap-2">
                <WarehouseIcon className="w-4 h-4 text-blue-400" />
                <h3 className="text-sm font-semibold text-white">Downstream Warehouse Stock Runways</h3>
              </div>
              <span className="text-xs text-slate-400">Shock Horizon: {durationDays} days</span>
            </div>

            <div className="space-y-2">
              {impact.warehouse_runway_analysis?.map((item, idx) => (
                <div key={idx} className="p-3 rounded-lg bg-nexus-850 border border-nexus-800 flex items-center justify-between text-xs">
                  <div>
                    <span className="font-mono font-bold text-white">{item.warehouse_id}</span>
                    <span className="text-slate-400 ml-2">SKU: {item.product_id}</span>
                    <div className="text-[10px] text-slate-500 mt-0.5">
                      Daily demand: {item.daily_demand} units/day &bull; Current stock: {formatNumber(item.current_stock)}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-white font-mono">{item.stock_runway_days} Days Runway</div>
                    <span
                      className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                        item.stockout_expected
                          ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                          : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      }`}
                    >
                      {item.stockout_expected ? 'Stockout Imminent' : 'Buffer Safe'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Alternative Supplier Recovery Options */}
          <div className="p-5 rounded-xl bg-nexus-900 border border-nexus-700/60 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-nexus-800 pb-3">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-semibold text-white">Discovered Alternative Suppliers</h3>
              </div>
              <span className="text-xs text-emerald-400 font-semibold">Available for Reallocation</span>
            </div>

            <div className="space-y-3">
              {impact.alternative_suppliers?.map((alt) => (
                <div key={alt.supplier_id} className="p-3 rounded-lg bg-nexus-850 border border-nexus-800 text-xs space-y-2">
                  <div className="flex justify-between items-center">
                    <div>
                      <span className="font-bold text-white">{alt.name}</span>
                      <span className="text-slate-500 font-mono ml-2">({alt.supplier_id})</span>
                    </div>
                    <RiskBadge scoreOrTier={alt.risk_score} />
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-[11px] text-slate-400 pt-1 border-t border-nexus-800">
                    <div>Capacity: <span className="font-mono text-white">{formatNumber(alt.available_capacity)}</span></div>
                    <div>Unit Cost: <span className="font-mono text-white">INR {alt.unit_cost}</span></div>
                    <div>On-Time: <span className="font-mono text-emerald-400">{formatPercent(alt.on_time_rate)}</span></div>
                  </div>
                </div>
              ))}
            </div>

            <div className="p-3 rounded-lg bg-blue-500/10 border border-blue-500/20 text-xs text-slate-300">
              <span className="font-semibold text-blue-400">Next Step:</span> To calculate optimal quantity allocations across these alternative suppliers, proceed to the <strong>Optimization Engine</strong>.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
