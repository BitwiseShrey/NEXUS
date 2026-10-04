import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Eye, TrendingUp, AlertTriangle, Cpu, Sliders, CheckCircle2, ChevronRight } from 'lucide-react';

const stages = [
  { name: 'MONITOR', path: '/', icon: Eye },
  { name: 'PREDICT', path: '/forecast', icon: TrendingUp },
  { name: 'ANALYZE IMPACT', path: '/impact', icon: AlertTriangle },
  { name: 'SIMULATE', path: '/simulation', icon: Sliders },
  { name: 'OPTIMIZE', path: '/optimize', icon: Cpu },
  { name: 'RECOMMEND', path: '/recommendations', icon: CheckCircle2 },
];

export const WorkflowBreadcrumb: React.FC = () => {
  const location = useLocation();

  const getActiveStageIndex = () => {
    const p = location.pathname;
    if (p === '/' || p === '/network') return 0;
    if (p === '/forecast' || p === '/risk') return 1;
    if (p === '/impact') return 2;
    if (p === '/simulation') return 3;
    if (p === '/optimize') return 4;
    if (p === '/recommendations') return 5;
    return 0;
  };

  const activeIdx = getActiveStageIndex();

  return (
    <div className="w-full bg-nexus-900/60 backdrop-blur-md border-b border-nexus-700/40 px-6 py-2.5">
      <div className="max-w-7xl mx-auto flex items-center justify-between overflow-x-auto no-scrollbar gap-2">
        <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest hidden md:inline-block">
          Core Workflow
        </span>
        <div className="flex items-center space-x-1 md:space-x-2">
          {stages.map((stage, idx) => {
            const Icon = stage.icon;
            const isActive = idx === activeIdx;
            const isCompleted = idx < activeIdx;

            return (
              <React.Fragment key={stage.name}>
                <Link
                  to={stage.path}
                  className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/30'
                      : isCompleted
                      ? 'text-slate-300 hover:text-white hover:bg-nexus-800'
                      : 'text-slate-500 hover:text-slate-300'
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : isCompleted ? 'text-blue-400' : 'text-slate-500'}`} />
                  <span>{stage.name}</span>
                </Link>
                {idx < stages.length - 1 && (
                  <ChevronRight className="w-3.5 h-3.5 text-slate-600 shrink-0" />
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default WorkflowBreadcrumb;
