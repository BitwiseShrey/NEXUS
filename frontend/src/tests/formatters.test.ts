import { describe, it, expect } from 'vitest';
import {
  formatINR,
  formatPercent,
  formatNumber,
  getRiskBadgeColor,
  getStatusBadgeColor,
} from '../utils/formatters';

describe('Formatters and UI Helpers', () => {
  it('formats currency in Indian Rupees (INR ₹) with Lakh and Crore scaling', () => {
    expect(formatINR(0)).toBe('₹0');
    expect(formatINR(125000)).toBe('₹1.25 Lakh');
    expect(formatINR(19291240.54)).toBe('₹1.93 Cr');
    expect(formatINR(undefined)).toBe('₹0');
  });

  it('formats decimal fraction percentages into display strings', () => {
    expect(formatPercent(0.945)).toBe('94.5%');
    expect(formatPercent(1.0)).toBe('100.0%');
    expect(formatPercent(undefined)).toBe('0%');
  });

  it('formats standard quantities with en-IN comma separation', () => {
    expect(formatNumber(50000)).toBe('50,000');
    expect(formatNumber(1234567)).toBe('12,34,567');
    expect(formatNumber(undefined)).toBe('0');
  });

  it('maps risk tiers and numeric probabilities to proper styles', () => {
    expect(getRiskBadgeColor(0.15).text).toContain('emerald'); // LOW
    expect(getRiskBadgeColor(0.25).text).toContain('amber');   // MEDIUM
    expect(getRiskBadgeColor(0.85).text).toContain('rose');    // HIGH
    expect(getRiskBadgeColor('CRITICAL').text).toContain('rose');
  });

  it('maps operational facility and route statuses', () => {
    expect(getStatusBadgeColor('ACTIVE').text).toContain('emerald');
    expect(getStatusBadgeColor('CONGESTED').text).toContain('amber');
    expect(getStatusBadgeColor('SEVERED').text).toContain('rose');
  });
});
