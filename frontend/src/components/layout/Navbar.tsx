import React, { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { RefreshCw, Activity, CheckCircle2, AlertCircle, Database, BrainCircuit } from 'lucide-react';
import { getHealthStatus } from '../../api';

export const Navbar: React.FC = () => {
  const queryClient = useQueryClient();
  const [isRefreshing, setIsRefreshing] = useState(false);

  const { data: health, isLoading } = useQuery({
    queryKey: ['system-health'],
    queryFn: getHealthStatus,
    refetchInterval: 30000,
  });

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await queryClient.invalidateQueries();
    setTimeout(() => setIsRefreshing(false), 600);
  };

  const isOnline = health?.status === 'ONLINE' && health?.database === 'HEALTHY';
  const allModelsReady = health?.all_systems_operational;

  return (
    <header className="h-16 bg-nexus-900/90 backdrop-blur-md border-b border-nexus-700/40 px-6 flex items-center justify-between z-10 sticky top-0">
      {/* Title & Core Philosophy */}
      <div className="flex items-center space-x-3">
        <h1 className="text-sm font-semibold text-white tracking-wide">
          Supply Chain Control Center
        </h1>
        <span className="hidden lg:inline-block text-slate-600">|</span>
        <span className="hidden lg:inline-block text-xs text-slate-400 italic">
          "What is likely to go wrong, what will it affect, and what should we do about it?"
        </span>
      </div>

      {/* Status Badges & Controls */}
      <div className="flex items-center space-x-3">
        {/* ML Status */}
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-nexus-850 border border-nexus-700 text-xs">
          <BrainCircuit className="w-3.5 h-3.5 text-blue-400" />
          <span className="text-slate-400 font-medium">Models:</span>
          <span className={`font-semibold ${allModelsReady ? 'text-emerald-400' : 'text-amber-400'}`}>
            {allModelsReady ? '3 Ready' : 'Loading'}
          </span>
        </div>

        {/* Database Status */}
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-nexus-850 border border-nexus-700 text-xs">
          <Database className="w-3.5 h-3.5 text-blue-400" />
          <span className="text-slate-400 font-medium">DB:</span>
          <span className="text-slate-200 font-mono font-medium">SQLite/PG</span>
        </div>

        {/* Live Backend Connection Indicator */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-nexus-850 border border-nexus-700 text-xs">
          <span
            className={`w-2 h-2 rounded-full ${
              isLoading ? 'bg-slate-400' : isOnline ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'
            }`}
          />
          <span className="text-slate-300 font-medium font-mono text-[11px]">
            {isLoading ? 'Checking' : isOnline ? 'API Connected' : 'Disconnected'}
          </span>
        </div>

        {/* Refresh Button */}
        <button
          onClick={handleRefresh}
          disabled={isRefreshing}
          title="Refresh All Network Telemetry"
          className="p-2 rounded-lg bg-nexus-850 hover:bg-nexus-800 text-slate-400 hover:text-slate-200 border border-nexus-700 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-blue-400' : ''}`} />
        </button>
      </div>
    </header>
  );
};
