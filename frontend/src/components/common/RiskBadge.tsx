import React from 'react';
import { getRiskBadgeColor } from '../../utils/formatters';

interface RiskBadgeProps {
  scoreOrTier: number | string;
  label?: string;
  size?: 'sm' | 'md';
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ scoreOrTier, label, size = 'sm' }) => {
  const { bg, text, border } = getRiskBadgeColor(scoreOrTier);
  const displayText =
    label ||
    (typeof scoreOrTier === 'number'
      ? `${(scoreOrTier * 100).toFixed(1)}% Risk`
      : scoreOrTier.toUpperCase());

  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-3 py-1 text-sm font-medium';

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border ${bg} ${text} ${border} ${sizeClasses}`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />
      {displayText}
    </span>
  );
};
