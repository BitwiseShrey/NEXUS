import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import {
  ShieldAlert,
  AlertTriangle,
  Activity,
  Sliders,
  CheckCircle2,
  TrendingDown,
  Layers,
  ChevronRight,
  Sparkles,
} from 'lucide-react';
import { getNetworkRisks, getSuppliers, predictSupplierRisk } from '../api';
import { RiskPredictRequest, RiskPredictResponse, Supplier } from '../types';
import { RiskBadge } from '../components/common/RiskBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import { LoadingSkeleton, ErrorState } from '../components/common/FeedbackStates';
import { formatNumber, formatPercent } from '../utils/formatters';

export const RiskIntelligence: React.FC = () => {
  const [selectedSupplierId, setSelectedSupplierId] = useState<string>('SUP_001');

  // Interactive Live Scoring State
  const [testProfile, setTestProfile] = useState<RiskPredictRequest>({
    on_time_rate: 0.84,
    average_delay: 4.2,
    delay_frequency: 0.16,
    quality_score: 0.90,
    lead_time: 5.5,
    lead_time_variability: 2.0,
    capacity_utilization: 0.94,
    historical_delays: 10,
  });

  const { data: networkRisks, isLoading: loadingRisks, error: errorRisks } = useQuery({
    queryKey: ['network-risks'],
    queryFn: getNetworkRisks,
  });

  const { data: suppliers, isLoading: loadingSuppliers } = useQuery({
    queryKey: ['suppliers-list'],
    queryFn: () => getSuppliers({ limit: 50 }),
  });

  // Supervised ML Prediction Mutation
  const predictMutation = useMutation({
    mutationFn: (req: RiskPredictRequest) => predictSupplierRisk(req),
  });

  if (loadingRisks || loadingSuppliers) {
    return <LoadingSkeleton rows={6} height="h-28" />;
  }

  if (errorRisks) {
    return <ErrorState message="Failed to fetch unified network risk profile from backend." />;
  }

  const selectedSupplier = suppliers?.find((s) => s.supplier_id === selectedSupplierId) || suppliers?.[0];

  const handleRunCustomPrediction = () => {
    predictMutation.mutate(testProfile);
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            Supply Chain Risk Command Center
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Supervised XGBoost disruption classifier and multi-dimensional explainable vulnerability indices.
          </p>
        </div>

        {/* Global Risk Badge */}
        <div className="flex items-center gap-3 p-2.5 rounded-xl bg-nexus-900 border border-nexus-700">
          <div className="text-right">
            <div className="text-[10px] uppercase font-semibold text-slate-400">Composite Risk Score</div>
            <div className="text-sm font-bold text-white">
              {((networkRisks?.composite_network_risk_score ?? 0.14) * 100).toFixed(1)} / 100
            </div>
          </div>
          <RiskBadge scoreOrTier={networkRisks?.risk_status || 'LOW_RISK'} size="md" />
        </div>
      </div>

      {/* 4 Risk Dimension Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-nexus-900 border border-blue-500/20 shadow-md">
          <span className="text-xs font-semibold text-slate-400 uppercase">Supplier Disruption Index</span>
          <div className="text-2xl font-bold text-white mt-1">
            {formatPercent(networkRisks?.dimensions?.supplier_risk ?? 0.12)}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Based on historical delays & QA</p>
        </div>

        <div className="p-4 rounded-xl bg-nexus-900 border border-amber-500/20 shadow-md">
          <span className="text-xs font-semibold text-slate-400 uppercase">Inventory Stockout Index</span>
          <div className="text-2xl font-bold text-amber-400 mt-1">
            {formatPercent(networkRisks?.dimensions?.inventory_risk ?? 0.08)}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Safety stock breach exposure</p>
        </div>

        <div className="p-4 rounded-xl bg-nexus-900 border border-emerald-500/20 shadow-md">
          <span className="text-xs font-semibold text-slate-400 uppercase">Route Transit Risk</span>
          <div className="text-2xl font-bold text-emerald-400 mt-1">
            {formatPercent(networkRisks?.dimensions?.route_risk ?? 0.09)}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Long-haul road vs rail corridors</p>
        </div>

        <div className="p-4 rounded-xl bg-nexus-900 border border-purple-500/20 shadow-md">
          <span className="text-xs font-semibold text-slate-400 uppercase">Warehouse Congestion</span>
          <div className="text-2xl font-bold text-purple-400 mt-1">
            {formatPercent(networkRisks?.dimensions?.warehouse_risk ?? 0.15)}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Capacity stress & utilization &gt; 80%</p>
        </div>
      </div>

      {/* Main Two-Column View: Supplier Roster + Interactive Prediction Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Supplier Vulnerability Roster */}
        <div className="lg:col-span-2 p-5 rounded-xl bg-nexus-900 border border-nexus-700/60 shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-nexus-800 pb-3">
            <div>
              <h3 className="text-sm font-semibold text-white">Tier-1 & Tier-2 Supplier Roster & Vulnerability</h3>
              <p className="text-xs text-slate-400">Click any supplier to inspect features and disruption drivers.</p>
            </div>
            <span className="text-xs text-slate-400">{suppliers?.length} Vendors Active</span>
          </div>

          <div className="overflow-x-auto max-h-[500px]">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-nexus-850 text-slate-400 uppercase text-[10px] tracking-wider sticky top-0 border-b border-nexus-800">
                <tr>
                  <th className="py-2.5 px-3">Supplier</th>
                  <th className="py-2.5 px-3">Category</th>
                  <th className="py-2.5 px-3 text-right">On-Time</th>
                  <th className="py-2.5 px-3 text-right">Quality</th>
                  <th className="py-2.5 px-3 text-right">Lead Time</th>
                  <th className="py-2.5 px-3 text-right">Risk Score</th>
                  <th className="py-2.5 px-3 text-center">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-nexus-800/60">
                {suppliers?.map((sup) => {
                  const isSelected = sup.supplier_id === selectedSupplier?.supplier_id;
                  return (
                    <tr
                      key={sup.supplier_id}
                      onClick={() => setSelectedSupplierId(sup.supplier_id)}
                      className={`cursor-pointer transition-colors ${
                        isSelected ? 'bg-blue-600/15 border-l-2 border-blue-500' : 'hover:bg-nexus-850/50'
                      }`}
                    >
                      <td className="py-2.5 px-3">
                        <div className="font-semibold text-white">{sup.supplier_name}</div>
                        <div className="text-[10px] text-slate-500 font-mono">{sup.supplier_id} &bull; {sup.location}</div>
                      </td>
                      <td className="py-2.5 px-3 text-slate-300">{sup.product_categories}</td>
                      <td className="py-2.5 px-3 text-right font-mono">{formatPercent(sup.on_time_rate)}</td>
                      <td className="py-2.5 px-3 text-right font-mono">{formatPercent(sup.quality_score)}</td>
                      <td className="py-2.5 px-3 text-right font-mono">{sup.lead_time}d</td>
                      <td className="py-2.5 px-3 text-right">
                        <RiskBadge scoreOrTier={sup.risk_score} />
                      </td>
                      <td className="py-2.5 px-3 text-center">
                        <span className={`text-xs font-semibold ${isSelected ? 'text-blue-400' : 'text-slate-500'}`}>
                          {isSelected ? 'Selected' : 'View'}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right: Selected Supplier Drill-Down & Live ML Predictor */}
        <div className="lg:col-span-1 space-y-4">
          {/* Selected Supplier Detail Card */}
          {selectedSupplier && (
            <div className="p-5 rounded-xl bg-nexus-900 border border-nexus-700/60 shadow-xl space-y-4">
              <div className="border-b border-nexus-800 pb-3">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono text-blue-400 font-bold uppercase">{selectedSupplier.supplier_id}</span>
                  <RiskBadge scoreOrTier={selectedSupplier.risk_score} />
                </div>
                <h3 className="text-base font-bold text-white mt-1">{selectedSupplier.supplier_name}</h3>
                <p className="text-xs text-slate-400">{selectedSupplier.location}</p>
              </div>

              <div className="space-y-2 text-xs">
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Monthly Capacity:</span>
                  <span className="font-mono text-white">{formatNumber(selectedSupplier.capacity)} units</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Base Unit Cost:</span>
                  <span className="font-mono text-white">INR {selectedSupplier.unit_cost}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">On-Time Reliability:</span>
                  <span className="font-mono text-emerald-400 font-semibold">{formatPercent(selectedSupplier.on_time_rate)}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Quality QA Pass Rate:</span>
                  <span className="font-mono text-white font-semibold">{formatPercent(selectedSupplier.quality_score)}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-nexus-850">
                  <span className="text-slate-400">Nominal Lead Time:</span>
                  <span className="font-mono text-white">{selectedSupplier.lead_time} days</span>
                </div>
              </div>

              {/* Explainable Risk Drivers for this supplier */}
              <div className="p-3 rounded-lg bg-nexus-850 border border-nexus-800 space-y-1.5">
                <span className="text-[11px] font-semibold text-slate-300 block">Identified Risk Drivers:</span>
                <ul className="text-xs text-slate-400 space-y-1 list-disc list-inside">
                  {selectedSupplier.on_time_rate < 0.93 && (
                    <li className="text-amber-300">Late shipment vulnerability: {(1 - selectedSupplier.on_time_rate) * 100}% late dispatches</li>
                  )}
                  {selectedSupplier.quality_score < 0.95 && (
                    <li className="text-amber-300">QA rejection rate: {(1 - selectedSupplier.quality_score) * 100}% defect margin</li>
                  )}
                  {selectedSupplier.risk_score <= 0.20 && (
                    <li className="text-emerald-400">Operating within nominal risk boundaries</li>
                  )}
                </ul>
              </div>
            </div>
          )}

          {/* Interactive ML Risk Prediction Simulator */}
          <div className="p-5 rounded-xl bg-nexus-900 border border-nexus-700/60 shadow-xl space-y-3">
            <div className="flex items-center gap-2 border-b border-nexus-800 pb-2">
              <Sparkles className="w-4 h-4 text-blue-400" />
              <h4 className="text-xs font-bold text-white uppercase tracking-wider">Live XGBoost Inference</h4>
            </div>
            <p className="text-[11px] text-slate-400">
              Adjust operational features to evaluate ML disruption probability in real time:
            </p>

            <div className="space-y-2 text-xs">
              <div>
                <div className="flex justify-between text-slate-400 mb-1">
                  <span>On-Time Rate:</span>
                  <span className="font-mono text-white">{(testProfile.on_time_rate * 100).toFixed(0)}%</span>
                </div>
                <input
                  type="range"
                  min="0.60"
                  max="1.0"
                  step="0.02"
                  value={testProfile.on_time_rate}
                  onChange={(e) => setTestProfile({ ...testProfile, on_time_rate: parseFloat(e.target.value) })}
                  className="w-full accent-blue-500 bg-nexus-800"
                />
              </div>

              <div>
                <div className="flex justify-between text-slate-400 mb-1">
                  <span>Capacity Utilization:</span>
                  <span className="font-mono text-white">{(testProfile.capacity_utilization * 100).toFixed(0)}%</span>
                </div>
                <input
                  type="range"
                  min="0.50"
                  max="0.99"
                  step="0.02"
                  value={testProfile.capacity_utilization}
                  onChange={(e) => setTestProfile({ ...testProfile, capacity_utilization: parseFloat(e.target.value) })}
                  className="w-full accent-blue-500 bg-nexus-800"
                />
              </div>

              <div>
                <div className="flex justify-between text-slate-400 mb-1">
                  <span>Historical Delays:</span>
                  <span className="font-mono text-white">{testProfile.historical_delays} shipments</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="20"
                  step="1"
                  value={testProfile.historical_delays}
                  onChange={(e) => setTestProfile({ ...testProfile, historical_delays: parseInt(e.target.value) })}
                  className="w-full accent-blue-500 bg-nexus-800"
                />
              </div>

              <button
                onClick={handleRunCustomPrediction}
                disabled={predictMutation.isPending}
                className="w-full mt-2 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-bold text-white transition-all shadow-md shadow-blue-500/20 disabled:opacity-50"
              >
                {predictMutation.isPending ? 'Scoring...' : 'Score with XGBoost'}
              </button>

              {predictMutation.data && (
                <div className="p-3 rounded-lg bg-nexus-850 border border-blue-500/30 mt-3 space-y-1.5 animate-fadeIn">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400 font-medium">Disruption Probability:</span>
                    <span className="text-sm font-bold text-white font-mono">
                      {(predictMutation.data.disruption_probability * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400 font-medium">Risk Tier:</span>
                    <RiskBadge scoreOrTier={predictMutation.data.risk_tier} />
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1">
                    <span className="font-semibold text-slate-300">Drivers:</span>{' '}
                    {predictMutation.data.risk_drivers.join(', ')}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
