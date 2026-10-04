import { apiClient } from './client';
import {
  SystemHealth,
  Supplier,
  Product,
  Warehouse,
  RouteItem,
  InventoryItem,
  DemandZone,
  NetworkSummary,
  AnalyticsSummary,
  GeoFacilityCollection,
  ForecastRequest,
  ForecastResponse,
  RiskPredictRequest,
  RiskPredictResponse,
  NetworkRiskProfile,
  AnomalyEvent,
  AnomalyItem,
  ImpactAnalyzeRequest,
  ImpactAnalyzeResponse,
  ScenarioSimulateRequest,
  ScenarioSimulateResponse,
  OptimizeRequest,
  OptimizeResponse,
  RecommendationItem,
} from '../types';

// Health
export const getHealthStatus = async (): Promise<SystemHealth> => {
  const { data } = await apiClient.get<SystemHealth>('/health');
  return data;
};

// Entities
export const getSuppliers = async (params?: { status?: string; category?: string; limit?: number }): Promise<Supplier[]> => {
  const { data } = await apiClient.get<Supplier[]>('/api/v1/suppliers', { params });
  return data;
};

export const getProducts = async (params?: { category?: string; criticality?: number; limit?: number }): Promise<Product[]> => {
  const { data } = await apiClient.get<Product[]>('/api/v1/products', { params });
  return data;
};

export const getWarehouses = async (params?: { status?: string; limit?: number }): Promise<Warehouse[]> => {
  const { data } = await apiClient.get<Warehouse[]>('/api/v1/warehouses', { params });
  return data;
};

export const getRoutes = async (params?: { origin?: string; destination?: string; mode?: string; status?: string; limit?: number }): Promise<RouteItem[]> => {
  const { data } = await apiClient.get<RouteItem[]>('/api/v1/routes', { params });
  return data;
};

export const getInventory = async (params?: { warehouse_id?: string; product_id?: string; critical_only?: boolean; limit?: number }): Promise<InventoryItem[]> => {
  const { data } = await apiClient.get<InventoryItem[]>('/api/v1/inventory', { params });
  return data;
};

export const getDemandZones = async (params?: { region?: string; limit?: number }): Promise<DemandZone[]> => {
  const { data } = await apiClient.get<DemandZone[]>('/api/v1/demand', { params });
  return data;
};

export const getNetworkSummary = async (): Promise<NetworkSummary> => {
  const { data } = await apiClient.get<NetworkSummary>('/api/v1/network');
  return data;
};

// Analytics & GIS
export const getAnalyticsSummary = async (): Promise<AnalyticsSummary> => {
  const { data } = await apiClient.get<AnalyticsSummary>('/api/v1/analytics/summary');
  return data;
};

export const getGisFacilities = async (): Promise<GeoFacilityCollection> => {
  const { data } = await apiClient.get<GeoFacilityCollection>('/api/v1/analytics/gis/facilities');
  return data;
};

// Forecasting
export const generateForecast = async (req: ForecastRequest): Promise<ForecastResponse> => {
  const { data } = await apiClient.post<ForecastResponse>('/api/v1/forecast', req);
  return data;
};

export const getForecasts = async (): Promise<any[]> => {
  const { data } = await apiClient.get<any[]>('/api/v1/forecasts');
  return data;
};

// Risk
export const predictSupplierRisk = async (req: RiskPredictRequest): Promise<RiskPredictResponse> => {
  const { data } = await apiClient.post<RiskPredictResponse>('/api/v1/risk/predict', req);
  return data;
};

export const getNetworkRisks = async (): Promise<NetworkRiskProfile> => {
  const { data } = await apiClient.get<NetworkRiskProfile>('/api/v1/risks');
  return data;
};

// Anomaly
export const detectAnomalies = async (events: AnomalyEvent[]): Promise<{ total_events_scanned: number; anomalies_detected_count: number; anomalies: AnomalyItem[] }> => {
  const { data } = await apiClient.post('/api/v1/anomaly/detect', { events });
  return data;
};

// Impact Analysis
export const analyzeImpact = async (req: ImpactAnalyzeRequest): Promise<ImpactAnalyzeResponse> => {
  const { data } = await apiClient.post<ImpactAnalyzeResponse>('/api/v1/impact/analyze', req);
  return data;
};

// Simulation
export const simulateScenario = async (req: ScenarioSimulateRequest): Promise<ScenarioSimulateResponse> => {
  const { data } = await apiClient.post<ScenarioSimulateResponse>('/api/v1/scenario/simulate', req);
  return data;
};

// Optimization
export const runOptimization = async (req: OptimizeRequest): Promise<OptimizeResponse> => {
  const { data } = await apiClient.post<OptimizeResponse>('/api/v1/optimize', req);
  return data;
};

export const getOptimizationRuns = async (): Promise<any[]> => {
  const { data } = await apiClient.get<any[]>('/api/v1/optimization-runs');
  return data;
};

// Recommendations
export const getRecommendations = async (): Promise<RecommendationItem[]> => {
  const { data } = await apiClient.get<RecommendationItem[]>('/api/v1/recommendations');
  return data;
};
