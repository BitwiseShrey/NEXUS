import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Navbar } from './Navbar';
import { WorkflowBreadcrumb } from '../common/WorkflowBreadcrumb';

export const AppLayout: React.FC = () => {
  return (
    <div className="flex h-screen bg-nexus-950 text-slate-100 overflow-hidden">
      {/* Persistent Sidebar */}
      <Sidebar />

      {/* Main Content Viewport */}
      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        <Navbar />
        <WorkflowBreadcrumb />
        <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
