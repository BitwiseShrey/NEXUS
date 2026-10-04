import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import {
  ShieldAlert,
  Boxes,
  Truck,
  DollarSign,
  AlertTriangle,
  ArrowRight,
  TrendingUp,
  Activity,
  CheckCircle2,
  Users,
} from 'lucide-react';
import {
  getAnalyticsSummary,
  getNetworkRisks,
  getNetworkSummary,
  getSuppliers,
  getInventory,
} from '../api';
import { KpiCard } from '../components/common/KpiCard';
import { RiskBadge } from '../components/common/RiskBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import { LoadingSkeleton, ErrorState } from '../components/common/FeedbackStates';
import { formatINR, formatNumber, formatPercent } from '../utils/formatters';

export const ExecutiveOverview: React.FC = () => {
  const {
    data: analytics,
    isLoading: loadingAnalytics,
    error: errorAnalytics,
    refetch: refetchAnalytics,
  } = useQuery({
    queryKey: ['analytics-summary'],
    queryFn: getAnalyticsSummary,
  });

  const {
    data: risks,
    isLoading: loadingRisks,
    error: errorRisks,
  } = useQuery({
    queryKey: ['network-risks'],
    queryFn: getNetworkRisks,
  });

  const { data: network } = useQuery({
    queryKey: ['network-summary'],
    queryFn: getNetworkSummary,
  });

  const { data: suppliers } = useQuery({
    queryKey: ['critical-suppliers'],
    queryFn: () => getSuppliers({ limit: 10 }),
  });

  const { data: criticalInventory } = useQuery({
    queryKey: ['critical-inventory'],
    queryFn: () => getInventory({ critical_only: true, limit: 8 }),
  });

  if (loadingAnalytics || loadingRisks) {
    return <LoadingSkeleton rows={6} height="h-28" />;
  }

  if (errorAnalytics || errorRisks) {
    return (
      <ErrorState
        message="Unable to load operational analytics telemetry. Please verify backend connection."
        onRetry={refetchAnalytics}
      />
    );
  }

  const netRiskScore = risks?.composite_network_risk_score ?? 0.14;
  const highRiskSupsCount = risks?.top_vulnerable_suppliers?.length ?? analytics?.suppliers?.high_risk_suppliers_count ?? 0;
  const criticalStockoutCount = analytics?.inventory?.critical_stockout_skus ?? 0;
  const onTimeRate = analytics?.fulfillment?.on_time_delivery_rate ?? 0.93;
  const invValuation = analytics?.inventory?.total_inventory_valuation_inr ?? 0;

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            Executive Supply Chain Overview
            <span className="text-xs font-normal px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/30">
              Live Digital Twin
            </span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time monitoring across 83 facilities, 160 transit corridors, and 50,000 historical order flows.
          </p>
        </div>

        {/* Global Network Risk Status Pill */}
        <div className="flex items-center gap-3 p-2.5 rounded-xl bg-nexus-900 border border-nexus-700">
          <div className="text-right">
            <div className="text-[10px] uppercase font-semibold text-slate-400">Network Vulnerability</div>
            <div className="text-sm font-bold text-white">{(netRiskScore * 100).toFixed(1)} / 100</div>
          </div>
          <RiskBadge scoreOrTier={risks?.risk_status || 'LOW_RISK'} size="md" />
        </div>
      </div>

      {/* Top KPI Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          title="On-Time Delivery SLA"
          value={formatPercent(onTimeRate)}
          subtitle={`${formatNumber(analytics?.fulfillment?.sample_orders_analyzed)} orders tracked`}
          trend={onTimeRate >= 0.90 ? 'Healthy' : 'Degraded'}
          trendUp={onTimeRate >= 0.90}
          icon={Activity}
          color="emerald"
        />
        <KpiCard
          title="Inventory Valuation"
          value={formatINR(invValuation)}
          subtitle={`${analytics?.inventory?.total_skus_tracked ?? 500} warehouse SKUs`}
          icon={DollarSign}
          color="blue"
        />
        <KpiCard
          title="Vulnerable Suppliers"
          value={highRiskSupsCount}
          subtitle={`Out of ${analytics?.suppliers?.total_suppliers ?? 20} active vendors`}
          trend={highRiskSupsCount > 0 ? 'Action Req' : 'Normal'}
          trendUp={highRiskSupsCount === 0}
          icon={AlertTriangle}
          color={highRiskSupsCount > 0 ? 'amber' : 'emerald'}
        />
        <KpiCard
          title="Stockout Risk SKUs"
          value={criticalStockoutCount}
          subtitle="Stock below reorder point"
          trend={criticalStockoutCount > 0 ? 'Buffer Alert' : 'Nominal'}
          trendUp={criticalStockoutCount === 0}
          icon={Boxes}
          color={criticalStockoutCount > 0 ? 'rose' : 'emerald'}
        />
      </div>

      {/* Decision-Loop Quick Action Banner */}
      <div className="p-4 rounded-xl bg-gradient-to-r from-blue-900/40 via-nexus-900 to-indigo-900/30 border border-blue-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-blue-400 animate-ping" />
            <h3 className="text-sm font-semibold text-white">Decision Intelligence Action Loop</h3>
          </div>
          <p className="text-xs text-slate-300 max-w-2xl">
            NEXUS predicts disruption probabilities, calculates cascading shortage impacts, and computes cost-optimized reallocation plans before stockouts occur.
          </p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <Link
            to="/impact"
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white shadow-md shadow-blue-600/30 transition-all"
          >
            <span>Run Impact Propagation</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
          <Link
            to="/optimize"
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-nexus-800 hover:bg-nexus-700 text-xs font-semibold text-slate-200 border border-nexus-700 transition-all"
          >
            <span>Solve OR-Tools</span>
          </Link>
        </div>
      </div>

      {/* Two Column Section: Multi-Dimensional Risk + At-Risk Inventory */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Breakdown Dimension Card */}
        <div className="lg:col-span-1 p-5 rounded-xl bg-nexus-900 border border-nexus-700/60 shadow-lg space-y-4">
          <div className="flex items-center justify-between border-b border-nexus-800 pb-3">
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-blue-400" />
              <h3 className="text-sm font-semibold text-white">Risk Dimensions</h3>
            </div>
            <Link to="/risk" className="text-xs text-blue-400 hover:underline">
              Inspect All &rarr;
            </Link>
          </div>

          <div className="space-y-3">
            {risks?.dimensions && (
              <>
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-400">Supplier Disruption Risk</span>
                    <span className="text-slate-200 font-mono font-medium">
                      {(risks.dimensions.supplier_risk * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full h-1.5 bg-nexus-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-500 rounded-full"
                      style={{ width: `${Math.min(risks.dimensions.supplier_risk * 100, 100)}%` }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-400">Inventory Stockout Risk</span>
                    <span className="text-slate-200 font-mono font-medium">
                      {(risks.dimensions.inventory_risk * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full h-1.5 bg-nexus-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-amber-500 rounded-full"
                      style={{ width: `${Math.min(risks.dimensions.inventory_risk * 100, 100)}%` }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-400">Route Transit Exposure</span>
                    <span className="text-slate-200 font-mono font-medium">
                      {(risks.dimensions.route_risk * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full h-1.5 bg-nexus-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-emerald-500 rounded-full"
                      style={{ width: `${Math.min(risks.dimensions.route_risk * 100, 100)}%` }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-400">Warehouse Congestion</span>
                    <span className="text-slate-200 font-mono font-medium">
                      {(risks.dimensions.warehouse_risk * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full h-1.5 bg-nexus-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-purple-500 rounded-full"
                      style={{ width: `${Math.min(risks.dimensions.warehouse_risk * 100, 100)}%` }}
                    />
                  </div>
                </div>
              </>
            )}
          </div>

          <div className="pt-2 border-t border-nexus-800">
            <span className="text-[11px] text-slate-400">Top Vulnerable Suppliers:</span>
            <ul className="mt-2 space-y-1.5">
              {risks?.top_vulnerable_suppliers?.map((sup) => (
                <li key={sup.supplier_id} className="flex items-center justify-between text-xs p-1.5 rounded bg-nexus-850">
                  <span className="font-medium text-slate-300 truncate max-w-[160px]">{sup.name}</span>
                  <RiskBadge scoreOrTier={sup.risk_score} />
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Critical Inventory & At-Risk SKU Table */}
        <div className="lg:col-span-2 p-5 rounded-xl bg-nexus-900 border border-nexus-700/60 shadow-lg space-y-4">
          <div className="flex items-center justify-between border-b border-nexus-800 pb-3">
            <div className="flex items-center gap-2">
              <Boxes className="w-4 h-4 text-amber-400" />
              <h3 className="text-sm font-semibold text-white">Critical Stockout Warnings (Safety Stock Breaches)</h3>
            </div>
            <span className="text-xs text-slate-400">
              Mean runway: {analytics?.inventory?.mean_stock_coverage_days ?? 0} days
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-nexus-850 text-slate-400 uppercase text-[10px] tracking-wider border-b border-nexus-800">
                <tr>
                  <th className="py-2.5 px-3">Warehouse</th>
                  <th className="py-2.5 px-3">Product SKU</th>
                  <th className="py-2.5 px-3 text-right">Current Stock</th>
                  <th className="py-2.5 px-3 text-right">Reorder Point</th>
                  <th className="py-2.5 px-3 text-right">Stockout Risk</th>
                  <th className="py-2.5 px-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-nexus-800/60">
                {criticalInventory && criticalInventory.length > 0 ? (
                  criticalInventory.map((item) => (
                    <tr key={item.inventory_id} className="hover:bg-nexus-850/50 transition-colors">
                      <td className="py-2.5 px-3 font-mono font-medium text-white">{item.warehouse_id}</td>
                      <td className="py-2.5 px-3 font-mono text-slate-300">{item.product_id}</td>
                      <td className="py-2.5 px-3 text-right font-mono">{formatNumber(item.current_stock)}</td>
                      <td className="py-2.5 px-3 text-right font-mono text-slate-400">{formatNumber(item.reorder_point)}</td>
                      <td className="py-2.5 px-3 text-right">
                        <RiskBadge scoreOrTier={item.stockout_risk} />
                      </td>
                      <td className="py-2.5 px-3 text-center">
                        <StatusBadge
                          status={item.current_stock < item.safety_stock ? 'CRITICAL' : 'BELOW_ROP'}
                        />
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={6} className="py-6 text-center text-slate-500 italic">
                      All inventory stock levels currently satisfy safety thresholds.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
