import React, { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import {
  Sliders,
  Play,
  Layers,
  ArrowRight,
  TrendingDown,
  AlertTriangle,
  RotateCcw,
  CheckCircle2,
  Cpu,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { simulateScenario, getSuppliers, getWarehouses, getRoutes } from '../api';
import { ScenarioSimulateRequest, ScenarioSimulateResponse } from '../types';
import { KpiCard } from '../components/common/KpiCard';
import { StatusBadge } from '../components/common/StatusBadge';
import { LoadingSkeleton, ErrorState } from '../components/common/FeedbackStates';
import { formatNumber } from '../utils/formatters';

export const ScenarioSimulation: React.FC = () => {
  const [scenarioType, setScenarioType] = useState<ScenarioSimulateRequest['scenario_type']>('SUPPLIER_FAILURE');
  const [selectedSupplier, setSelectedSupplier] = useState<string>('SUP_001');
  const [selectedWarehouse, setSelectedWarehouse] = useState<string>('WH_01');
  const [selectedRoute, setSelectedRoute] = useState<string>('RT_0001');
  const [capacityReduction, setCapacityReduction] = useState<number>(0.80);
  const [demandSpikePercent, setDemandSpikePercent] = useState<number>(0.50);
  const [durationDays, setDurationDays] = useState<number>(10);

  const { data: suppliers } = useQuery({ queryKey: ['sim-suppliers'], queryFn: () => getSuppliers({ limit: 20 }) });
  const { data: warehouses } = useQuery({ queryKey: ['sim-warehouses'], queryFn: () => getWarehouses() });
  const { data: routes } = useQuery({ queryKey: ['sim-routes'], queryFn: () => getRoutes({ limit: 40 }) });

  const simMutation = useMutation<ScenarioSimulateResponse, Error, ScenarioSimulateRequest>({
    mutationFn: (req) => simulateScenario(req),
  });

  // Run initial default simulation
  React.useEffect(() => {
    handleRunSimulation();
  }, []);

  const handleRunSimulation = (e?: React.FormEvent) => {
    if (e) e.preventDefault();

    const params: Record<string, any> = { duration_days: durationDays };
    if (scenarioType === 'SUPPLIER_FAILURE') {
      params.supplier_id = selectedSupplier;
      params.capacity_reduction = capacityReduction;
    } else if (scenarioType === 'ROUTE_DISRUPTION') {
      params.route_id = selectedRoute;
    } else if (scenarioType === 'DEMAND_SPIKE') {
      params.demand_spike_percent = demandSpikePercent;
    } else if (scenarioType === 'WAREHOUSE_SHUTDOWN') {
      params.warehouse_id = selectedWarehouse;
    } else if (scenarioType === 'COMBINED_DISRUPTION') {
      params.supplier_id = selectedSupplier;
      params.capacity_reduction = capacityReduction;
      params.route_id = selectedRoute;
      params.demand_spike_percent = demandSpikePercent;
    }

    simMutation.mutate({
      scenario_type: scenarioType,
      parameters: params,
    });
  };

  const sim = simMutation.data;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            What-If Scenario Simulation Builder
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Simulate operational shocks on an in-memory clone of the digital twin without altering persistent base data.
          </p>
        </div>

        <span className="text-[11px] font-mono px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/30">
          State Isolation Active (Non-destructive)
        </span>
      </div>

      {/* Scenario Control Configuration Card */}
      <form
        onSubmit={handleRunSimulation}
        className="p-5 rounded-xl bg-nexus-900 border border-nexus-700/60 shadow-xl space-y-4"
      >
        <div className="flex items-center justify-between border-b border-nexus-800 pb-3">
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-blue-400" />
            <h3 className="text-sm font-semibold text-white">Scenario Shock Builder</h3>
          </div>
          <div className="flex gap-2">
            {[
              { id: 'SUPPLIER_FAILURE', label: 'Supplier Cut' },
              { id: 'ROUTE_DISRUPTION', label: 'Route Severance' },
              { id: 'DEMAND_SPIKE', label: 'Demand Surge' },
              { id: 'WAREHOUSE_SHUTDOWN', label: 'WH Shutdown' },
              { id: 'COMBINED_DISRUPTION', label: 'Combined Compound' },
            ].map((tab) => (
              <button
                type="button"
                key={tab.id}
                onClick={() => setScenarioType(tab.id as any)}
                className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                  scenarioType === tab.id
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'bg-nexus-850 text-slate-400 hover:text-white'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Dynamic Parameter Controls based on selected scenario type */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          {(scenarioType === 'SUPPLIER_FAILURE' || scenarioType === 'COMBINED_DISRUPTION') && (
            <>
              <div>
                <label className="block text-slate-400 font-medium mb-1.5">Supplier Node:</label>
                <select
                  value={selectedSupplier}
                  onChange={(e) => setSelectedSupplier(e.target.value)}
                  className="w-full p-2 rounded-lg bg-nexus-850 border border-nexus-700 text-white font-mono"
                >
                  {suppliers?.map((s) => (
                    <option key={s.supplier_id} value={s.supplier_id}>
                      {s.supplier_id} - {s.supplier_name}
                    </option>
                  ))}
                </select>
              </div>

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
            </>
          )}

          {(scenarioType === 'ROUTE_DISRUPTION' || scenarioType === 'COMBINED_DISRUPTION') && (
            <div>
              <label className="block text-slate-400 font-medium mb-1.5">Severed Corridor:</label>
              <select
                value={selectedRoute}
                onChange={(e) => setSelectedRoute(e.target.value)}
                className="w-full p-2 rounded-lg bg-nexus-850 border border-nexus-700 text-white font-mono"
              >
                {routes?.map((r) => (
                  <option key={r.route_id} value={r.route_id}>
                    {r.route_id} ({r.origin} &rarr; {r.destination})
                  </option>
                ))}
              </select>
            </div>
          )}

          {(scenarioType === 'DEMAND_SPIKE' || scenarioType === 'COMBINED_DISRUPTION') && (
            <div>
              <div className="flex justify-between text-slate-400 font-medium mb-1.5">
                <span>Demand Surge:</span>
                <span className="font-mono text-white">+{(demandSpikePercent * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.20"
                max="1.50"
                step="0.10"
                value={demandSpikePercent}
                onChange={(e) => setDemandSpikePercent(parseFloat(e.target.value))}
                className="w-full accent-blue-500 bg-nexus-800"
              />
            </div>
          )}

          {scenarioType === 'WAREHOUSE_SHUTDOWN' && (
            <div>
              <label className="block text-slate-400 font-medium mb-1.5">Target Warehouse:</label>
              <select
                value={selectedWarehouse}
                onChange={(e) => setSelectedWarehouse(e.target.value)}
                className="w-full p-2 rounded-lg bg-nexus-850 border border-nexus-700 text-white font-mono"
              >
                {warehouses?.map((w) => (
                  <option key={w.warehouse_id} value={w.warehouse_id}>
                    {w.warehouse_id} - {w.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          <div>
            <div className="flex justify-between text-slate-400 font-medium mb-1.5">
              <span>Disruption Duration:</span>
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
            disabled={simMutation.isPending}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-bold text-white shadow-lg shadow-blue-500/20 transition-all disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>{simMutation.isPending ? 'Simulating...' : 'Execute Digital Twin Simulation'}</span>
          </button>
        </div>
      </form>

      {/* Before vs After Disruption Comparative Analytics */}
      {sim && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white">Before vs After Shock State Comparison</h3>
            <span className="text-xs text-slate-400 font-mono">Scenario: {sim.scenario_type}</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Before (Nominal Base State) */}
            <div className="p-5 rounded-xl bg-nexus-900 border border-nexus-700/60 shadow-lg space-y-3">
              <div className="flex items-center justify-between border-b border-nexus-800 pb-2.5">
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                  Nominal Base State (Before)
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  Healthy Network
                </span>
              </div>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Total Consumer Demand:</span>
                  <span className="font-mono text-white font-bold">153,750 units</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Active Supplier Capacity:</span>
                  <span className="font-mono text-white font-bold">314,500 units</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Net Capacity Reserve:</span>
                  <span className="font-mono text-emerald-400 font-bold">+160,750 units</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Severed Routes:</span>
                  <span className="font-mono text-slate-300">0 corridors</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Nominal Service Level:</span>
                  <span className="font-mono text-emerald-400 font-bold">98.5%</span>
                </div>
              </div>
            </div>

            {/* After (Simulated Disruption State) */}
            <div className="p-5 rounded-xl bg-nexus-900 border border-rose-500/30 shadow-lg space-y-3">
              <div className="flex items-center justify-between border-b border-nexus-800 pb-2.5">
                <span className="text-xs font-bold uppercase tracking-wider text-rose-400">
                  Simulated Shock State (After)
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20">
                  Shock Applied
                </span>
              </div>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Total Consumer Demand:</span>
                  <span className="font-mono text-white font-bold">
                    {formatNumber(sim.simulated_network_state.total_demand_units)} units
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Available Supplier Capacity:</span>
                  <span className="font-mono text-white font-bold">
                    {formatNumber(sim.simulated_network_state.total_available_supplier_capacity)} units
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Compromised Suppliers:</span>
                  <span className="font-mono text-rose-400 font-bold">
                    {sim.simulated_network_state.compromised_suppliers_count} vendor(s)
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Severed Routes:</span>
                  <span className="font-mono text-rose-400 font-bold">
                    {sim.simulated_network_state.severed_routes_count} corridor(s)
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Net Capacity Balance:</span>
                  <span className="font-mono text-amber-400 font-bold">
                    {formatNumber(sim.simulated_network_state.net_capacity_balance)} units
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Action Callout to Optimize */}
          <div className="p-4 rounded-xl bg-nexus-900 border border-blue-500/30 flex items-center justify-between">
            <div className="space-y-0.5">
              <h4 className="text-xs font-bold text-white">Shock state successfully captured in digital twin memory.</h4>
              <p className="text-[11px] text-slate-400">
                Proceed to Optimization to compute the mathematically optimal multi-echelon response using Google OR-Tools.
              </p>
            </div>
            <Link
              to="/optimize"
              className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-bold text-white shadow-md shadow-blue-500/20"
            >
              <Cpu className="w-3.5 h-3.5" />
              <span>Solve with OR-Tools</span>
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};
