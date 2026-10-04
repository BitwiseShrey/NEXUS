import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Activity } from 'lucide-react';

import { KpiCard } from '../components/common/KpiCard';
import { RiskBadge } from '../components/common/RiskBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import { WorkflowBreadcrumb } from '../components/common/WorkflowBreadcrumb';
import { LoadingSkeleton, ErrorState, EmptyState } from '../components/common/FeedbackStates';

describe('Common UI Components Rendering', () => {
  it('renders KpiCard with title, value, and subtitle', () => {
    render(
      <KpiCard
        title="On-Time Delivery SLA"
        value="94.8%"
        subtitle="50,000 orders tracked"
        icon={Activity}
        color="emerald"
      />
    );
    expect(screen.getByText('On-Time Delivery SLA')).toBeDefined();
    expect(screen.getByText('94.8%')).toBeDefined();
    expect(screen.getByText('50,000 orders tracked')).toBeDefined();
  });

  it('renders RiskBadge with correct percentage formatting', () => {
    const { rerender } = render(<RiskBadge scoreOrTier={0.15} />);
    expect(screen.getByText(/15.0% Risk/i)).toBeDefined();

    rerender(<RiskBadge scoreOrTier={0.88} />);
    expect(screen.getByText(/88.0% Risk/i)).toBeDefined();
  });

  it('renders StatusBadge', () => {
    render(<StatusBadge status="ACTIVE" />);
    expect(screen.getByText('ACTIVE')).toBeDefined();
  });

  it('renders WorkflowBreadcrumb with all 6 core stages', () => {
    render(
      <BrowserRouter>
        <WorkflowBreadcrumb />
      </BrowserRouter>
    );
    expect(screen.getByText('MONITOR')).toBeDefined();
    expect(screen.getByText('PREDICT')).toBeDefined();
    expect(screen.getByText('ANALYZE IMPACT')).toBeDefined();
    expect(screen.getByText('SIMULATE')).toBeDefined();
    expect(screen.getByText('OPTIMIZE')).toBeDefined();
    expect(screen.getByText('RECOMMEND')).toBeDefined();
  });

  it('renders LoadingSkeleton, ErrorState, and EmptyState', () => {
    render(<LoadingSkeleton rows={3} />);
    render(<ErrorState message="Connection refused" />);
    expect(screen.getByText('Connection refused')).toBeDefined();

    render(<EmptyState title="No items found" subtitle="Try changing your search" />);
    expect(screen.getByText('No items found')).toBeDefined();
    expect(screen.getByText('Try changing your search')).toBeDefined();
  });
});
