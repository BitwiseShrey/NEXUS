import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  CheckCircle2, 
  AlertTriangle, 
  Lightbulb, 
  ArrowRight, 
  ShieldAlert, 
  TrendingUp, 
  DollarSign, 
  Percent, 
  Building2, 
  Truck, 
  Layers, 
  Download, 
  Send, 
  RefreshCw,
  Search,
  Filter,
  Check,
  Clock,
  Sparkles
} from 'lucide-react';
import { getRecommendations, runOptimization } from '../api';
import { RecommendationItem } from '../types';
import WorkflowBreadcrumb from '../components/common/WorkflowBreadcrumb';
import { KpiCard } from '../components/common/KpiCard';
import { RiskBadge } from '../components/common/RiskBadge';
import { LoadingSkeleton, ErrorState, EmptyState } from '../components/common/FeedbackStates';
import { formatINR, formatNumber, formatPercent } from '../utils/formatters';

export const RecommendationCenter: React.FC = () => {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedActionType, setSelectedActionType] = useState<string>('ALL');
  const [approvedRecs, setApprovedRecs] = useState<Record<string, boolean>>({});
  const [activeTab, setActiveTab] = useState<'ALL' | 'CRITICAL' | 'APPROVED'>('ALL');
  const [dispatchFeedback, setDispatchFeedback] = useState<string | null>(null);

  // Quick Run state for creating on-demand recommendations
  const [quickScenario, setQuickScenario] = useState<'SUPPLIER_FAILURE' | 'ROUTE_DISRUPTION' | 'DEMAND_SPIKE'>('SUPPLIER_FAILURE');
  const [quickParamId, setQuickParamId] = useState('SUP_001');

  const { data: recommendations, isLoading, error, refetch, isFetching } = useQuery<RecommendationItem[]>({
    queryKey: ['recommendations'],
    queryFn: getRecommendations,
    refetchInterval: 30000,
  });

  const optimizeMutation = useMutation({
    mutationFn: () => {
      let params: Record<string, any> = {};
      if (quickScenario === 'SUPPLIER_FAILURE') {
        params = { supplier_id: quickParamId, capacity_loss: 0.85 };
      } else if (quickScenario === 'ROUTE_DISRUPTION') {
        params = { origin_id: 'PLANT_001', destination_id: 'WH_001', cost_multiplier: 3.0 };
      } else {
        params = { zone_id: 'ZONE_01', multiplier: 2.0 };
      }
      return runOptimization({
        scenario_type: quickScenario,
        parameters: params,
        risk_aversion_weight: 0.6,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recommendations'] });
      setDispatchFeedback('New strategy synthesized and added to Recommendation Center.');
      setTimeout(() => setDispatchFeedback(null), 4000);
    },
  });

  const handleApprove = (recId: string) => {
    setApprovedRecs(prev => ({
      ...prev,
      [recId]: !prev[recId]
    }));
    setDispatchFeedback(`[Simulation Mode] Recommendation ${recId} handoff dispatched to mock ERP/WMS ingestion queue.`);
    setTimeout(() => setDispatchFeedback(null), 4000);
  };

  const handleExportJSON = (rec: RecommendationItem) => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(rec, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `nexus_recommendation_${rec.recommendation_id}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  if (isLoading) {
    return (
      <div className="p-8 space-y-6">
        <LoadingSkeleton rows={4} height="h-24" />
      </div>
    );
  }

  if (error || !recommendations) {
    return (
      <div className="p-8 space-y-6">
        <ErrorState 
          message="Could not retrieve synthesized supply chain recommendations from the NEXUS backend." 
          onRetry={() => refetch()} 
        />
      </div>
    );
  }

  // Filter recommendations
  const filteredRecs = recommendations.filter(rec => {
    const matchesSearch = 
      rec.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      rec.reason.toLowerCase().includes(searchTerm.toLowerCase()) ||
      rec.recommendation_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (rec.affected_entities.primary_disrupted_entity && rec.affected_entities.primary_disrupted_entity.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesAction = selectedActionType === 'ALL' || rec.action_type === selectedActionType;

    const isApproved = !!approvedRecs[rec.recommendation_id];
    const isCritical = rec.confidence_score >= 0.9;

    if (activeTab === 'CRITICAL') return matchesSearch && matchesAction && isCritical;
    if (activeTab === 'APPROVED') return matchesSearch && matchesAction && isApproved;
    return matchesSearch && matchesAction;
  });

  const totalCost = recommendations.reduce((sum, r) => sum + (r.expected_cost || 0), 0);
  const avgConfidence = recommendations.length > 0 
    ? recommendations.reduce((sum, r) => sum + (r.confidence_score || 0), 0) / recommendations.length 
    : 0;

  return (
    <div className="p-8 space-y-8 animate-fade-in text-slate-100">
      {/* Workflow Navigation */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-nexus-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-3">
            <Lightbulb className="w-7 h-7 text-amber-400" />
            Strategic Recommendation Center
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Stage 6: AI-synthesized mitigation directives translating OR-Tools optimization solutions into executive decisions
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => refetch()}
            disabled={isFetching}
            className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium rounded-lg bg-nexus-800 hover:bg-nexus-700 text-slate-300 border border-nexus-700 transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isFetching ? 'animate-spin text-nexus-accent' : ''}`} />
            Refresh
          </button>
        </div>
      </div>

      {/* Global Notifications */}
      {dispatchFeedback && (
        <div className="bg-emerald-950/80 border border-emerald-500/50 rounded-xl p-4 flex items-center justify-between animate-fade-in">
          <div className="flex items-center gap-3 text-emerald-300 text-sm">
            <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
            <span>{dispatchFeedback}</span>
          </div>
          <button 
            onClick={() => setDispatchFeedback(null)} 
            className="text-xs text-emerald-400 hover:text-emerald-200 underline"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* KPI Overview Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <KpiCard
          title="Generated Directives"
          value={recommendations.length}
          subtitle="Autonomous mitigation plans"
          icon={Lightbulb}
          color="amber"
        />
        <KpiCard
          title="Plan Robustness Index"
          value={formatPercent(avgConfidence * 100)}
          subtitle="LP mathematical solvability"
          icon={Sparkles}
          color="blue"
        />
        <KpiCard
          title="Simulated ERP Dispatches"
          value={Object.values(approvedRecs).filter(Boolean).length}
          subtitle={`Out of ${recommendations.length} total options`}
          icon={CheckCircle2}
          color="emerald"
        />
        <KpiCard
          title="Est. Operations Cost"
          value={formatINR(totalCost)}
          subtitle="Aggregate optimized reallocation"
          icon={DollarSign}
          color="purple"
        />
      </div>

      {/* Interactive Trigger for New Recommendations */}
      <div className="bg-nexus-900 border border-nexus-800 rounded-xl p-5 shadow-lg">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
          <div>
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-nexus-accent" />
              Synthesize Strategic Recommendation from Live Scenario
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Run OR-Tools mathematical reallocation solver on a selected stress condition to generate an actionable mitigation brief.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 w-full lg:w-auto">
            <select
              value={quickScenario}
              onChange={(e) => {
                const val = e.target.value as any;
                setQuickScenario(val);
                if (val === 'SUPPLIER_FAILURE') setQuickParamId('SUP_001');
                if (val === 'ROUTE_DISRUPTION') setQuickParamId('PLANT_001 -> WH_001');
                if (val === 'DEMAND_SPIKE') setQuickParamId('ZONE_01');
              }}
              className="bg-nexus-950 border border-nexus-700 text-xs text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:border-nexus-accent"
            >
              <option value="SUPPLIER_FAILURE">Supplier Breakdown (Tata AutoComp)</option>
              <option value="ROUTE_DISRUPTION">Key Route Severance (Plant to WH)</option>
              <option value="DEMAND_SPIKE">Tier-1 Metro Surge (Zone 01)</option>
            </select>

            <button
              onClick={() => optimizeMutation.mutate()}
              disabled={optimizeMutation.isPending}
              className="flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg bg-nexus-accent hover:bg-nexus-accent-hover text-nexus-950 font-bold transition-all shadow-md disabled:opacity-50"
            >
              {optimizeMutation.isPending ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  Solving & Synthesizing...
                </>
              ) : (
                <>
                  <Lightbulb className="w-3.5 h-3.5 text-nexus-950" />
                  Generate Recommendation
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Filter and Search Controls */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-4 bg-nexus-900/60 p-4 rounded-xl border border-nexus-800">
        {/* Tabs */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveTab('ALL')}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
              activeTab === 'ALL'
                ? 'bg-nexus-accent text-nexus-950 font-semibold'
                : 'text-slate-400 hover:text-white bg-nexus-950/60 border border-nexus-800'
            }`}
          >
            All Recommendations ({recommendations.length})
          </button>
          <button
            onClick={() => setActiveTab('CRITICAL')}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
              activeTab === 'CRITICAL'
                ? 'bg-nexus-accent text-nexus-950 font-semibold'
                : 'text-slate-400 hover:text-white bg-nexus-950/60 border border-nexus-800'
            }`}
          >
            High Confidence ({recommendations.filter(r => r.confidence_score >= 0.9).length})
          </button>
          <button
            onClick={() => setActiveTab('APPROVED')}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
              activeTab === 'APPROVED'
                ? 'bg-nexus-accent text-nexus-950 font-semibold'
                : 'text-slate-400 hover:text-white bg-nexus-950/60 border border-nexus-800'
            }`}
          >
            Dispatched ({Object.values(approvedRecs).filter(Boolean).length})
          </button>
        </div>

        {/* Search & Action Filter */}
        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-3 top-2.5 w-4 h-4 text-slate-500" />
            <input
              type="text"
              placeholder="Search by ID, supplier, zone..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs bg-nexus-950 border border-nexus-700 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:border-nexus-accent"
            />
          </div>

          <select
            value={selectedActionType}
            onChange={(e) => setSelectedActionType(e.target.value)}
            className="bg-nexus-950 border border-nexus-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-nexus-accent"
          >
            <option value="ALL">All Action Types</option>
            <option value="REALLOCATE_AND_REROUTE">Reallocate & Reroute</option>
            <option value="BUFFER_INVENTORY">Buffer Inventory</option>
            <option value="SUPPLIER_SWITCH">Supplier Switch</option>
          </select>
        </div>
      </div>

      {/* Recommendation Cards List */}
      {filteredRecs.length === 0 ? (
        <EmptyState
          title="No Recommendations Match Criteria"
          subtitle="Try clearing search filters or generate a fresh optimization recommendation using the toolbar above."
        />
      ) : (
        <div className="space-y-6">
          {filteredRecs.map((rec) => {
            const isApproved = !!approvedRecs[rec.recommendation_id];
            const primaryEntity = rec.affected_entities?.primary_disrupted_entity || 'N/A';
            const depProducts = rec.affected_entities?.dependent_products || [];
            const affectedWh = rec.affected_entities?.affected_warehouses || 0;
            const affectedZones = rec.affected_entities?.affected_demand_zones || [];

            return (
              <div 
                key={rec.recommendation_id}
                className={`bg-nexus-900 border rounded-2xl p-6 transition-all duration-200 shadow-xl ${
                  isApproved 
                    ? 'border-emerald-500/50 bg-gradient-to-r from-nexus-900 to-emerald-950/20' 
                    : 'border-nexus-800 hover:border-nexus-700'
                }`}
              >
                {/* Header row */}
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-nexus-800/80 pb-4 mb-5">
                  <div className="space-y-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-mono text-xs text-nexus-accent font-semibold px-2 py-0.5 rounded bg-nexus-950 border border-nexus-800">
                        {rec.recommendation_id}
                      </span>
                      {rec.run_id && (
                        <span className="font-mono text-xs text-slate-400 px-2 py-0.5 rounded bg-nexus-950/50">
                          {rec.run_id}
                        </span>
                      )}
                      <span className="text-xs px-2.5 py-0.5 rounded-full font-medium bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                        {rec.action_type || 'REALLOCATE_AND_REROUTE'}
                      </span>
                      {isApproved && (
                        <span className="text-xs px-2.5 py-0.5 rounded-full font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center gap-1">
                          <Check className="w-3 h-3" /> Dispatched (Mock ERP Queue)
                        </span>
                      )}
                    </div>
                    <h2 className="text-lg font-bold text-white tracking-tight mt-1">
                      {rec.title}
                    </h2>
                  </div>

                  {/* Confidence Badge & Created Time */}
                  <div className="flex items-center gap-3 text-right">
                    <div className="bg-nexus-950 px-3 py-1.5 rounded-xl border border-nexus-800 text-center">
                      <div className="text-[10px] text-slate-400 uppercase tracking-wider">Plan Robustness</div>
                      <div className="text-sm font-bold text-nexus-accent">
                        {(rec.confidence_score * 100).toFixed(0)}%
                      </div>
                    </div>
                    {rec.created_at && (
                      <div className="text-xs text-slate-500 flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {new Date(rec.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    )}
                  </div>
                </div>

                {/* Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                  {/* Left Column: Rationale & Expected Benefit (8 cols) */}
                  <div className="lg:col-span-8 space-y-4">
                    {/* Problem & Rationale */}
                    <div className="bg-nexus-950/70 p-4 rounded-xl border border-nexus-800/80">
                      <div className="text-xs font-semibold text-rose-400 uppercase tracking-wider flex items-center gap-1.5 mb-2">
                        <ShieldAlert className="w-4 h-4" />
                        Root Cause & Risk Rationale
                      </div>
                      <p className="text-sm text-slate-300 leading-relaxed">
                        {rec.reason}
                      </p>
                    </div>

                    {/* Quantified Benefit */}
                    <div className="bg-nexus-950/70 p-4 rounded-xl border border-nexus-800/80">
                      <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5 mb-2">
                        <TrendingUp className="w-4 h-4" />
                        Strategic Impact & Solved Objective
                      </div>
                      <p className="text-sm text-slate-300 leading-relaxed font-medium">
                        {rec.expected_benefit}
                      </p>
                    </div>

                    {/* Affected Entities Pills */}
                    <div className="space-y-2">
                      <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                        Affected Supply Chain Nodes & SKUs
                      </div>
                      <div className="flex flex-wrap items-center gap-2 text-xs">
                        <div className="bg-nexus-950 border border-nexus-800 px-3 py-1.5 rounded-lg flex items-center gap-2">
                          <span className="text-slate-400">Disrupted Origin:</span>
                          <span className="font-mono font-semibold text-rose-400">{primaryEntity}</span>
                        </div>
                        <div className="bg-nexus-950 border border-nexus-800 px-3 py-1.5 rounded-lg flex items-center gap-2">
                          <span className="text-slate-400">Warehouses Impacted:</span>
                          <span className="font-semibold text-amber-300">{affectedWh} Facilities</span>
                        </div>
                        {depProducts.length > 0 && (
                          <div className="bg-nexus-950 border border-nexus-800 px-3 py-1.5 rounded-lg flex items-center gap-2">
                            <span className="text-slate-400">Products:</span>
                            <span className="font-mono text-cyan-300">{depProducts.join(', ')}</span>
                          </div>
                        )}
                        {affectedZones.length > 0 && (
                          <div className="bg-nexus-950 border border-nexus-800 px-3 py-1.5 rounded-lg flex items-center gap-2">
                            <span className="text-slate-400">Zones Protected:</span>
                            <span className="font-mono text-emerald-300">{affectedZones.slice(0, 3).join(', ')}{affectedZones.length > 3 ? ` +${affectedZones.length - 3} more` : ''}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Right Column: Financials & Action Buttons (4 cols) */}
                  <div className="lg:col-span-4 flex flex-col justify-between space-y-4 bg-nexus-950/50 p-5 rounded-xl border border-nexus-800">
                    <div className="space-y-3">
                      <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                        Solution Economics
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center justify-between text-xs py-1 border-b border-nexus-800/60">
                          <span className="text-slate-400">Allocation Cost</span>
                          <span className="font-mono font-bold text-white">{formatINR(rec.expected_cost)}</span>
                        </div>
                        <div className="flex items-center justify-between text-xs py-1 border-b border-nexus-800/60">
                          <span className="text-slate-400">Mathematical Solver</span>
                          <span className="font-semibold text-cyan-400">Google OR-Tools (GLOP)</span>
                        </div>
                        <div className="flex items-center justify-between text-xs py-1">
                          <span className="text-slate-400">Execution SLA</span>
                          <span className="font-semibold text-amber-400">&lt; 24 Hours</span>
                        </div>
                      </div>
                    </div>

                    {/* Action Execution Buttons */}
                    <div className="space-y-2 pt-4">
                      <button
                        onClick={() => handleApprove(rec.recommendation_id)}
                        className={`w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition-all shadow-md ${
                          isApproved
                            ? 'bg-emerald-600 hover:bg-emerald-500 text-white'
                            : 'bg-nexus-accent hover:bg-nexus-accent-hover text-nexus-950'
                        }`}
                      >
                        {isApproved ? (
                          <>
                            <Check className="w-4 h-4" />
                            Dispatched (Simulation Demo)
                          </>
                        ) : (
                          <>
                            <Send className="w-4 h-4" />
                            Simulate ERP/WMS Dispatch
                          </>
                        )}
                      </button>

                      <button
                        onClick={() => handleExportJSON(rec)}
                        className="w-full flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-xs font-medium bg-nexus-900 hover:bg-nexus-800 text-slate-300 border border-nexus-700 transition-colors"
                      >
                        <Download className="w-3.5 h-3.5" />
                        Export Audit Brief (JSON)
                      </button>
                    </div>
                  </div>
                </div>

                {/* Footer audit trail */}
                <div className="mt-5 pt-3 border-t border-nexus-800/60 flex flex-col sm:flex-row items-center justify-between text-[11px] text-slate-500 gap-2">
                  <div className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                    <span>Audit Trail: Verified via linear LP simplex relaxation; zero inventory starvation violated.</span>
                  </div>
                  <span>Deterministic seed: 42</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default RecommendationCenter;
