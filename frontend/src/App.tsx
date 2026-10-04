import React, { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import 'leaflet/dist/leaflet.css';

import { AppLayout } from './components/layout/AppLayout';
import { LoadingSkeleton } from './components/common/FeedbackStates';

// Lazy-loaded route views for optimal bundle splitting and fast initial page load
const ExecutiveOverview = lazy(() => import('./pages/ExecutiveOverview').then(m => ({ default: m.ExecutiveOverview })));
const DigitalTwinMap = lazy(() => import('./pages/DigitalTwinMap').then(m => ({ default: m.DigitalTwinMap })));
const DemandIntelligence = lazy(() => import('./pages/DemandIntelligence').then(m => ({ default: m.DemandIntelligence })));
const RiskIntelligence = lazy(() => import('./pages/RiskIntelligence').then(m => ({ default: m.RiskIntelligence })));
const ImpactAnalysis = lazy(() => import('./pages/ImpactAnalysis').then(m => ({ default: m.ImpactAnalysis })));
const ScenarioSimulation = lazy(() => import('./pages/ScenarioSimulation').then(m => ({ default: m.ScenarioSimulation })));
const OptimizationEngine = lazy(() => import('./pages/OptimizationEngine').then(m => ({ default: m.OptimizationEngine })));
const RecommendationCenter = lazy(() => import('./pages/RecommendationCenter').then(m => ({ default: m.RecommendationCenter })));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 2, // 2 minutes background cache
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<AppLayout />}>
            <Route
              path="/"
              element={
                <Suspense fallback={<div className="p-8"><LoadingSkeleton rows={4} height="h-28" /></div>}>
                  <ExecutiveOverview />
                </Suspense>
              }
            />
            <Route
              path="/network"
              element={
                <Suspense fallback={<div className="p-8"><LoadingSkeleton rows={4} height="h-28" /></div>}>
                  <DigitalTwinMap />
                </Suspense>
              }
            />
            <Route
              path="/forecast"
              element={
                <Suspense fallback={<div className="p-8"><LoadingSkeleton rows={4} height="h-28" /></div>}>
                  <DemandIntelligence />
                </Suspense>
              }
            />
            <Route
              path="/risk"
              element={
                <Suspense fallback={<div className="p-8"><LoadingSkeleton rows={4} height="h-28" /></div>}>
                  <RiskIntelligence />
                </Suspense>
              }
            />
            <Route
              path="/impact"
              element={
                <Suspense fallback={<div className="p-8"><LoadingSkeleton rows={4} height="h-28" /></div>}>
                  <ImpactAnalysis />
                </Suspense>
              }
            />
            <Route
              path="/simulation"
              element={
                <Suspense fallback={<div className="p-8"><LoadingSkeleton rows={4} height="h-28" /></div>}>
                  <ScenarioSimulation />
                </Suspense>
              }
            />
            <Route
              path="/optimize"
              element={
                <Suspense fallback={<div className="p-8"><LoadingSkeleton rows={4} height="h-28" /></div>}>
                  <OptimizationEngine />
                </Suspense>
              }
            />
            <Route
              path="/recommendations"
              element={
                <Suspense fallback={<div className="p-8"><LoadingSkeleton rows={4} height="h-28" /></div>}>
                  <RecommendationCenter />
                </Suspense>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
