import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Network,
  TrendingUp,
  ShieldAlert,
  GitFork,
  Sliders,
  Cpu,
  CheckCircle2,
  Box,
  Layers,
} from 'lucide-react';

const navItems = [
  { name: 'Executive Overview', path: '/', icon: LayoutDashboard },
  { name: 'Digital Twin Network', path: '/network', icon: Network },
  { name: 'Demand Intelligence', path: '/forecast', icon: TrendingUp },
  { name: 'Risk Intelligence', path: '/risk', icon: ShieldAlert },
  { name: 'Impact Analysis', path: '/impact', icon: GitFork },
  { name: 'What-If Simulation', path: '/simulation', icon: Sliders },
  { name: 'Optimization Engine', path: '/optimize', icon: Cpu },
  { name: 'Recommendation Center', path: '/recommendations', icon: CheckCircle2 },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-nexus-900 border-r border-nexus-700/40 flex flex-col shrink-0 h-screen sticky top-0">
      {/* Brand Header */}
      <div className="h-16 flex items-center px-6 border-b border-nexus-700/40 gap-3">
        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Layers className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="flex items-center gap-1.5">
            <span className="font-extrabold text-base tracking-wider text-white">NEXUS</span>
            <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30">
              v1.0
            </span>
          </div>
          <p className="text-[10px] text-slate-400 font-medium">Supply Chain Intelligence</p>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 py-4 px-3 overflow-y-auto space-y-1">
        <div className="px-3 pb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
          Decision Loop
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-nexus-850'
                }`
              }
            >
              <Icon className="w-4 h-4 shrink-0" />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </div>

      {/* Digital Twin Status Footer */}
      <div className="p-4 border-t border-nexus-700/40 bg-nexus-950/40">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <Box className="w-4 h-4 text-blue-400" />
            <span className="font-medium">Digital Twin</span>
          </div>
          <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
            83 Nodes
          </span>
        </div>
        <p className="text-[10px] text-slate-500 mt-1">Calibrated on Indian Hubs</p>
      </div>
    </aside>
  );
};
