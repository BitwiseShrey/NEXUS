import React from 'react';
import { AlertCircle, RefreshCw, FolderSearch } from 'lucide-react';

export const LoadingSkeleton: React.FC<{ rows?: number; height?: string }> = ({
  rows = 4,
  height = 'h-12',
}) => {
  return (
    <div className="w-full space-y-3 animate-pulse">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className={`w-full ${height} bg-nexus-850/80 rounded-lg border border-nexus-800`} />
      ))}
    </div>
  );
};

export const ErrorState: React.FC<{ message: string; onRetry?: () => void }> = ({
  message,
  onRetry,
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 rounded-xl bg-rose-500/5 border border-rose-500/20 text-center my-4">
      <div className="p-3 bg-rose-500/10 rounded-full text-rose-400 mb-3">
        <AlertCircle className="w-6 h-6" />
      </div>
      <h3 className="text-sm font-semibold text-rose-300">Data Fetching Error</h3>
      <p className="text-xs text-slate-400 mt-1 max-w-md">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-nexus-800 hover:bg-nexus-700 text-xs font-medium text-slate-200 border border-nexus-700 transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Request</span>
        </button>
      )}
    </div>
  );
};

export const EmptyState: React.FC<{ title: string; subtitle?: string }> = ({
  title,
  subtitle,
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-10 rounded-xl bg-nexus-900 border border-nexus-800 text-center my-4">
      <div className="p-3 bg-nexus-800/80 rounded-full text-slate-400 mb-3">
        <FolderSearch className="w-6 h-6" />
      </div>
      <h3 className="text-sm font-semibold text-slate-200">{title}</h3>
      {subtitle && <p className="text-xs text-slate-400 mt-1 max-w-sm">{subtitle}</p>}
    </div>
  );
};
