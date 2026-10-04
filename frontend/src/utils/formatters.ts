/**
 * NEXUS Formatting & Visual Presentation Utilities
 */

export const formatINR = (val: number | undefined | null): string => {
  if (val === undefined || val === null || isNaN(val)) return '₹0';
  if (Math.abs(val) >= 10000000) {
    return `₹${(val / 10000000).toFixed(2)} Cr`;
  }
  if (Math.abs(val) >= 100000) {
    return `₹${(val / 100000).toFixed(2)} Lakh`;
  }
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(val);
};

export const formatNumber = (val: number | undefined | null, decimals: number = 0): string => {
  if (val === undefined || val === null || isNaN(val)) return '0';
  return new Intl.NumberFormat('en-IN', {
    maximumFractionDigits: decimals,
    minimumFractionDigits: decimals,
  }).format(val);
};

export const formatPercent = (val: number | undefined | null, decimals: number = 1): string => {
  if (val === undefined || val === null || isNaN(val)) return '0%';
  return `${(val * 100).toFixed(decimals)}%`;
};

export const getRiskBadgeColor = (scoreOrTier: number | string): { bg: string; text: string; border: string } => {
  if (typeof scoreOrTier === 'string') {
    const tier = scoreOrTier.toUpperCase();
    if (tier.includes('CRITICAL') || tier.includes('HIGH')) {
      return { bg: 'bg-rose-500/10', text: 'text-rose-400', border: 'border-rose-500/30' };
    }
    if (tier.includes('MODERATE') || tier.includes('ELEVATED')) {
      return { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/30' };
    }
    return { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/30' };
  }

  const score = scoreOrTier;
  if (score >= 0.45) {
    return { bg: 'bg-rose-500/10', text: 'text-rose-400', border: 'border-rose-500/30' };
  }
  if (score >= 0.20) {
    return { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/30' };
  }
  return { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/30' };
};

export const getStatusBadgeColor = (status: string | undefined): { bg: string; text: string; border: string } => {
  const s = (status || 'UNKNOWN').toUpperCase();
  if (s === 'ACTIVE' || s === 'OPERATIONAL' || s === 'OPEN' || s === 'DELIVERED') {
    return { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/30' };
  }
  if (s === 'CONGESTED' || s === 'LATE' || s === 'RESTRICTED') {
    return { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/30' };
  }
  if (s === 'DISRUPTED' || s === 'SHUTDOWN' || s === 'BLOCKED' || s === 'SEVERED' || s === 'OFFLINE' || s === 'CANCELED') {
    return { bg: 'bg-rose-500/10', text: 'text-rose-400', border: 'border-rose-500/30' };
  }
  return { bg: 'bg-slate-500/10', text: 'text-slate-400', border: 'border-slate-500/30' };
};
